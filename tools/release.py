#!/usr/bin/env python3
"""
Cut a GitHub release from the current submodule pins.

Usage:
    python tools/release.py <tag> [--notes-file <file>] [--draft]
                            [--no-build] [--dry-run]

Runs build.py, packages, tags this repository and uploads the package with
the GitHub CLI (`gh auth login` first). The zip and the loose ROM images are
both attached: the zip carries the documents, the loose files save a click.

The release describes one state of the four sources, so it refuses to run
unless this repository is clean and every submodule sits exactly on its
recorded commit - otherwise the tag would point at a package nobody can
rebuild.
"""
import argparse
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifest
import package as packager


def run(cmd, cwd=None, dry_run=False):
    print("+", " ".join(cmd))
    if dry_run:
        return True
    return subprocess.run(cmd, cwd=cwd).returncode == 0


def check_clean():
    ok = True
    dirty = packager.git(["status", "--porcelain"], manifest.REPO_ROOT)
    # Submodule lines are reported here too; they are checked one by one
    # below with a message that says which one and why.
    dirty = [ln for ln in dirty.splitlines()
             if not ln[3:].startswith(manifest.VENDOR + "/")]
    if dirty:
        print("ERROR: working tree has uncommitted changes:")
        print("\n".join(dirty))
        ok = False

    for entry in manifest.REPOS:
        full = manifest.abspath(entry["path"])
        pinned = packager.git(["rev-parse", f"HEAD:{entry['path']}"],
                              manifest.REPO_ROOT)
        head = packager.git(["rev-parse", "HEAD"], full)
        if not head:
            print(f"ERROR: {entry['path']} is not checked out")
            ok = False
        elif head != pinned:
            print(f"ERROR: {entry['path']} is at {head[:12]}, but this "
                  f"repository records {pinned[:12]}; commit the new pin "
                  f"or check out the recorded one")
            ok = False
        elif packager.git(["status", "--porcelain"], full):
            print(f"ERROR: {entry['path']} has local changes")
            ok = False
    return ok


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tag", help="release tag, e.g. v0.1.0")
    parser.add_argument("--notes-file", default=None,
                        help="markdown file used as the release notes")
    parser.add_argument("--draft", action="store_true")
    parser.add_argument("--no-build", action="store_true",
                        help="reuse the ROMs already in the submodules")
    parser.add_argument("--dry-run", action="store_true",
                        help="build and package, but do not tag or upload")
    args = parser.parse_args()
    version = args.tag.lstrip("v")

    if shutil.which("gh") is None and not args.dry_run:
        print("ERROR: gh not found (https://cli.github.com/)")
        return 1
    if not check_clean():
        return 1

    if not args.no_build:
        if not run([sys.executable, manifest.abspath("tools", "build.py")]):
            return 1
    if not run([sys.executable, manifest.abspath("tools", "package.py"),
                "--version", version]):
        return 1

    out_dir = manifest.abspath(manifest.DIST,
                               f"{packager.NAME}-{version}")
    assets = [f"{out_dir}.zip"]
    for entry in manifest.REPOS:
        for _, dst_rel, _ in entry["artifacts"]:
            assets.append(os.path.join(out_dir, dst_rel))

    existing = packager.git(["tag", "--list", args.tag], manifest.REPO_ROOT)
    if not existing:
        if not run(["git", "tag", "-a", args.tag, "-m", args.tag],
                   manifest.REPO_ROOT, args.dry_run):
            return 1
    if not run(["git", "push", "origin", args.tag],
               manifest.REPO_ROOT, args.dry_run):
        return 1

    cmd = ["gh", "release", "create", args.tag,
           "--title", f"{packager.NAME} {args.tag}"]
    if args.notes_file:
        cmd += ["--notes-file", args.notes_file]
    else:
        cmd += ["--generate-notes"]
    if args.draft:
        cmd.append("--draft")
    cmd += assets
    if not run(cmd, manifest.REPO_ROOT, args.dry_run):
        return 1

    print("\nOK" + (" (dry run: nothing tagged or uploaded)"
                    if args.dry_run else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
