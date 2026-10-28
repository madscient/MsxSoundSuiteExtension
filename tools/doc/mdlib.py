"""
Markdown helpers shared by the translation tools in this directory.

An English document doc/en/NAME.md is its Japanese original doc/NAME.md
with two lines inserted after the title, so Japanese line k (k >= 2) is
English line k + 2, and the two documents' headings pair up by position.
"""
import os
import re
import unicodedata

LINK_RE = re.compile(r"\[((?:[^\[\]]|\[[^\]]*\])*)\]\(([^)\s]+)\)")
CODE_RE = re.compile(r"`([^`]+)`")
HEADER = 2
NOTE = ("> This is an English translation of the [Japanese original](../%s). "
        "Where the two differ, the Japanese version is authoritative.")


def read(path):
    data = open(path, "rb").read()
    if b"\r" in data:
        raise SystemExit("%s: has CR; the documents are LF only" % path)
    text = data.decode("utf-8")
    if not text.endswith("\n"):
        raise SystemExit("%s: does not end with a newline" % path)
    return text[:-1].split("\n")


def write(path, lines):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def slug(heading):
    """The anchor GitHub gives a heading line (an approximation of github-slugger
    that holds for the documents in these repositories)."""
    text = heading.lstrip("#").strip().replace("`", "")
    out = []
    for ch in text.lower():
        if ch == " ":
            out.append("-")
        elif ch in "-_":
            out.append(ch)
        elif ch.isascii():
            if ch.isalnum():
                out.append(ch)
        elif unicodedata.category(ch)[0] in "LNM":
            out.append(ch)
    return "".join(out)


def is_fence(line):
    """A code fence, also one indented under a list item."""
    return line.lstrip().startswith("```")


def headings(lines):
    """[(index, line)] of the headings outside code fences."""
    fence = False
    res = []
    for i, l in enumerate(lines):
        if is_fence(l):
            fence = not fence
        elif not fence and re.match(r"#{1,6} ", l):
            res.append((i, l))
    return res


def anchors(lines):
    seen = {}
    res = []
    for _, h in headings(lines):
        s = slug(h)
        n = seen.get(s, 0)
        seen[s] = n + 1
        res.append(s if n == 0 else "%s-%d" % (s, n))
    return res


def heading_map(ja, en, offset=HEADER):
    """Japanese anchor -> English anchor, pairing the headings by position.
    A Japanese heading with no heading at its English line maps to None."""
    en_at = {i: a for (i, _), a in zip(headings(en), anchors(en))}
    return {a: en_at.get(i + offset if i else 0)
            for (i, _), a in zip(headings(ja), anchors(ja))}


def posix_relpath(path, start):
    return os.path.relpath(path, start).replace(os.sep, "/")


class Linker:
    """What a link in doc/NAME.md should become in doc/en/NAME.md.

    A link to a document that has an English version keeps pointing at the
    English one, with the anchor carried over to the English heading in the
    same position. Anything else keeps pointing at what the Japanese pointed
    at, which from doc/en/ is one directory further up.
    """

    def __init__(self, ja_dir, en_dir, docs=None):
        self.ja_dir = ja_dir
        self.en_dir = en_dir
        self.docs = dict(docs or {})
        self.maps = {}

    def has_en(self, name):
        return name in self.docs or os.path.isfile(os.path.join(self.en_dir, name))

    def anchor_map(self, name):
        if name not in self.maps:
            if name in self.docs:
                ja, en = self.docs[name]
            else:
                ja = read(os.path.join(self.ja_dir, name))
                en = read(os.path.join(self.en_dir, name))
            self.maps[name] = heading_map(ja, en)
        return self.maps[name]

    def expect(self, target, name):
        """(the English target, or None) and a reason when it is None."""
        if target.startswith(("http://", "https://", "mailto:")):
            return target, None
        file_part, sep, anchor = target.partition("#")
        dest = file_part or name
        if "/" not in file_part and dest.endswith(".md") and self.has_en(dest):
            if not sep:
                return target, None
            new = self.anchor_map(dest).get(anchor)
            if new is None:
                return None, "no English heading for #%s in %s" % (anchor, dest)
            return "%s#%s" % (file_part, new), None
        moved = posix_relpath(os.path.join(self.ja_dir, file_part), self.en_dir)
        return moved + (sep + anchor if sep else ""), None


def links(line):
    return [t for _, t in LINK_RE.findall(line)]
