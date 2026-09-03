#!/usr/bin/env python3
"""
What each source repository produces and where it lands.

This is the single place that names build commands, ROM images and
documents; build.py, sync_docs.py and package.py all read it, so a new
target is added here and nowhere else.

The order of REPOS is a build order, not a listing order: Y8960 links
the Y8960 build of the other three into its 128KB cartridge image, so it
has to come last.
"""
import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VENDOR = "vendor"
DIST = "dist"
DOCS = "docs"

# Y8960's rom.py looks for the other three under its own vendor/ first and
# falls back to `../<repo>` relative to its own root. Because all four are
# siblings here, that fallback resolves to our own submodules, so Y8960's
# nested submodules are deliberately left uninitialised - one checkout of
# each repository, and the images that go into the cartridge are the ones
# we just built.
REPOS = [
    {
        "key": "msx-music",
        "title": "MSX-MUSIC Basic Extension",
        "path": f"{VENDOR}/MsxMusicBasicExtension",
        "steps": [
            ["tools/zbuild/build.py", "gbios", "basic"],
            ["tools/zbuild/rom.py", "mmbe"],
            ["tools/zbuild/build.py", "y8960_gbios", "y8960_basic"],
            ["tools/zbuild/rom.py", "mmbe_y8960"],
        ],
        # Shipped as-is, with the size the image must have.
        "artifacts": [("build/rom/mmbe.rom", "standalone/mmbe.rom", 16384)],
        # Built but not shipped: consumed by the Y8960 cartridge image.
        "inputs": ["build/rom/mmbe_y8960.rom"],
        "docs": [
            ("doc/basic-reference.md", "msx-music/basic-reference.md",
             "MSX-MUSIC 拡張BASIC リファレンス"),
            ("doc/new-feature.md", "msx-music/new-feature.md",
             "MSX-MUSIC 拡張BASIC 新機能ガイド（従来版との差分）"),
        ],
    },
    {
        "key": "msx-audio",
        "title": "MSX-AUDIO Basic Extension Lite",
        "path": f"{VENDOR}/MsxAudioBasicExtensionLite",
        "steps": [
            ["tools/zbuild/build.py", "audio", "y8960"],
            ["tools/zbuild/rom.py", "audio", "y8960"],
        ],
        "artifacts": [("build/rom/mabel.rom", "standalone/mabel.rom", 16384)],
        "inputs": ["build/rom/mabel_y8960.rom"],
        "docs": [
            ("doc/basic-reference.md", "msx-audio/basic-reference.md",
             "MSX-AUDIO 拡張BASIC リファレンス"),
        ],
    },
    {
        "key": "sfg",
        "title": "SFG Basic Extension",
        "path": f"{VENDOR}/SFGBasicExtension",
        "steps": [
            ["tools/zbuild/build.py", "sfg", "sfg_y8960"],
            ["tools/zbuild/rom.py", "sfg", "sfg_y8960"],
        ],
        "artifacts": [("build/rom/sfg.rom", "standalone/sfg.rom", 16384)],
        "inputs": ["build/rom/sfg_y8960.rom"],
        "docs": [
            ("doc/basic-reference.md", "sfg/basic-reference.md",
             "SFG 拡張BASIC リファレンス"),
        ],
    },
    {
        "key": "y8960",
        "title": "Y8960 Basic Extension / MSSE cartridge",
        "path": f"{VENDOR}/Y8960BasicExtension",
        "steps": [
            ["tools/zbuild/build.py", "--all"],
            ["tools/zbuild/rom.py"],
            # The other three stamp their version during assembly; this one
            # is a post-pass over the finished image.
            ["tools/zbuild/version.py", "build/rom/y8960bas.rom"],
        ],
        "artifacts": [("build/rom/y8960bas.rom", "y8960bas.rom", 131072)],
        "inputs": [],
        "docs": [
            ("doc/basic-reference.md", "y8960/basic-reference.md",
             "Y8960 拡張BASIC リファレンス"),
            ("doc/msse-abi.md", "y8960/msse-abi.md",
             "MSSE 統合インターフェース（ROM/アプリケーション開発者向け）"),
            ("doc/hardware.md", "y8960/hardware.md",
             "Y8960 ハードウェア（本ファームウェアが依存する範囲）"),
            ("doc/sequencer-bios.md", "y8960/sequencer-bios.md",
             "Y8960 シーケンサーBIOS（アプリケーション開発者向け）"),
        ],
    },
]

# Markdown links in the copied documents that point outside the copy.
# Anything not listed keeps working because co-located documents stay
# co-located; anything that pointed into a private source tree is unlinked
# (the link markup is dropped, the label text stays).
LINK_REWRITE = {
    "../src/inc/msse.inc": None,
    "../src/inc/y8960hw.inc": None,
    "../../MsxMusicBasicExtension": "../msx-music/basic-reference.md",
}

DOC_SECTIONS = [
    ("msx-music", "MSX-MUSIC Basic Extension"),
    ("msx-audio", "MSX-AUDIO Basic Extension Lite"),
    ("sfg", "SFG Basic Extension"),
    ("y8960", "Y8960 Basic Extension / MSSE"),
]


def repo(key):
    for r in REPOS:
        if r["key"] == key:
            return r
    raise KeyError(key)


def abspath(*parts):
    return os.path.join(REPO_ROOT, *parts)
