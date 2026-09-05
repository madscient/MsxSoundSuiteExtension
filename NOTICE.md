# 権利表示

## 利用条件

このリポジトリで配布している ROM イメージは、**個人利用に限り**許諾されて
います。

**ROM イメージの再配布には、MSX ライセンシングコーポレーションの許諾が別途
必要です。** 再配布に当たる行為には、ROM イメージを含むファイルの公開・
頒布、他のソフトウェアへの同梱、ROM を書き込んだ媒体の配布が含まれます。

## 拡張BASIC / BIOS 本体

MSX-MUSIC Basic Extension、MSX-AUDIO Basic Extension Lite、SFG Basic
Extension、MIDI Play Basic Extension は、日本楽器製造株式会社（YAMAHA）
および株式会社アスキーの著作物をフォークして改造したものです。ソース
コードは公開しません。

Y8960 Basic Extension および Y8960 シーケンサーBIOS は新規に書き起こした
ものです。

## リズム音色データ

MSX-AUDIO Basic Extension Lite が持つリズム音色3本（`TB_RTM`）は、OPLL の
ROM リズム音色を Y8950 のレジスタへ変換したものです。出典は下記です。

> "Copyright free OPLL(x) ROM patches"
> https://github.com/plgDavid/misc/wiki/Copyright-free-OPLL(x)-ROM-patches
> David Viens, Hubert Lamontagne 作, CC BY-SA

これを含む ROM（`standalone/mabel.rom`、`y8960bas.rom`）について許諾を得て
再配布する場合は、この出典を明記してください。

## ハードウェア

Y8960 は [Y8960_Cartridge](https://github.com/hra1129/Y8960_Cartridge) です。
本リポジトリの成果物はそのファームウェアであり、ハードウェア自体は含みません。
