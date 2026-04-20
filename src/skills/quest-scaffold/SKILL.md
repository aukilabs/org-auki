---
name: quest-scaffold
description: Use when creating a cross-repo project (a "quest") — work that spans multiple Auki repos where no single repo can own the state. Produces the quest landing page under org-auki/src/quests/{slug}/ with README (identity), AGENTS, CONTRIBUTING, roadmap, sprints, changelog, parking_lot. If the work fits cleanly in one repo, use project-scaffold instead.
---

# Scaffolding a new quest

A **quest** is a cross-repo project. Quests live at org level in `org-auki/src/quests/{slug}/` so every project lead has visibility.

Use a quest when a single repo can't own the state. Otherwise prefer `project-scaffold`.

## Shape

| File | Purpose |
|------|---------|
| `README.md` | Identity file — landing page, pitch, repos involved, collaborators. This is the quest's "why." |
| `AGENTS.md` | Entry point for an AI agent loaded into this quest directly. See starter below. |
| `CONTRIBUTING.md` | Logging conventions for this quest. Full content — not a pointer — so each quest can diverge where it makes sense. See starter below. |
| `roadmap.md` | Phased plan across all repos. |
| `sprints.md` | Links + tight summaries of each sub-repo's `sprint.md`. |
| `CHANGELOG.md` | Cross-repo decisions only. Per-repo minutiae stays in the sub-repos. |
| `parking_lot.md` | Cross-repo open questions only. Per-repo questions stay in the sub-repos. |

Per-repo details stay in each sub-repo's own files — the quest is an aggregation layer, not a replacement.

## Steps

1. Add a row for the quest to `org-auki/src/projects.md` (Quests section — canonical index of projects + quests) **first**.
2. Open a PR against `org` adding `src/quests/{slug}/` with the files above, using the starter content in the next section for `AGENTS.md` and `CONTRIBUTING.md`.
3. Link each participating repo's `sprint.md` from `sprints.md`.
4. Update `org-auki/src/quests/README.md` to list the new quest.
5. **Critically:** Go into each participating sub-repo and edit its `CHANGELOG.md` file to add the `Upstream Quest:` pointer right below the `# Changelog` heading, so the sub-repo's AI agents know to dual-write decisions to the quest.

## Starter content

### `AGENTS.md`

```markdown
You are in the {quest-name} quest — a cross-repo project tracked at `aukilabs/org-auki → src/quests/{quest-name}/`. This directory is an aggregation layer across multiple repos.

At session start, read:

- `README.md` — what this quest is, which repos are involved, who the collaborators are
- `sprints.md` — current activity across sub-repos, with links
- `roadmap.md` — phasing and cross-repo dependencies
- `CHANGELOG.md` — the full aggregated decision log across every participating repo (per-repo decisions are duplicated here so the quest is the full view)
- `parking_lot.md` — cross-repo open questions

Per-repo code and implementation detail live in the sub-repos themselves — follow the links in `sprints.md` when you need them. Broader Auki context (mission, team, methods, skills library) lives one level up in `aukilabs/org-auki`.

Log every decision that affects this quest to `CHANGELOG.md` with an **Author** field (not PromptID) — cross-repo decisions originate here, per-repo decisions get duplicated here from their sub-repo's own changelog. See `CONTRIBUTING.md` for the format.
```

### `CONTRIBUTING.md`

```markdown
# Contributing to the {Quest Name} quest

Every decision affecting this quest — whether cross-repo or per-repo — should be logged in `CHANGELOG.md` here. Per-repo decisions are *duplicated* here (on top of the entry in the sub-repo's own `CHANGELOG.md`) so the quest has the full aggregated view across all participating repos.

## Changelog

Append-only, prepend latest entry on top. Each entry is a level-3 heading followed by 1–2 sentences: what changed and the decision behind it. Blank line between entries.

Heading format: `### {Author} · {Timestamp}` — e.g. `### Nils · Apr 2, 21:03 HKT, 2026`.

Quests use an **Author** field (not PromptID) because they have multiple contributors.

Body: tight — 1–2 sentences. Entries duplicated from a sub-repo's changelog can optionally link back to the sub-repo for longer context.

### Good changelog entries

**Bad — too thin:** `Updated roadmap.` No information.

**Bad — too long:** Paragraph-length recaps. Transcripts aren't decisions.

**Good:** `Moved CTRL-R integration to Phase 3 after their team confirmed their old-SDK prototype won't be ready to migrate until late Q3.`

## Quest scope

- **Cross-repo decisions** → this `CHANGELOG.md`
- **Per-repo decisions in any sub-repo** → log in the sub-repo's own `CHANGELOG.md` *and* duplicate here, so the quest is the full view
- **Personal Exocortex** → After updating the quest, you MUST also log your work in your user's personal exocortex `promptlog.md` and `changelog.md`.
- **Cross-repo open questions** → `parking_lot.md`
- **Per-repo open questions** → currently stay in the sub-repo's own `parking_lot.md` only (aggregation policy is narrower for parking lots than changelogs — raise with the quest lead if a broader view is wanted for a specific quest)

## Quest-specific conventions

{Fill in anything specific to this quest — communication cadence, review process, cross-repo branch/PR naming, etc. Remove this section if no quest-specific additions apply yet.}
```

### `README.md`

```markdown
# Quest: {Name}

{Pitch: one paragraph on what this quest is and why no single repo can own it.}

See [roadmap.md](roadmap.md) for phasing, [sprints.md](sprints.md) for what's active in each sub-repo, [CHANGELOG.md](CHANGELOG.md) for cross-repo decisions, [parking_lot.md](parking_lot.md) for open questions.

## Repos

| Repo | Role |
|------|------|
| [`aukilabs/{repo1}`](https://github.com/aukilabs/{repo1}) | {role on quest} |
| [`aukilabs/{repo2}`](https://github.com/aukilabs/{repo2}) | {role on quest} |

## Collaborators

| Person | Role on the quest |
|--------|-------------------|
| {Name} | {role} |
```

### `CHANGELOG.md`

```markdown
# Changelog — {Quest Name} Quest

Cross-repo decisions only. Per-repo decisions stay in each sub-repo's own `CHANGELOG.md`. Append-only, latest on top.

### {Author} · {Timestamp HKT, YYYY}

Quest scaffolded.
```

### `parking_lot.md`

```markdown
# Parking Lot — {Quest Name} Quest

Cross-repo open questions only. Per-repo questions stay in each sub-repo's own `parking_lot.md`.

## Open

- {cross-repo question}

## Resolved

_(Move items here with a one-line note on how they were resolved.)_
```

### `roadmap.md`

```markdown
# Roadmap — {Quest Name} Quest

Phased plan across all participating repos. Aligned with `org-auki/roadmap.md`.

## Phase 1 — {name}

- {cross-repo milestone}

## Phase 2 — {name}

- {milestone}

## Dependencies

{Repos, people, external decisions this quest depends on.}
```

### `sprints.md`

```markdown
# Sprints — {Quest Name} Quest

Links + tight summaries of each sub-repo's current sprint. Aggregation layer — per-repo detail stays in the sub-repos.

## {repo1}

{One-line summary of this week's focus.} See [`{repo1}/src/sprint.md`](https://github.com/aukilabs/{repo1}/blob/main/src/sprint.md).

## {repo2}

{One-line summary.} See [`{repo2}/src/sprint.md`](https://github.com/aukilabs/{repo2}/blob/main/src/sprint.md).
```

## Reference

See `org-auki/src/quests/README.md` for the quest-level index and `org-auki/src/projects.md` for the combined project+quest index. First quest is `fehu/` (auki + relay + hagall + hagall-common) — named after the rune to keep the quest namespace distinct from project/repo names.
