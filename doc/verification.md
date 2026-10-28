# 検証の取り決め

MSSE（MSX Sound Suite Extension）を構成する6本の ROM は、それぞれ別の
リポジトリで開発され、どれも openMSX を呼ぶ検証ハーネスを `tools/emu` に
持っている。この文書は**6リポジトリに共通する検証の取り決め**を定める。
正は MsxSoundSuiteExtension の `doc/verification.md` で、各リポジトリはこの
文書を参照する。

ROM どうしのインターフェースは [`msse-abi.md`](../docs/y8960/msse-abi.md) が定める。
この文書が扱うのは、それが守られていることをどう確かめるか。

| リポジトリ | ID | ハーネスの入口 |
|---|--:|---|
| [MsxMusicBasicExtension](https://github.com/madscient/MsxMusicBasicExtension) | 0 | `tools/emu/run.py` |
| [MsxAudioBasicExtensionLite](https://github.com/madscient/MsxAudioBasicExtensionLite) | 1 | `tools/emu/run.py` |
| [Y8960BasicExtension](https://github.com/madscient/Y8960BasicExtension) | 2 | `tools/emu/run.py` |
| [SFGBasicExtension](https://github.com/madscient/SFGBasicExtension) | 3 | `tools/emu/run_sfg.py` |
| [MidiPlayBasicExtension](https://github.com/madscient/MidiPlayBasicExtension) | 4 | `tools/emu/run.py` |
| [MakotoBasicExtension](https://github.com/madscient/MakotoBasicExtension) | なし | `tools/emu/run.py` |

Makoto は Y8960 カートリッジに入らないので ID を持たず、統合版に関わる取り決め
（下の「Y8960BasicExtension が保証すること」と、見つけた欠陥の返し方）は
掛からない。

## 責任の分担

**統合 ROM イメージを作れるのは Y8960BasicExtension だけ。** 他の4本を
`vendor/` のサブモジュールとして持ち、`tools/zbuild/rom.py` が 128KB の
カートリッジに結合する。他のリポジトリは自分の 16KB しか持たないので、
受け渡しの相手を揃えられない。分担はここから決まる。

### 各構成 ROM のリポジトリが保証すること

**単体版と MSSE 版が同じに動くこと。**

MSSE 版と単体のカートリッジとして売る版を分けて持つ ROM は、共通部分を
確かめるスクリプトを**両方のターゲットで走らせ、同じ結果になること**を
完了条件とする。片方でしか走っていないスクリプトを残さない。

自 ROM の中で閉じているものは、その ROM のリポジトリの責任範囲に入る。

- 自分のステートメントが実際にディスパッチされること
- 自分のカートリッジヘッダと `XBTAB` の形
- 受け渡しの相手が居ないときに安全に戻ること

### Y8960BasicExtension が保証すること

**MSSE 統合版に固有の機能。** 相手を揃えないと確かめられないものはすべて
Y8960BasicExtension。

- 結合した 128KB イメージで、ページ1 の受け渡しが実際に相手へ着地すること
- 受け渡しの前後でバンクレジスタ・`H.TIMI`・`HIMEM`・テキストポインタが
  取り決めどおりであること
- `4010h` のシグネチャと `4060h` のアタッチエントリを経由する、
  アプリケーションからの経路
- 結合時の検証（`rom.py` が各 ROM の `XBTAB` の署名・ID・後半バンク番号を
  照合する）

MSSE 固有のスクリプトを各リポジトリが持つことは妨げない。回帰の役に立つ。
ただし**そのリポジトリの完了条件には入れない**。

### 見つけた欠陥は、見つけた側が直して PR で返す

**MSSE 統合版に固有の機能で見つかった欠陥は、原因がどの ROM にあっても
Y8960BasicExtension が調査し、修正し、`vendor/` のサブモジュール経由で
その ROM のリポジトリへ PR を送る。**

理由は保証の分担と同じところから出ている。128KB のイメージを組めるのは
Y8960BasicExtension だけなので、**再現できるのも、直したことを確かめられるのも
そこだけ**である。依頼だけを渡すと、受け取った側は自分の修正が効いたか
どうかを確かめられないまま出すことになる。

修正そのものは相手のリポジトリの木でしか意味を持たない。だから統合側に
パッチを溜めるのではなく、サブモジュールの作業ツリーで直して PR にする。
単体版に同じ欠陥が残らないのは前と同じで、直しが上流に入るためである。

手順。

1. **`vendor/<repo>` で作業する。`../<repo>` の作業リポジトリでは作業しない。**
   隣は別のセッションが編集していることがある。書く前に両方の `git status`
   を見て、相手が同じファイルを触っていないか確かめる
2. `git fetch` して、**origin の既定ブランチから枝を切る。** 固定されている
   コミットから切ると、その後に入った変更と衝突する
3. 直したパスだけを staged して即コミットし、push して `gh` で PR を出す
4. PR が入ったら、`vendor/` のコミットを進め、**その中でビルドし直して**
   （`build/` は gitignore されているので、進めるだけでは古い ROM が残る）
   統合側の試験を回す

**単体版でその欠陥が出ないことの確認は、相手のリポジトリの責任のまま。**
Y8960BasicExtension が確かめられるのは統合版だけで、単体版のハーネスは相手の
リポジトリにしかない。

この形をとるのは**欠陥**のとき。仕様を変える、機能を足す、といった依頼は
これまでどおり `doc/prompt-*.md` に書いて相手のセッションに渡す ―― 相手が
決めることを、見つけた側が実装で先取りしない。

## openMSX の場所

**環境変数 `OPENMSX_DIR` を唯一の正とする。リポジトリは既定値を持たない。**

openMSX はインストーラを使わず展開して置くことが多く、置き場所がマシン
ごとに違う。PATH にもレジストリにも入らないので、システムに聞いて分かる
方法が無い。各リポジトリがソースに既定値を書くと、書いた時点のそのマシンの
事情がリポジトリごとに固まって割れていき、**外れたことが分かるのは openMSX
を起動しようとした瞬間**になる。

- `OPENMSX_DIR` は `openmsx.exe` のあるフォルダを指す
- 未設定なら、openMSX を起動する前に案内を出して `exit 1`
- 設定されているが実行ファイルが無い場合は、見に行ったパスを出して
  `exit 1`。設定漏れと置き場所間違いは直し方が違うので、文言を分ける

使う側はマシンごとに一度設定すればよく、6本すべてに効く。

```
setx OPENMSX_DIR "<openmsx.exe のあるフォルダ>"
```

`OPENMSX_USER_DIR`（`persistent` やユーザー側 `share` の置き場所）は既定を
持ったままでよい。`~/Documents/openMSX` は openMSX 自身がユーザーディレクト
リを置く場所で、マシンによって変わるものではない。

ハーネスを直すときは、`OPENMSX_DIR` を実行ファイル以外にも使っていないかを
見る。素の machine を探すのに openMSX のインストール先を見ているハーネスが
あり、そこも未設定を通る形にしないと `None` が漏れる。

確かめ方は3通り。

| | 期待 |
|---|---|
| `OPENMSX_DIR` 未設定 | 案内を出して `exit 1` |
| 存在しないフォルダを設定 | どのパスを見に行ったかを出して `exit 1` |
| 正しく設定 | 従来どおり走る |

## サイレント実行

**openMSX はウィンドウを作らずに走らせる。既存のスクリプトも例外なく。**

openMSX のウィンドウはキーボードのフォーカスを奪う。試験中に手元でキーを
打つと、それがそのままエミュレートされた MSX のキーマトリクスへ入り、
打ち込み中の BASIC の行が壊れる。並行して走る別の作業ともフォーカスを
奪い合う。ウィンドウが無ければ届きようがない。

共通部（`prelude.tcl`）の先頭で切る。

```tcl
if {![info exists ::env(OMSX_VIDEO)]} {
    set ::renderer none
}
```

`OMSX_VIDEO` を付けたときだけウィンドウが戻る。落ちた試験を目で見たい
ときのための逃げ道で、既定はサイレント。

代償はスクリーンショットで、`renderer none` では `screenshot` が
`Current renderer doesn't support taking screenshots.` で失敗する。試験の
最後で撮っていると、このエラーが結果を置き換えてしまう。撮る側を
`OMSX_VIDEO` で括るか、少なくとも `catch` で包んで結果を壊さないようにする。

```tcl
proc snap {name} {
    if {[info exists ::env(OMSX_VIDEO)]} {
        screenshot -raw [file join [file dirname $::env(OMSX_OUT)] $name]
    }
}
```

画面の内容を判定に使いたい場合は、スクリーンショットではなく VRAM を
読む。`renderer none` でも読めるので、サイレントのまま画面上のエラー
メッセージを拾える。

ハーネスの Python 側も openMSX の標準出力を捨て、標準エラーだけを拾って
結果に添える。ウィンドウが無いぶん、Tcl の遅延コマンドで起きたエラーは
どこにも出ない ―― openMSX がダイアログに出すだけだからで、出力ファイルは
書かれないまま試験が固まる。遅延させる本体は `catch` で包み、エラーを
出力ファイルへ落としてから終わること。

## proc の名前

**テストスクリプトが定義する proc に openMSX が使う名前を取られても、
Tcl は黙って通す。壊れるのは別のところで、エラーはどこにも出ない。**

たとえば `proc step`。`step` は openMSX が
`share/scripts/_disasm.tcl` から提供する名前で、この名前を取ると次のことが
起きる。

1. どこかが `peek16` を呼ぶ。openMSX は `_disasm.tcl` を**そのとき初めて**
   読み込む（`share/scripts/lazy.tcl` の遅延ロード）
2. そのスクリプトの末尾は `namespace import disasm::*` で、こちらが取った
   名前とぶつかり `can't import command "step": already exists` で失敗する
3. 遅延ローダーは **source する前に**そのスクリプトを一覧から外している
   ので、失敗は恒久的になる。`peek16` は二度と定義されない
4. 打鍵の `type_via_keybuf` はブレークポイントの中で `peek16` を使うので、
   以後1文字も MSX へ届かない。例外はブレークポイントの中で起きるため、
   出力にも画面にも出ない

結果として出るのは「どのステートメントも効かなかった」という試験結果で、
名前を取ったこととは何のつながりも見えない。この形はリポジトリをまたいで
繰り返し起きる。

### 止め方

**名前の一覧を人が覚えるのではなく、`proc` を包んで openMSX に問い合わせる。**
共通部（`prelude.tcl`）に置く。

```tcl
rename proc ::_proc
::_proc proc {name arglist body} {
    if {[::openmsx::is_command_name $name]} {
        catch {puts $::emu_out "!! proc $name: openMSX already uses that name"}
        catch {flush $::emu_out}
        exit 1
    }
    uplevel 1 [list ::_proc $name $arglist $body]
}
```

`::openmsx::is_command_name`（`share/init.tcl`）は、**読み込み済みの
コマンドに加えて、まだ読み込まれていない遅延スクリプトが提供する名前も**
見る。`info commands` で自前に判定すると、いちばん危ない遅延分をすり抜ける
―― 上の `step` はまさにそれで、`_disasm.tcl` が読まれるまでコマンドとして
存在しない。

出力ファイルへ書いてから止めること。`exit` するだけでは、ハーネスは中身の
無い結果ファイルを読んで「出力なし」とだけ言う。

包みを外す口も要る。試験が始まったあとは openMSX が自分のスクリプトを
読み込んで自分のコマンドを定義し直すことがあり、それはこちらの関知する
ところではない。最初の遅延コマンド（すべて `safe` を通る）で戻す。

```tcl
::_proc unguard {} {
    if {[info commands ::_proc] ne ""} {
        rename ::proc {}
        rename ::_proc ::proc
    }
}
```

したがって**この検査が効くのはスクリプトの読み込み中に定義される proc
だけ**で、試験の実行中に定義するものは見ない。テストスクリプトの proc は
読み込み時に定義されるので、実用上はこれで足りる。

### グローバル変数も同じ

openMSX の設定は Tcl のグローバル変数として見えているので、`set ::samples
{}` のような代入は設定そのものを壊す。壊れ方はエミュレータが進まなくなる
だけで、やはりエラーも出力も出ない。`::wt_smp` のように接頭辞を付ける。
**`proc` の包みはこちらを捕まえない。**

## 並行して走らせる

セッションは同時に動く。**ひとつの実行が触るファイルは、その実行だけの
ものにする。**

openMSX は**カートリッジのイメージを走っている間ずっと掴んでいる**（マップ
する）。掴まれている間に何ができて何ができないかは、Windows 10 上の openMSX で
測った（2026-09-05）。

| 操作 | 結果 |
|---|---|
| 読む | 通る |
| `open(path, "wb")`（切り詰め） | `[Errno 22] Invalid argument` |
| 一時ファイルを作って置き換え | `PermissionError: [WinError 5]` |
| 消す・改名する | `PermissionError: [WinError 32]` |

**つまり別セッションのビルドが成果物を更新できない。** しかも Errno 22 は
誰が掴んでいるかを何も言わない。失敗するのはビルドのほうで、走っている
試験は何事もなく通るので、原因が見えにくい。イメージ自体は壊れない
（切り詰めが `open` の時点で弾かれるので、中身は元のまま残る）。

### 実行ごとの作業ディレクトリ

**ビルドの成果物をそのままエミュレータへ渡さない。** ハーネスがその実行
専用のディレクトリへ複製し、複製のほうを挿す。

同じ理屈で、**その実行が書くものはすべてそこへ置く** ―― 結果のテキスト、
ビルドから起こしたシンボル表、スクリーンショット。同時に走る2本が同じ
出力ファイルへ書くと中身が混ざり、シンボル表を共有すると、別のビルドの
番地でブレークポイントが置かれる。どちらもエラーにはならない。

実行が終わったら、結果だけを定位置（`out/<machine>/`）へ移してディレクトリ
ごと捨てる。定位置に残るのは完結したファイルだけになる。

複製の**ファイル名は変えない**。openMSX のデバッガブル名はファイル名から
できているので（`<name>.rom romblocks`）、名前を変えると Tcl 側が見に行く
先が変わる。

machine 定義の XML から ROM を指している場合は、XML の `<filename>` も
実行ごとの複製を指す必要がある。マシン名ごと実行専用にすることになる。

### ビルド側

掴まれていて書けなかったときは、**理由を書いて止まる**。Errno 22 のまま
上げてもエミュレータの話だとは分からない。

```python
    try:
        with open(out_path, "wb") as f:
            f.write(image)
    except OSError as e:
        sys.exit(f"{out_path} not written: {e}\n"
                 "Something has the image open - an emulator running it "
                 "holds it for the whole run.")
```

古い openMSX を探して落とす、という手は採らない。並行して走っている別
セッションの試験を殺す。

### 期限を2つ置く

**この規則だけでは足りない。**残った openMSX を前にすると、名前で探して落とす
誘惑が戻ってくる。名前で探して落とすと（`Get-Process openmsx | Stop-Process`
など）、並行して走っている別のリポジトリの試験も巻き込む。

孤児が生まれる道筋はこうである。

| | |
|---|---|
| 1 | `safe` で包んでいない `after` の中で Tcl エラーが出て、誰も `finish` を呼ばない |
| 2 | openMSX 側に期限が無いので、そのまま生き続ける |
| 3 | ランナーの `subprocess.run` に `timeout` が無いので、親が待ち続ける |
| 4 | ハーネスが親だけを切る。**子が孤児になる** |
| 5 | 孤児が CPU を食い続ける |

**2 と 3 を塞げば、名前で探して落とす理由そのものが無くなる。**規則を繰り返す
のではなく、規則を守らなくて済む形にする。

| 塞ぐもの | 置き場所 | 単位 | 既定 | 上書き |
|---|---|---|--:|---|
| 試験が `finish` を呼ばない | `prelude.tcl` | エミュレート時間 | 1800 秒 | `OMSX_DEADLINE` |
| openMSX 自体が進まない | 各リポジトリのランナー | 実時間 | 600 秒 | `OMSX_RUN_TIMEOUT` |

前者は結果ファイルへ「期限切れ」と書いて抜ける。**症状が「終わらない」から
「結果の1行」に変わる**のが要点で、そこが読めれば次の人は当たれる。後者は
`subprocess.run(..., timeout=)` で、これは期限切れのときに自分の子を kill して
から投げ直す ―― **自分が起こしたものだけを相手にする。**

**前者が先に効くように値を選ぶ。**単位が違うので直接は比べられないが、
`throttle off` ではエミュレート時間のほうがずっと速く進むので、既定値どうしなら
前者が先に来る。逆転すると、結果の1行を書く前に kill されて症状は「終わらない」
に戻る。実時間の期限を下げるときは、この向きを確かめること。

ランナーの名前はリポジトリごとに違う（`run.py`／`run_sfg.py`）ので、実装は
各リポジトリに任せる。取り決めは「期限を2つ持つこと」「単位と既定値」
「名前で探さないこと」までである。

試験が期限に届くようになったら、期限を上げる前になぜ長いのかを見ること。

**実装と実測は SFGBasicExtension にある**（`tools/emu/tcl/prelude.tcl` と
`tools/emu/run_sfg.py`）。`finish` を呼ばない tcl は 1.4 秒で「期限切れ」を
書いて終わり、`OMSX_RUN_TIMEOUT=2` で走らせると落として報告し、openMSX は
残らない。全 28 本 × 8 構成で期限は誤爆しない。**他のリポジトリでは未検証。**

### openMSX が書き込む先

イメージのほかに、openMSX 自身が書く場所が2つあり、**どちらも既定では
リポジトリをまたいで共有されている**。

| | 場所 | 中身 |
|---|---|---|
| `OPENMSX_HOME` | `~/Documents/openMSX` | `persistent/<machine>/untitled1/` の CMOS・SRAM・firmwareswitch |
| `OPENMSX_USER_DATA` | `~/Documents/openMSX/share` | BIOS ROM（`systemroms`）、`machines`、`extensions`、`settings.xml` |

マシンのインスタンス名は openMSX のプロセスごとに `untitled1` から振られる
ので、**同じマシンを2つのセッションが同時に走らせると、同じ
`persistent/<machine>/untitled1/` を共有する。** 一方の CMOS や SRAM が
他方に残り、片方が消しにいけば走っている側の足元が消える。

**`OPENMSX_HOME` を実行専用ディレクトリに向ける。**`OPENMSX_USER_DATA` も
一緒に明示すること ―― 既定が `<home>/share` なので、home だけ動かすと BIOS
ROM とマシン定義まで一緒に消え、何も起動しなくなる（`!! no output
(exit=1)` になる）。

```python
    env=dict(os.environ,
             OPENMSX_HOME=str(workdir),          # persistent はここへ
             OPENMSX_USER_DATA=str(USER_SHARE))  # systemroms と machines は共有のまま
```

まっさらな `persistent` から起動して問題ないことは、FS-A1FX / A1WX / A1ST /
A1GT の4機種で確かめてある（2026-09-06）。毎回工場出荷状態から始まるので、
前の実行の状態が次に残らない。温めた `persistent` を必要とする機種に当たっ
たら、共有のものからその実行のディレクトリへ複製して種にする ―― 共有側を
書き換えるのではなく。

### settings.xml を共有ファイルへ書き戻さない

`settings.xml` は `share` の下、つまり**共有側**にある。そして openMSX は
**既定で終了時にそこへ書き戻す**（`save_settings_on_exit` の既定は true）。
試験が変えた設定がそのまま残り、他のリポジトリの実行にも、手で起動した
openMSX にも効く。同時に終わった2本は書き込みを取り合う。

共通部（`prelude.tcl`）で切る。読むのはそのままで、書き戻しだけが止まる。

```tcl
set save_settings_on_exit off
```

**ハーネスが必要とする設定は、共有ファイルに入っていることを当てにせず、
自分で書く。** あるリポジトリが共有ファイルに残した値（たとえば
`default_type_proc`）は、他のリポジトリの試験にも効く。共有ファイルを
掃除した誰かが、別のリポジトリの試験の打鍵方法を黙って変えることになる。

`share/.filecache`（ROM の sha1 索引）も共有側に書かれるが、これは
キャッシュなので放置する。
