#!/usr/bin/env python3
"""
Render the diagrams in docs/ from their PlantUML sources.

Usage:
    python tools/diagram.py [--check]

Requires PlantUML and a JRE; the jar's path comes from PLANTUML_JAR. There
is no default: the jar ships inside editor extensions whose directory name
carries a version number, so no path stays valid across an update. This
build's node diagrams also need Graphviz on PATH, which PlantUML calls for
its layout.

--check runs no PlantUML and needs no jar. Each rendered file carries the
sha256 of the source it was made from, so staleness is decided by reading
the two files. Timestamps would not do it: a fresh clone gets whatever
mtimes the checkout writes, and the documents are often updated without a
build (see docs/build-and-release.md).
"""
import argparse
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifest

STAMP_RE = re.compile(r"<!-- plantuml source sha256:([0-9a-f]{64}) -->")
XML_DECL_RE = re.compile(r"^<\?xml[^>]*\?>")


def source_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def stamp_of(path):
    """The source hash recorded in a rendered file, or None."""
    if not os.path.isfile(path):
        return None
    with io.open(path, "r", encoding="utf-8", errors="replace") as f:
        head = f.read(4096)
    m = STAMP_RE.search(head)
    return m.group(1) if m else None


def add_stamp(path, digest):
    """Record the source hash in the rendered file.

    The comment goes after the XML declaration rather than before it: a
    declaration is only a declaration at the very start of the file.
    """
    with io.open(path, "r", encoding="utf-8") as f:
        text = f.read()
    text = STAMP_RE.sub("", text)
    comment = f"<!-- plantuml source sha256:{digest} -->"
    m = XML_DECL_RE.match(text)
    at = m.end() if m else 0
    text = text[:at] + comment + text[at:]
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def find_jar():
    jar = os.environ.get("PLANTUML_JAR")
    if not jar:
        print("ERROR: PLANTUML_JAR is not set; point it at plantuml.jar")
        return None
    if not os.path.isfile(jar):
        print(f"ERROR: PLANTUML_JAR does not name a file: {jar}")
        return None
    if shutil.which("java") is None:
        print("ERROR: java not found on PATH")
        return None
    return jar


def render(jar, src, dst):
    out_dir = os.path.dirname(dst)
    cmd = ["java", "-jar", jar, "-tsvg", "-charset", "UTF-8",
           "-o", out_dir, src]
    print("+", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        return False
    if not os.path.isfile(dst):
        print(f"ERROR: PlantUML wrote no {os.path.basename(dst)}; it names "
              f"the output after the source, so a `@startuml <name>` in the "
              f"source would put it elsewhere")
        return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="report staleness without rendering")
    args = parser.parse_args()

    jar = None
    if not args.check:
        jar = find_jar()
        if jar is None:
            return 1

    stale = False
    for src_rel, dst_rel, _ in manifest.DIAGRAMS:
        src = manifest.abspath(manifest.DOCS, src_rel)
        dst = manifest.abspath(manifest.DOCS, dst_rel)
        if not os.path.isfile(src):
            print(f"ERROR: missing {manifest.DOCS}/{src_rel}")
            return 1
        digest = source_hash(src)
        if stamp_of(dst) == digest:
            print(f"    {dst_rel} (unchanged)")
            continue
        if args.check:
            reason = "missing" if not os.path.isfile(dst) else "OUT OF DATE"
            print(f"    {dst_rel} ({reason})")
            stale = True
            continue
        if not render(jar, src, dst):
            return 1
        add_stamp(dst, digest)
        print(f"    {dst_rel} (rendered, {os.path.getsize(dst)} bytes)")

    if args.check and stale:
        print("\na diagram is out of date; run tools/diagram.py")
        return 1

    print("\nOK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
