---
name: project-scaffold
description: Use when creating a new Auki project exocortex. Produces the standard file structure (README, vision, AGENTS, CONTRIBUTING, roadmap, glossary, CHANGELOG, parking_lot, src/ with readme and sprint) and adds the project to the canonical list in org-auki/src/projects.md. For work that spans multiple repos, use quest-scaffold instead.
---

# Scaffolding a new project

Every Auki project follows the same exocortex shape. The project exocortex isn't a special folder — it emerges from the structure of the repo itself.

## Shape

| File | Purpose | Who maintains |
|------|---------|---------------|
| `README.md` | GitHub landing page — discovery, setup, short intro. | Project lead |
| `vision.md` | Aspirational "why" — what this project is, why it exists, the dream. Distinct from `README.md` because GitHub's landing-page slot is already doing setup work. | Project lead |
| `AGENTS.md` | Entry point for an AI agent loaded into this repo. See starter below. | Project lead |
| `CONTRIBUTING.md` | Logging conventions for this project. Full content — not a pointer — so each project can diverge where it makes sense. See starter below. | Project lead |
| `roadmap.md` | Where the project is headed. At least 3 months, at most 3 years. Must align to `org-auki/roadmap.md`. | Project lead |
| `glossary.md` | Project-specific vocabulary — terms someone new wouldn't know. | Anyone on the project |
| `CHANGELOG.md` | Append-only, latest on top. Uses an **Author** field (not PromptID) since projects have multiple contributors. | Anyone on the project |
| `parking_lot.md` | Open questions needing human input before work can proceed. | Anyone on the project |
| `src/` | The actual code. | Contributors |
| `src/readme.md` | AI-generated description of what the code does today. No fluff. | AI agent |
| `src/sprint.md` | Current work and next steps. At most a week of work. | Project lead (updated weekly) |

## Steps

1. Add a row for the project to `org-auki/src/projects.md` (canonical list) **first**.
2. Create the repo at `github.com/aukilabs/{slug}`.
3. Scaffold the files above, using the starter content in the next section for `AGENTS.md`, `CONTRIBUTING.md`, and `vision.md`.
4. Each contributor symlinks the project into their personal exocortex:
   ```bash
   ln -s ~/project-repo ~/my-exocortex/{project-name}
   ```

## Starter content

### `vision.md`

```markdown
# Vision: {Project Name}

{One paragraph: what this project is and why it exists — the aspirational version.}

{One paragraph: how this project serves Auki's mission — the real world web, intercognitive capacity, perception-first strategy, etc.}

## Who works on it

{Lead, core contributors, cross-functional partners.}
```

### `AGENTS.md`

```markdown
You are in the {project-name} project — one of the Auki Labs projects listed in `aukilabs/org-auki → src/projects.md`.

At session start, read:

- `vision.md` — why this project exists
- `src/sprint.md` — what's being worked on this week
- `CHANGELOG.md` — recent decisions
- `parking_lot.md` — open questions needing input
- `src/readme.md` — what the code currently does

Broader Auki context (mission, team, methods, skills library) lives in `aukilabs/org-auki`. If you're running inside a personal exocortex, `org-auki/` is already symlinked in. Otherwise clone `aukilabs/org-auki` as a sibling directory and symlink it.

**Upstream Quest:** Check the top of `CHANGELOG.md`. If an upstream quest is declared there, you MUST dual-write any entries you make here to the quest's aggregate changelog.

Log changes to `CHANGELOG.md` with an **Author** field (not PromptID — projects have multiple contributors). See `CONTRIBUTING.md` for the exact format.
```

### `CONTRIBUTING.md`

```markdown
# Contributing to {Project Name}

Every change to a document in this repo should be logged in `CHANGELOG.md`.

## Changelog

Append-only, prepend latest entry on top. Each entry is a level-3 heading followed by 1–2 sentences: what changed and the decision behind it. Blank line between entries.

Heading format: `### {Author} · {Timestamp}` — e.g. `### Nils · Apr 2, 21:03 HKT, 2026`.

Project-level repos use an **Author** field (not PromptID) because they have multiple contributors.

Body: tight — 1–2 sentences. The changelog captures the decision, not a transcript.

**Upstream Quests:** If the `CHANGELOG.md` header declares an upstream quest, you must *dual-write* your entry. First append it here, then append it to the quest's changelog so the quest maintains a complete aggregated view.

**Personal Exocortex:** Don't forget that your interaction with this repo still originated from a user prompt. After updating this repo's `CHANGELOG.md`, you MUST also log the work in your user's personal exocortex `promptlog.md` and `changelog.md`.

### Good changelog entries

**Bad — too thin:** `Fixed typo.` No information.

**Bad — too long:** Paragraph-length recaps of everything discussed. The changelog is not a transcript.

**Good:** `Studied MemPalace retrieval system. Decided our exocortex doesn't need vector search yet — structured files solve 70% of the retrieval problem at zero infrastructure cost.`

## Project-specific conventions

{Fill in anything specific to this project — code style, testing, review process, release cadence, branch naming, etc. Remove this section if no project-specific additions apply yet.}
```

### `README.md`

```markdown
# {Project Name}

{One-paragraph intro — what this is, who it's for.}

## What it does

{2–5 bullets describing the functionality at a high level.}

## Status

See [`src/readme.md`](src/readme.md) for what's implemented today and [`src/sprint.md`](src/sprint.md) for current work.

## Why

See [`vision.md`](vision.md) for the aspirational "why."

## Repo layout

```
{project}/
  README.md        ← This file
  vision.md        ← Why this project exists
  AGENTS.md        ← Entry point for AI agents
  CONTRIBUTING.md  ← Logging and conventions
  roadmap.md       ← Where this is headed
  glossary.md      ← Project vocabulary
  CHANGELOG.md     ← What changed and why
  parking_lot.md   ← Open questions needing input
  src/
    readme.md      ← Honest status of what's built
    sprint.md      ← Current work, next steps
```
```

### `CHANGELOG.md`

```markdown
# Changelog

*(If this project joins a cross-repo quest, add `Upstream Quest: [name](../../org-auki/src/quests/name/CHANGELOG.md)` here so agents know to dual-write.)*

Append-only. Latest entry on top. Level-3 heading + 1–2 sentences per entry.

### {Author} · {Timestamp HKT, YYYY}

Initial scaffold — project created.
```

### `parking_lot.md`

```markdown
# Parking Lot

Open questions that need human input before work can proceed. Append-only — park the question, then either resolve it in place or link to where it got resolved.

## Open

- {first open question here}

## Resolved

_(Move items here with a one-line note on how they were resolved.)_
```

### `roadmap.md`

```markdown
# Roadmap

At least 3 months out, at most 3 years. Phased. Must align to `org-auki/roadmap.md`.

## Phase 1 — {name}

- {milestone}

## Phase 2 — {name}

- {milestone}

## Dependencies

{External repos, people, decisions this depends on.}
```

### `glossary.md`

```markdown
# Glossary

Project-specific vocabulary — terms someone new wouldn't know.

| Term | Meaning |
|------|---------|
| {term} | {short definition} |
```

### `src/readme.md`

```markdown
# src/

Honest status of what's actually implemented today. AI-maintained — no fluff, no aspirations. For the aspirational version see `../vision.md`.

## Implemented

{Concrete features/components that work end-to-end.}

## In progress

{What's being actively built. Link to `sprint.md` for weekly detail.}

## Not yet

{What's on the roadmap but hasn't started.}
```

### `src/sprint.md`

```markdown
# Sprint — week of {YYYY-MM-DD}

At most a week of work. Updated weekly by the project lead.

## This week

- {task}

## Next up

- {task}

## Last week — done

- {task}

## Blockers

{Anything waiting on someone else.}
```

## If the work spans multiple repos

Use `quest-scaffold` instead. Quests aggregate state across repos; single-repo work stays in the project structure above.
