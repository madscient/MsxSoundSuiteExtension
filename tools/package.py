#!/usr/bin/env python3
"""
Collect the built ROMs and the documents into a release package.

Usage:
    python tools/package.py [--version <version>] [--skip-docs-check]

Produces dist/MsxSoundSuiteExtension-<version>/ and the zip beside it.
Nothing is built here: run tools/build.py first.

The version defaults to `git describe` of this repository, so a package cut
from a tagged commit is named after the tag.
"""
import argparse
import hashlib
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

    out_dir = manifest.abspath(manifest.DIST, f"{NAME}-{version}")
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    print(f"=== {NAME} {version} ===")
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
