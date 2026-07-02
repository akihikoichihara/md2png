# md2png

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Markdown ファイルを高品質な PNG 画像に変換する CLI ツール。
Markdown の表を TeX / スライド / ドキュメントに貼れる画像として書き出せます。

A CLI tool that converts Markdown files into high-quality PNG images.
Ideal for embedding Markdown tables into TeX, slides, or documents.

`Markdown → HTML →（Chromium レンダリング）→ PNG` の流れで変換し、
`device_scale_factor` を上げて **約 300dpi 相当**の解像度を確保します。
表の外接矩形＋外余白でぴったり切り出すため、印刷・PDF 化しても罫線が欠けません。

Converts via `Markdown → HTML → Chromium rendering → PNG`,
achieving **~300 dpi** resolution via `device_scale_factor`.
The output is cropped to the table bounds with outer padding,
so borders never disappear when printed or embedded in a PDF.

---

## セットアップ / Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

日本語フォントは OS 標準のもの（Mac: 游ゴシック / Hiragino、Windows: Yu Gothic、
Linux: 要 `Noto Sans JP` インストール）を自動で使います。

Japanese fonts are picked up automatically from the OS
(Mac: Hiragino / 游ゴシック, Windows: Yu Gothic,
Linux: install `Noto Sans JP` separately).

---

## 使い方 / Usage

```bash
# 入出力を指定 → fig-1.png を出力
# Specify input and output → writes fig-1.png
python md2png.py -i ./hyou1.md -o ./fig-1.png

# 出力を省略 → 入力と同名の hyou1.png を出力
# Omit output → writes hyou1.png (same stem as input)
python md2png.py -i ./hyou1.md

# 4象限などヘッダなしの表を対等なマスとして描画
# Render all cells equally (no header highlight) — for quadrant matrices etc.
python md2png.py -i ./quad.md --flat

# 解像度を上げる（約 384dpi）
# Increase resolution (~384 dpi)
python md2png.py -i ./hyou1.md -s 4
```

---

## オプション / Options

| オプション / Option | 説明 / Description | 既定値 / Default |
|---|---|---|
| `-i`, `--input` | 入力 Markdown ファイル（必須）/ Input Markdown file (required) | — |
| `-o`, `--output` | 出力 PNG ファイル / Output PNG file | 入力と同名の `.png` / Same stem as input |
| `-s`, `--scale` | `device_scale_factor`（≒ dpi） | `3.125`（≒ 300dpi） |
| `--flat` | ヘッダ強調・縞模様を消し全マスを対等に / Disable header highlight and row stripes | 無効 / off |

---

## スタイル / Styles

| モード / Mode | 見た目 / Appearance | 用途 / Use case |
|---|---|---|
| 通常 / Default | 1 行目をグレーのヘッダとして強調＋偶数行に薄い縞 / Grey header row + alternating row stripes | 見出し付きの一般的な表 / Standard tables with a header |
| `--flat` | 全マスを白・対等に描画 / All cells white and equal | 4象限マトリクスなどヘッダを持たない表 / Quadrant matrices and headerless tables |

いずれも外枠は角丸（`border-radius: 10px`）で、罫線の外側に 16px の余白が入ります。

Both modes use rounded corners (`border-radius: 10px`) and 16 px outer padding around the border.

---

## CSS のカスタマイズ / CSS Customization

`md2png.py` 内の `CSS`（通常スタイル）と `FLAT_CSS`（`--flat` 時の上書き）を編集することで、
表の見た目を自由に変えられます。

Edit `CSS` (base style) and `FLAT_CSS` (overrides applied with `--flat`) in `md2png.py`
to customize the table appearance.

| 変数 / Variable | 役割 / Role |
|---|---|
| `CSS` | 全モード共通の基本スタイル / Base style applied to all modes |
| `FLAT_CSS` | `--flat` 指定時に `CSS` へ追記される上書きスタイル / Overrides appended when `--flat` is used |

代表的なカスタマイズ例 / Common customizations:

```python
# 角丸の強さ（既定 10px）/ Corner radius (default 10px)
border-radius: 10px;

# 外余白の量（既定 16px）/ Outer padding (default 16px)
.wrap { padding: 16px; }

# フォントサイズ（既定 15px）/ Font size (default 15px)
.wrap { font-size: 15px; }

# ヘッダの背景色（既定 #f0f3f6）/ Header background color (default #f0f3f6)
th { background: #f0f3f6; }

# 外枠・罫線の色（既定 #c8c8c8）/ Border color (default #c8c8c8)
border: 1px solid #c8c8c8;
```

---

## Markdown の書き方メモ / Markdown Tips

- 表は **ヘッダ行 + 区切り行（`|---|---|`）+ データ行** が必須です。
  Tables require a **header row + separator row (`|---|---|`) + data rows**.
- セル内で改行したいときは `<br>` を使います（表のセルは生の改行を扱えません）。
  Use `<br>` for line breaks inside cells (raw newlines are not supported in table cells).
- 列の寄せは区切り行のコロンで指定します（`|:--|`＝左、`|--:|`＝右、`|:--:|`＝中央）。
  Column alignment is set with colons in the separator row (`|:--|` left, `|--:|` right, `|:--:|` center).

```markdown
| 項目 | 内容 | 値 |
|:-----|:-----|----:|
| 速度 | 平均 | 12.3 |
| 標高 | 最大 | 456 |
```

---

## 動作確認用ファイル / Sample Files

| ファイル / File | 内容 / Description |
|---|---|
| `hyou1.md` / `hyou1.png` / `fig-1.png` | 基本の表 / Basic table (`-i` only and `-i -o` patterns) |
| `quad.md` / `quad-flat.png` / `quad-normal.png` | 4象限表 / Quadrant table (`--flat` on and off) |

---

## ライセンス / License

[MIT License](LICENSE) © 2026 Akihiko Ichihara
