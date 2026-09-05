# MSX Sound Suite Extension

MSX Sound Suite Extension（MSSE）は、[Y8960 カートリッジ](https://github.com/hra1129/Y8960_Cartridge)
向けの拡張BASICと BIOS の総称です。

## 入手

ROM イメージは [Releases](../../releases) から入手してください。
**個人利用に限り許諾されています。**再配布には MSX ライセンシング
コーポレーションの許諾が別途必要です（[`NOTICE.md`](NOTICE.md)）。

| ファイル | サイズ | 用途 |
|---|--:|---|
| `y8960bas.rom` | 128KB | Y8960 カートリッジ用。下記5つをすべて収めたイメージ |
| `standalone/mmbe.rom` | 16KB | MSX-MUSIC 単体用。本体内蔵 MSX-MUSIC の差し替え、または ROM カートリッジ |
| `standalone/mabel.rom` | 16KB | MSX-AUDIO（Y8950）単体カートリッジ用 |
| `standalone/sfg.rom` | 16KB | SFG-01/05 と併用する単体カートリッジ用 |
| `standalone/midi.rom` | 16KB | MIDI インターフェースを鳴らす単体カートリッジ用 |

`y8960bas.rom` はページ1（`4000H`-`7FFFH`）を5つの拡張BASICで分け合います。
電源投入時に表に出るのは MSX-MUSIC Basic Extension で、`CALL MINIT` /
`CALL MUSIC` / `CALL AUDIO` / `CALL SFG` / `CALL MIDI` で切り替わります。

### ソースコードについて

リリースページに並ぶ「Source code (zip)」「Source code (tar.gz)」は GitHub が
すべてのリリースに自動で付けるもので、中身はこのリポジトリのドキュメントと
ビルド用スクリプトだけです。**拡張BASIC 本体のソースコードは含まれません。**

MSX-MUSIC / MSX-AUDIO / SFG / MIDI Play の各 Basic Extension は日本楽器製造株式会社
（YAMAHA）および株式会社アスキーの著作物をフォークしたもので、許諾されて
いるのはバイナリの配布に限られます。ソースは非公開のリポジトリにあり、この
リポジトリはその参照（`vendor/`）を持つだけなので、アーカイブ内では空の
ディレクトリになります。

## 収録内容

### MSX-MUSIC Basic Extension

従来の MSX-MUSIC 拡張BIOSとの完全互換性を持ち、MML が強化されています。
従来互換の FMBIOS を搭載しているため、既存のアプリケーションにも対応します。

### MSX-AUDIO Basic Extension Lite

MSX-MUSIC Basic Extension を MSX-AUDIO 向けに改修したもので、従来の
MSX-AUDIO 拡張BASICとほぼ互換性があります。ADPCM 再生は MML のみのサポート
です。拡張BIOS、MBIOS は搭載していません。

### SFG Basic Extension

MSX-MUSIC Basic Extension を SFG-01/05 向けに移植したものです。
MSX-MUSIC 互換 MML で OPM/OPP を演奏できます。

### MIDI Play Basic Extension

MIDI インターフェースを鳴らす拡張BASICです。MSX-MUSIC 互換 MML に MSX-MIDI
互換の拡張コマンドを加えたもので、MIDI チャンネル 1〜16 を同時に演奏します。
MSX-MIDI（FS-A1GT 内蔵）と YAMAHA SFG-01/05 のインターフェースに実行時分岐で
対応します。（開発中）

### Y8960 Basic Extension

Y8960 にネイティブ対応した拡張BASICです。従来の `PLAY` 文のような逐次演奏
方式ではなく、MML コンパイラ方式を取っています。MML コンパイラが生成した
シーケンスデータを最大4つまで同時に保持・演奏できます。（開発中）

### Y8960 シーケンサーBIOS

Y8960 Basic Extension が作成したシーケンスデータを、DOS アプリケーションや
ROM カートリッジから使用するための BIOS です。（開発中）

## ドキュメント

ステートメントと MML の仕様、および ROM／アプリケーション開発者向けの
取り決めは [`docs/`](docs/) にあります。目次は [`docs/README.md`](docs/README.md)。

## 権利

配布している ROM イメージは個人利用に限り許諾されています。再配布には
MSX ライセンシングコーポレーションの許諾が別途必要です。著作権表示と、
再配布の許諾を得た場合に明記すべき出典は [`NOTICE.md`](NOTICE.md) に
あります。
