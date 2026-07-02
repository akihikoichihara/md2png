# md2png

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 日本語

Markdown ファイルを高品質な PNG 画像に変換する CLI ツール。
Markdown の表を TeX / スライド / ドキュメントに貼れる画像として書き出せます。

`Markdown → HTML →（Chromium レンダリング）→ PNG` の流れで変換し、
`device_scale_factor` を上げて **約 300dpi 相当**の解像度を確保します。
表の外接矩形＋外余白でぴったり切り出すため、印刷・PDF 化しても罫線が欠けません。

### セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

日本語フォントは OS 標準のもの（Mac: 游ゴシック / Hiragino、Windows: Yu Gothic、
Linux: 要 `Noto Sans JP` インストール）を自動で使います。

### 使い方

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

### オプション

| オプション | 説明 | 既定値 |
|---|---|---|
| `-i`, `--input` | 入力 Markdown ファイル（必須） | — |
| `-o`, `--output` | 出力 PNG ファイル | 入力と同名の `.png` |
| `-s`, `--scale` | `device_scale_factor`（≒ dpi） | `3.125`（≒ 300dpi） |
| `--flat` | ヘッダ強調・縞模様を消し全マスを対等に | 無効（グレーヘッダ） |

### スタイル

| モード | 見た目 | 用途 |
|---|---|---|
| 通常 | 1 行目をグレーのヘッダとして強調＋偶数行に薄い縞 | 見出し付きの一般的な表 |
| `--flat` | 全マスを白・対等に描画 | 4象限マトリクスなどヘッダを持たない表 |

いずれも外枠は角丸（`border-radius: 10px`）で、罫線の外側に 16px の余白が入ります。

### CSS のカスタマイズ

`md2png.py` 内の `CSS`（通常スタイル）と `FLAT_CSS`（`--flat` 時の上書き）を編集することで、
表の見た目を自由に変えられます。

| 変数 | 役割 |
|---|---|
| `CSS` | 全モード共通の基本スタイル |
| `FLAT_CSS` | `--flat` 指定時に `CSS` へ追記される上書きスタイル |

代表的なカスタマイズ例：

```python
border-radius: 10px;        # 角丸の強さ（既定 10px）
.wrap { padding: 16px; }    # 外余白の量（既定 16px）
.wrap { font-size: 15px; }  # フォントサイズ（既定 15px）
th { background: #f0f3f6; } # ヘッダの背景色（既定 #f0f3f6）
border: 1px solid #c8c8c8;  # 外枠・罫線の色（既定 #c8c8c8）
```

### Markdown の書き方メモ

- 表は **ヘッダ行 + 区切り行（`|---|---|`）+ データ行** が必須です。
- セル内で改行したいときは `<br>` を使います（表のセルは生の改行を扱えません）。
- 列の寄せは区切り行のコロンで指定します（`|:--|`＝左、`|--:|`＝右、`|:--:|`＝中央）。

```markdown
| 項目 | 内容 | 値 |
|:-----|:-----|----:|
| 速度 | 平均 | 12.3 |
| 標高 | 最大 | 456 |
```

### 動作確認用ファイル

| ファイル | 内容 |
|---|---|
| `hyou1.md` / `hyou1.png` / `fig-1.png` | 基本の表（`-i` のみ / `-i -o` 両パターン） |
| `quad.md` / `quad-flat.png` / `quad-normal.png` | 4象限表（`--flat` あり / なしの比較） |

### ライセンス

[MIT License](LICENSE) © 2026 Akihiko Ichihara

---

## English

A CLI tool that converts Markdown files into high-quality PNG images.
Ideal for embedding Markdown tables into TeX, slides, or documents.

Converts via `Markdown → HTML → Chromium rendering → PNG`,
achieving **~300 dpi** resolution via `device_scale_factor`.
The output is cropped to the table bounds with outer padding,
so borders never disappear when printed or embedded in a PDF.

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Japanese fonts are picked up automatically from the OS
(Mac: Hiragino / 游ゴシック, Windows: Yu Gothic,
Linux: install `Noto Sans JP` separately).

### Usage

```bash
# Specify input and output → writes fig-1.png
python md2png.py -i ./hyou1.md -o ./fig-1.png

# Omit output → writes hyou1.png (same stem as input)
python md2png.py -i ./hyou1.md

# Render all cells equally (no header highlight) — for quadrant matrices etc.
python md2png.py -i ./quad.md --flat

# Increase resolution (~384 dpi)
python md2png.py -i ./hyou1.md -s 4
```

### Options

| Option | Description | Default |
|---|---|---|
| `-i`, `--input` | Input Markdown file (required) | — |
| `-o`, `--output` | Output PNG file | Same stem as input with `.png` |
| `-s`, `--scale` | `device_scale_factor` (≒ dpi) | `3.125` (≒ 300 dpi) |
| `--flat` | Disable header highlight and row stripes | off |

### Styles

| Mode | Appearance | Use case |
|---|---|---|
| Default | Grey header row + alternating row stripes | Standard tables with a header |
| `--flat` | All cells white and equal | Quadrant matrices and headerless tables |

Both modes use rounded corners (`border-radius: 10px`) and 16 px outer padding around the border.

### CSS Customization

Edit `CSS` (base style) and `FLAT_CSS` (overrides applied with `--flat`) in `md2png.py`
to customize the table appearance.

| Variable | Role |
|---|---|
| `CSS` | Base style applied to all modes |
| `FLAT_CSS` | Overrides appended when `--flat` is used |

Common customizations:

```python
border-radius: 10px;        # Corner radius (default 10px)
.wrap { padding: 16px; }    # Outer padding (default 16px)
.wrap { font-size: 15px; }  # Font size (default 15px)
th { background: #f0f3f6; } # Header background color (default #f0f3f6)
border: 1px solid #c8c8c8;  # Border color (default #c8c8c8)
```

### Markdown Tips

- Tables require a **header row + separator row (`|---|---|`) + data rows**.
- Use `<br>` for line breaks inside cells (raw newlines are not supported in table cells).
- Column alignment is set with colons in the separator row (`|:--|` left, `|--:|` right, `|:--:|` center).

```markdown
| Item | Content | Value |
|:-----|:--------|------:|
| Speed | Average | 12.3 |
| Altitude | Max | 456 |
```

### Sample Files

| File | Description |
|---|---|
| `hyou1.md` / `hyou1.png` / `fig-1.png` | Basic table (`-i` only and `-i -o` patterns) |
| `quad.md` / `quad-flat.png` / `quad-normal.png` | Quadrant table (`--flat` on and off) |

### License

[MIT License](LICENSE) © 2026 Akihiko Ichihara
