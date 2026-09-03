#!/usr/bin/env python3
"""
Build every source repository's ROM images.

Usage:
    python tools/build.py [<key> ...] [--dirty]

With no key, all four are built in manifest order. Requires zmac
(https://48k.ca/zmac.html); each repository picks it up from the ZMAC_EXE
environment variable, which is passed through unchanged.

A submodule with local modifications is refused: the version string burned
into every image comes from the last commit, so a dirty tree produces a ROM
that no commit reproduces. --dirty builds anyway, for a local trial.
"""
import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifest


def submodule_state(path):
    """(head, dirty) for a checked-out submodule, or (None, False)."""
    full = manifest.abspath(path)
    if not os.path.isdir(os.path.join(full, ".git")) and \
       not os.path.isfile(os.path.join(full, ".git")):
        return None, False
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=full,
                          capture_output=True, text=True).stdout.strip()
    status = subprocess.run(["git", "status", "--porcelain"], cwd=full,
                            capture_output=True, text=True).stdout.strip()
    return head, bool(status)


def run_step(path, step):
    cwd = manifest.abspath(path)
    cmd = [sys.executable] + step
    print("+", " ".join(cmd), f"({path})")
    result = subprocess.run(cmd, cwd=cwd)
    return result.returncode == 0


def build_repo(entry, allow_dirty):
    print(f"\n=== {entry['title']} ===")
    head, dirty = submodule_state(entry["path"])
    if head is None:
        print(f"ERROR: {entry['path']} is not checked out "
              f"(git submodule update --init {entry['path']})")
        return False
    print(f"    {head[:12]}{' (dirty)' if dirty else ''}")
    if dirty and not allow_dirty:
        print("ERROR: working tree has local changes; commit them or "
              "pass --dirty")
        return False

    for step in entry["steps"]:
        if not run_step(entry["path"], step):
            print(f"ERROR: step failed: {' '.join(step)}")
            return False

    missing = [rel for rel, _, _ in entry["artifacts"]] + entry["inputs"]
    missing = [rel for rel in missing
               if not os.path.isfile(manifest.abspath(entry["path"], rel))]
    if missing:
        print(f"ERROR: build produced no {missing}")
        return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("keys", nargs="*",
                        help=f"one of: {[r['key'] for r in manifest.REPOS]}")
    parser.add_argument("--dirty", action="store_true",
                        help="build even if a submodule has local changes")
    args = parser.parse_args()

    entries = manifest.REPOS
    if args.keys:
        unknown = [k for k in args.keys
                   if k not in [r["key"] for r in manifest.REPOS]]
        if unknown:
            parser.error(f"unknown key(s): {unknown}")
        entries = [r for r in manifest.REPOS if r["key"] in args.keys]

    for entry in entries:
        if not build_repo(entry, args.dirty):
            return 1
    print("\nOK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
