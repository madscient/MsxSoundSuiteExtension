# 英語版の道具

公開文書の英語版（各ソースリポジトリの `doc/en/`）を作り、日本語版に追いつかせるための
道具。読者は、6本のソースリポジトリで文書を書く AI と開発者。

英語版は日本語版の訳で、**日本語版が正**。英語版は日本語版と1行ずつ対応させる ――
タイトルの後ろに注記の2行を挟むだけで、日本語の k 行目（k ≥ 2）は英語の k+2 行目に
なる。照合も、リンクの書き換えも、この対応に乗っている。

**道具はここ（MsxSoundSuiteExtension の `tools/doc/`）にだけ置く。** ソースリポジトリには
写さず、隣にあるこの作業ツリーのものを走らせる。写すと片方だけが古くなる。以下の
コマンドは、ソースリポジトリの根で打つ形で書いてある。

| | |
|---|---|
| `check.py` | 日本語版と英語版を1行ずつ突き合わせる。`--selftest` で、壊した写しを拾うことを見る |
| `assemble.py` | 訳者が返した範囲をつないで英語版にし、リンクを書き換える |
| `corpus.py` | 兄弟の日英を行で対にする。見出しの下書きを作る。訳語を引く |
| `mdlib.py` | 上の3本の部品。アンカーは GitHub の作り方を写した `slug` で作る |
| `brief.md` | 訳者（サブエージェント）への依頼の雛形 |
| `glossary.md` | 6本の英語版で使う訳語 |

**`translation.py` だけは、各ソースリポジトリが自分の `tools/doc/` に持つ。** 英語版が
今の日本語版から訳されたものかを見る道具で、記録（同じ場所の `translation.txt`）が
リポジトリごとの状態だから。各リポジトリの試験の入口から呼ばれている。

## 日本語版を直したとき

1. 同じ変更を英語版の同じ行に入れる。日本語版に行を足したら、英語版にも同じ位置に足す
2. `python ../MsxSoundSuiteExtension/tools/doc/check.py doc/<名前>.md doc/en/<名前>.md` を回し、
   エラーが 0 なのを見る。注意（`number` `non-ascii` `inline-extra`）は数えずに読む。
   「16進」を hexadecimal にした行や、記号を残した行が毎回出る
3. `python tools/doc/translation.py --mark <名前>.md` で記録し、`translation.py` が
   up to date を出すのを見る

## 新しく英訳するとき

置き場所、冒頭の注記、`translation.py` は兄弟と同じにする。作業フォルダ（scratchpad）に
次を作ってから訳者に配る。

1. **原文を先に直す。**実装と突き合わせて直しておく。それでも、訳していると原文の
   誤りが見つかる。直したら、訳者が返した英語の同じ行も直す（渡した写しと今の原文を
   `git diff --no-index` で比べると、直した行が出る）
2. **兄弟の対訳**：`python ../MsxSoundSuiteExtension/tools/doc/corpus.py pair <作業>/corpus <兄弟のリポジトリ>...`
3. **見出しの対訳表**：`python ../MsxSoundSuiteExtension/tools/doc/corpus.py heads <作業>/corpus doc/<名前>.md ... > <作業>/headmap.tsv`。
   兄弟と同じ見出しには兄弟の訳が入る。空いた英語を全部埋めてから配る。文書をまたいで
   「…」で見出しを指している所が、これでそろう
4. **訳語集**：`../MsxSoundSuiteExtension/tools/doc/glossary.md` を作業フォルダへ写して足す。
   兄弟の訳は `python ../MsxSoundSuiteExtension/tools/doc/corpus.py terms <作業>/corpus <語>...`
   で引く。**訳者へ配る前に足す語も、兄弟の訳を引いてから入れる。**訳者は訳語集を兄弟の
   対訳より優先するので、先に足した語が兄弟とずれていると、そのずれが全訳者に広がる。
   **訳し終えたら、足した語を MsxSoundSuiteExtension への依頼文に表で並べる。**ここの
   `glossary.md` に入れるのは MsxSoundSuiteExtension のセッションが行う
5. **原文を切る**：`sed -n '<最初>,<最後>p' doc/<名前>.md > <作業>/ja/<部分>.md`。
   節の切れ目で切り、表やコードの途中で切らない
6. **訳者に配る**：`brief.md` を作業フォルダへ写し、担当（原文の部分、最初の行番号、
   出力の名前）を書き足して渡す。訳者は1行を1行に訳し、リンクの行き先を変えない
7. **範囲ごとに照合**：`python ../MsxSoundSuiteExtension/tools/doc/check.py doc/<名前>.md <作業>/en/<部分>.md --part <最初> <最後> --headmap <作業>/headmap.tsv`
8. **つなぐ**：`python ../MsxSoundSuiteExtension/tools/doc/assemble.py doc doc/en <名前>=<部分>,<部分>... <名前>=...`。
   互いにリンクしている文書は1回で渡す。アンカーの対はその場で作るため。**つないだあとは
   `doc/en/` を直接直す。**範囲から組み直すと、英語版に入れた直しが黙って消える。なので
   `assemble.py` は、既にある英語版を `--overwrite` 無しでは上書きしない
9. **照合**：`python ../MsxSoundSuiteExtension/tools/doc/check.py doc/<名前>.md doc/en/<名前>.md --headmap <作業>/headmap.tsv`。
   **先に `--selftest` を回し、全部 caught なのを見てから本物の結果を信じる**
10. `python tools/doc/translation.py --mark <名前>.md ...`
11. 公開は MsxSoundSuiteExtension の `tools/manifest.py` に載せてもらう。依頼は
    `doc/prompt-*.md` に書いて渡す（[`msse-doc-rule.md`](../../doc/msse-doc-rule.md)）

## 照合が見ないもの

- **訳の意味。**見るのは行の形、コードブロック、インラインコード、リンクの行き先、
  `**` の数、2桁以上の数字、残った非 ASCII 文字
- 1桁の数。「8分音符4つ」を four eighth notes と書いても、4 eighth notes と書いても通る
- 行の中の語順。ただし行をまたいで語を入れ替えると、インラインコードや数字が隣の行へ
  移り、両方の行で指摘が出る。原文と同じ行に置き直す

## 踏みやすいもの

- 走るのは `../MsxSoundSuiteExtension` の作業ツリーにある版。隣の作業ツリーは古いことが
  あるので、使う前に fetch して origin より遅れていないかを見る
- Git Bash から `assemble.py` に `名前=<パス>,<パス>` を渡すと、カンマより後ろの
  `/x/...` の形のパスは Windows のパスに直らない。`X:/...` の形で渡す
- 文書は UTF-8 で LF。`check.py` は CR を含むファイルを読まずに止まる
