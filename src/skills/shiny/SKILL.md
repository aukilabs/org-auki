---
name: shiny
description: Takes an uploaded file (PDF, HTML, markdown, or plain text) and re-renders it as a polished, self-contained HTML document using the Auki design system (colours + token set). Use when someone wants a polished, self-contained branded document.
---

# /shiny

Takes a file and outputs a fully self-contained branded HTML document. No internet connection needed to view the output (fonts are embedded). The result can be opened in a browser and printed to PDF.

---

## Step 1 — Receive the file

The user uploads a file. Supported formats:
- **PDF** — use the Read tool; extract page by page if multi-page (max 20 pages per call)
- **HTML** — read the raw markup; extract the text content and structure from the existing tags
- **Markdown** — parse headings, paragraphs, lists, code blocks, tables directly
- **Plain text / .txt** — infer structure from blank lines, indentation, and capitalisation patterns

If no file is provided, ask: *"Upload the file you'd like to style."*

---

## Step 2 — Ask two questions

Ask both at once to keep it brief:

> "Two quick questions:
> 1. **Light or dark mode?** (Dark is the default Auki look; light works better for printed PDFs)
> 2. **What's the document title?** (Use the filename or first heading if you'd prefer I infer it)"

Set the `data-theme` attribute on `<html>` accordingly:
- Dark: `<html lang="en" data-theme="dark">` (or omit `data-theme` — defaults to dark)
- Light: `<html lang="en" data-theme="light">`

---

## Step 3 — Parse the document structure

Read through the file content and identify the following structural elements:

| What you see | What it becomes |
|---|---|
| Document title / filename / first large heading | `<h1 class="shiny-title">` in the title block |
| Subtitle, date, or description line | `<p class="shiny-subtitle">` |
| Section heading (PDF: short line, often bold or caps; MD: `##`) | `<h2>` inside a `<section class="shiny-section">` |
| Sub-heading (PDF: slightly larger than body; MD: `###`) | `<h3>` inside the section |
| Body paragraphs | `<p>` |
| Bullet list | `<ul><li>` |
| Numbered list | `<ol><li>` |
| Inline code or technical terms | `<code>` |
| Code block / pre-formatted text | `<pre><code>` |
| **Titled card** — a visually enclosed block with a short bold/coloured title on the first line, then descriptive body text. Common in business PDFs as track boxes, feature callouts, or named option blocks. | `<div class="shiny-card"><p class="shiny-card-title">Title</p><p>Body text</p></div>` |
| **Two-column comparison table** — "before vs after", "current vs proposed", left column is old state, right is new. | `<table class="shiny-compare"><thead><tr><th>Col A</th><th>Col B</th></tr></thead><tbody>…</tbody></table>` |
| **Accent callout** — important note, warning, or highlighted statement that should stand out. | `<div class="shiny-callout"><p>…</p></div>` |
| **Soft callout** — supporting note, qualification, or aside that is secondary to the main flow. | `<div class="shiny-callout--soft"><p>…</p></div>` |
| Metrics / key numbers (e.g. "97% accuracy", "£140k ARR") | `<div class="doc-metrics">` with `<div class="doc-metric">` cards |
| Plain table (not a comparison) | `<table>` — the CSS handles basic table styling |

**For PDFs specifically:**
- Lines that are significantly shorter than body text and appear at the start of a visual block are likely headings
- Lines that are ALL CAPS are likely section labels → use `<h2>`
- Bullet characters (•, –, ▪, or lines starting with a dash) → `<ul><li>`
- Lines starting with numbers followed by a period (1. 2. 3.) → `<ol><li>`
- If you cannot reliably identify structure, wrap everything in `<p>` — clean prose is better than incorrectly tagged hierarchy

**Do not invent, summarise, or paraphrase content.** Copy the text exactly. Only the visual presentation changes.

---

## Step 4 — Generate the HTML skeleton

Use this structure. Fill in the title, subtitle, mode, and the parsed body content.

```html
<!doctype html>
<html lang="en" data-theme="dark">
<!-- data-theme="dark" or data-theme="light" per the user's choice -->
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FILL: Document title</title>
<style>
  /* SHINY_CSS_PLACEHOLDER */
</style>
</head>
<body>

<div class="shiny-top-rule"></div>

<div class="shiny-chrome">
  <button class="shiny-theme-btn" id="theme-btn" aria-label="Toggle light/dark mode">
    <svg class="icon-sun" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>
    <svg class="icon-moon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
  </button>
</div>

<div class="shiny-body">

  <div class="shiny-title-block">
    <h1 class="shiny-title">FILL: Document title</h1>
    <p class="shiny-subtitle">FILL: Subtitle, date, or source — omit if nothing meaningful</p>
  </div>

  <div class="shiny-content">

    <!-- FILL: Parsed document content goes here.
         Group related sections with <section class="shiny-section">...</section>
         Use h2, h3, p, ul, ol, pre, code, table for standard content.

         Titled card (named box with bold/coloured title + body):
           <div class="shiny-card">
             <p class="shiny-card-title">Track name or label</p>
             <p>Description text.</p>
           </div>

         Two-column comparison table (current vs proposed, before vs after):
           <table class="shiny-compare">
             <thead><tr><th>Current</th><th>Proposed</th></tr></thead>
             <tbody><tr><td>…</td><td>…</td></tr></tbody>
           </table>

         Accent callout (important / highlighted note):
           <div class="shiny-callout"><p>…</p></div>

         Soft callout (supporting note or qualification):
           <div class="shiny-callout--soft"><p>…</p></div>
    -->

  </div>

</div>

<footer class="shiny-footer">
  <span>Auki Labs</span>
  <span>FILL: Date or source filename</span>
</footer>

<script>
  (function(){
    var html=document.documentElement,btn=document.getElementById('theme-btn'),
    sun=btn.querySelector('.icon-sun'),moon=btn.querySelector('.icon-moon'),
    darks=document.querySelectorAll('.logo-dark'),lights=document.querySelectorAll('.logo-light');
    function apply(t){html.setAttribute('data-theme',t);localStorage.setItem('shiny-theme',t);
    var l=t==='light';sun.style.display=l?'block':'none';moon.style.display=l?'none':'block';
    darks.forEach(function(e){e.style.display=l?'none':'block';});
    lights.forEach(function(e){e.style.display=l?'block':'none';});}
    var saved=localStorage.getItem('shiny-theme')||html.getAttribute('data-theme')||'dark';
    apply(saved);
    btn.addEventListener('click',function(){apply(html.getAttribute('data-theme')==='light'?'dark':'light');});
  })();
</script>

</body>
</html>
```

---

## Step 5 — Assemble

Run the assembler to inline the CSS (with fonts) and embed the logos:

```bash
python3 org/src/skills/shiny/scripts/assemble-shiny.py <skeleton.html> <output.html>
```

The assembler replaces:
- `/* SHINY_CSS_PLACEHOLDER */` → full inlined CSS (tokens + shiny styles, fonts as base64)
 (logo embedding removed for public sync)

Save the output as `shiny-{original-filename}.pdf`. The assembler handles the HTML → PDF conversion using headless Chrome automatically — no extra steps needed. If Chrome is unavailable on the system it will fall back to HTML with a message.

---

## Step 6 — Output

Tell the user the path to the assembled file and how to use it:

> "Done — saved as `shiny-{filename}.pdf`. Open it directly or share it. If you'd like the HTML version too (e.g. to use the light/dark toggle interactively), run the assembler with a `.html` output path."

If the file had images: note that images embedded in PDFs cannot be extracted automatically and will not appear in the output. If the user wants them included, they can add `<img>` tags to the skeleton manually before assembling.

---

## Content rules

- **Copy text exactly** — do not paraphrase, summarise, or improve the source content
- **Preserve structure** — headings, lists, and tables should map to their closest HTML equivalent
- **Strip presentation** — remove source-specific styling (font sizes, colours, margins) — let the Auki CSS handle all presentation
- **Handle images gracefully** — if a PDF contains figures, add a comment `<!-- [Figure: description] — image not extracted -->` at the right position
