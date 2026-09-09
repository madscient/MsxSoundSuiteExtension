#!/usr/bin/env python3
"""
Collect the material for a release changelog.

Usage:
    python tools/changelog.py [--since <tag>] [--output <file>|-]

Prints what changed since the previous release: the diff of the published
documents under docs/, and the commits of each source repository between
the pin the previous tag recorded and the pin checked out here now.

This produces material, not a changelog. Which of these changes an end user
can notice is a judgement no filter decides, so the summary is written by
hand (or by a session reading this file) and handed to
`release.py --notes-file`.

The commit subjects quoted here come from the private source repositories
and name internal issues and documents, so the output itself is not
publishable; only the summary written from it is.
"""
import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifest

# Directories whose changes can reach the ROM. Everything else in the source
# repositories (tools/, doc/, CLAUDE.md) is listed too, further down, because
# a change to the assembler scripts can still move a byte; the split only
# says which commits to read first.
SOURCE_DIRS = ["src"]

DEFAULT_OUTPUT = os.path.join(manifest.DIST, "changelog-material.md")


def git(args, cwd=None):
    """Run git and return stdout, or None if it failed.

    The encoding is pinned because commit subjects are UTF-8 while the
    console code page on Windows is not.
    """
    out = subprocess.run(["git"] + args, cwd=cwd or manifest.REPO_ROOT,
                         capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    return out.stdout.rstrip("\n") if out.returncode == 0 else None


def previous_tag():
    tags = git(["tag", "--list", "v*", "--sort=-v:refname"])
    return tags.splitlines()[0] if tags else None


def docs_section(since):
    stat = git(["diff", "--stat", since, "--", manifest.DOCS])
    body = git(["diff", since, "--", manifest.DOCS])
    lines = [f"## 公開ドキュメントの差分（{since} → 作業ツリー）", ""]
    if not stat:
        lines += ["変更なし。", ""]
        return lines
    lines += ["```", stat, "```", "", "<details><summary>差分の全文</summary>",
              "", "```diff", body, "```", "", "</details>", ""]
    return lines


def repo_section(entry, since):
    path = entry["path"]
    full = manifest.abspath(path)
    lines = [f"## {entry['title']}", "", f"`{path}`", ""]

    pinned = git(["rev-parse", f"{since}:{path}"])
    head = git(["rev-parse", "HEAD"], full)
    if pinned is None:
        lines += [f"{since} はこのサブモジュールを記録していない（当時は"
                  "存在しなかったか、配置が違う）。", ""]
        return lines
    if head is None:
        lines += ["チェックアウトされていない。`git submodule update --init` "
                  "を先に実行すること。", ""]
        return lines
    if git(["cat-file", "-e", f"{pinned}^{{commit}}"], full) is None:
        lines += [f"{since} が記録するコミット `{pinned[:12]}` がここに無い。"
                  "`git fetch` を先に実行すること。", ""]
        return lines
    if head == pinned:
        lines += [f"`{pinned[:12]}` のまま。変更なし。", ""]
        return lines

    rng = f"{pinned}..{head}"
    lines += [f"`{pinned[:12]}` → `{head[:12]}`", ""]

    src = (git(["log", "--format=%h %s", rng, "--"] + SOURCE_DIRS, full)
           or "").splitlines()
    allc = (git(["log", "--format=%h %s", rng], full) or "").splitlines()
    src_hashes = {ln.split(" ", 1)[0] for ln in src}
    rest = [ln for ln in allc if ln.split(" ", 1)[0] not in src_hashes]

    lines += [f"### ROM に届きうる変更（{len(src)} / {len(allc)} コミット）", ""]
    for ln in src:
        sha = ln.split(" ", 1)[0]
        files = git(["show", "--name-only", "--format=", sha, "--"]
                    + SOURCE_DIRS, full) or ""
        touched = ", ".join(f"`{f}`" for f in files.split())
        lines.append(f"- {ln}")
        if touched:
            lines.append(f"  - {touched}")
    lines += ["", f"### その他（{len(rest)} コミット）", ""]
    lines += [f"- {ln}" for ln in rest]
    lines.append("")
    return lines


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", default=None,
                        help="tag to compare against; defaults to the "
                             "newest v* tag")
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT,
                        help=f"where to write; - for stdout "
                             f"(default {DEFAULT_OUTPUT})")
    args = parser.parse_args()

    since = args.since or previous_tag()
    if since is None:
        print("ERROR: no v* tag found; pass --since <tag>")
        return 1
    if git(["rev-parse", f"{since}^{{commit}}"]) is None:
        print(f"ERROR: {since} is not a commit in this repository")
        return 1

    lines = [
        f"# リリースノート用の材料（{since} 以降）",
        "",
        "**この文書は公開しない。** 非公開のソースリポジトリのコミット件名を",
        "そのまま含む。ここから書き起こした要約だけをリリースノートに載せる。",
        "",
        "利用者に見える変更を拾う順序：まず公開ドキュメントの差分（新しい",
        "ステートメント・MML・挙動の訂正はここに出る）、次に各リポジトリの",
        "「ROM に届きうる変更」。「その他」は検証・内部文書・作業手順で、",
        "利用者に見えるものはまず無い。",
        "",
    ]
    lines += docs_section(since)
    for entry in manifest.REPOS:
        lines += repo_section(entry, since)

    text = "\n".join(lines) + "\n"
    if args.output == "-":
        sys.stdout.buffer.write(text.encode("utf-8"))
        return 0
    out = args.output if os.path.isabs(args.output) \
        else manifest.abspath(args.output)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"wrote {os.path.relpath(out, manifest.REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
