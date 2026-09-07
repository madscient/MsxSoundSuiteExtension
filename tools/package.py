#!/usr/bin/env python3
"""
Collect the built ROMs and the documents into a release package.

Usage:
    python tools/package.py [--version <version>] [--skip-docs-check]

Produces dist/MsxSoundSuiteExtension-<version>/ and the zip beside it.
Nothing is built here: run tools/build.py first.

The ROMs embedded in the cartridge image are checked against the ones we
built before anything is copied; see check_cartridge_identity.

The version defaults to `git describe` of this repository, so a package cut
from a tagged commit is named after the tag.
"""
import argparse
import hashlib
import importlib.util
import os
import shutil
import subprocess
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifest

NAME = "MsxSoundSuiteExtension"
EXTRA_FILES = ["README.md", "NOTICE.md"]


def git(args, cwd):
    out = subprocess.run(["git"] + args, cwd=cwd, capture_output=True,
                         text=True)
    return out.stdout.strip() if out.returncode == 0 else ""


def default_version():
    described = git(["describe", "--tags", "--always", "--dirty"],
                    manifest.REPO_ROOT)
    return described.lstrip("v") or "0.0.0"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def relpath(path):
    return os.path.relpath(path, manifest.REPO_ROOT).replace(os.sep, "/")


def load_y8960_targets():
    """Import Y8960's bank layout from its own build configuration.

    Transcribing the bank numbers into this file would let the layout move
    on one side only, which is the drift this check exists to catch.
    targets.py is a constant module with no imports of its own, so loading
    it runs nothing.
    """
    path = manifest.abspath(manifest.repo("y8960")["path"],
                            "tools", "zbuild", "targets.py")
    if not os.path.isfile(path):
        print(f"ERROR: missing {relpath(path)} (check out the submodules)")
        return None
    spec = importlib.util.spec_from_file_location("y8960_targets", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_cartridge_identity():
    """Refuse to package a cartridge holding ROMs we did not build.

    Comparing the stamped version strings would not do it: they carry a
    date and no more, so two builds made on one day compare equal. The
    bank images are compared byte for byte instead.

    Where each image came from needs no checking: rom.py embeds what sits
    under the directory build.py hands it, which is our own vendor/. What
    the comparison still catches is a cartridge that was linked before the
    image it holds was last written - an older build left in place, or a
    ROM reassembled from stale intermediate output afterwards.
    """
    targets = load_y8960_targets()
    if targets is None:
        return False

    entry = manifest.repo("y8960")
    our_vendor = manifest.abspath(manifest.VENDOR)

    src_rel = entry["artifacts"][0][0]
    name = os.path.splitext(os.path.basename(src_rel))[0]
    if name not in targets.ROM:
        print(f"ERROR: {src_rel} is not one of Y8960's ROM images "
              f"({list(targets.ROM)}); manifest.py and targets.py disagree")
        return False
    cart_path = manifest.abspath(entry["path"], src_rel)
    if not os.path.isfile(cart_path):
        print(f"ERROR: missing {entry['path']}/{src_rel} (run tools/build.py)")
        return False

    cfg = targets.ROM[name]
    bank_size = cfg["bank_size"]
    cart = open(cart_path, "rb").read()

    ok = True
    for key in cfg["prebuilt"]:
        prebuilt = targets.PREBUILT[key]
        bank = prebuilt["bank"]
        at = bank * bank_size
        span = 2 * bank_size
        if "rel" not in prebuilt:
            print(f"ERROR: {key}: Y8960's targets.py names no 'rel'; that "
                  f"checkout predates Y8960_PREBUILT_DIR "
                  f"(git submodule update --remote {entry['path']})")
            ok = False
            continue
        chosen = os.path.join(our_vendor, prebuilt["rel"])
        if not os.path.isfile(chosen):
            print(f"ERROR: {key}: missing {relpath(chosen)} "
                  f"(run tools/build.py)")
            ok = False
            continue

        slice_ = cart[at:at + span]
        image = open(chosen, "rb").read()
        if hashlib.sha256(slice_).hexdigest() != hashlib.sha256(image).hexdigest():
            print(f"ERROR: {name} bank #{bank} ({key}) is not the ROM we built")
            print(f"    in {src_rel} at bank #{bank} "
                  f"(offset {at:#07x}, {span} bytes)")
            print(f"        {hashlib.sha256(slice_).hexdigest()}")
            print(f"    {relpath(chosen)}")
            print(f"        {hashlib.sha256(image).hexdigest()}")
            if len(image) != span:
                print(f"    sizes differ: {span} vs {len(image)} bytes")
            else:
                diff = [i for i in range(span) if slice_[i] != image[i]]
                print(f"    differs in {len(diff)} of {span} bytes, "
                      f"{diff[0]:#06x}..{diff[-1]:#06x} within the bank")
            print(f"    rom.py was pointed at this very file, so nothing "
                  f"else was linked in its place: either the cartridge "
                  f"predates that ROM, or something rewrote the image after "
                  f"it was linked. Rebuild both.")
            ok = False
            continue

        print(f"    {name} bank #{bank:<2d} == {relpath(chosen)}")
    return ok


def collect_roms(out_dir):
    """Copy each shipped ROM; returns its package-relative paths."""
    copied = []
    for entry in manifest.REPOS:
        for src_rel, dst_rel, size in entry["artifacts"]:
            src = manifest.abspath(entry["path"], src_rel)
            if not os.path.isfile(src):
                print(f"ERROR: missing {entry['path']}/{src_rel} "
                      f"(run tools/build.py)")
                return None
            actual = os.path.getsize(src)
            if actual != size:
                print(f"ERROR: {src_rel} is {actual} bytes, expected {size}")
                return None
            dst = os.path.join(out_dir, dst_rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            print(f"    {dst_rel}  ({actual} bytes)")
            copied.append(dst_rel)
    return copied


def write_buildinfo(out_dir, version):
    lines = [f"{NAME} {version}", ""]
    lines.append("ソースリビジョン")
    for entry in manifest.REPOS:
        full = manifest.abspath(entry["path"])
        head = git(["rev-parse", "HEAD"], full)
        date = git(["log", "-1", "--format=%cd", "--date=short"], full)
        dirty = " (dirty)" if git(["status", "--porcelain"], full) else ""
        lines.append(f"  {entry['title']}")
        lines.append(f"    {os.path.basename(entry['path'])} "
                     f"{head[:12]} {date}{dirty}")
    lines.append("")
    lines.append("SHA256")
    for root, _, files in sorted(os.walk(out_dir)):
        for name in sorted(files):
            path = os.path.join(root, name)
            rel = os.path.relpath(path, out_dir).replace(os.sep, "/")
            lines.append(f"  {sha256(path)}  {rel}")
    text = "\n".join(lines) + "\n"
    with open(os.path.join(out_dir, "MANIFEST.txt"), "w",
              encoding="utf-8", newline="\n") as f:
        f.write(text)


def make_zip(out_dir, zip_path):
    root = os.path.dirname(out_dir)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for cur, _, files in sorted(os.walk(out_dir)):
            for name in sorted(files):
                path = os.path.join(cur, name)
                z.write(path, os.path.relpath(path, root).replace(os.sep, "/"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default=None)
    parser.add_argument("--skip-docs-check", action="store_true",
                        help="package even if docs/ is older than the sources")
    args = parser.parse_args()
    version = args.version or default_version()

    if not args.skip_docs_check:
        check = subprocess.run([sys.executable,
                                manifest.abspath("tools", "sync_docs.py"),
                                "--check"], capture_output=True, text=True)
        if check.returncode != 0:
            print(check.stdout)
            print("ERROR: docs/ is stale; run tools/sync_docs.py and commit")
            return 1

    print(f"=== {NAME} {version} ===")
    if not check_cartridge_identity():
        return 1

    out_dir = manifest.abspath(manifest.DIST, f"{NAME}-{version}")
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    if collect_roms(out_dir) is None:
        return 1

    shutil.copytree(manifest.abspath(manifest.DOCS),
                    os.path.join(out_dir, "docs"))
    print("    docs/")
    for name in EXTRA_FILES:
        src = manifest.abspath(name)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(out_dir, name))
            print(f"    {name}")

    write_buildinfo(out_dir, version)
    print("    MANIFEST.txt")

    zip_path = f"{out_dir}.zip"
    make_zip(out_dir, zip_path)
    print(f"\n-> {os.path.relpath(zip_path, manifest.REPO_ROOT)} "
          f"({os.path.getsize(zip_path)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
