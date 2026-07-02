# md2png

Markdown ファイルを高品質な PNG 画像に変換する CLI ツール。
Markdown の表を TeX / スライド / ドキュメントに貼れる画像として書き出せます。

`Markdown → HTML →（Chromium レンダリング）→ PNG` の流れで変換し、
`device_scale_factor` を上げて **約 300dpi 相当**の解像度を確保します。
表の外接矩形＋外余白でぴったり切り出すため、印刷・PDF 化しても罫線が欠けません。

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install markdown playwright
playwright install chromium
```

日本語フォントは OS 標準のもの（Mac: 游ゴシック / Hiragino、Windows: Yu Gothic、
Linux: 要 `Noto Sans JP` インストール）を自動で使います。

## 使い方

```bash
# 入出力を指定 → fig-1.png を出力
python md2png.py -i ./hyou1.md -o ./fig-1.png

# 出力を省略 → 入力と同名の hyou1.png を出力
python md2png.py -i ./hyou1.md

# 4象限などヘッダなしの表を対等なマスとして描画
python md2png.py -i ./quad.md --flat

# 解像度を上げる（約 384dpi）
python md2png.py -i ./hyou1.md -s 4
```

## オプション

| オプション | 説明 | 既定値 |
|---|---|---|
| `-i`, `--input` | 入力 Markdown ファイル（必須） | — |
| `-o`, `--output` | 出力 PNG ファイル | 入力と同名の `.png` |
| `-s`, `--scale` | `device_scale_factor`（≒ dpi） | `3.125`（≒ 300dpi） |
| `--flat` | ヘッダ強調・縞模様を消し全マスを対等に | 無効（グレーヘッダ） |

## スタイル

| モード | 見た目 | 用途 |
|---|---|---|
| 通常 | 1 行目をグレーのヘッダとして強調＋偶数行に薄い縞 | 見出し付きの一般的な表 |
| `--flat` | 全マスを白・対等に描画 | 4象限マトリクスなどヘッダを持たない表 |

いずれも外枠は角丸（`border-radius: 10px`）で、罫線の外側に 16px の余白が入ります。

## CSS のカスタマイズ

`md2png.py` 内の `CSS`（通常スタイル）と `FLAT_CSS`（`--flat` 時の上書き）を編集することで、
表の見た目を自由に変えられます。

| 変数 | 役割 |
|---|---|
| `CSS` | 全モード共通の基本スタイル |
| `FLAT_CSS` | `--flat` 指定時に `CSS` へ追記される上書きスタイル |

代表的なカスタマイズ例：

```python
# 角丸の強さ（既定 10px）
border-radius: 10px;

# 外余白の量（既定 16px）
.wrap { padding: 16px; }

# フォントサイズ（既定 15px）
.wrap { font-size: 15px; }

# ヘッダの背景色（既定 #f0f3f6）
th { background: #f0f3f6; }

# 外枠・罫線の色（既定 #c8c8c8）
border: 1px solid #c8c8c8;
```

## Markdown の書き方メモ

- 表は **ヘッダ行 + 区切り行（`|---|---|`）+ データ行** が必須です。
- セル内で改行したいときは `<br>` を使います（表のセルは生の改行を扱えません）。
- 列の寄せは区切り行のコロンで指定します（`|:--|`＝左、`|--:|`＝右、`|:--:|`＝中央）。

```markdown
| 項目 | 内容 | 値 |
|:-----|:-----|----:|
| 速度 | 平均 | 12.3 |
| 標高 | 最大 | 456 |
```

## 動作確認用ファイル

| ファイル | 内容 |
|---|---|
| `hyou1.md` / `hyou1.png` / `fig-1.png` | 基本の表（`-i` のみ / `-i -o` 両パターン） |
| `quad.md` / `quad-flat.png` / `quad-normal.png` | 4象限表（`--flat` あり / なしの比較） |
