# 作業計画と実行経緯

このリポジトリを保守する側の内部文書。公開しない（`docs/` には複製しない）。
利用者向けは [`README.md`](../README.md)、保守手順は
[`docs/build-and-release.md`](../docs/build-and-release.md)。

## 統合する ROM の探し場所を呼ぶ側から渡す

Y8960 の `rom.py` は統合する4本を自身の `vendor/` と `../<repo>` の両方から
探し、両方在って中身が違えば止まる。Y8960 の作業機では兄弟の作業リポジトリが
常に並んでいるため、この検査が必ず発火して `vendor/` から組めない。探し場所を
呼ぶ側が環境変数で渡せば候補が1つになり、検査そのものが要らなくなる。

依頼元は Y8960BasicExtension（`doc/prompt-msse-prebuilt-dir.md`、4段すべてが
済んだら向こうで削除される）。

**外に出る値**：環境変数 `Y8960_PREBUILT_DIR`。4本のリポジトリが並んでいる
ディレクトリの絶対パス。読むのは Y8960 の `rom.py` と MSSE の `package.py`
だけなので、後から変えても波及先は2ファイル。

| | どちら | すること | 状態 |
|--:|---|---|---|
| 1 | MSSE | y8960 のステップに `Y8960_PREBUILT_DIR` を渡す | 済 |
| 2 | Y8960 | `PREBUILT` に `rel` を足し、`rom.py` は渡された根＋`rel` だけを見る。`paths` は残す | 未 |
| 3 | MSSE | `package.py` の `check_cartridge_identity` を `rel` に切り替える | 段2 待ち |
| 4 | Y8960 | `paths` を消す | 未 |

段1 が段2 より先である必要がある。段2 が先に入ると、MSSE 配下では Y8960 の
入れ子 `vendor/` が空（意図的に未初期化）なので統合 ROM を組めなくなる。

### 段3 で行うこと

- `check_cartridge_identity` の候補を `prebuilt["rel"]` から組み、MSSE 自身の
  `vendor` で解決する。候補は1本なので `chosen` の選択は消える
- `ours` / `under()` の判定と `submodule deinit` を勧めるメッセージを消す。
  段2 が入れば `rom.py` は渡された根しか見ないので、入れ子が実体化していても
  混入しない
- sha256 の比較は残す。経路が1本でも、`rom.py` がその版を実際に埋めたかは
  別の事実で、古い `.hex` から組んだ場合はここでしか捕まらない
- `manifest.py` 冒頭の説明と `docs/build-and-release.md` の
  「サブモジュールの配置」「カートリッジと単体版の同一性検査」から、
  `../<repo>` フォールバックと入れ子の話を消す

### 段1 の確度

- **確認済み** ―― `build.run_step` が y8960 の entry にだけ
  `Y8960_PREBUILT_DIR` を渡し、他の entry には渡さないこと。両方の entry で
  `run_step` を呼び、子プロセスで `os.environ` を読んで確かめた
- **確認済み** ―― 段2 が未着手であること。`vendor/Y8960BasicExtension`
  (`ab66f6f`) の `rom.py` は `Y8960_PREBUILT_DIR` を参照せず、`PREBUILT` に
  `rel` も無い。よって段1 は挙動を変えない
- **確認済み** ―― 通しのビルドとパッケージ化。`tools/build.py` が5本すべてを
  組み、`tools/package.py` の同一性検査が4バンクとも `vendor/` のビルド出力と
  一致した。この時点の `rom.py` はまだ `../<repo>` から取っている
