# 製品名の表記

**この文書は、6リポジトリに共通する製品名の表記の取り決め。** エンドユーザーと
アプリケーション作者が読む文書を書くか直すかする前に、ここを読む。役割は
仕様書、読者は文書を書く AI と開発者、公開しない。

書き方そのものの取り決めは [`msse-doc-rule.md`](msse-doc-rule.md) が正。
この文書はそこから参照される名前の表で、名前だけを持つ。

## 名前

| 対象 | 製品名 | 短縮型・略称 |
|---|---|---|
| MSX-MUSIC 向けの拡張BASIC | MSX-MUSIC BASIC Extension V2 | MSX-MUSIC V2, MUSICV2, V2 (*) |
| MSX-AUDIO 向けの拡張BASIC | MSX-AUDIO BASIC Extension Lite | MSX-AUDIO Lite, AUDIO Lite, Lite (*) |
| SFG 向けの拡張BASIC | SFG BASIC Extension | SFG BASIC, SFGBX, SFG (*) |
| Y8960 の OPM 向けの拡張BASIC | OPM BASIC Extension | （未定。決まるまで短縮しない） |
| MIDI 向けの拡張BASIC | MIDI Play BASIC Extension | MIDI BASIC, MIDI Play |
| Makoto カートリッジ（YM2608）向けの拡張BASIC | Makoto BASIC Extension | Makoto BASIC, Makoto (*) |
| Y8960 向けの拡張BASIC | Y8960 BASIC Extension | Y8960BASIC |
| Y8960 のシーケンサーBIOS | Y8960 Sequencer BIOS | Y8960BIOS |
| 6本の総称、および Y8960 カートリッジのファームウェア | MSX Sound Suite Extension | MSX Sound Suite, Sound Suite, MSSX |

(*) 一般名詞や他の固有名詞（SFG と Makoto が該当。どちらもハードウェアの名前でも
ある）と混同しない文脈でのみ使う。兄弟との比較のように、何と何を並べているかが
直前に書いてある場所。

## 一般名詞と使い分ける

**「拡張BASIC」は MSX-BASIC の機能拡張ソフトウェア一般を指す普通名詞。**
特定の製品を指すときは製品名を書く。

- 「この拡張BASIC は割り込みをフックする」 ―― 一般名詞。よい
- 「当時の MSX-MIDI 拡張BASIC」 ―― 当時の製品。よい
- 「MSX-MUSIC 拡張BASIC の同ステートメントと同機能」 ―― 兄弟の製品を
  指しているので `MSX-MUSIC BASIC Extension V2` と書く

## Sequencer BIOS の日本語表記

**見出しと初出は `Y8960 Sequencer BIOS`、以降の本文は「シーケンサーBIOS」。**
日本語の読みやすさを保ったまま、正式名を一度は示すため。

## MSSE と MSSX

**公開する文書では `MSX Sound Suite`（初出は `MSX Sound Suite Extension（MSSX）`）
を使う。** `MSSE` は内部略称で、公開しない文書 ―― ソースリポジトリの
`README.md`、`CLAUDE.md`、`plan.md`、`tools/` の文書と、MsxSoundSuiteExtension の
`doc/` と `tools/` の文書 ―― でだけ使う。MsxSoundSuiteExtension の `README.md` と
`README.en.md` はエンドユーザーが読むので `MSSX` を使う
（[`msse-doc-rule.md`](msse-doc-rule.md#公開かどうかは機械で決まる)）。

## 変えないもの

表記の統一は文書の中だけで、次のものには及ばない。**変えると別のものを壊す。**

- リポジトリ名（`MsxMusicBasicExtension` など）
- ROM に焼かれた文字列。`'MSSE8960'` シグネチャ、
  `MSX-MUSIC BASIC Extension Licensed by MSX-LC`
- ファイル名（`msse-abi.md`）、ビルドターゲットと成果物名（`Y8960BE`、
  `mmbe.rom`、`midi_y8960.rom`）
- `src/` のコメントとシンボル

`'MSSE8960'` の8バイトは ABI を凍結した時点の綴りで、製品名の表記が変わっても
変えない（[`msse-abi.md`](../docs/y8960/msse-abi.md)）。

## 内部の表記揺れは許容する

公開しない文書 ―― `CLAUDE.md`、`plan.md`、ソースリポジトリの `README.md`、
`tools/emu/README.md` ―― では内部略称（MMBE, MABEL, SFGBE, OPMBE, MPBE, Y8960BE, MSSE）を使ってよい。
**そろえる労力を、読者のいない場所に使わない。**
