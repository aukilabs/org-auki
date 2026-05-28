#!/usr/bin/env python3
"""Assemble a self-contained Auki roundup/page HTML from a skeleton.

Replaces:
  /* ROUNDUP_CSS_PLACEHOLDER */   → full contents of roundup-style.css (inlined)
  MONOGRAM_WHITE_B64              → base64 of auki-monogram-white.svg
  MONOGRAM_BLACK_B64              → base64 of auki-monogram-black.svg
  WORDMARK_WHITE_B64              → base64 of auki-wordmark-white.svg
  WORDMARK_BLACK_B64              → base64 of auki-wordmark-black.svg

Usage:
    python3 assemble-page.py <skeleton.html> [<output.html>]
    If output.html is omitted, assembles in-place.
"""

import sys
import os
import base64
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
# scripts/ -> page/ -> presentation/ -> skills/ -> src/
SRC_DIR    = SCRIPT_DIR.parent.parent.parent.parent
DESIGN_DIR = SRC_DIR / "design"

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def main():
    if len(sys.argv) < 2:
        print("Usage: assemble-page.py <skeleton.html> [<output.html>]", file=sys.stderr)
        sys.exit(1)

    input_path  = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else input_path

    html = input_path.read_text(encoding="utf-8")

    # 1. Inline CSS
    css_path = DESIGN_DIR / "html" / "roundup-style.css"
    css = css_path.read_text(encoding="utf-8")
    html = html.replace("  /* ROUNDUP_CSS_PLACEHOLDER */", css, 1)

    # 2. Inline logos
    assets = DESIGN_DIR / "core" / "assets"
    replacements = {
        "MONOGRAM_WHITE_B64": b64(assets / "auki-monogram-white.svg"),
        "MONOGRAM_BLACK_B64": b64(assets / "auki-monogram-black.svg"),
        "WORDMARK_WHITE_B64": b64(assets / "auki-wordmark-white.svg"),
        "WORDMARK_BLACK_B64": b64(assets / "auki-wordmark-black.svg"),
    }
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)

    # 3. Verify nothing left behind
    missing = [p for p in ["ROUNDUP_CSS_PLACEHOLDER"] + list(replacements.keys()) if p in html]
    if missing:
        print(f"ERROR: unresolved placeholders: {missing}", file=sys.stderr)
        sys.exit(1)

    output_path.write_text(html, encoding="utf-8")
    print(f"Assembled: {output_path}  ({output_path.stat().st_size:,} bytes)")

if __name__ == "__main__":
    main()
