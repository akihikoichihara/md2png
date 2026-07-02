#!/usr/bin/env python3
"""Markdown ファイルを高品質な PNG に変換する汎用ツール。

使い方:
    md2png.py -i ./hyou1.md -o ./fig-1.png   # 入出力を指定
    md2png.py -i ./hyou1.md                   # 省略時は ./hyou1.png を出力

Markdown → HTML →（Chromium レンダリング）→ PNG の流れ。
device_scale_factor で 300dpi 相当の解像度を確保する。
"""
import argparse
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

# --- レンダリング用の CSS（角丸・外余白つきの標準テーブルスタイル） ---
CSS = """
  body { margin: 0; padding: 0; background: #fff; }
  /* 内容を包む余白枠。この div を撮影して罫線の外側に余白を確保する
     （要素単位スクショは margin/外側 padding を無視するため、内側 padding で効かせる） */
  .wrap {
    display: inline-block;
    padding: 16px;
    background: #fff;
    font-family: "Yu Gothic", "Hiragino Sans", "Noto Sans JP", sans-serif;
    font-size: 15px;
    color: #1a1a1a;
  }
  table {
    /* 角丸を効かせるため separate にし、セル間の隙間は 0 にする */
    border-collapse: separate;
    border-spacing: 0;
    /* 外枠と角丸。overflow:hidden で角からはみ出す罫線を切り落とす */
    border: 1px solid #c8c8c8;
    border-radius: 10px;
    overflow: hidden;
  }
  th, td {
    /* 内側の罫線は右・下のみ引いて二重線を防ぐ */
    border-right: 1px solid #c8c8c8;
    border-bottom: 1px solid #c8c8c8;
    padding: 10px 16px;
    text-align: left;
  }
  /* 各行の最終セルは右罫線を消す（外枠と重なるため） */
  th:last-child, td:last-child { border-right: none; }
  /* 最終行は下罫線を消す（外枠と重なるため） */
  tr:last-child td { border-bottom: none; }
  th {
    background: #f0f3f6;
    font-weight: 600;
    border-bottom: 2px solid #888;
  }
  tr:nth-child(even) td { background: #fafbfc; }
"""

# --flat 用の上書き CSS。ヘッダ強調・縞模様を消して全マスを対等に見せる
# （4象限マトリクスやヘッダを持たない表向け）。CSS は後勝ちなので末尾に連結する。
FLAT_CSS = """
  th { background: #fff; font-weight: 400; border-bottom: 1px solid #c8c8c8; }
  tr:nth-child(even) td { background: #fff; }
  th, td { vertical-align: top; }
"""


def md_to_png(
    input_path: Path, output_path: Path, scale: float, flat: bool = False
) -> None:
    md_text = input_path.read_text(encoding="utf-8")

    # Markdown -> HTML（table 拡張などを有効化）
    body_html = markdown.markdown(
        md_text, extensions=["tables", "fenced_code", "sane_lists"]
    )

    style = CSS + FLAT_CSS if flat else CSS
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>{style}</style></head>
<body><div class="wrap">{body_html}</div></body></html>"""

    with sync_playwright() as p:
        browser = p.chromium.launch()
        # device_scale_factor=3.125 で 96dpi×3.125 ≒ 300dpi 相当
        page = browser.new_page(device_scale_factor=scale)
        page.set_content(html)
        page.locator(".wrap").screenshot(path=str(output_path))
        browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Markdown ファイルを高品質な PNG に変換する。"
    )
    parser.add_argument(
        "-i", "--input", required=True, help="入力 Markdown ファイル（.md）"
    )
    parser.add_argument(
        "-o",
        "--output",
        help="出力 PNG ファイル（省略時は入力と同名の .png）",
    )
    parser.add_argument(
        "-s",
        "--scale",
        type=float,
        default=3.125,
        help="device_scale_factor（既定 3.125 ≒ 300dpi）",
    )
    parser.add_argument(
        "--flat",
        action="store_true",
        help="ヘッダ強調・縞模様を消して全マスを対等に（4象限などヘッダなしの表向け）",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        parser.error(f"入力ファイルが見つかりません: {input_path}")

    # 出力未指定なら入力と同じ場所・同じ名前で拡張子を .png に
    output_path = Path(args.output) if args.output else input_path.with_suffix(".png")

    md_to_png(input_path, output_path, args.scale, args.flat)
    print(f"{output_path} を出力しました")


if __name__ == "__main__":
    main()
