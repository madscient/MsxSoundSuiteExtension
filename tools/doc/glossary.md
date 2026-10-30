# 訳語集

6本のソースリポジトリの公開文書を英訳するときの訳語。6本の `doc/en/` の訳し方に
揃えてある。ここに無い語は、`corpus.py pair` で作った対訳（`[タグ:行]`、`JA:`、
`EN:` の3行で1組）を `corpus.py terms` で引き、兄弟の訳し方に従う。**訳し終えたら、
ここに無かった語をここに足す。**次に訳すリポジトリが、兄弟から拾い直さずに済む。

## 製品名

製品名は [`naming.md`](../../doc/naming.md) の表記をそのまま使い、訳さない。

| 日本語 | 英語 |
|---|---|
| MSX-AUDIO BASIC Extension Lite | そのまま |
| MSX-MUSIC BASIC Extension V2（以下 V2） | そのまま。定義のあとは V2 |
| Y8960 BASIC Extension / OPM BASIC Extension / MIDI Play BASIC Extension / Makoto BASIC Extension | そのまま |
| SFG BASIC Extension（以下 SFGBX） | SFG BASIC Extension (hereafter SFGBX)。定義のあとは SFGBX |
| 当時の MSX-AUDIO 拡張BASIC | the original MSX-AUDIO BASIC extension（**original を落とさない**） |
| 当時の MSX-MUSIC 拡張BASIC | the original MSX-MUSIC BASIC extension |
| 従来の / 当時の MSX-MIDI 拡張BASIC | the original MSX-MIDI BASIC extension（比較表の列見出しは Original MSX-MIDI BASIC extension） |
| 当時（単独） | originally / at the time / the original ...（文脈で） |
| 当時の資料 / 原典 | the original documentation |
| 拡張BASIC（一般名詞） | BASIC extension |
| この拡張BASIC | this BASIC extension |
| 他の拡張BASIC / 別の拡張BASIC | another BASIC extension / other BASIC extensions |
| 別の音源拡張BASIC | another sound BASIC extension |
| 版で違う / どちらの版でも（SFG BASIC Extension と OPM BASIC Extension） | differs between the two BASIC extensions / in both BASIC extensions |
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
| MSX Sound Suite カートリッジ版（Y8960 カートリッジに入る版） | the MSX Sound Suite cartridge build (the build in the Y8960 cartridge) |
| 単体のカートリッジ | a standalone cartridge |
| Y8960 カートリッジに入る ROM（の1つ） | (one of) the ROMs in the Y8960 cartridge |
| 音源拡張 ROM | sound extension ROM |
| 切り替える（別の ROM へ） | switch to |
| 引き受ける（ステートメントの名前を） | take（"does not take these four"） |
| 名前ごと登録しない | does not register the name(s) at all |
| 実行し直す（`CALL MIDI` を） | run again |
| 拡張スロット | expanded slot |

## 音源とチップ

| 日本語 | 英語 |
|---|---|
| 音源 | sound chip（「FM 音源」は the FM sound chip。文脈で FM） |
| 音源（MIDI 機器を含む総称のとき） | sound source |
| 音源番号（`PLAY #n` の） | sound chip number |
| OPM 系の FM 音源 | an OPM-family FM sound chip |
| 本体内蔵の MSX-MUSIC | the built-in MSX-MUSIC |
| 機械（MSX の） | machine |
| 音源チップのタイマー / 音源のタイマー | the sound chip's timer |
| 1基しかない | there is only one |
| 直流が出る | a DC level is output |
| 読み出し専用 | read-only |
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
| 刻み方 / 時間の刻み | the tick source |
| 演奏の刻み | the playback tick |
| 刻みの周期のずれ | drift of the tick period |
| 〜から作ったクロックで数える | counts with a clock derived from ... |
| 高精度タイマー | the high-precision timer |
| 1/60 秒（で刻む） | 1/60 second（形容詞は 1/60-second ticks） |
| 画面の割り込み | the screen interrupt |
| 画面の垂直同期 / 垂直同期 | the screen's vertical sync / vertical sync |
| PAL（ヨーロッパ仕様の映像方式） | PAL (the European video standard) |
| 割り込みの頻度 | interrupt rate |
| 割り込みフックを奪う | take over the interrupt hook |
| 演奏管理 | playback management |
| 待ち行列に積む | queue |
| BASIC の遅くなる割合 / BASIC の重さ | how much BASIC slows down / load on BASIC |
| スループット | throughput |
| ずれ（テンポの） | deviation |
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
| 時間を取らない（音符が） | take no time |
| 受け付ける / 無視される | accept / is ignored |
| 黙って捨てられる | silently discarded |
| 断る（ADPCM に関わるものを） | refuse |
| 明け渡す（初期化したものを） | release |
| 定めない（動作は／鳴り方は） | is not defined |
| 頭打ちになる | is capped |
| 効く | takes effect |
| 鳴らし直す | re-sound |
| 控え（書き込んだ値の） | the record of the values written |
| 控え（チャンネルに置く LFO の設定） | kept for that channel（同じ節に音色の record があるので record にしない） |
| PLAY 文をまたいで残る | persists across PLAY statements |
| 声部 | part |
| リズム用 MML / メロディ用 MML | rhythm MML / melody MML |
| リズム有り / リズム無し | with rhythm / without rhythm |
| 文字（リズムの打楽器を表す英字） / `<文字>` | letter / `<letter>`（MML 一覧の表の見出しの「文字」は兄弟と同じ Character） |
| 鳴る側（`In` の表） | Sounds from |
| 式で作った文字列 | strings built by expressions |
| 文字列定数 / 文字列変数 | string constants / string variables |
| 整数型配列 / 要素 | integer array / element |
| 第1添字 / 第2添字 / 2 次元で宣言 | first subscript / second subscript / declared two-dimensionally |
| デバイス番号 / CPU メモリ | device number / CPU memory |
| 転送元 / 転送先 | source / destination |
| N88-BASIC(86) | そのまま |

## 音符と音高

| 日本語 | 英語 |
|---|---|
| 音符 / 休符 | note / rest |
| 四分音符 / 8分音符 / 12分音符 / 16分音符 / 96分音符 / 全音符 | quarter note / eighth note / twelfth note / sixteenth note / 96th note / whole note |
| 四分休符 / 12分休符 | quarter rest / twelfth rest |
| 3分休符 | third rest |
| 長さを持てない（音符が） | cannot have a length |
| つなぎが切れる（`&` の） / つないだ音符 | breaks the join / the joined note |
| 中央のド | middle C |
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
| リムショット | rimshot |
| 打楽器 | percussion |
| アクセント / アクセントボリューム | accent / accent volume |

## 音色と FM のパラメータ

| 日本語 | 英語 |
|---|---|
| プリセット音色 / プリセット | preset voices / presets |
| 既定の音色 | the default voice |
| ユーザー音色 / ユーザー音色領域 | user voice / the user voice area |
| 音色本体（40 バイト） | the voice body |
| レコード（音色の） | record |
| 音色の種別 | voice type |
| 音色配列 | voice array |
| 音色ごとの移調 | per-voice transpose |
| 番号の読み替え（音色の） | renumbering / read the example with that number instead |
| 持ち回す（音色データを配列で） | carry around |
| 音色ごとの LFO / LFO の項目 | per-voice LFO / the LFO items |
| LFO のトリガ | LFO trigger |
| 速さ・深さ・波形（LFO の） | speed, depth and waveform |
| 効き具合（PMS/AMS） | sensitivity (PMS/AMS) |
| 乗る（LFO に） / 外す（LFO から） | ride on / remove |
| 打つ（`S1` を） / 打ち直す | issue / issue again |
| 発音させるオペレータ | operators to sound |
| フィードバック量 / 接続形態 | feedback amount / connection |
| トータルレベル / トータルレベルへの加算 | total level / addition to the total level |
| 周波数倍率 / デチューン 1・2 | frequency multiplier / detune 1, 2 |
| キースケーリングレート / レベルキースケール | key scaling rate / level key scaling |
| ファーストディケイレート / セカンドディケイレート / ファーストディケイレベル | first decay rate / second decay rate / first decay level |
| ベロシティによる音量変化の感度 | sensitivity of volume change to velocity |
| 値の向きが逆（レートとレベル） | run in the opposite direction |
| 平板に鳴る | sound flatter |

## SFG と OPM

| 日本語 | 英語 |
|---|---|
| SFG（単独） | the SFG（ハードウェア。SFG-01/SFG-05 とその ROM。製品を指さない） |
| SFG 本体の ROM / SFG の ROM | the SFG's own ROM / the SFG ROM |
| OPM のタイマ A | OPM timer A |
| 出力先（OPM の左右） | output destination |
| 左右の出し分け | left/right output |

## Makoto と YM2608

| 日本語 | 英語 |
|---|---|
| Makoto（YM2608 カートリッジ） / Makoto（単独） | Makoto (the YM2608 cartridge) / Makoto（ハードウェアの名前。製品を指さない） |
| Misato（YMF288 カートリッジ） / Misato（単独） | Misato (the YMF288 cartridge) / Misato |
| SSG（PSG 互換部） / SSG | SSG (the PSG-compatible part) / SSG（訳さない） |
| SSG用（の文字列） | (the string) for SSG |
| 表のバンク / 裏のバンク（YM2608 のレジスタ） | the first bank / the second bank |
| 挿さっている / 挿さっていない | is inserted / with no ... inserted |
| 識別コード（音源の） | the chip's ID code |
| タイマー A | timer A |
| 音源の割り込み / 本体に届く | the sound chip's interrupt / reach the MSX computer |
| テストレジスタ / プリスケーラ | the test register / the prescaler |
| フラグの制御 / 割り込みの許可 | flag control / interrupt enable |

## MIDI

| 日本語 | 英語 |
|---|---|
| MIDI インターフェース / インターフェース | MIDI interface / interface |
| インターフェース番号 | interface number |
| 自動判別（する） | auto-detection / auto-detect |
| 自作（インターフェース） | homebuilt |
| 只MIDI | Tada MIDI（海外のコミュニティでは Tada MIDI Cable で通じる。持ち主の指示） |
| BIT2 MIDIサウルス | BIT2 MIDI Saurus |
| MIDIインターフェース3 / MSX MIDIインターフェース2 | MIDI Interface 3 / MSX MIDI Interface 2 |
| MIDI OUT を2系統 | two MIDI OUT outputs |
| 音源モジュール | sound module |
| MIDI 機器 | MIDI device |
| GM のドラムキット | the GM drum kit |
| ベロシティ / ノート番号 | velocity / note number |
| オールサウンドオフ / リセットオールコントローラー | All Sound Off / Reset All Controllers |
| モノモード | mono mode |
| ベンドレンジ | bend range |
| ポルタメントコントロール | portamento control |
| データエントリ MSB / LSB | Data Entry MSB / LSB |
| シーケンサーへの合図 | signals to a sequencer |
| ストップ / スタート / コンティニュー | Stop / Start / Continue |
| 受け手 | the receiver |
| ステータスバイト / ランニングステータス | status byte / running status |
| システムリアルタイムメッセージ | system real-time messages |
| ワイヤに出るバイト列 | the bytes on the wire |
| インプリメンテーションチャート | implementation chart |

## 書き方

- 範囲の `〜` は `-` にする（`0〜7` → `0-7`、`` `01H`〜`12H` `` → `` `01H`-`12H` ``）。コードブロックの注釈の中も同じ。負の数を含む範囲は `-1200 to 1200` のように to で書く
- 「16進」「10進」は hexadecimal / decimal。数字が消えるのは構わない
- 数値、16進の値、レジスタ名、オペコードは写す。訳さない
- 全角の括弧は半角にし、英語の空白を入れる。「」は "…"。―― と —— は ` — `
- 「・」で並べたものは英語の並べ方にする（`7・8・9` → `7, 8 and 9`）。「／」は ` / `
- turboR は turbo R（兄弟の英語版に合わせる）
- 見出しを「…」で指している所は、見出しの対訳表の英語を "…" で書く
- 文体は簡潔な技術英語、現在形。説明を足さない、情報を落とさない
