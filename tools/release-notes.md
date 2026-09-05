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

下の「Source code (zip / tar.gz)」は GitHub が自動で付けるもので、中身は
ドキュメントとビルド用スクリプトだけです。拡張BASIC 本体のソースコードは
含まれません（バイナリの配布のみが許諾されているため）。

zip にはドキュメントと、各 ROM のビルド元コミットおよび SHA256 を記録した
`MANIFEST.txt` が入っています。

ステートメントと MML の仕様は [`docs/`](https://github.com/madscient/MsxSoundSuiteExtension/tree/master/docs) を参照して
ください。
