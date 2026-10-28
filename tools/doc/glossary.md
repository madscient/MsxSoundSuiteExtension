# 訳語集

6本のソースリポジトリの公開文書を英訳するときの訳語。英語版のある兄弟（Y8960 BASIC
Extension、MSX-MUSIC BASIC Extension V2、MSX-AUDIO BASIC Extension Lite の `doc/en/`）の
訳し方に揃えてある。ここに無い語は、`corpus.py pair` で作った対訳（`[タグ:行]`、`JA:`、
`EN:` の3行で1組）を `corpus.py terms` で引き、兄弟の訳し方に従う。**訳し終えたら、
ここに無かった語をここに足す。**次に訳すリポジトリが、兄弟から拾い直さずに済む。

## 製品名

製品名は [`naming.md`](../../doc/naming.md) の表記をそのまま使い、訳さない。

| 日本語 | 英語 |
|---|---|
| MSX-AUDIO BASIC Extension Lite | そのまま |
| MSX-MUSIC BASIC Extension V2（以下 V2） | そのまま。定義のあとは V2 |
| Y8960 BASIC Extension / OPM BASIC Extension / MIDI Play BASIC Extension | そのまま |
| 当時の MSX-AUDIO 拡張BASIC | the original MSX-AUDIO BASIC extension（**original を落とさない**） |
| 当時の MSX-MUSIC 拡張BASIC | the original MSX-MUSIC BASIC extension |
| 当時（単独） | originally / at the time / the original ...（文脈で） |
| 当時の資料 | the original documentation |
| 拡張BASIC（一般名詞） | BASIC extension |
| この拡張BASIC | this BASIC extension |
| 他の拡張BASIC / 別の拡張BASIC | another BASIC extension / other BASIC extensions |
| 拡張BASICステートメント | BASIC extension statements |
| 拡張命令 | extended statements |

## ROM と版

| 日本語 | 英語 |
|---|---|
| Y8960 カートリッジ版（`mabel_y8960.rom`） | the Y8960 cartridge build |
| カートリッジ版（単独） | the cartridge build |
| 単体カートリッジ版 / 単体の MSX-AUDIO カートリッジ版 | the standalone cartridge build / the standalone MSX-AUDIO cartridge build |
| V2 のカートリッジ版 / V2 の差し替え版 | V2's cartridge build / V2's replacement build |
| ROM のファイル名（`mabel.rom` など） | そのまま |

## 音源とチップ

| 日本語 | 英語 |
|---|---|
| 音源 | sound chip（「FM 音源」は the FM sound chip。文脈で FM） |
| FM 音源チャンネル | FM channel |
| FM音源用・PCM音源用・リズム音用・PSG音源用（の文字列） | (the string) for FM / for PCM / for rhythm / for PSG |
| 拡張OPL2部（OPL2EX） | the extended OPL2 part (OPL2EX) |
| 拡張OPLL部（OPLLEX） | the extended OPLL part (OPLLEX) |
| SSGS（PSG 互換部） | SSGS (the PSG-compatible part) |
| 第1セット / 第2セット（SSGS） | the first set / the second set（of SSGS） |
| 本体 PSG | the internal PSG |
| ハードウェアミキサー / ミキサー | hardware mixer / mixer |
| マスター | master |
| 音源ブロック | sound block |
| サンプルRAM | sample RAM |
| 波形選択 | waveform selection |
| 正弦波 / 半波整流 | sine wave / half-wave rectified |
| 2チップ構成 | two-chip configuration |
| 音源BIOS（MBIOS） | the sound BIOS (MBIOS) |
| ミュージックキーボード | music keyboard |
| インスツルメント | instrument |
| MK 記録 | MK recording |
| アドレスカウンタ | address counter |
| 振幅レジスタ | amplitude register |
| ミキサ（PSG の R7） | mixer |

## 演奏と MML

| 日本語 | 英語 |
|---|---|
| ステートメント / 文 | statement |
| 引数 / パラメータ | argument / parameter（原文に合わせる） |
| 文字列（PLAY の） / ストリング | string |
| ストリング番号 | string number |
| 第1文字列 | the 1st string |
| チャンネル | channel |
| 〜声（FM 9 声） | voices（9 FM voices） |
| 楽音 | melodic sounds |
| リズム音 | rhythm sounds |
| ユニゾン | unison |
| 音色 / 音色ライブラリ / ユーザ音色 | voice / voice library / user voice |
| 音色パラメータ / 音色名 / 略号 | voice parameters / voice name / abbreviation |
| ボイスファイル / ボイスファイル定義 | voice file / voice file definitions |
| 配列変数 | array variable |
| 定位 | panning |
| パンポット | panpot |
| 左端 / 中央 / 右端 | the far left / the center / the far right |
| パワーパンニング | power panning |
| 音長 / 音の長さ | length / note length |
| 刻む（音の長さを） | time（例：「音の長さを音源のタイマーで刻む」→ "times note lengths with the sound chip's timer"） |
| 刻み（名詞） | tick |
| 刻み方 | the tick source |
| 刻みの細かさ | tick resolution |
| 刻めない | cannot be expressed in whole ticks（文脈で言い換えてよい） |
| フレーム | frame |
| 端数 | remainder / fraction |
| 繰り越す / 持ち越す | carry over |
| 割り込み / 割り込みフック / フック | interrupt / interrupt hook / hook |
| オーバーヘッド | overhead |
| バックグラウンド処理 | background processing |
| 初期化 / 解放 | initialize, initialization / release |
| ワークエリア | work area |
| 切り替えのステートメント | the switching statements |
| ページ1 を渡す / ページ渡し | hand page 1 over / handing over page 1 |
| 表に出る（ROM が） | be switched in |
| 次の周（演奏の繰り返し） | the next pass |
| 行き先 | destination |
| 後始末 | cleanup |
| 時間を消費しない / 時間を進める | consumes no time / advances time |
| 受け付ける / 無視される | accept / is ignored |
| 効く | takes effect |
| 鳴らし直す | re-sound |

## 音符と音高

| 日本語 | 英語 |
|---|---|
| 音符 / 休符 | note / rest |
| 四分音符 / 8分音符 / 12分音符 / 16分音符 / 96分音符 / 全音符 | quarter note / eighth note / twelfth note / sixteenth note / 96th note / whole note |
| 四分休符 / 12分休符 | quarter rest / twelfth rest |
| n 分音符 | an nth note |
| 連符 / 連符長 | tuplet / the tuplet length |
| 付点 / 付点休符 | dot / dotted rest |
| タイ / レガート | tie / legato |
| キーオン / キーオフ | key-on / key-off |
| ノートオン / ノートオフ | note-on / note-off |
| ポルタメント | portamento |
| 到達点の音符 | the target note |
| 始点 | start point |
| しゃくり上げる | scoop up |
| スライド（する） | slide |
| ピッチ / 音高 / 音程 | pitch |
| ピッチベンド | pitch bend |
| トランスポーズ / 移調 | transpose |
| セント / 半音 | cent / semitone |
| 音律 / 完全平均律 / 純正律 | temperament / equal temperament / just intonation |
| エンベロープ / ハードウェアエンベロープ | envelope / hardware envelope |
| エンベロープ形状 / エンベロープ周期 | envelope shape / envelope period |
| ノイズの周期 | noise period |
| トーン／ノイズ | tone/noise |
| バスドラム / スネアドラム / タムタム / シンバル / ハイハット | bass drum / snare drum / tom-tom / cymbal / hi-hat |
| アクセント / アクセントボリューム | accent / accent volume |

## 書き方

- 範囲の `〜` は `-` にする（`0〜7` → `0-7`、`` `01H`〜`12H` `` → `` `01H`-`12H` ``）。コードブロックの注釈の中も同じ。負の数を含む範囲は `-1200 to 1200` のように to で書く
- 「16進」「10進」は hexadecimal / decimal。数字が消えるのは構わない
- 数値、16進の値、レジスタ名、オペコードは写す。訳さない
- 全角の括弧は半角にし、英語の空白を入れる。「」は "…"。―― と —— は ` — `
- 「・」で並べたものは英語の並べ方にする（`7・8・9` → `7, 8 and 9`）。「／」は ` / `
- turboR は turbo R（兄弟の英語版に合わせる）
- 見出しを「…」で指している所は、見出しの対訳表の英語を "…" で書く
- 文体は簡潔な技術英語、現在形。説明を足さない、情報を落とさない
