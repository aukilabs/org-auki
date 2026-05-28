---
name: community-update
description: Generates a combined community-facing presentation that aggregates all internal weekly updates into a single master document. Run once per week after individual updates have been committed. Reads all presentations from the target week in aukilabs/presentations, synthesises them by project, applies NDA redaction, and commits a community-update page to community/week-{NN}.html. Always community audience — this is the outward-facing digest.
---

# /community-update

Reads every presentation committed this week, synthesises the work by project into a single community-facing document, and commits it to the public `community/` directory. This is the one document external audiences see — it replaces the individual updates as the community-facing record of the week.

Always `community` audience. Always `page` format (scrollable HTML). Always runs `/nda-redact` before committing.

---

## Step 1 — Confirm the week

Resolve the target week:

```bash
eval "$(org/src/skills/presentation/harvest/scripts/week-scope.sh)"
# $HARVEST_WEEK      → ISO week number (e.g. 20)
# $HARVEST_WEEK_LABEL → human label (e.g. "Week 20")
# $HARVEST_SINCE     → YYYY-MM-DD (most recent Friday)
# $HARVEST_UNTIL     → YYYY-MM-DD (today)
```

Announce what you found:

> "I'll build the community update for **Week {NN}** ({YYYY-MM-DD} → {YYYY-MM-DD}). Is that right, or do you want a different week?"

Wait for confirmation. If the user specifies a different week, re-run the script with `--week {N}` or use the provided dates directly.

---

## Step 2 — Fetch this week's presentations

Read `aukilabs/presentations/internal/week-{NN}/` via the GitHub API. List every `.html` file in that directory.

For each file:
1. Parse the `<script type="application/json" id="pulse-meta">` block to get: `title`, `author`, `projects`, `tags`.
2. Extract the document body — strip CSS, scripts, and chrome; keep heading text, paragraph text, list items, and metric values. The same `extractText()` approach used by the AI Lambda is sufficient.
3. Store as a structured entry: `{ author, projects, title, content }`.

Once all files are parsed, report what you found:

> "Found **N presentations** this week:
> - Alex K — Posemesh SDK (2 projects)
> - Charlie S — Pulse, Park
> - …
>
> Does this look right? Any updates missing that should be included?"

Wait for their response. If they name missing updates that haven't been committed yet, ask them to commit those first and re-run. If they want to proceed without a specific person's update, note the omission in a comment and continue.

---

## Step 3 — Clarifying questions

Ask only these — keep it short:

> "Before I build the community update:
>
> 1. **Spotlight** — is there one achievement from this week that should lead the document? (If not, I'll pick the most significant one.)
> 2. **Anything to exclude?** — is any update, project, or detail not ready for public release this week?
> 3. **Any framing or context to add?** — e.g. a milestone reached, a launch approaching, or a theme that ties the week together. (Optional — skip if nothing applies.)"

All three are optional. If the user says "just build it", proceed with AI-chosen spotlight and no exclusions.

---

## Step 4 — Synthesise by project

Before writing any HTML, build a mental model of the week by project — not by author.

### Group by project

Across all presentations, collect every initiative under its project name. A presentation covering two projects contributes to both. A project touched by two authors gets both contributions merged into one section.

For each project, synthesise:
- What shipped (the most concrete, specific, complete things)
- What's actively in progress (named initiatives with clear direction)
- What's coming next (near-term plans that are meaningful to an external audience)

### Spotlight selection

If the user named a spotlight: use it exactly. Lead with it.

If not, pick the single most externally significant achievement across all projects:
- Prefer shipped, concrete outcomes over in-progress work
- Prefer things that change a capability, metric, or user experience — not internal tooling
- Prefer the thing a developer or partner would find most interesting

The spotlight is one strong paragraph — 3–5 sentences. Not a list. Not a section. A direct, declarative opening statement about the most important thing that happened.

### NDA filter (pre-generate)

Before drafting sections, scan each project's synthesised content and mentally flag:
- Named partners / customers not yet announced
- Financial figures (ARR, deal sizes, runway)
- Unreleased feature names or internal codenames
- Personnel matters not yet public
- Technical vulnerabilities or security findings
- Internal tooling names under NDA

You will run `/nda-redact` formally in Step 6, but flag these now so your draft doesn't build narrative around content that will be removed — that produces awkward gaps. Where a project's contribution is mostly sensitive, describe the category of work rather than the specifics ("infrastructure work to support a major upcoming integration" vs naming the partner).

---

## Step 5 — Generate

Build the document using the same template and assembly process as `/page`.

### Document structure

| # | Section | Notes |
|---|---|---|
| — | Spotlight | Always first. One strong prose paragraph. The lead. |
| 01 | By project | One subsection per project touched this week. See below. |
| 02 | What's coming | Aggregated near-term plans across all teams. |

No blockers section — this is a community document.

---

### Spotlight block

Place this immediately after the document header (before section 01), outside the section numbering:

```html
<div class="callout">
  <p>{3–5 sentence spotlight paragraph — the single most significant achievement of the week, written for an external technical audience.}</p>
</div>
```

The spotlight is not a section header and does not get a section number. It is a callout that leads the document. Write it last, after you've drafted everything else, so you know what the real highlight is.

---

### By project (Section 01)

One `<h3>` per project, followed by whatever components fit that project's content. Each project subsection is self-contained — a reader should be able to read just their project of interest.

```html
<h2>01 &nbsp; By project</h2>

<h3>Project Name</h3>
<!-- components chosen freely from the component guide below -->
```

**Component guide — same as `/page`, applied per project:**

Use prose (`<p>`) when the content flows as connected thought. Use a bullet list (`<ul>`) for discrete parallel items. Use a metrics strip (`.metrics`) when there are 2–5 real, meaningful numbers. Use a callout (`.callout`) for the single most important thing from that project — max 1 per project, only if something genuinely stands out.

Order within a project subsection:
1. What shipped (most concrete first)
2. What's in progress (brief — name the initiative and its current state)
3. Skip "what's next" at the project level — save forward-looking content for Section 02

If a project had a very quiet week (one small shipped item, nothing in progress), keep its subsection to a single short paragraph. Don't pad.

If two authors both contributed to the same project, write the project section as a unified narrative — not "Alex did X, Charlie did Y." The community update is about the project, not the individual.

---

### What's coming (Section 02)

Aggregated near-term plans across all projects. Write as a bullet list grouped by project tag. Only include plans that are concrete enough to be meaningful — "continuing work on X" is not a plan. "Shipping Y in Week {NN+1}" or "first external test of Z with a partner" is.

```html
<h2>02 &nbsp; What's coming</h2>
<ul>
  <li><strong>Project A</strong> — {what's specifically planned next, in one clause}.</li>
  <li><strong>Project B</strong> — {what's specifically planned next}.</li>
</ul>
```

If a project has nothing meaningful coming up that's safe to share publicly, omit it from this section.

---

### Tone — community voice

This document is the public face of the week. Write it as a technically literate external audience would want to read it — not as internal shorthand.

- Declarative and specific. State what changed, not that work happened.
- "We shipped X" not "progress was made on X"
- Technical depth is fine — the community audience is developers and partners
- No emoji. No exclamation points.
- Don't name individual contributors unless it's genuinely relevant to an external reader (e.g. a new team member who will be a point of contact)
- If a project had no externally shareable work this week, omit it entirely — don't write placeholder text

---

### Self-containment — assembly

Use the same assemble script as `/page`:

```bash
python3 org/src/skills/presentation/page/scripts/assemble-page.py <output.html>
```

Write the skeleton HTML with `/* ROUNDUP_CSS_PLACEHOLDER */` in the `<style>` block and the four logo placeholder strings in the logo `<img>` tags. The script inlines everything. Confirm it prints `Assembled: <path>` before treating the document as complete.

---

## Step 6 — NDA redaction

Run `/nda-redact` on the fully assembled HTML:

```
/nda-redact --html <assembled output> --audience community
```

After redaction, summarise what was changed and show the author the list of redacted passages. Flag anything ambiguous — ask the author to confirm before committing.

---

## Step 7 — Output

### Pulse metadata (required)

Include in `<head>` before `<style>`:

```html
<script type="application/json" id="pulse-meta">
{
  "id": "community-update-{YYYY}-{NN}",
  "title": "Week {NN} — Community Update",
  "author": "Auki Labs",
  "authorSlug": "auki-labs",
  "date": "YYYY-MM-DD",
  "week": "YYYY-NN",
  "format": "community-update",
  "audience": "community",
  "projects": ["{all project names covered, kebab-case}"],
  "tags": ["digest", "community"],
  "thumbnail": null
}
</script>
```

`projects` should list every project covered — the Pulse platform uses this for project-page filtering. `date` is today's date.

---

### File path

```
community/week-{NN}.html
```

e.g. `community/week-20.html`

This goes in `aukilabs/presentations`. The `community/` directory is public — no auth required.

---

### Commit

Commit with a message like:

```
Week {NN} community update — {N} projects, {M} contributors
```

Push using the author's own Git credentials.

---

### Confirm

After committing:

> "Community update committed — `community/week-{NN}/community-update.html`.
>
> It covers: {comma-separated project list}
> Contributors: {N} ({list of authors})
>
> {N} passages were redacted for community. Review them above before sharing the link."

---

## Notes

**Source of truth is `internal/`** — always read from `internal/week-{NN}/` not from `community/`. Internal presentations have full detail; community presentations (if any exist individually) may already be redacted and will under-inform the digest.

**One community update per week** — if `community/week-{NN}.html` already exists, warn the user before overwriting: "A community update for Week {NN} already exists. Overwrite it?"

**Missing presentations** — if a team member hasn't committed their update yet, note the gap in your opening report (Step 2) but don't block on it. The user can run this skill again once the missing update lands.

**The spotlight is the most important editorial decision** — don't pick the most technical thing or the most recently shipped thing. Pick the thing that best represents what Auki is building, that would make a developer or partner want to follow along. When in doubt, ask the user.
