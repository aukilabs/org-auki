---
name: page
description: Generates an Auki Labs weekly update as a styled scrollable HTML document (single page, print-friendly). Use when someone wants to create a weekly update, work update, team update, one-pager, or progress report in document form (vs. a slide deck). Routes through audience selection and gathers content via probing questions before generating the file. Calls /harvest to pre-fill context from Git when available.
---

# /page

Generates a scrollable HTML document ("page format") using the Auki design system. The structure is fixed (five sections), but the content within each section is assembled freely from available components — you decide what fits.

---

## Step 1 — Audience

**Skip this step if audience was already passed by a router** (`/presentation` always passes `internal`; `/presentation-external` passes `investor`, `client`, or `community`). Use the passed value and proceed to Step 2.

If audience was not passed, ask:

> "Who is this one-pager for?"
> - **Internal** — full detail, unredacted, includes blockers and asks. Stored privately.
> - **Investor** — stored privately, shared directly with investors. Omit blockers. Tone: traction metrics, growth signals, strategic wins, business outcomes.
> - **Client** — stored privately, shared directly with a specific client. Omit blockers. Tone: delivery-focused, value to the client, outcomes.
> - **Community** — the only public audience. Omit blockers. AI-redacts NDA material, financials, unreleased features, partner names. Tone: accessible, outward-facing.

---

## Step 2 — Find the work

**Skip this step if a harvest digest was already passed by a router** (`/presentation` and `/presentation-external` both run harvest before routing). Use the passed digest to pre-fill Step 4's content and proceed directly to Step 3.

If no digest was passed (skill invoked directly), run `/harvest` now:

```
/harvest --author <name> --since <YYYY-MM-DD>
```

Run this silently. `/harvest` reads CHANGELOGs, merged PRs, closed issues, and skill diffs for the current ISO week and returns a structured digest of shipped / in-progress / skill-changes / other-commits.

**Only fall back to the conversational prompt if:**
- `/harvest` returns an empty digest (no PRs, no CHANGELOG entries, no commits found), OR
- The contributor is clearly not GitHub-backed (sales, ops, etc. with no repos in `org/projects.md`)

Fallback prompt (use only if harvest is empty or not applicable):

> "Where can I find the work this one-pager covers? For example:
> - A GitHub repo or PR list I can browse
> - A Linear or Notion project
> - A Discord channel or doc you can paste from
> - Or just tell me what you worked on and I'll ask from there"

Browse what's available. Extract shipped items, metrics, blockers, and next steps directly where possible. Only ask for things you can't infer.

---

## Step 3 — Probing questions

Ask only what you don't already know. Adapt based on what you've already gathered.

**Always ask:**
- Who is this for? (name, role, project)
- What time period?
- What's the single most important thing that happened? (for TL;DR)

**Ask if not already known:**
- What shipped? Any completed work, milestones, releases?
- Any metrics or numbers to highlight?
- What's currently in progress?
- What's coming up next?

**Internal only:**
- Any blockers or asks?

---

## Step 4 — Generate

Build the document from the template at `org/src/design/html/template.html`.

### Self-containment — do this before writing the file

Every generated HTML file must be completely self-contained. No external file dependencies except Google Fonts (CDN, requires internet — acceptable).

#### ⚠️ Do NOT paste vendor files yourself

`roundup-style.css` is ~366 KB with TT Firs Neue fonts already base64-embedded inside it. Pasting it through LLM output risks truncation — a truncated stylesheet silently breaks the page's appearance with no error.

**Use the assemble script instead.** Write the skeleton HTML with a placeholder comment, then run:

```bash
python3 org/src/skills/presentation/page/scripts/assemble-page.py <output.html>
```

The script replaces every placeholder with the correct inlined content and exits non-zero if any placeholder is unresolved. Confirm it prints `Assembled: <path>` before treating the document as complete.

#### Write placeholder comments in the skeleton

In `<head>`, inside the `<style>` block, put this exact comment where the CSS should go:

```html
<style>
  /* ROUNDUP_CSS_PLACEHOLDER */
</style>
```

#### Write placeholder strings in the logo img tags

Copy the logo block verbatim from `org/src/design/html/template.html`. The `src` attributes already contain the right placeholder strings — leave them exactly as written:

```html
<img class="mark logo-dark"  src="data:image/svg+xml;base64,MONOGRAM_WHITE_B64" alt="">
<img class="mark logo-light" src="data:image/svg+xml;base64,MONOGRAM_BLACK_B64" alt="">
<img class="wm logo-dark"    src="data:image/svg+xml;base64,WORDMARK_WHITE_B64"  alt="Auki Labs">
<img class="wm logo-light"   src="data:image/svg+xml;base64,WORDMARK_BLACK_B64"  alt="Auki Labs">
```

The result is a single HTML file that renders correctly with no external dependencies beyond an internet connection for Google Fonts (DM Sans fallback). It can be committed to any repo, emailed, or opened locally.

### Section structure (always these five, in order)

| # | Section | Notes |
|---|---|---|
| 01 | TL;DR | Always one prose paragraph. Write this last. |
| 02 | What shipped | Flexible — see component guide below |
| 03 | What's in progress | Flexible |
| 04 | Blockers & asks | **Internal only** — omit entirely for investor/client/community |
| 05 | What's next | Renumber to 04 if blockers omitted |

---

### Component guide — assemble freely

You have these building blocks. Use what the content calls for. Nothing is mandatory except the TL;DR paragraph.

---

#### Prose paragraph `<p>`
The default. Use for narrative, context, and explanation. TL;DR is always a prose paragraph. Use prose when the content flows as connected thought rather than discrete items.

---

#### Bullet list `<ul>` + `<li>`
Use for discrete, parallel items — shipped features, next steps, blockers. Each item should be roughly the same level of specificity. Bold the item name, dash, then the detail.

```html
<ul>
  <li><strong>Item name</strong> — what it is, why it matters.</li>
</ul>
```

Skip if items are better told as prose, or if there's only one item.

---

#### Workstream headings `<h3>`
Use when there are 2+ distinct named streams of work within a section. The h3 names the stream; prose or a short list follows. Most common in "What's in progress."

```html
<h3>Workstream name</h3>
<p>What's happening, current state, where it's headed.</p>
```

Skip if work is a single thread, or if items are better as a flat list.

---

#### Metrics strip `.metrics` + `.metric`
Use when there are 2–5 real, meaningful numbers that are immediately legible. Numbers should speak for themselves with a short label. Most natural at the top of "What shipped." Can occasionally appear in TL;DR for a single landmark number.

```html
<div class="metrics">
  <div class="metric">
    <div class="metric-value">94<span class="unit">%</span></div>
    <div class="metric-delta up">↑ from 71%</div>
    <div class="metric-label">Pose accuracy</div>
  </div>
</div>
```

`metric-delta` classes: `up` (green), `down` (red), or no class (muted/neutral).

**Skip if:** fewer than 2 meaningful numbers, numbers need too much explanation, or the week had no measurable output. Don't invent metrics.

---

#### Callout `.callout`
Use for the single most important insight, consequence, or unblock that deserves visual emphasis — something the reader must not miss.

```html
<div class="callout">
  <p>The most important thing — an unblock, a milestone, a key consequence.</p>
</div>
```

**Skip if** nothing particularly stands out. Don't force one. Max 1 per section, 2 per document.

Placement: after the list or prose, never before. Appropriate in blockers for a critical timeline-impacting issue.

---

### Tone — Auki voice

- Declarative and precise. State outcomes, not activity.
- "We shipped X" not "I have been working on X"
- Metrics stated matter-of-factly, not hyped
- No emoji. No exclamation points.
- Sentence case for body copy. Title case for product/project names.

---

### Audience adjustments

**All non-internal audiences (investor/client/community):**
- Remove the blockers section entirely
- Renumber "What's next" to 04
- Change footer notice to match audience

**Community only — additionally:**
- Call `/nda-redact` as a post-processing step before writing the file
- Tone: accessible, outward-facing

**Investor tone:** traction metrics, growth signals, strategic wins, business outcomes. De-emphasise deep technical detail.

**Client tone:** delivery-focused — what was built, what value was delivered, what's coming next for that client.

**Audience badge CSS class:**
- `internal`  → `<span class="audience-badge">Internal</span>`
- `investor`  → `<span class="audience-badge investor">Investor</span>`
- `client`    → `<span class="audience-badge client">Client</span>`
- `community` → `<span class="audience-badge community">Community</span>`

---

## Step 5 — Output

### Embed Pulse metadata (required)

Include this block in `<head>` **before** the `<style>` tag. The Pulse platform reads it to build the presentation index — without it, the index falls back to path inference and loses title, projects, tags, and author details.

```html
<script type="application/json" id="pulse-meta">
{
  "id": "{author}-{YYYY}-{NN}-page",
  "title": "Week {NN} — {Project · Project}",
  "author": "Full Name",
  "authorSlug": "first-last",
  "date": "YYYY-MM-DD",
  "week": "YYYY-NN",
  "format": "roundup",
  "audience": "internal",
  "projects": ["project-a", "project-b"],
  "tags": ["shipped"],
  "thumbnail": null
}
</script>
```

Fill every field from the content gathered in Steps 1–4. `projects` are Auki project names in lowercase kebab-case. `tags` are freeform — common values: `shipped`, `research`, `design`, `infrastructure`. `thumbnail` is `null` unless an image was explicitly uploaded.

---

### File path

Write the completed self-contained HTML file to the `aukilabs/presentations` storage repo, under the audience-specific top-level directory:

| Audience | Path |
|---|----|
| `internal`  | `internal/week-{NN}/{author}.html`  |
| `investor`  | `investors/week-{NN}.html`          |
| `client`    | `clients/week-{NN}.html`            |
| `community` | `community/week-{NN}.html`          |

Slug format:
- `week-{NN}`: ISO week number, zero-padded for sort stability (e.g. `week-20`). Use `/harvest`'s `HARVEST_WEEK_LABEL` if available.
- `{author}`: first-name + last-initial, kebab-case (e.g. `charlie-s`, `alex-k`).

Access control is enforced at the directory level by the platform — anything under `internal/`, `investors/`, or `clients/` is private; only `community/` is public.

Confirm with the author: "Here's your update — open it in a browser to preview. Does anything need adjusting?"

Then commit and push using the author's own Git credentials.