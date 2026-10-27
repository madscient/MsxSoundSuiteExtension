## 利用条件

この ROM イメージは**個人利用に限り**許諾されています。

**再配布には MSX ライセンシングコーポレーションの許諾が別途必要です。**
詳細は同梱の `NOTICE.md` を参照してください。

## 収録物

| ファイル | サイズ | 用途 |
|---|--:|---|
| `y8960bas.rom` | 128KB | Y8960 カートリッジ用。5つの拡張BASICをすべて収めたイメージ |
| `mmbe.rom` | 16KB | MSX-MUSIC 単体用。本体内蔵 MSX-MUSIC の差し替え、または ROM カートリッジ |
| `mabel.rom` | 16KB | MSX-AUDIO（Y8950）単体カートリッジ用 |
| `sfg.rom` | 16KB | SFG-01/05 と併用する単体カートリッジ用 |
| `midi.rom` | 16KB | MIDI インターフェースを鳴らす単体カートリッジ用 |
| `makoto.rom` | 16KB | Makoto（YM2608）・Misato（YMF288）単体カートリッジ用。`y8960bas.rom` には含まれない |

下の「Source code (zip / tar.gz)」は GitHub が自動で付けるもので、中身は
ドキュメントとビルド用スクリプトだけです。拡張BASIC 本体のソースコードは
含まれません（バイナリの配布のみが許諾されているため）。

zip にはドキュメントと、各 ROM のビルド元コミットおよび SHA256 を記録した
`MANIFEST.txt` が入っています。

ステートメントと MML の仕様は [`docs/`](https://github.com/madscient/MsxSoundSuiteExtension/tree/master/docs) を参照して
ください。

---

## Terms of use

These ROM images are licensed for **personal use only**.

**Redistribution requires separate permission from MSX Licensing Corporation.**
See the included `NOTICE.md` (in Japanese) for details.

## Contents

| File | Size | Purpose |
|---|--:|---|
| `y8960bas.rom` | 128KB | For the Y8960 cartridge. Contains all five BASIC extensions |
| `mmbe.rom` | 16KB | Standalone MSX-MUSIC. Replaces the built-in MSX-MUSIC of a computer, or runs as a ROM cartridge |
| `mabel.rom` | 16KB | Standalone cartridge for MSX-AUDIO (Y8950) |
| `sfg.rom` | 16KB | Standalone cartridge used together with an SFG-01/05 |
| `midi.rom` | 16KB | Standalone cartridge that drives a MIDI interface |
| `makoto.rom` | 16KB | Standalone cartridge for Makoto (YM2608) and Misato (YMF288). Not included in `y8960bas.rom` |

The "Source code (zip / tar.gz)" files below are added automatically by GitHub and
contain only the documentation and build scripts. They do not contain the source
code of the BASIC extensions (only distribution of the binaries is permitted).

The zip contains the documentation and `MANIFEST.txt`, which records the commit
each ROM was built from and its SHA256.

See [`docs/`](https://github.com/madscient/MsxSoundSuiteExtension/tree/master/docs) (in Japanese)
for the specifications of the statements and MML.
