#!/usr/bin/env python3
"""Assemble a self-contained /shiny document and export it as a PDF.

Builds a fully inlined HTML file (fonts embedded), then uses
headless Chrome to render it to PDF. Falls back to HTML if Chrome is
not available.

Replaces in the HTML skeleton:
  /* SHINY_CSS_PLACEHOLDER */   → tokens.css + shiny-style.css, fonts base64-embedded

Usage:
    python3 assemble-shiny.py <skeleton.html> [<output.pdf>]

    Output defaults to the same path as the input, with a .pdf extension.
    Pass a path ending in .html to skip PDF conversion and keep HTML only.
"""

import sys, re, base64, subprocess, shutil, tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SRC_DIR    = SCRIPT_DIR.parent.parent.parent
DESIGN_DIR = SRC_DIR / "design"
FONTS_DIR  = DESIGN_DIR / "core" / "fonts"
ASSETS_DIR = DESIGN_DIR / "core" / "assets"

# Chrome locations to try, in order of preference
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
    shutil.which("chromium-browser") or "",
]

def find_chrome():
    for path in CHROME_CANDIDATES:
        if path and Path(path).exists():
            return path
    return None

def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")

def embed_fonts(css: str) -> str:
    for filename in ["TT-Firs-Neue-Regular.ttf", "TT-Firs-Neue-Medium.ttf", "TT-Firs-Neue-Bold.ttf"]:
        font_path = FONTS_DIR / filename
        if not font_path.exists():
            continue
        encoded = b64(font_path)
        css = re.sub(
            r'url\("[^"]*' + re.escape(filename) + r'"\)',
            f'url("data:font/truetype;base64,{encoded}")',
            css
        )
    return css

def build_css(strip_remote: bool = False) -> str:
    tokens_css = (DESIGN_DIR / "core" / "tokens.css").read_text(encoding="utf-8")
    shiny_css  = (DESIGN_DIR / "html" / "shiny-style.css").read_text(encoding="utf-8")
    tokens_css = embed_fonts(tokens_css)
    if strip_remote:
        # Remove Google Fonts @import so headless Chrome doesn't make network calls
        tokens_css = re.sub(r'@import url\("https://[^"]+"\);?\s*', '', tokens_css)
    return tokens_css + "\n\n" + shiny_css

def build_html(skeleton: str, strip_remote: bool = False, force_light: bool = False) -> str:
    html = skeleton
    if force_light:
        # PDFs are always rendered on white paper — override whatever the user chose
        html = html.replace('data-theme="dark"', 'data-theme="light"')
        html = html.replace("data-theme='dark'", "data-theme='light'")
        # Remove the theme attribute entirely if it wasn't set (defaults to dark)
        html = html.replace('<html lang="en">', '<html lang="en" data-theme="light">')
    html = html.replace("  /* SHINY_CSS_PLACEHOLDER */", build_css(strip_remote), 1)
    return html
def html_to_pdf(html_path: Path, pdf_path: Path) -> bool:
    chrome = find_chrome()
    if not chrome:
        return False

    import os, uuid
    tmp_profile = Path(tempfile.gettempdir()) / f"chrome-shiny-{uuid.uuid4().hex[:8]}"
    tmp_profile.mkdir(exist_ok=True)

    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-extensions",
        "--run-all-compositor-stages-before-draw",
        f"--user-data-dir={tmp_profile}",
        f"--print-to-pdf={pdf_path}",
        "--no-pdf-header-footer",
        f"file://{html_path}",
    ]

    import time, shutil as _shutil
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Chrome writes the PDF then idles — poll for the file rather than waiting for exit
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            if pdf_path.exists() and pdf_path.stat().st_size > 1024:
                return True
            if proc.poll() is not None:
                break
            time.sleep(0.5)
        return pdf_path.exists() and pdf_path.stat().st_size > 1024
    finally:
        try:
            proc.kill()
            proc.wait(timeout=5)
        except Exception:
            pass
        _shutil.rmtree(tmp_profile, ignore_errors=True)

def assemble(input_path: Path, output_path: Path) -> None:
    skeleton = input_path.read_text(encoding="utf-8")
    html     = build_html(skeleton)  # for HTML output; PDF path re-builds with strip_remote=True

    want_pdf = output_path.suffix.lower() != ".html"

    if want_pdf:
        # For PDF: light mode always (white paper), no remote font requests
        html = build_html(skeleton, strip_remote=True, force_light=True)
        # Write HTML to a temp file, convert to PDF, clean up
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
            tmp_path = Path(tmp.name)
            tmp_path.write_text(html, encoding="utf-8")

        pdf_out = output_path.with_suffix(".pdf")
        ok = html_to_pdf(tmp_path.resolve(), pdf_out)
        tmp_path.unlink(missing_ok=True)

        if ok:
            print(f"Assembled: {pdf_out}  ({pdf_out.stat().st_size // 1024:,} KB)")
            return

        # Chrome not available or conversion failed — fall back to HTML
        html_out = output_path.with_suffix(".html")
        html_out.write_text(html, encoding="utf-8")
        chrome = find_chrome()
        if not chrome:
            print(f"⚠  Chrome not found — saved as HTML instead: {html_out}")
            print("   Open in a browser and use File → Print → Save as PDF to export.")
        else:
            print(f"⚠  PDF conversion failed — saved as HTML instead: {html_out}")
    else:
        # Caller explicitly asked for HTML
        output_path.write_text(html, encoding="utf-8")
        print(f"Assembled: {output_path}  ({output_path.stat().st_size // 1024:,} KB)")

def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path  = Path(sys.argv[1]).resolve()
    # Default output: same stem as input, .pdf extension
    default_out = input_path.with_suffix(".pdf")
    output_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else default_out

    if not input_path.exists():
        print(f"ERROR: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    assemble(input_path, output_path)

if __name__ == "__main__":
    main()
