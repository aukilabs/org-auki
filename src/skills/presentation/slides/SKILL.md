---
name: slides
description: Generates a self-contained reveal.js HTML slide deck. Handles two modes — weekly update (default) and product deck. Weekly update mode gathers work via /harvest and tells the story of a contributor's week. Product deck mode gathers product/company information and produces a standalone pitch or product presentation. Both modes share the same slide types, design system, and themes.
---

# /slides

Generates a reveal.js slide deck using the Auki design system. The format is freeform — the skill is the author. The design system provides components; the skill decides the structure, chooses the slide types, and writes the narrative.

**Two modes:**
- **Weekly update** (default) — covers a contributor's work for a specific week. Runs `/harvest`, asks narrative questions, generates the deck, and commits to `internal/week-NN/{author}.html`.
- **Product deck** — standalone product or pitch presentation. Skips harvest. Asks product questions instead. Commits to `product-decks/{slug}.html`.

> **If `type = product-deck` was passed: stop here and jump to [Product Deck Mode](#product-deck-mode) at the bottom of this file.** Do not run harvest. Do not ask weekly-update questions. Steps 0–10 below are for weekly updates only.

These decks are primarily **read**, not pitched live. They're committed to a repo, opened in a browser, and consumed at the reader's own pace. That means slides can be denser than a conference keynote — multiple bullets, a metric, and a callout on one slide is fine as long as they're all about the same topic.

**The guiding question at every step:** What is the single most important thing this deck communicates? Everything else serves that.

---

## Step 0 — Theme

**Skip this step if theme was already passed by a router** (`/presentation` passes the theme chosen in Step 1.5). Use the passed value and proceed to Step 1.

If invoked directly (no theme passed), ask:

> "Which theme? **Auki** (default), **Cactus**, or **Gotu**."

Default to `auki` if the user doesn't specify. The theme is used at the end when running `assemble.py --theme <theme>` and determines the brand colours, fonts, and logo.

| Theme    | Accent        | Heading font  | Body font    |
|----------|---------------|---------------|--------------|
| `auki`   | Orange #FD9E2F| TT Firs Neue  | DM Sans      |
| `cactus` | Green #36D359 | Questrial     | Nunito Sans  |
| `gotu`   | Blue #2670F8  | DM Sans Bold  | DM Sans      |

---

## Step 1 — Audience

**Skip this step if audience was already passed by a router** (`/presentation` always passes `internal`; `/presentation-external` passes `investor`, `client`, or `community`). Use the passed value and proceed to Step 2.

If audience was not passed, ask:

> "Who is this deck for?"
> - **Internal** — full detail, unredacted, includes blockers and asks. Stored privately.
> - **Investor** — stored privately, shared directly with investors. Omit blockers. Traction metrics, growth signals, strategic wins.
> - **Client** — stored privately, shared directly with a specific client. Omit blockers. Delivery-focused, value to that client.
> - **Community** — the only public audience. Omit blockers. AI-redacts NDA material, financials, unreleased features, partner names. Tone: accessible, outward-facing.

All four go to the `aukilabs/presentations` storage repo under different top-level directories (`internal/`, `investors/`, `clients/`, `community/`). Access control is enforced at the directory level.

---

## Step 2 — Find the work

**Skip this step if a harvest digest was already passed by a router** (`/presentation` and `/presentation-external` both run harvest before routing). Use the passed digest as the raw material for narrative synthesis in Step 4 and proceed directly to Step 3.

If no digest was passed (skill invoked directly), run `/harvest` now:

```
/harvest --author <name> --since <YYYY-MM-DD>
```

Run this silently. `/harvest` reads CHANGELOGs, merged PRs, closed issues, and skill diffs for the current ISO week and returns a structured digest of shipped / in-progress / skill-changes / other-commits.

**Only fall back to the conversational prompt if:**
- `/harvest` returns an empty digest (no PRs, no CHANGELOG entries, no commits found), OR
- The contributor is clearly not GitHub-backed (sales, ops, etc. with no repos in `org/projects.md`)

Fallback prompt (use only if harvest is empty or not applicable):

> "Where can I find the work this deck covers? For example:
> - A GitHub repo or PR list I can browse
> - A Linear or Notion project
> - A Discord channel or doc you can paste from
> - Or just tell me what you worked on and I'll ask from there"

---

## Step 3 — Deck length

Ask the user, or decide based on content volume:

- **Short (6-10 slides)** — tight week, single workstream, quick sync
- **Standard (10-18 slides)** — typical week with 2-3 threads of work
- **Long (18-30 slides)** — major release, multi-team digest, investor presentation
- **Let me decide** — skill judges based on content volume

If the user has no preference: fewer than 4 distinct things → short; 4-8 things → standard; 8+ or a major release → long. Don't pad a short week with filler slides.

---

## Step 4 — Build the narrative

**Do not structure this like the roundup.** The roundup's five sections are a document structure — wrong for a presentation. A slide deck tells a story. Its shape comes from the content, not from reporting categories.

### Read everything first

Before thinking about slides, read all available material. Build a picture of the week. Then ask:

- What is the single most interesting or significant thing from this period?
- Is there a transformation, breakthrough, or thing that was hard and got done?
- What data tells a story — a number that changed, a trend, a comparison?
- What decisions were made? What is still unresolved?
- What does the audience most need to understand?

### Choose an arc before touching slide types

**This is the step most AI-generated decks skip — and it's why they all feel the same.**

Before choosing any slide types, write one sentence that identifies:
1. What is the single most important thing this week?
2. What kind of story does that create?
3. Which arc below fits that story?

Then commit to that arc and build the sequence explicitly. Do not drift back to the default formula while building.

---

#### The six arcs

**ARC 1 — The reveal** *(one big thing shipped)*
Use when: a single change is dramatically better than before.
```
Title
→ The problem (what was broken / slow / missing) — content slide, not statement
→ The solution (statement — what changed, in one sentence)
→ How it works (graphic or content)
→ The numbers (stats — show impact, not effort)
→ What it enables next (content)
→ Closing
```
*The problem slide comes FIRST. The reader needs to feel the pain before they feel the relief.*

**ARC 2 — The growth story** *(metrics-led)*
Use when: a number changed meaningfully and the story is "why and what it means."
```
Title
→ The headline chart or number (graphic or stats — this is slide 2, not slide 6)
→ What drove it (content — causes, not just description)
→ Context: where we started, where we are (split or compare)
→ What comes next (content)
→ Closing
```
*The data IS the opening. Don't bury it. Lead with the chart.*

**ARC 3 — The decision** *(major architectural or strategic choice)*
Use when: the most important thing is a decision that was made, not a feature that shipped.
```
Title
→ The old state and its constraints (content — be specific about the ceiling)
→ What we evaluated (split — options compared)
→ The verdict (statement — one sentence: what we chose and why)
→ The new design (graphic/architecture)
→ Implications for integrators/operators (content)
→ Migration / next steps (content)
→ Closing
```
*The split comparison belongs in the middle, not at the end. It's the reasoning, not a detail.*

**ARC 4 — The thread** *(parallel workstreams)*
Use when: 3–4 distinct things shipped with no single dominant story.
```
Title
→ The headline beat (statement — one sentence about the week overall)
→ Section 01 divider
→ Thread A (1–2 slides)
→ Section 02 divider
→ Thread B (1–2 slides)
→ Section 03 divider (if needed)
→ Thread C
→ What's next
→ Closing
```
*The section dividers are structural, not decorative. They signal "new topic." Use them only for genuinely distinct areas.*

**ARC 5 — The demo** *(something visual shipped)*
Use when: what shipped is best understood by seeing it. The visual IS the argument.
```
Title
→ The visual (image slide or expandable screenshot — this is slide 2)
→ What you're looking at (statement or content — brief)
→ How it works (content or graphic)
→ The numbers (stats — only if meaningful)
→ What's next
→ Closing
```
*The screenshot comes before the explanation. Don't explain something the reader hasn't seen yet.*

**ARC 6 — The situation report** *(slow or strategic week)*
Use when: nothing dramatic shipped but the week has shape — something was learned, a decision is approaching, or context shifted.
```
Title
→ Where things stand (content — state of play, not "what shipped")
→ What changed this week (content — subtle shifts, findings, experiments)
→ The decision or moment approaching (statement or split)
→ What we need (content — blockers, asks, dependencies)
→ Closing
```

---

### Sanity check — before writing any HTML

After writing the outline and before opening the first `<section>` tag, run three checks on each slide in the list.

**1. Data-visual logic check**
Every chart type implies a specific claim about the data. Before using a chart, confirm the data actually supports that claim.

| Chart type | What it claims | Ask yourself |
|---|---|---|
| Horizontal bar | These items have different magnitudes of something | Do my items actually have a quantitative value to compare? |
| Vertical column | This quantity changes over time or across periods | Do my columns represent a real measure per period? |
| Line / trend | This value moves over time in a meaningful direction | Is the direction itself the point, or just one number? |
| Donut / ring | This is a proportion of a whole | Do my segments actually sum to a meaningful whole? |
| Architecture | These components have structural relationships | Are the relationships real, or am I just drawing boxes? |

If the answer to "ask yourself" is no — use a content slide or a statement instead. **A bar chart that lists things without comparing them is not a chart. It is a list with misleading visual weight.**

**2. Reader comprehension check**
For each slide, ask: *would someone who doesn't work on this project understand what this slide is claiming in under 30 seconds?*

If no, one of three things is wrong:
- The heading isn't stating the point clearly enough (fix the heading)
- The slide is missing the context that makes the content meaningful (add a `slide-desc` line)
- The slide is too technical for its audience (reframe or cut)

This is especially critical for graphic slides. A chart without a clear "so what" in the heading is a chart the reader will skim and forget.

**3. Heading-visual agreement check**
The heading makes a claim. The visual should be evidence for that exact claim — not evidence for a related but different claim.

| ✗ Mismatch | ✓ Aligned |
|---|---|
| Heading: "We added 5 chart patterns" / Visual: bar chart of pattern names | Heading: "Five chart patterns — each maps to a specific data claim" / Visual: content slide listing each pattern and its use case |
| Heading: "Latency improved" / Visual: chart of relay node counts | Heading: "Domain join latency — 7-week trend" / Visual: line chart of latency values |
| Heading: "SDK adoption growing" / Visual: pie chart of audience types | Heading: "SDK downloads — Wk 12 to Wk 20" / Visual: column chart of weekly downloads |

If the heading and visual don't agree, either change the visual, change the heading, or drop the slide.

---

## Step 5 — Slide types and markup

All slides are `<section>` elements. Use banner comments between them:

\`\`\`html
<!-- ================================================================
N. SLIDE NAME · OPTIONAL SUBTITLE
================================================================= -->
<section class="slide-xxx" data-background-color="var(--bg)">
  …
</section>
\`\`\`

Use sub-slide suffixes (`12a`, `12b`) when extending a section without renumbering. Scoped `<style>` blocks inside a `<section>` are fine for one-off, slide-specific components — global theme additions go in the theme CSS.

### Heading wrapper patterns

Two patterns for the heading block — pick the right one:

**Standard** (`slide-header` + `eyebrow` div) — use for most slides:
```html
<div class="slide-header">
  <div class="eyebrow">Scope label</div>
  <h2 class="slide-heading">Specific heading</h2>
</div>
```

**With context line** (`slide-heading-wrap` + `slide-heading-label`) — use when adding a `slide-desc` line under the heading:
```html
<div class="slide-heading-wrap">
  <span class="slide-heading-label">Scope label</span>
  <h2 class="slide-heading">Specific heading</h2>
  <p class="slide-desc">One grounding sentence before the content.</p>
</div>
```

For `slide-graphic` and `slide-split`, put the heading directly on the section (no wrapper div) — these slides need every pixel of vertical space.

The eyebrow is always optional. If the heading already establishes context, omit it.

---

### Content density and conciseness

These two are in tension. A slide needs enough content to justify its existence, but a bullet that runs to three lines is a paragraph pretending to be a list item.

**The floor:** each bullet must be specific enough that removing it would leave a gap in the reader's understanding. If you can remove it and the slide still makes the same point, cut it.

**The ceiling:** each bullet is one thought, one fact, one consequence. Target 8–14 words. Hard cap at 18. If you need more, either the heading isn't doing enough work or the bullet has two ideas — split it or cut the weaker one.

**On overflow:** if slides overflow the viewable height, the answer is fewer bullets and shorter sentences, not a smaller font. The auto-fit script shrinks text down to a minimum, but a slide at 11px is unreadable. Overflow means you wrote too much.

**By slide type:**

| Type | Floor | Ceiling | If too thin |
|---|---|---|---|
| content (bullets) | 4 items, each specific | 6 items max; each a single thought, concise | Merge into adjacent slide |
| stats | 2 cards | 5 cards | Use a statement slide for a single number |
| graphic | Visual carries the point | One visual per slide; no decoration | Drop it; a sentence is clearer |
| statement | 1 sentence, declarative | 2 sentences max | Could be a callout on another slide |
| split | 3 items per side | 5 items per side | Not enough contrast — use a statement |

**The context rule:** every number needs a comparator ("72ms — down from 420ms") and every claim needs a consequence ("compliance up 20pp — the same staff, the same store"). Don't write half a fact. But don't pad the second half either.

---

### Slide type variety

**Before writing the slide list, take one pass and ask:** for each piece of content, is there a more precise slide type than bullets? If you have written 3 or more bullet slides in a row, pause and check — not to force a different type, but to confirm that bullets genuinely are the right choice for each one. Sometimes they are. Sometimes one of them is actually a metric, a comparison, or a single statement that would land harder in its own type.

| Content type | Default instinct | Better choice |
|---|---|---|
| A metric that improved | bullet: "latency dropped 60%" | `slide-compare` or `slide-stats` |
| Two states being compared | two bullet slides | `slide-split` |
| A single dramatic fact | bullet at the top of a list | `slide-statement` |
| Structured rows of data | nested bullets | `slide-table` |
| Something visual shipped | bullet describing it | `slide-graphic` or `slide-image` |
| Context for numbers | standalone bullets | `slide-stats` with body text below |
| 3–6 named things with short descriptions | bullet list | `slide-highlights` (feature cards) |
| A sequence or process | numbered bullets | `slide-steps` |
| A graphic that needs explanation | graphic slide + next slide explaining | `slide-half` (text + visual together) |

**Minimum variety:** a deck must use at least 3 different content slide types (title and closing don't count). A deck of all bullet slides is always wrong, regardless of content.

---

### Title (`.slide-title`) — always first

\`\`\`html
<!-- ================================================================
1. TITLE
================================================================= -->
<section class="slide-title" data-background-color="var(--bg)">
  <div></div><!-- spacer pushes content to bottom -->
  <div class="title-bottom">
    <div class="title-left">
      <span class="title-top-anchor"></span>
      <div class="eyebrow">Building the real-world web.</div>
      <h1 class="title">Project Name</h1>
      <p class="subtitle">One sentence — what the week was about.</p>
    </div>
    <div class="meta">
      <span class="meta-author">Full Name</span>
      <span class="meta-date">12 May 2026 &nbsp;&middot;&nbsp; <span style="color:var(--orange)">Week 20</span></span>
      <div class="meta-projects">
        <span class="project-tag">Park</span>
        <span class="project-tag">SDK</span>
      </div>
    </div>
  </div>
</section>
\`\`\`

Project/team name in `<h1>`. No week numbers in the heading — week goes in `.meta-date` only. Subtitle is optional; omit if nothing adds to the title.

---

### Section divider (`.slide-section`) — optional

\`\`\`html
<section class="slide-section" data-background-color="var(--bg)">
  <div class="section-num">01</div>
  <div class="section-name-wrap">
    <h2 class="section-title">What shipped</h2>
  </div>
</section>
\`\`\`

The structure is exact. `auki-theme.css` styles `.section-num` as the 240px ghost number and uses `.section-name-wrap` as the flex column that holds `.section-title`. If you drop the wrapper or rename the classes (e.g. `<span class="section-number">`, bare `<h1>`), the slide-section CSS rules don't match, the layout collapses to reveal's default column, and the title gets pinned to the top of the slide instead of vertically centered next to the ghost number.

**Use only when:** deck is 12+ slides with 3+ clearly distinct topic areas. Skip for decks under 12 slides or when content reads as one continuous story.

---

### Statement (`.slide-statement`) — optional

\`\`\`html
<section class="slide-statement" data-background-color="var(--bg)">
  <div class="statement-wrap">
    <div class="eyebrow">Relay</div>
    <p class="statement-text">The relay rewrite landed. Latency dropped 60%.</p>
  </div>
</section>
\`\`\`

Use for major milestones, dramatic beats, the single most important point. Skip when the most important thing fits naturally as a content slide heading.

---

### Content — bullets (`.slide-content`)

\`\`\`html
<section class="slide-content" data-background-color="var(--bg)">
  <div class="slide-header">
    <div class="eyebrow">Relay</div>
    <h2 class="slide-heading">What shipped this week</h2>
  </div>
  <div class="slide-body">
    <ul>
      <li><strong>libp2p transport</strong> — replaced the HTTP relay; latency down 60%</li>
      <li><strong>Dynamic cluster discovery</strong> — nodes now self-register via Vinland</li>
      <li><strong>Preview stream</strong> — K1 humanoid renders live at 60 Hz in Park</li>
    </ul>
    <div class="callout">
      <p>The HTTP removal unblocks the mobile SDK — no more websocket workaround needed.</p>
    </div>
  </div>
</section>
\`\`\`

Max 5-6 bullets per slide. Bold the item name, dash, then the specific detail. Callout is optional — max 2 per deck, placed after the list.

**Adding context with `.slide-desc`** — you may add one sentence that grounds the reader before the bullet list. Use it when the heading alone is too thin to carry the reader into the list. Keep it to a single sentence. Omit when the heading is self-explanatory.

**Placement: inside `.slide-header`, immediately after the `<h2>` — never inside `.slide-body`.** The negative `margin-top` on `.slide-desc` is designed to pull it visually against the heading within the same container. Placing it inside `.slide-body` breaks this relationship and can cause the desc to visually detach or get clipped.

\`\`\`html
<div class="slide-header">
  <div class="eyebrow">Relay</div>
  <h2 class="slide-heading">What shipped this week</h2>
  <p class="slide-desc">Four changes landed — the relay rewrite being the headline.</p>
</div>
<div class="slide-body">
  <ul>
    <li>...</li>
  </ul>
</div>
\`\`\`

The `.slide-desc` class renders at 17px muted body text with a slight negative top margin to sit close under the heading. When `slide-desc` is present, keep the bullet list to **4 items max** — 5 bullets + a desc will overflow the slide height.

---

### Content — prose (`.slide-content`, prose variant)

\`\`\`html
<section class="slide-content" data-background-color="var(--bg)">
  <div class="slide-header">
    <div class="eyebrow">Architecture</div>
    <h2>Why we switched transport layers</h2>
  </div>
  <div class="slide-body">
    <p>The previous HTTP relay created a hard ceiling on throughput…</p>
    <p>libp2p gives us direct peer connections with automatic fallback to relay when NAT traversal fails.</p>
  </div>
</section>
\`\`\`

Use when content flows as connected thought rather than a list. Max 2-3 paragraphs per slide.

---

### Stats (`.slide-stats`)

\`\`\`html
<section class="slide-stats" data-background-color="var(--bg)">
  <div class="slide-header">
    <div class="eyebrow">Performance</div>
    <h2>This week</h2>
  </div>
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-value">60<span class="unit">%</span></div>
      <div class="stat-delta up">↓ latency</div>
      <div class="stat-label">End-to-end relay</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">60<span class="unit">Hz</span></div>
      <div class="stat-delta up">↑ from 24Hz</div>
      <div class="stat-label">K1 preview stream</div>
    </div>
  </div>
</section>
\`\`\`

2-5 cards. `.stat-delta` classes: `up` (accent), `down` (red), or none (muted). Skip if fewer than 2 real numbers.

**Adding context below the cards** — when the numbers need a consequence or a single sentence of explanation, add a `<p class="muted">` directly after the `.stats-grid`. Keep it to one sentence. Use a `callout` div instead if the consequence is significant enough to stand out.

\`\`\`html
  <div class="stats-grid">
    <!-- cards -->
  </div>
  <p class="muted" style="margin-top: 24px; font-size: 16px; line-height: 1.6;">The latency drop accounts for the relay rewrite alone — no other infrastructure changes landed this week.</p>
\`\`\`

---

### Graphic — chart or diagram (`.slide-graphic`)

Five reference patterns live in `org/src/design/slides/slide-types/graphic.html`. Copy the relevant pattern verbatim and replace the placeholder data. **Never invent numbers — only use data from the harvest or content the user has provided.**

| Pattern | When to use |
|---|---|
| **A — Horizontal bar** | Comparing named items on a single metric (benchmarks, usage, rankings) |
| **B — Line / trend** | Change over time, 6–8 data points, one or two series |
| **C — Architecture / flow** | System structure, data flow, before/after topology |
| **D — Vertical column** | Weekly time-series, SDK call volume, build counts by period |
| **E — Donut / ring** | Single metric as % of goal, two-part composition, progress indicator |

```html
<section class="slide-graphic" data-background-color="var(--bg)">
  <h2 class="slide-heading">Chart title — make a specific claim</h2>
  <div class="graphic-area">
    <svg viewBox="0 0 800 360" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-height:400px;">
      <!-- copy pattern A–E from graphic.html and replace placeholder values -->
    </svg>
  </div>
</section>
```

No heading wrapper on graphic slides — they need the vertical space. CSS classes for all chart patterns live in `auki-theme.css` under `/* SVG graphic utility classes */`. Use them instead of inline fill/stroke — the theme handles dark/light mode switching.

---

### Split (`.slide-split`) — text/bullets side by side

Use when comparing two states, options, or workstreams as bullet lists. Good for before/after reasoning, option A vs B, two parallel threads that need equal weight.

No heading wrapper on split slides — the heading sits directly on the section, above `.split-body`.

```html
<section class="slide-split" data-background-color="var(--bg)">
  <h2 class="slide-heading">Transport layer: before and after</h2>
  <div class="split-body">
    <div class="split-left">
      <div class="eyebrow is-issue">Before</div>
      <ul>
        <li>All traffic via central relay — 180ms average latency</li>
        <li>Single point of failure for all domains</li>
      </ul>
    </div>
    <div class="split-divider"></div>
    <div class="split-right">
      <div class="eyebrow">After</div>
      <ul>
        <li>Direct peer connections via libp2p — 72ms average latency</li>
        <li>Automatic fallback when NAT traversal fails</li>
      </ul>
    </div>
  </div>
</section>
\`\`\`

**Trigger:** any time you're writing a before/after, old vs new, or option A vs B using words — use this instead of two consecutive content slides.

---

### Compare (`.slide-compare`) — metric before/after with big numbers

Use when the comparison is a measurable change — a number that moved. The visual weight of the large figure carries the argument. This is the correct type for "we improved X from Y to Z."

\`\`\`html
<section class="slide-compare" data-background-color="var(--bg)">
  <div class="slide-header">
    <div class="eyebrow">Relay</div>
    <h2 class="slide-heading">Latency — before and after</h2>
  </div>
  <div class="compare-grid">
    <div class="compare-before">
      <div class="compare-label">Before</div>
      <div class="compare-value">180<span class="unit">ms</span></div>
      <p class="compare-desc">HTTP relay — central bottleneck, single point of failure</p>
    </div>
    <div class="compare-after">
      <div class="compare-label">After</div>
      <div class="compare-value">72<span class="unit">ms</span></div>
      <div class="compare-delta-badge">−60%</div>
      <p class="compare-desc">libp2p direct peers — automatic relay fallback when NAT blocks</p>
    </div>
  </div>
</section>
\`\`\`

The "before" card renders muted; the "after" card is orange-accented. `.compare-delta-badge` sits top-right of the after card — use it to show the percentage change. `.compare-desc` is a short sentence under each value.

**Trigger:** any time a metric changed and the magnitude of the change is the point — use this instead of a stats slide with two cards or a text bullet that says "improved from X to Y."

---

### Highlights — feature cards (`.slide-highlights`)

Use for "what shipped" lists, capability summaries, or any 3–6 items where individual cards land better than a bullet list. Each card has a bold title and a one-line description.

Default grid is **3 columns**. For 4 items as a 2×2, override `grid-template-columns` inline. For 2 items, override to `repeat(2, 1fr)`.

```html
<section class="slide-highlights" data-background-color="var(--bg)">
  <div class="slide-header">
    <div class="eyebrow">SDK</div>
    <h2 class="slide-heading">What shipped this week</h2>
  </div>
  <div class="highlights-grid">
    <div class="highlight-card">
      <div class="highlight-title">libp2p transport</div>
      <p class="highlight-desc">Direct peer connections — HTTP relay removed, latency halved</p>
    </div>
    <div class="highlight-card">
      <div class="highlight-title">Cluster discovery</div>
      <p class="highlight-desc">Nodes self-register via Vinland on domain join</p>
    </div>
    <div class="highlight-card">
      <div class="highlight-title">Preview stream</div>
      <p class="highlight-desc">K1 humanoid renders live at 60 Hz in Park</p>
    </div>
    <div class="highlight-card">
      <div class="highlight-title">iOS 17 fix</div>
      <p class="highlight-desc">Audio session routing corrected for AVFoundation defaults</p>
    </div>
  </div>
</section>
```

For a 2×2 layout (4 items): add `style="grid-template-columns: repeat(2, 1fr)"` to `.highlights-grid`.

**Trigger:** any time you'd write a bullet list of 3–6 named things that each have a short description — use this instead.

---

### Steps — numbered sequence (`.slide-steps`)

Use for process explanations, how-it-works breakdowns, rollout order, or any content where the sequence is the point. Each step has a numbered label, a bold title, and an optional description.

```html
<section class="slide-steps" data-background-color="var(--bg)">
  <div class="slide-header">
    <div class="eyebrow">Relay</div>
    <h2 class="slide-heading">How domain join works</h2>
  </div>
  <div class="steps-list">
    <div class="step">
      <div class="step-num">01</div>
      <div class="step-body">
        <div class="step-title">Client calls joinDomain()</div>
        <p class="step-desc">SDK sends a join request with domain ID and optional relay hint</p>
      </div>
    </div>
    <div class="step">
      <div class="step-num">02</div>
      <div class="step-body">
        <div class="step-title">Vinland resolves the cluster</div>
        <p class="step-desc">Domain ID maps to a relay cluster via the Vinland registry</p>
      </div>
    </div>
    <div class="step">
      <div class="step-num">03</div>
      <div class="step-body">
        <div class="step-title">libp2p attempts direct connection</div>
        <p class="step-desc">NAT traversal via hole-punching; relay fallback if blocked</p>
      </div>
    </div>
  </div>
</section>
```

3–5 steps is the sweet spot. **Hard cap: 7 steps.** Beyond 7, the auto-fit script will scale down text and row padding to make things fit, but the slide will look cramped regardless. If you have 8+ sequential items, split them across two step slides or convert to a bullet list.

The `.step-desc` is optional — omit if the title alone is self-explanatory. Omitting `.step-desc` on all steps is one way to fit more steps without overflow.

**Trigger:** any time the content is a sequence — how something works, how to integrate, what happens in order — use this instead of a numbered bullet list.

---

### Half — text + visual (`.slide-half`)

50/50 layout: left side carries the heading and bullets or prose; right side holds a chart, architecture SVG, or screenshot. Use when a graphic supports the text argument but isn't strong enough to stand alone as a full graphic slide.

```html
<section class="slide-half" data-background-color="var(--bg)">
  <div class="half-left">
    <div class="slide-header">
      <div class="eyebrow">Relay</div>
      <h2 class="slide-heading">New transport layer</h2>
    </div>
    <div class="slide-body">
      <ul>
        <li><strong>libp2p</strong> — direct peer connections; no central relay hop</li>
        <li><strong>Vinland</strong> — cluster discovery replaces static relay config</li>
        <li><strong>Fallback</strong> — relay still used when NAT traversal fails</li>
      </ul>
    </div>
  </div>
  <div class="half-right">
    <svg viewBox="0 0 520 420" xmlns="http://www.w3.org/2000/svg" style="width:100%;">
      <!-- architecture or chart SVG -->
    </svg>
  </div>
</section>
```

The right side can also hold a contained `<img>` for screenshots. Keep the left to 3–4 bullets max — the visual on the right is doing half the work.

**SVG sizing constraint:** the right half has a `max-height: 400px` CSS cap. Keep SVG viewBoxes no taller than 400 units (e.g. `viewBox="0 0 500 380"`) and ensure all drawn elements sit within the viewBox bounds — content that extends beyond the viewBox clips or overflows the slide boundary.

**Trigger:** any time you have a graphic slide where the visual alone doesn't fully explain the point — pair it with the text on the left instead of adding a separate explanation slide.

---

### Data table (`.slide-table`)

Use for structured, scannable rows: open/closed tickets, in-progress todos, user lists, version tables. Pair with `.pill` labels for status. Keep to 5–8 rows max — dense tables don't read well at presentation scale.

**Status pills:** `.pill.open` (green), `.pill.closed` (muted), `.pill.in-progress` (orange), `.pill.review` (purple).

```html
<section class="slide-content" data-background-color="var(--bg)">
  <div class="slide-header"><h2>Open issues — spatial audio</h2></div>
  <div class="slide-body">
    <table class="slide-table">
      <thead>
        <tr>
          <th>Issue</th>
          <th>Owner</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Latency spike on iOS 17.4</td>
          <td>Alex K</td>
          <td><span class="pill in-progress">In progress</span></td>
        </tr>
        <tr>
          <td>Android headset mic dropout</td>
          <td>Sam R</td>
          <td><span class="pill review">Review</span></td>
        </tr>
        <tr>
          <td>Stereo width clamp regression</td>
          <td>Jordan L</td>
          <td><span class="pill open">Open</span></td>
        </tr>
        <tr>
          <td>Session ID collision in relay</td>
          <td>Charlie S</td>
          <td><span class="pill closed">Closed</span></td>
        </tr>
      </tbody>
    </table>
  </div>
</section>
```

---

### Image / screenshot

**Full-bleed:**
\`\`\`html
<section class="slide-image"
  data-background-image="data:image/png;base64,{encoded}"
  data-background-size="cover">
  <div class="image-caption">Caption text</div>
</section>
\`\`\`

**Contained:**
\`\`\`html
<section class="slide-content" data-background-color="var(--bg)">
  <div class="slide-header"><h2>Park — domain view</h2></div>
  <div class="slide-body">
    <img src="data:image/png;base64,{encoded}" alt="Park domain view"
         style="width:100%;max-width:1280px;border-radius:8px;" />
  </div>
</section>
\`\`\`

Cap `max-width: 1280px` so the browser only ever downscales — text stays crisp on HiDPI.

---

### Annotated screenshot (`figure.magnify-area`)

Hover shows a 2.4× circular loupe — no JS wiring needed, just the class.

\`\`\`html
<section class="slide-content" data-background-color="var(--bg)">
  <div class="slide-header">
    <div class="eyebrow">Cactus</div>
    <h2>Planogram detection — new overlay</h2>
  </div>
  <div class="slide-body">
    <figure class="magnify-area" style="position:relative;display:inline-block;">
      <div class="screenshot-stage">
        <img src="data:image/png;base64,{encoded}" alt="Planogram overlay"
             style="width:100%;max-width:1100px;" />
      </div>
      <div class="loupe" style="position:absolute;"></div>
      <p class="muted" style="font-size:.75rem;margin-top:.5rem;">Hover to magnify</p>
    </figure>
  </div>
</section>
\`\`\`

---

### Click-to-expand image (`figure.expandable`)

Click opens a fullscreen lightbox. Esc or backdrop click to dismiss.

\`\`\`html
<figure class="expandable" style="display:inline-block;cursor:zoom-in;">
  <div class="screenshot-stage">
    <img src="data:image/png;base64,{encoded}" alt="SDK flow diagram"
         style="width:100%;max-width:900px;border-radius:6px;" />
  </div>
  <div class="muted" style="font-size:.75rem;margin-top:.4rem;">Click to enlarge</div>
</figure>
\`\`\`

Multiple expandable figures can sit on a single slide — the lightbox script handles all of them.

---

### Closing slide — optional

\`\`\`html
<section class="slide-closing" data-background-color="var(--bg)">
  <div class="closing-bottom">
    <div class="eyebrow">Project · Week N</div>
    <h2 class="closing-heading">That\'s the week.</h2>
    <p class="closing-body">Questions? Find Author on Discord — DM directly.</p>
  </div>
</section>
\`\`\`

**⚠️ Common error — do not do this:** agents sometimes copy the title slide's two-column grid structure (with `.title-left` and `.meta` blocks) onto the closing slide. That is wrong. The closing slide has **one wrapper div** (`.closing-bottom`) with flat children — eyebrow, heading, body paragraph — and nothing else. No `.meta` block, no `.closing-left`, no grid, no author/date/week info.

The section is flex-column centered on both axes. Use the author's name or Discord handle in the contact line. Never mention Slack.
---

## Step 6 — Helper class inventory

**Eyebrow guidance** — the eyebrow has three valid jobs. Pick one per slide. Using it any other way wastes the space.

1. **Scope / team** — says which project, team, or system the slide is about: `"Relay"`, `"SDK telemetry"`, `"Park beta"`. Use when the heading alone doesn't establish the context.
2. **Temporal / situational** — says when or why this is relevant: `"This week"`, `"Since Wk 14"`, `"Decision"`, `"Still unresolved"`. Use when timing or status is the key dimension.
3. **Access / audience qualifier** — says who this is for: `"Internal only"`, `"Investors"`. Use sparingly — only when the content on that specific slide is restricted in a way the badge alone doesn't convey.

The eyebrow must NOT echo the heading. If the heading already says the topic, the eyebrow should add a different dimension — not repeat it in different words.

| ✗ Avoid | ✓ Better | Why |
|---|---|---|
| eyebrow="Blockers" + heading="Blockers & asks" | eyebrow="Internal only" + heading="Blockers & asks" | Scope/audience, not repetition |
| eyebrow="Performance" + heading="Performance this week" | eyebrow="Relay" + heading="Latency — 7-week trend" | Identifies the system, heading is specific |
| eyebrow="Relay" + heading="Relay infrastructure" | eyebrow="Decision" + heading="Why we chose libp2p" | Adds situational context |
| eyebrow="What's next" + heading="What's next" | eyebrow="Week 21 priorities" + heading="What's next" | Makes the timeframe explicit |

If you genuinely have nothing useful to add with the eyebrow — skip it. An absent eyebrow is better than a redundant one.

**Typography**
`.eyebrow` — uppercase accent label · `.eyebrow.is-issue` — red variant · `.muted` — de-emphasised body text · `.prose` — slightly tighter body copy for dense content · `.accent` / `.lime` / `.highlight` — inline colour utilities

**Status**
`.callout` (max 2 per deck) · `.pill` · `.pill.open` / `.pill.closed` / `.pill.in-progress` / `.pill.review` · `.dot.green` / `.dot.amber` / `.dot.red` · `.sev.crit` / `.sev.high` / `.sev.med` / `.sev.low`

**Dividers**
`.hairline` — 1px rule, no margin · `.slide-rule` — 1px rule with 20px top/bottom margin

---

## Step 7 — Interactive behaviours

Three IIFE modules live in `org/src/design/slides/template.html`. Copy them verbatim into every generated deck — each activates on a hook class with zero per-slide wiring.

| Module | Hook class | What it does |
|---|---|---|
| `setupMagnifiers()` | `figure.magnify-area` | Hover shows a 2.4× circular loupe. Re-initialises on `slidechanged` and `resize`. |
| `setupLightbox()` | `figure.expandable` | Click → fullscreen overlay. Esc closes in capture phase, pre-empting Reveal's overview toggle. |

Also copy verbatim from the template: overview button JS, theme toggle IIFE, auto-fit IIFE.

---

## Step 8 — Self-containment

Every deck is a single fully self-contained HTML file. Only permitted external dependency: Google Fonts.

**CSS** — `assemble.py` handles this automatically based on `--theme`. Do not manually inline CSS.

- `auki` — inlines `reveal.css` + `auki-theme.css` (with TT Firs Neue base64-embedded)
- `cactus` — inlines `reveal.css` + `auki-theme.css` (base layout) + `cactus-theme.css` (brand override, Questrial + Nunito Sans via CDN)
- `gotu` — inlines `reveal.css` + `auki-theme.css` (base layout) + `gotu-theme.css` (brand override, DM Sans via CDN)

**Fonts** — for `auki`, `assemble.py` replaces `@font-face` relative URLs with base64 data URIs automatically. For `cactus` and `gotu`, fonts load from Google Fonts CDN.

**Logos** — `assemble.py` base64-encodes the correct logo SVGs per theme automatically. The placeholder names in the skeleton HTML are the same for all themes — `assemble.py` maps them to the right files:

| Placeholder        | auki                      | cactus            | gotu            |
|--------------------|---------------------------|-------------------|-----------------|
| `MONOGRAM_WHITE_B64` | auki-monogram-white.svg | cactus-dark.svg   | gotu-dark.svg   |
| `MONOGRAM_BLACK_B64` | auki-monogram-black.svg | cactus-light.svg  | gotu-light.svg  |
| `WORDMARK_WHITE_B64` | auki-wordmark-white.svg | cactus-dark.svg   | gotu-dark.svg   |
| `WORDMARK_BLACK_B64` | auki-wordmark-black.svg | cactus-light.svg  | gotu-light.svg  |

**Reveal.js JS** — inline `org/src/design/slides/vendor/reveal.js` at end of `<body>` before `Reveal.initialize()`. 

**CRITICAL:** Copy the **entire** `Reveal.initialize({...})` block **verbatim** from `org/src/design/slides/template.html` lines 707–751. This includes the 1280×720 canvas dimensions plus all behavioural flags (controlsLayout, fragmentInURL, overview, keyboard, etc.). These are not optional — they activate deck-chrome features and prevent the exact 960×700 fallback regression that causes right-side overflow and mis-centering.

**PDF print shadow fix** — Chrome rasterises `box-shadow` as solid coloured rectangles in print mode. Add at the end of the inlined CSS:

\`\`\`css
@media print,
html.print-pdf,
body.print-pdf {
  .deck-chrome,
  .stat-card,
  .callout,
  .compare-side,
  .pill,
  .project-tag {
    box-shadow: none !important;
  }
}
\`\`\`

---

## Step 9 — Output

### Embed Pulse metadata (required)

Every generated deck must include this block in `<head>`, **before** the `<style>` tag. The Pulse platform reads it to build the presentation index — without it, the index falls back to path inference and loses title, projects, tags, and author details.

```html
<script type="application/json" id="pulse-meta">
{
  "id": "{author}-{YYYY}-{NN}-slides",
  "title": "{What the deck is about — the main topic or headline}",
  "author": "Full Name",
  "authorSlug": "first-last",
  "date": "YYYY-MM-DD",
  "week": "YYYY-NN",
  "format": "slides",
  "audience": "internal",
  "projects": ["project-a", "project-b"],
  "tags": ["shipped"],
  "thumbnail": null
}
</script>
```

**`title` — format: `[Product or Team] — [what was done or built]`**

The left side is the product or team name. The right side is the specific thing that happened — a feature, release, milestone, or concise description. This is what appears on the Pulse card.

- **Good:** `"Relay — binary framing and message compression shipped"`, `"Cactus — v0.5 planogram release"`, `"Infrastructure — Kubernetes migration and monitoring overhaul"`, `"Developer Relations — SDK hackathon recap and community growth"`, `"Pulse — annual leave tracking feature"`
- **Avoid:** `"Week 20 — Cactus"` (week belongs in the `week` field, not the title), `"Cactus"` (too vague — which week, what happened?), `"The relay rewrite"` (no product prefix), `"Relay shipped"` (too short, no specifics)

The left side should always be the product or team, never a feature name or verb. The right side should be specific enough that someone browsing the Pulse directory knows what the deck covers without opening it.

`projects` are Auki project names in lowercase kebab-case. `tags` are freeform — common values: `shipped`, `research`, `design`, `infrastructure`. `thumbnail` is `null` unless an image was explicitly uploaded.

---

### File path

| Audience | Path |
|---|----|
| `internal`  | `internal/week-{NN}/{author}.html`  |
| `investor`  | `investors/week-{NN}.html`          |
| `client`    | `clients/week-{NN}.html`            |
| `community` | `community/week-{NN}.html`          |

Slug: `week-{NN}` (ISO week, zero-padded), `{author}` (first-name + last-initial, kebab-case: `charlie-s`, `alex-k`).

### Deck construction checklist

- [ ] `<script id="pulse-meta">` block present in `<head>` with all fields filled
- [ ] Audience badge class set correctly in `.deck-chrome`
- [ ] Title slide: project/team name in `<h1>`, no week number in heading, date in `.meta-date`
- [ ] Closing slide: **no `.meta` block, no `.closing-left` wrapper** — only eyebrow + h2 + p inside `.closing-bottom`
- [ ] `slide-desc` paragraphs are inside `.slide-header` (after the h2), not inside `.slide-body`
- [ ] No mention of Slack anywhere — use Discord
- [ ] All placeholder text replaced with actual content
- [ ] Section dividers used only if 12+ slides with 3+ distinct topics
- [ ] Any run of 3+ bullet slides reviewed — confirmed each one genuinely needs bullets, not a more precise type
- [ ] Any before/after comparison uses `slide-compare` (metric) or `slide-split` (text), not two bullet slides
- [ ] Stats slide has 2-5 cards with real numbers
- [ ] Non-internal decks have blockers/asks removed
- [ ] Community decks have NDA-sensitive content redacted via `/nda-redact`
- [ ] Banner comments between every section (`<!-- === N. NAME === -->`)
- [ ] Sub-slide suffixes used where extending without renumbering (`12a`, `12b`)
- [ ] All images inlined as base64 data URIs
- [ ] `assemble.py` run with correct `--theme` flag (`auki`, `cactus`, or `gotu`)
- [ ] All four logo variants base64-embedded (handled by assemble.py)
- [ ] Reveal.js JS inlined at end of `<body>`
- [ ] `Reveal.initialize()` config copied **verbatim** from template.html lines 707–751 (width: 1280, height: 720, margin, minScale, maxScale, controlsLayout, fragmentInURL, overview, keyboard, etc. — verify these three fields are present)
- [ ] Theme toggle IIFE included (from template)
- [ ] Overview button JS included (from template)
- [ ] Auto-fit IIFE included (from template)
- [ ] `setupMagnifiers()` IIFE included (from template)
- [ ] `setupLightbox()` IIFE included (from template)
- [ ] PDF print shadow override block in CSS

**If images were attached (Step 10):**
- [ ] Each attached image set as `data-image="data:...;base64,..."` on its `<section>`, `data-image-caption` set
- [ ] Gallery button added to `.deck-controls` (before `#overview-btn`)
- [ ] Gallery overlay HTML added after `.deck-chrome`
- [ ] Image attachment IIFE added after `setupLightbox()` (copy from `template.html`)
- [ ] `assemble.py` re-run after adding images

### Quality check

After generating, review the deck:
- Does this look like the roundup in slide form? **If yes, rethink the structure.** That's a document, not a presentation.
- Does each slide have a clear theme — one topic it is about?
- Does the deck have a shape — opening beat, substance, close — that fits the actual content?
- Are there any slides that add no information? Cut them.
- Is the deck the right length? Don't pad, don't squeeze.
- Would a first-time reader understand what happened and why it matters without a separate document?

### Common generation errors — fix before committing

These are the most frequent mistakes made during generation. Check each one explicitly.

**Error 1 — Closing slide structure.** The closing slide must have this exact shape: `<section class="slide-closing">` → `<div class="closing-bottom">` → eyebrow + h2 + p. Nothing else. No `.meta` block (name, date, week, project tags). No `.closing-left` wrapper. Agents frequently copy the title slide's two-column grid structure here — that is wrong.

**Error 2 — `slide-desc` placement.** The `slide-desc` paragraph must be inside `.slide-header`, directly after the `<h2>`, not inside `.slide-body`. Placing it in `.slide-body` detaches it visually from the heading and can cause it to be clipped by overflow.

**Error 3 — Heading-visual agreement (sanity check #3).** For every graphic or stats slide, confirm that the heading makes a specific claim and the visual is direct evidence for that exact claim — not a related but different claim. If you cannot verify this without rendering, flag it in your reply and offer to convert the slide to a content type instead.

**Error 4 — Assemble script skipped or wrong theme (Step 9).** The `assemble.py` script **must** be run after writing the skeleton HTML — **never skip this step, even if the CSS appears to be in place.** Always pass `--theme <theme>` matching the brand chosen in Step 0. The CSS and logo placeholders must be in the skeleton before running.

The script includes a hard precondition guard: it refuses to write output unless `<script id="pulse-meta">` is present, at least two `<style>` blocks exist (reveal.css + auki-theme), and the four logo data-URIs are present. If the guard fires, report the error rather than manually pasting CSS or logos. Confirm the script prints `Assembled (theme): <path>` before treating the file as complete. Do not proceed to Step 10 until confirmed.

**Error 5 — Slack references.** Auki uses Discord, not Slack. Any mention of Slack in the deck or in contact lines is wrong. The closing slide contact line should say "Find [Author] on Discord" or "DM [Author] directly."

**Error 6 — Theme toggle IIFE missing.** The theme toggle script block from `template.html` **must** be copied verbatim into the generated deck — never omit it. Without it, the toggle button renders but does nothing: clicking it has no effect, and both icons may appear simultaneously. This IIFE must appear as a standalone `<script>` block after the PDF button listener and before the auto-fit IIFE. The checklist item `Theme toggle IIFE included (from template)` must be confirmed — if you cannot verify you copied it, open `template.html`, locate the `// ── Theme toggle ──` block, and paste it now.

**Error 7 — Reveal.initialize() config incomplete.** The entire `Reveal.initialize({...})` block **must** be copied verbatim from `org/src/design/slides/template.html` lines 707–751. Do not write a minimal version from memory. The extra fields (width/height 1280×720, controlsLayout, fragmentInURL, overview, keyboard, postMessage, etc.) are functional — they wire up the deck-chrome buttons, URL hash stability, overview grid, and other IIFEs that were included in the skeleton. Without them the deck renders at the wrong canvas size (causing the exact "not centered, right side cut off" regression) and interactive features break. Always open the template and paste the full block.

---

## Step 10 — Image attachments

**This step is mandatory. Do not skip it. Do not commit the deck before completing it.**

After the quality check, stop and ask — every time, without exception:

> "Would you like to attach any images to slides? Share file paths and tell me which slide each should go on. If you don't have any, just say no and I'll commit."

**Wait for an explicit "no" before proceeding.** Silence, no response, or "looks good" is not a "no." A "no" or "none" means proceed to commit. Any other response means re-read it as an image attachment request or a correction.

Never assume the user has no images — they may have screenshots, diagrams, or demo recordings. The image attachment system exists specifically for this workflow.

### When images are provided

**For each image:**

1. Read the file as binary, base64-encode it, construct a data URI:
   ```python
   import base64, mimetypes
   mime = mimetypes.guess_type(path)[0] or 'image/png'
   with open(path, 'rb') as f:
       uri = f'data:{mime};base64,' + base64.b64encode(f.read()).decode()
   ```

2. On the matching `<section>`, add two attributes:
   ```html
   <section class="slide-content"
            data-image="data:image/png;base64,{encoded}"
            data-image-caption="Optional caption describing the image">
   ```
   The caption is shown in the gallery overlay. Use the slide heading as the caption if the user doesn't provide one.

### Gallery chrome — add to the deck if any images were attached

The gallery button and overlay are **not** included in the base template — add them when at least one image is attached.

**1. Gallery button** — insert into `.deck-controls`, immediately before `#overview-btn`:

```html
<!-- Gallery button — JS shows/hides based on whether any slide has data-image -->
<button class="deck-btn" id="gallery-btn" aria-label="View attached images" style="display:none">
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="1" y="3" width="12" height="9" rx="1.5" stroke="currentColor" stroke-width="1.2"/>
    <circle cx="4.5" cy="6.5" r="1" fill="currentColor"/>
    <path d="M1.5 10L4.5 7L7 9.5L9.5 7L12.5 10" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/>
  </svg>
</button>
```

**2. Gallery overlay** — insert immediately after the closing `</div>` of `.deck-chrome`, before `<div class="reveal">`:

```html
<!-- Gallery overlay — populated by JS -->
<div class="gallery-overlay" id="gallery-overlay">
  <div class="gallery-header">
    <span class="gallery-title">Attached images</span>
    <button class="gallery-close" id="gallery-close" aria-label="Close gallery">&times;</button>
  </div>
  <div class="gallery-scroll">
    <div class="gallery-grid" id="gallery-grid"></div>
  </div>
</div>
```

**3. Image attachment JS IIFE** — copy verbatim from `template.html` (the block labelled `// ── Slide image attachment system ──`). Add it at the end of `<body>` after `setupLightbox()`.

`setupLightbox()` (Step 7, copied from `template.html`) must already be in the deck — it defines `window._openLightbox`. If it's missing, add it now before adding the image attachment IIFE.

### Gallery CSS

The gallery overlay, gallery button, and per-slide image button CSS are all part of `auki-theme.css` — `assemble.py` inlines them automatically. If the assembled deck looks broken (overlay visible by default, deck pushed down), the issue is a stale theme file. Re-run `assemble.py` with the current `auki-theme.css`.

---

## Product Deck Mode

> **Entry point:** `/presentation` passes `type = product-deck`. Jump here from Step 2 when that flag is present. All steps below replace Steps 2–10 for this mode. Steps 0 (theme) and 1 (audience) still apply first.

Product decks are standalone presentations — not tied to a specific week, not sourced from harvest. They tell a product or company story for an audience outside the team (investors, partners, prospects). The structure is cleaner: no author meta on the title slide, no "find me on Discord" on the closing slide.

**Everything else is identical to weekly update slides** — same slide types, same CSS, same themes, same assemble.py, same IIFEs. No special handling needed at the design system level.

---

### PD Step 1 — Check for existing deck and gather product information

**Before asking any questions**, check `product-decks/featured.json` in the presentations repo for an entry matching the product the user mentioned.

```
presentations repo: product-decks/featured.json
```

If a deck entry exists for this product (i.e. `deck` is not null):

> "There's an existing [Product] deck last updated on [date]. Would you like to:
> - **Update** — open the existing deck and make targeted changes (edit specific slides, refresh content)
> - **Fresh** — start a completely new deck from scratch"

**If Update:**
- Read the existing deck HTML file at `product-decks/{existing-filename}.html`
- Show the user the slide outline (headings and types) and ask what they want to change
- Work slide by slide — the user tells you which slides need updating, you make the edits
- Re-run `assemble.py --theme <theme>` on the modified file
- The output file gets a new date suffix (e.g. `cactus-2026-06.html`) — do not overwrite the old file

**If Fresh (or no existing deck):**
Ask these questions. Adapt and skip any you already know from context.

> 1. **Product / company name** — what are we making a deck for?
> 2. **One-liner** — what does it do and for whom? (e.g. "Posemesh is a decentralised spatial computing network for AR devices.")
> 3. **Audience for this deck** — who will read it? (Investors / Partners / Prospects / Internal review)
> 4. **The ask or goal** — what do you want the reader to do or believe after seeing this deck?
> 5. **Key points to cover** — what are the 3–5 most important things this deck must communicate?
> 6. **Traction or proof points** — any metrics, customers, or milestones worth including?
> 7. **Deck length** — short (8–12 slides), standard (12–20), or let me decide based on content?

Only ask what you don't already know. Don't ask all seven if the user volunteered the answers while describing what they want.

---

### PD Step 2 — Choose an arc

Product decks have their own narrative shapes. Commit to one before writing any slides.

**Arc P1 — The problem/solution**
Use when: the core insight is that an important problem is unsolved and you've solved it.
```
Title → The problem (specific, felt pain) → Why existing solutions fail →
The solution (statement) → How it works → Proof / traction → What's next / ask
```

**Arc P2 — The market thesis**
Use when: the most compelling thing is the timing — why this market, why now.
```
Title → The shift (what changed in the world) → The opportunity it creates →
Our position → The product → Proof → Ask
```

**Arc P3 — The product demo**
Use when: the product speaks for itself — visual-first.
```
Title → The visual (screenshot or graphic — slide 2) → What you're looking at →
How it works → Who it's for → Metrics / traction → Ask
```

**Arc P4 — The traction story**
Use when: you have real numbers and momentum is the strongest argument.
```
Title → The headline number (stats — slide 2) → What drove it →
The product that produced it → Where it's going → Ask
```

---

### PD Step 3 — Title and closing slide structure

Product decks use a stripped-down title slide — no author, no week, no project tags. The closing slide uses company contact details rather than a personal Discord handle.

**Title slide:**
```html
<section class="slide-title" data-background-color="var(--bg)">
  <div></div>
  <div class="title-bottom">
    <div class="title-left">
      <span class="title-top-anchor"></span>
      <div class="eyebrow">Category · Tagline</div>
      <h1 class="title">Product or Company Name</h1>
      <p class="subtitle">One sentence — what it does, for whom, and why it matters now.</p>
    </div>
    <!-- No .meta block — product decks carry no author/week attribution -->
  </div>
</section>
```

**Closing slide:**
```html
<section class="slide-closing" data-background-color="var(--bg)">
  <div class="closing-bottom">
    <div class="eyebrow">Company · Month Year</div>
    <h2 class="closing-heading">Let's build together.</h2>
    <p class="closing-body">contact@company.com &nbsp;&middot;&nbsp; company.com</p>
  </div>
</section>
```

No "find me on Discord" — use the company's public contact details or leave the body line empty.

---

### PD Step 4 — Build, assemble, and output

Follow Steps 4–8 of the weekly update flow for narrative, slide types, and self-containment — all identical.

After the deck is assembled and the image attachment step is complete, ask:

> "Update the product deck banner on Pulse with this new deck? (y/n)"

**If yes:** update `product-decks/featured.json` — set or replace the `deck` entry for this product:

```json
"deck": {
  "path": "product-decks/{slug}-{YYYY-MM}.html",
  "date": "YYYY-MM-DD",
  "title": "{Product Name} — Product Deck",
  "thumbnail": null
}
```

`thumbnail` is `null` by default. If the user wants a cover photo on the banner, ask them to provide an image path, base64-encode it, and set it as a data URI here (`"data:image/jpeg;base64,..."`).

Commit `featured.json` in the same commit as the deck HTML. This updates the banner immediately once the commit is merged.

**If no:** leave `featured.json` unchanged. The deck is stored but won't appear on the banner.

**Pulse metadata block** — still required, but with `week: null` and `tags: ["product-deck"]`:

```html
<script type="application/json" id="pulse-meta">
{
  "id": "{product-slug}-product-deck",
  "title": "{Product Name} — Product Deck",
  "author": "Full Name",
  "authorSlug": "first-last",
  "date": "YYYY-MM-DD",
  "week": null,
  "format": "slides",
  "audience": "internal",
  "projects": ["{product-slug}"],
  "tags": ["product-deck"],
  "thumbnail": null
}
</script>
```

**File path:** `product-decks/{product-slug}-{YYYY-MM}.html`

Examples: `product-decks/posemesh-2026-05.html`, `product-decks/cactus-investor-2026-05.html`

> **Do not add product deck entries to `index.json`.** They are committed to the presentations repo under `product-decks/` but are not surfaced in the Pulse UI directory until explicitly requested.

**assemble.py command:**
```bash
python3 scripts/assemble.py <skeleton.html> product-decks/{slug}-{YYYY-MM}.html --theme <theme>
```

---

### PD Checklist

- [ ] Checked `product-decks/featured.json` for existing deck before starting
- [ ] If updating: existing deck read, changes made slide by slide, new filename with updated date
- [ ] If fresh: arc chosen and committed before writing any slides
- [ ] Title slide: **no `.meta` block** — no author, date, week, or project tags
- [ ] Closing slide: company contact details (not Discord handle)
- [ ] `<script id="pulse-meta">` present with `week: null` and `tags: ["product-deck"]`
- [ ] File saved to `product-decks/{slug}-{YYYY-MM}.html`
- [ ] `assemble.py` run with correct `--theme` flag
- [ ] **Not added to `index.json`**
- [ ] Image attachment step (Step 10) still applies — ask before committing
- [ ] User asked about banner update — if yes, `featured.json` updated and committed alongside deck
