# Contributing to the Fehu quest

Every decision affecting this quest — whether cross-repo or per-repo — should be logged in `changelog.md` here. Per-repo decisions are *duplicated* here (on top of the entry in the sub-repo's own `changelog.md`) so the quest has the full aggregated view across all participating repos.

## Changelog

Append-only, prepend latest entry on top. Each entry is a level-3 heading followed by 1–2 sentences: what changed and the decision behind it. Blank line between entries.

Heading format: `### {Author} · {Timestamp}` — e.g. `### Nils · Apr 2, 21:03 HKT, 2026`.

Quests use an **Author** field (not PromptID) because they have multiple contributors.

Body: tight — 1–2 sentences. The changelog captures the decision, not a transcript. Entries duplicated from a sub-repo's changelog can optionally link back to the sub-repo for longer context.

### Good changelog entries

**Bad — too thin:** `Updated roadmap.` No information.

**Bad — too long:** Paragraph-length recaps. Transcripts aren't decisions.

**Good:** `Moved CTRL-R integration to Phase 3 after their team confirmed their old-SDK prototype won't be ready to migrate until late Q3.`

## Quest scope

- **Cross-repo decisions** → this `changelog.md`
- **Per-repo decisions in any sub-repo (auki, relay, hagall, hagall-common)** → log in the sub-repo's own `changelog.md` *and* duplicate here, so the quest is the full view
- **Cross-repo open questions** → `parking_lot.md`
- **Per-repo open questions** → currently stay in the sub-repo's own `parking_lot.md` only (if you want these aggregated too, raise it with the quest lead — policy is currently narrower for parking lots than changelogs)

## Quest-specific conventions

{Fill in anything specific to fehu — communication cadence across the four repos, review process, cross-repo branch/PR naming, etc. Empty for now.}
