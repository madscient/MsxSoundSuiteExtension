#!/usr/bin/env python3
"""
Compare an English translation with its Japanese original line by line.

    python tools/doc/check.py doc/NAME.md doc/en/NAME.md [--headmap TSV]
    python tools/doc/check.py doc/NAME.md PART.md --part FIRST LAST [--headmap TSV]
    python tools/doc/check.py ... --selftest

The first form takes a finished English document; the second, a
translator's part with no translation note, holding Japanese lines
FIRST-LAST and the link targets still as in the Japanese. --headmap is a
tab-separated table (document name, Japanese heading line, English heading
line) that the English headings must match.

Findings are printed as  LINE: KIND: DETAIL  with Japanese line numbers.
"number", "non-ascii" and "inline-extra" are notes: they are expected where
a word replaced a number (16進 -> hexadecimal), a symbol was kept, or an
English heading quoted in the text carries code the Japanese one does not,
so they are read, not counted. Any other kind makes the exit status 1.

--selftest breaks the English in known ways and fails unless each break
is reported, which is what the findings above are worth.
"""
import argparse
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mdlib

NUM_RE = re.compile(r"\d{2,}")
# Code lines that keep Japanese words are descriptions as much as syntax, and
# their commas and colons come out however the English sentence needs them.
PUNCT = set("[](){}<>=@+*#$&|~")
WIDE = str.maketrans({"（": "(", "）": ")", "＝": "="})
NOTES = {"number", "non-ascii", "inline-extra"}


def kind(line):
    if mdlib.is_fence(line):
        return ("fence",)
    if not line.strip():
        return ("blank",)
    m = re.match(r"(#{1,6}) ", line)
    if m:
        return ("heading", len(m.group(1)))
    if line.strip() == "---":
        return ("rule",)
    if re.match(r"\|(\s*:?-+:?\s*\|)+\s*$", line):
        return ("tablesep",)
    if line.startswith("|"):
        return ("table", line.count("|") - line.count("\\|") - 2 * line.count("`|`"))
    m = re.match(r"(\s*)(>+)\s?", line)
    if m:
        rest = line[m.end():]
        return ("quote", m.group(1), m.group(2), bool(re.match(r"\s*([-*+]|\d+\.)\s", rest)))
    m = re.match(r"(\s*)([-*+]|\d+\.)\s", line)
    if m:
        return ("list", m.group(1), "num" if m.group(2)[0].isdigit() else m.group(2))
    return ("text",)


def split_comment(code):
    """BASIC code and the comment after the first ' outside a string."""
    q = False
    for i, ch in enumerate(code):
        if ch == '"':
            q = not q
        elif ch == "'" and not q:
            return code[:i], code[i:]
    return code, ""


def skeleton(s):
    return "".join(ch for ch in s.translate(WIDE) if ch in PUNCT)


def load_headmap(path, name):
    hmap = {}
    for row in open(path, encoding="utf-8"):
        if row.strip():
            d, j, e = row.rstrip("\n").split("\t")[:3]
            if d == name:
                hmap[j] = e
    return hmap


def compare(ja, en, name, first, last, hmap, linker):
    """Findings [(line, kind, detail)] for English lines en against ja.
    With a linker the English is a finished document; without one it is a
    part holding Japanese lines first..last."""
    found = []

    def report(n, what, detail):
        found.append((n, what, detail))

    if linker:
        if len(en) < 3 or en[1] != "" or en[2] != mdlib.NOTE % name:
            report(1, "note", "the two lines after the title are not the translation note")
        pairs = [(1, ja[0], en[0] if en else "")]
        pairs += [(k + 1, ja[k], en[k + mdlib.HEADER]) for k in range(1, len(ja)) if k + mdlib.HEADER < len(en)]
        if len(en) != len(ja) + mdlib.HEADER:
            report(len(ja), "length", "Japanese %d lines, English %d (expected %d)"
                   % (len(ja), len(en), len(ja) + mdlib.HEADER))
    else:
        want = last - first + 1
        pairs = [(first + i, ja[first - 1 + i], en[i]) for i in range(min(want, len(en)))]
        if len(en) != want:
            report(last, "length", "the part has %d lines, expected %d" % (len(en), want))

    fence = False
    for n, j, e in pairs:
        kj = ("code",) if fence and not mdlib.is_fence(j) else kind(j)
        ke = ("code",) if fence and not mdlib.is_fence(e) else kind(e)
        if kj != ke:
            report(n, "shape", "%r vs %r" % (kj, ke))
        if mdlib.is_fence(j):
            if j != e:
                report(n, "fence", "%r vs %r" % (j, e))
            fence = not fence
            continue
        if fence:
            cj, mj = split_comment(j)
            ce, me = split_comment(e)
            nj = re.sub(r"<[^>]*>", "<>", cj).rstrip()
            ne = re.sub(r"<[^>]*>", "<>", ce).rstrip()
            if nj.isascii():
                if nj != ne:
                    report(n, "code", "%r vs %r" % (cj.rstrip(), ce.rstrip()))
            elif skeleton(nj) != skeleton(ne):
                report(n, "code", "punctuation %r vs %r" % (skeleton(nj), skeleton(ne)))
            if bool(mj) != bool(me):
                report(n, "comment", "a comment in one only")
            numbers(report, n, mj, me, "comment: ")
            odd(report, n, e)
            continue
        if kj[0] == "heading" and hmap is not None:
            want = hmap.get(j)
            if want is None:
                report(n, "heading", "not in the heading map: %r" % j)
            elif e != want:
                report(n, "heading", "%r, expected %r" % (e, want))
        if kj[0] == "tablesep" and j != e:
            report(n, "tablesep", "%r vs %r" % (j, e))
        sj, se = mdlib.CODE_RE.findall(j), mdlib.CODE_RE.findall(e)
        if len(se) < len(sj):
            report(n, "inline", "%d code spans vs %d" % (len(sj), len(se)))
        elif len(se) > len(sj):
            report(n, "inline-extra", "%d code spans vs %d (an English heading quoted?)" % (len(sj), len(se)))
        missing = collections.Counter(s for s in sj if s.isascii()) - collections.Counter(se)
        if missing:
            report(n, "inline", "missing %s" % list(missing.elements()))
        lj, le = mdlib.links(j), mdlib.links(e)
        if linker:
            want = []
            for t in lj:
                new, why = linker.expect(t, name)
                if new is None:
                    report(n, "links", why)
                want.append(new)
            lj = want
        if lj != le:
            report(n, "links", "%s vs %s" % (lj, le))
        numbers(report, n, j, e, "")
        if j.count("**") != e.count("**"):
            report(n, "bold", "%d vs %d" % (j.count("**"), e.count("**")))
        odd(report, n, mdlib.LINK_RE.sub(lambda m: m.group(1), e))
    return found


def numbers(report, n, j, e, what):
    cj, ce = collections.Counter(NUM_RE.findall(j)), collections.Counter(NUM_RE.findall(e))
    if cj != ce:
        report(n, "number", "%smissing %s extra %s" % (what, list((cj - ce).elements()), list((ce - cj).elements())))


def odd(report, n, e):
    chars = sorted(set(ch for ch in e if not ch.isascii()))
    if chars:
        report(n, "non-ascii", "".join(chars))


def dead_links(path):
    """[(line, target, reason)] for relative links in path that do not resolve."""
    res = []
    fence = False
    cache = {}
    for n, l in enumerate(mdlib.read(path), 1):
        if mdlib.is_fence(l):
            fence = not fence
            continue
        if fence:
            continue
        for t in mdlib.links(l):
            if t.startswith(("http://", "https://", "mailto:")):
                continue
            file_part, _, anchor = t.partition("#")
            dest = os.path.normpath(os.path.join(os.path.dirname(path), file_part)) if file_part else path
            if not os.path.exists(dest):
                res.append((n, t, "no such path"))
            elif anchor:
                if not dest.endswith(".md"):
                    res.append((n, t, "anchor into a file that is not Markdown"))
                    continue
                if dest not in cache:
                    cache[dest] = set(mdlib.anchors(mdlib.read(dest)))
                if anchor not in cache[dest]:
                    res.append((n, t, "no such anchor"))
    return res


def mutations(en, part, hmap):
    """(name, line index, broken line, the finding it must cause) per break."""
    first = 0 if part else 3

    def find(pred):
        fence = False
        for i, l in enumerate(en):
            if mdlib.is_fence(l):
                fence = not fence
                continue
            if i >= first and pred(l, fence):
                return i
        return None

    def plain(l):
        return re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), l)

    cases = []
    i = find(lambda l, f: not f and re.match(r"- ", l))
    if i is not None:
        cases.append(("list item made a paragraph", i, en[i][2:], "shape"))
    i = find(lambda l, f: f and "'" in l and split_comment(l)[0].strip() and split_comment(l)[1])
    if i is not None:
        code = split_comment(en[i])[0].rstrip()
        cases.append(("one character cut from code", i, code[:-1] + en[i][len(code):], "code"))
    i = find(lambda l, f: not f and re.search(r"\d{3,}[A-Za-z]", plain(l)))
    if i is not None:
        m = re.search(r"\d{3,}(?=[A-Za-z])", plain(en[i]))
        cases.append(("number with a unit dropped", i, en[i][:m.start()] + en[i][m.end():], "number"))
    i = find(lambda l, f: not f and l.count("`") >= 2 and not l.startswith("#"))
    if i is not None:
        cases.append(("inline code dropped", i, re.sub(r"`[^`]+`", "", en[i], count=1), "inline"))
    if hmap is not None:
        i = find(lambda l, f: not f and l.startswith("## "))
        if i is not None:
            cases.append(("heading reworded", i, en[i] + " x", "heading"))
    i = find(lambda l, f: not f and "**" in l and not l.startswith("#"))
    if i is not None:
        cases.append(("bold marker lost", i, en[i].replace("**", "", 1), "bold"))
    i = find(lambda l, f: not f and mdlib.links(l))
    if i is not None:
        cases.append(("link target changed", i, mdlib.LINK_RE.sub(r"[\1](\2x)", en[i], count=1), "links"))
    return cases


def selftest(ja, en, name, first, last, hmap, make_linker):
    part = make_linker is None

    def run(lines):
        linker = None if part else make_linker(lines)
        return {(n, k) for n, k, _ in compare(ja, lines, name, first, last, hmap, linker)}

    base = run(en)
    missed = 0
    for what, i, new, want in mutations(en, part, hmap):
        got = run(en[:i] + [new] + en[i + 1:]) - base
        n = first + i if part else (i - mdlib.HEADER + 1 if i >= 1 + mdlib.HEADER else i + 1)
        hit = (n, want) in got
        missed += not hit
        print("%-30s line %4d  %s" % (what, n, "caught" if hit else "MISSED %s" % sorted(got)))
    k = min(len(en) - 1, 10)
    hit = any(w == "length" for _, w in run(en[:k] + en[k + 1:]) - base)
    missed += not hit
    print("%-30s           %s" % ("line deleted", "caught" if hit else "MISSED"))
    return missed


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0].strip())
    ap.add_argument("ja")
    ap.add_argument("en")
    ap.add_argument("--headmap")
    ap.add_argument("--part", nargs=2, type=int, metavar=("FIRST", "LAST"))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")

    name = os.path.basename(args.ja)
    ja, en = mdlib.read(args.ja), mdlib.read(args.en)
    hmap = load_headmap(args.headmap, name) if args.headmap else None
    first, last = args.part if args.part else (1, len(ja))
    ja_dir, en_dir = os.path.dirname(os.path.abspath(args.ja)), os.path.dirname(os.path.abspath(args.en))

    def make_linker(lines):
        return mdlib.Linker(ja_dir, en_dir, {name: (ja, lines)})

    if args.selftest:
        sys.exit(1 if selftest(ja, en, name, first, last, hmap, None if args.part else make_linker) else 0)

    found = compare(ja, en, name, first, last, hmap, None if args.part else make_linker(en))
    for n, t, why in dead_links(args.ja):
        found.append((n, "dead-link", "%s: %s -> %s" % (os.path.basename(args.ja), t, why)))
    if not args.part:
        for n, t, why in dead_links(args.en):
            ja_n = n - mdlib.HEADER if n > 1 + mdlib.HEADER else 1
            found.append((ja_n, "dead-link", "en/%s: %s -> %s" % (name, t, why)))
    errors = [f for f in found if f[1] not in NOTES]
    for n, what, detail in found:
        print("%d: %s: %s" % (n, what, detail))
    print("%d error(s), %d note(s) to read" % (len(errors), len(found) - len(errors)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
