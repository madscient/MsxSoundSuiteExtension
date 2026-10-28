#!/usr/bin/env python3
"""
Join the translators' parts into English documents.

    python tools/doc/assemble.py [--overwrite] JA_DIR EN_DIR NAME=PART[,PART...] [NAME=...]

Each NAME is written to EN_DIR/NAME: the parts in order, with the
translation note after the title. An English document that already exists
is left alone unless --overwrite is given: once assembled, it is edited in
place, and assembling it again from the parts would silently undo those
edits. The parts carry the Japanese link
targets, which are rewritten here: anchors into a document translated in
this run or already in EN_DIR go to the English heading in the same
position, and anything else keeps pointing at what the Japanese pointed
at, one directory further up. Give every document that links to another
in the same run, so that the anchors between them can be paired.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mdlib


def main():
    args = sys.argv[1:]
    overwrite = "--overwrite" in args
    args = [a for a in args if a != "--overwrite"]
    if len(args) < 3:
        sys.exit(__doc__)
    ja_dir, en_dir = args[0], args[1]
    docs = {}
    for arg in args[2:]:
        name, _, parts = arg.partition("=")
        if not overwrite and os.path.exists(os.path.join(en_dir, name)):
            sys.exit("%s already exists; edit it in place, or pass --overwrite"
                     % os.path.join(en_dir, name))
        en = []
        for p in parts.split(","):
            en += mdlib.read(p)
        en[1:1] = ["", mdlib.NOTE % name]
        docs[name] = (mdlib.read(os.path.join(ja_dir, name)), en)

    linker = mdlib.Linker(os.path.abspath(ja_dir), os.path.abspath(en_dir), docs)
    bad = 0
    for name, (_, en) in docs.items():
        out = []
        fence = False
        for n, l in enumerate(en, 1):
            if mdlib.is_fence(l):
                fence = not fence
            if fence or n == 1 + mdlib.HEADER:
                out.append(l)
                continue

            def repl(m):
                nonlocal bad
                new, why = linker.expect(m.group(2), name)
                if new is None:
                    print("%s:%d: %s" % (name, n, why))
                    bad += 1
                    return m.group(0)
                return "[%s](%s)" % (m.group(1), new)

            out.append(mdlib.LINK_RE.sub(repl, l))
        mdlib.write(os.path.join(en_dir, name), out)
        print("%s: %d lines" % (name, len(out)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
