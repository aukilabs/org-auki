#!/usr/bin/env python3
"""Assemble a self-contained slide deck from an HTML skeleton.

The AI writes slide content and boilerplate HTML with placeholder comments.
This script handles every large binary asset the AI must not attempt to inline
itself — those files are too large to paste through LLM output without truncation.

Usage:
    python3 assemble.py <skeleton.html> [<output.html>] [--theme auki|cactus|gotu]

    If output.html is omitted, the input file is assembled in-place.
    --theme defaults to auki if not supplied.

Placeholders the AI should write (exact strings, case-sensitive):

    In <head>:
        <!-- REVEAL_CSS_PLACEHOLDER -->
        <!-- AUKI_THEME_PLACEHOLDER -->

    In <body> (before Reveal.initialize()):
        <!-- REVEAL_JS_PLACEHOLDER -->

    In logo <img> src attributes (copy verbatim from template.html):
        MONOGRAM_WHITE_B64
        MONOGRAM_BLACK_B64
        WORDMARK_WHITE_B64
        WORDMARK_BLACK_B64

All other HTML (slides, chrome, scripts) is written by the AI and left untouched.

Theme behaviour:
    auki   — TT Firs Neue embedded, Auki orange palette, Auki logos
    cactus — Questrial + Nunito Sans (CDN), Cactus green palette, Cactus logos
    gotu   — DM Sans Bold/Regular (CDN), Gotu blue palette, Gotu logos

For non-Auki themes, auki-theme.css provides the base layout rules and the
brand theme CSS (cactus-theme.css / gotu-theme.css) is inlined immediately
after as a cascade override. TT Firs Neue is NOT embedded for non-Auki themes.
"""

import sys
import argparse
import base64
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
# scripts/ -> slides/ -> presentation/ -> skills/ -> src/ -> design/
DESIGN_DIR = SCRIPT_DIR.parent.parent.parent.parent / "design"

PLACEHOLDERS = [
    "REVEAL_CSS_PLACEHOLDER",
    "AUKI_THEME_PLACEHOLDER",
    "REVEAL_JS_PLACEHOLDER",
    "MONOGRAM_WHITE_B64",
    "MONOGRAM_BLACK_B64",
    "WORDMARK_WHITE_B64",
    "WORDMARK_BLACK_B64",
    "DECK_DEFAULT_THEME",
]

# Default colour mode per theme (used to replace DECK_DEFAULT_THEME placeholder)
THEME_DEFAULT_MODE = {
    "auki":   "dark",
    "cactus": "dark",
    "gotu":   "light",
}

# Logo file mapping per theme.
# MONOGRAM_WHITE = dark-background logo (shown in dark mode)
# MONOGRAM_BLACK = light-background logo (shown in light mode)
# WORDMARK_* = same as monogram for non-Auki themes (no separate wordmark)
THEME_LOGOS = {
    "auki": {
        "MONOGRAM_WHITE_B64": "auki-monogram-white.svg",
        "MONOGRAM_BLACK_B64": "auki-monogram-black.svg",
        "WORDMARK_WHITE_B64": "auki-wordmark-white.svg",
        "WORDMARK_BLACK_B64": "auki-wordmark-black.svg",
    },
    "cactus": {
        "MONOGRAM_WHITE_B64": "cactus-dark.svg",    # light logo for dark bg
        "MONOGRAM_BLACK_B64": "cactus-light.svg",   # dark logo for light bg
        "WORDMARK_WHITE_B64": "cactus-dark.svg",
        "WORDMARK_BLACK_B64": "cactus-light.svg",
    },
    "gotu": {
        "MONOGRAM_WHITE_B64": "gotu-dark.svg",      # light logo for dark bg
        "MONOGRAM_BLACK_B64": "gotu-light.svg",     # dark logo for light bg
        "WORDMARK_WHITE_B64": "gotu-dark.svg",
        "WORDMARK_BLACK_B64": "gotu-light.svg",
    },
}


def b64_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def inline_fonts(css: str) -> str:
    """Replace TT Firs Neue relative font URLs with base64 data URIs."""
    font_dir = DESIGN_DIR / "core" / "fonts"
    for filename in ["TT-Firs-Neue-Regular.ttf", "TT-Firs-Neue-Medium.ttf"]:
        rel = f"../core/fonts/{filename}"
        b64 = b64_file(font_dir / filename)
        css = css.replace(f'url("{rel}")', f'url("data:font/truetype;base64,{b64}")')
    return css


def assemble(input_path: Path, output_path: Path, theme: str) -> None:
    html = input_path.read_text(encoding="utf-8")

    # -- CSS ------------------------------------------------------------------
    reveal_css = (DESIGN_DIR / "slides" / "vendor" / "reveal.css").read_text()
    auki_theme = (DESIGN_DIR / "slides" / "auki-theme.css").read_text()

    html = html.replace(
        "<!-- REVEAL_CSS_PLACEHOLDER -->",
        f"<style>\n{reveal_css}\n</style>",
    )

    if theme == "auki":
        theme_css = inline_fonts(auki_theme)
        style_block = f"<style>\n{theme_css}\n</style>"
    else:
        override_path = DESIGN_DIR / "slides" / f"{theme}-theme.css"
        if not override_path.exists():
            print(f"ERROR: theme file not found: {override_path}", file=sys.stderr)
            sys.exit(1)
        override_css = override_path.read_text(encoding="utf-8")
        # Base layout from auki-theme (no font embedding — theme uses CDN fonts)
        # Override CSS cascades on top via source order
        style_block = (
            f"<style>\n{auki_theme}\n</style>\n"
            f"<style>\n{override_css}\n</style>"
        )

    html = html.replace("<!-- AUKI_THEME_PLACEHOLDER -->", style_block)

    # -- JS -------------------------------------------------------------------
    reveal_js = (DESIGN_DIR / "slides" / "vendor" / "reveal.js").read_text()
    html = html.replace(
        "<!-- REVEAL_JS_PLACEHOLDER -->",
        f"<script>\n{reveal_js}\n</script>",
    )

    # -- Logos ----------------------------------------------------------------
    assets = DESIGN_DIR / "core" / "assets"
    for placeholder, filename in THEME_LOGOS[theme].items():
        html = html.replace(placeholder, b64_file(assets / filename))

    # -- Default theme mode ---------------------------------------------------
    html = html.replace("DECK_DEFAULT_THEME", THEME_DEFAULT_MODE[theme])

    # -- Verify ---------------------------------------------------------------
    remaining = [p for p in PLACEHOLDERS if p in html]
    if remaining:
        print(f"ERROR: unresolved placeholders: {remaining}", file=sys.stderr)
        sys.exit(1)

    # -- Design system guard (Step 9 precondition) -----------------------------
    # Hard check to catch regressions where agent started from blank
    # reveal.js scaffold (CDN + inline styles) instead of template.html
    # + placeholders + assemble.py. This prevents the exact failure mode
    # described in the community deck regression (no pulse-meta, no
    # inlined auki-theme.css, no four logo data-URIs, no IIFEs).
    if 'id="pulse-meta"' not in html:
        print("ERROR: pulse-meta metadata block missing. Skeleton must contain the full Pulse JSON script (id=\"pulse-meta\") before assemble.", file=sys.stderr)
        sys.exit(1)

    if html.count('<style>') < 2:
        print("ERROR: CSS not inlined (expected reveal.css + auki-theme.css). Assemble step incomplete or skipped.", file=sys.stderr)
        sys.exit(1)

    # Check for inlined logos (data URIs for monogram and wordmark variants)
    # Robust check: at least one monogram and one wordmark data URI present.
    if 'data:image/svg+xml;base64,' not in html or html.count('data:image/svg+xml;base64,') < 2:
        print("ERROR: Logo data-URIs not present or incomplete. Skeleton must use MONOGRAM_*_B64 and WORDMARK_*_B64 placeholders from template.html.", file=sys.stderr)
        sys.exit(1)

    # -- Reveal config guard --------------------------------------------------
    # Prevents the exact "minimal config" regression that causes 960×700
    # fallback, right-side overflow, and broken deck-chrome features.
    if 'width:                1280' not in html or 'height:               720' not in html:
        print("ERROR: Reveal.initialize() config is incomplete. Must contain width: 1280 and height: 720 (plus full behavioural flags) copied verbatim from template.html lines 707-751.", file=sys.stderr)
        sys.exit(1)

    output_path.write_text(html, encoding="utf-8")
    print(f"Assembled ({theme}): {output_path}  ({len(html):,} bytes)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Assemble a self-contained slide deck from an HTML skeleton."
    )
    parser.add_argument("input", help="Skeleton HTML file path")
    parser.add_argument("output", nargs="?", help="Output file path (default: in-place)")
    parser.add_argument(
        "--theme",
        choices=["auki", "cactus", "gotu"],
        default="auki",
        help="Brand theme to apply (default: auki)",
    )
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve() if args.output else input_path

    if not input_path.exists():
        print(f"ERROR: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    assemble(input_path, output_path, args.theme)


if __name__ == "__main__":
    main()
