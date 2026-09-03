# MSX Sound Suite Extension

MSX Sound Suite Extension（MSSE）は、[Y8960 カートリッジ](https://github.com/hra1129/Y8960_Cartridge)
向けの拡張BASICと BIOS の総称です。このリポジトリは、その成果物 ROM と
ドキュメントを配布するためのものです。

## 入手

ROM イメージは [Releases](../../releases) から入手してください。

| ファイル | サイズ | 用途 |
|---|--:|---|
| `y8960bas.rom` | 128KB | Y8960 カートリッジ用。下記4つをすべて収めたイメージ |
| `standalone/mmbe.rom` | 16KB | MSX-MUSIC 単体用。本体内蔵 MSX-MUSIC の差し替え、または ROM カートリッジ |
| `standalone/mabel.rom` | 16KB | MSX-AUDIO（Y8950）単体カートリッジ用 |
| `standalone/sfg.rom` | 16KB | SFG-01/05 と併用する単体カートリッジ用 |

`y8960bas.rom` はページ1（`4000H`-`7FFFH`）を4つの拡張BASICで分け合います。
電源投入時に表に出るのは MSX-MUSIC Basic Extension で、`CALL MINIT` /
`CALL MUSIC` / `CALL AUDIO` などで切り替わります。

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

## リポジトリ構成

| | |
|---|---|
| [`docs/`](docs/) | 各リポジトリから複製した公開ドキュメント |
| [`tools/`](tools/) | ビルド・パッケージ化・リリースのスクリプト |
| `vendor/` | 各拡張BASICのソースリポジトリ（サブモジュール、非公開） |
| `dist/` | 生成されたパッケージ（コミットしない） |

`vendor/` の4リポジトリは、ライセンスの都合でソースコードを公開できないため
非公開です。サブモジュールの取得には各リポジトリへのアクセス権が要ります。

## ビルドとリリース

前提:

| | |
|---|---|
| Python | 3.x |
| zmac | [48k.ca/zmac.html](https://48k.ca/zmac.html)。環境変数 `ZMAC_EXE` で場所を指定 |
| GitHub CLI | [cli.github.com](https://cli.github.com/)。`gh auth login` 済みであること |

```sh
git submodule update --init            # 4リポジトリを取得（--recursive は不要）
python tools/build.py                  # 全ROMをビルド
python tools/sync_docs.py              # docs/ を最新のソースから更新
python tools/package.py                # dist/ にパッケージと zip を生成
python tools/release.py v0.1.0         # ビルドからタグ付け・アップロードまで
```

`tools/release.py --dry-run` はビルドとパッケージ化だけを行い、タグ付けと
アップロードを行いません。

`docs/` はコミットして GitHub 上で参照できるようにします。`tools/package.py`
は `docs/` がソースより古いとパッケージ化を拒否するので、`sync_docs.py` の
結果を先にコミットしてください。

各リリースが4つのソースのどの状態を指すかはサブモジュールのコミットで決まり
ます。`tools/release.py` は、このリポジトリに未コミットの変更があるとき、
またはサブモジュールが記録されたコミットからずれているときは実行を拒否します。

`vendor/Y8960BasicExtension` は自身も他の3リポジトリをサブモジュール参照して
いますが、ここでは初期化しません。同じ階層に置いた `vendor/` 配下の3つを
フォールバックとして拾うため、各リポジトリのチェックアウトは1つで済みます。

## 権利

[`NOTICE.md`](NOTICE.md) を参照してください。ROM を再配布するときは、そこに
挙げた出典を明記してください。
