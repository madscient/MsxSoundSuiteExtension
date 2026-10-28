#!/usr/bin/env python3
"""
Japanese-English pairs from the repositories that already have doc/en/.

    python tools/doc/corpus.py pair OUT REPO...
    python tools/doc/corpus.py heads OUT DOC.md...
    python tools/doc/corpus.py terms OUT TERM...

pair   writes OUT/<repo>-<name>.txt for every doc/en/NAME.md that has a
       doc/NAME.md beside it, one entry per non-blank line pair
       ([tag:line], "JA: ...", "EN: ..."), and OUT/headings.tsv with the
       heading pairs. Hand these to translators so that they look up how a
       term was translated before.
heads  prints a heading table for DOC.md as check.py --headmap reads it:
       document name, Japanese heading, and the English heading where a
       sibling translated exactly the same heading (blank otherwise, to be
       filled in before the translators start), then the siblings it came
       from.
terms  prints up to three pairs per TERM in which the Japanese contains it.
"""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mdlib


def pairs(ja, en):
    yield 1, ja[0], en[0]
    for k in range(1, len(ja)):
        if k + mdlib.HEADER < len(en):
            yield k + 1, ja[k], en[k + mdlib.HEADER]


def cmd_pair(out, repos):
    os.makedirs(out, exist_ok=True)
    heads = []
    for repo in repos:
        tag_repo = os.path.basename(os.path.abspath(repo))
        for en_path in sorted(glob.glob(os.path.join(repo, "doc", "en", "*.md"))):
            name = os.path.basename(en_path)
            ja_path = os.path.join(repo, "doc", name)
            if not os.path.isfile(ja_path):
                continue
            tag = "%s-%s" % (tag_repo, name[:-3])
            ja, en = mdlib.read(ja_path), mdlib.read(en_path)
            rows = []
            for n, j, e in pairs(ja, en):
                if j.strip() or e.strip():
                    rows += ["[%s:%d]" % (tag, n), "JA: " + j, "EN: " + e]
                if j.startswith("#") and e.startswith("#"):
                    heads.append("\t".join((tag, j, e)))
            mdlib.write(os.path.join(out, tag + ".txt"), rows)
            print("%s: %d lines" % (tag, len(ja)))
    mdlib.write(os.path.join(out, "headings.tsv"), heads)


def text(heading):
    return heading.lstrip("#").strip()


def load_heads(out):
    """Japanese heading text -> [(tag, English heading text)]. The level is
    left out: a sibling may use the same heading one level deeper."""
    known = {}
    for row in mdlib.read(os.path.join(out, "headings.tsv")):
        tag, ja, en = row.split("\t")
        known.setdefault(text(ja), []).append((tag, text(en)))
    return known


def cmd_heads(out, docs):
    known = load_heads(out)
    for path in docs:
        name = os.path.basename(path)
        for _, h in mdlib.headings(mdlib.read(path)):
            hits = known.get(text(h), [])
            en = h[:len(h) - len(h.lstrip("#"))] + " " + hits[0][1] if hits else ""
            agree = all(e == hits[0][1] for _, e in hits)
            print("\t".join((name, h, en, " ".join(t for t, _ in hits) + ("" if agree else " (they differ)"))))


def cmd_terms(out, terms):
    entries = []
    for path in sorted(glob.glob(os.path.join(out, "*.txt"))):
        lines = mdlib.read(path)
        for i in range(0, len(lines) - 2, 3):
            entries.append((lines[i], lines[i + 1][4:], lines[i + 2][4:]))
    for t in terms:
        hits = [e for e in entries if t in e[1]]
        print("## %s (%d)" % (t, len(hits)))
        for tag, ja, en in hits[:3]:
            k = ja.find(t)
            print("  %s JA: %s" % (tag, ja[max(0, k - 40):k + 60]))
            print("  %s EN: %s" % (" " * len(tag), en[:260]))


def main():
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    if len(sys.argv) < 4 or sys.argv[1] not in ("pair", "heads", "terms"):
        sys.exit(__doc__)
    cmd, out, rest = sys.argv[1], sys.argv[2], sys.argv[3:]
    {"pair": cmd_pair, "heads": cmd_heads, "terms": cmd_terms}[cmd](out, rest)


if __name__ == "__main__":
    main()
