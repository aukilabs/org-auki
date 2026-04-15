# Contributing

Every change to any document in this repo should be logged in `changelog.md`.

If you are editing a file in another loaded repo, follow that repo’s changelog conventions. This org repo uses an **Author** field on each entry because multiple people contribute.

---

## Changelog

Append-only, prepend latest entry on top. Each entry is a level-3 heading followed by 1–2 sentences: what changed and the decision behind it. Blank line between entries.

Heading format: `### {Author} · {Timestamp}` — e.g. `### Nils · Apr 2, 21:03 HKT, 2026`.
Body: tight — 1–2 sentences. The changelog captures the decision, not a transcript.

### What makes a good changelog entry

Substantive edits should have a changelog entry. Write the decision in 1–2 tight sentences — not a transcript.

Don’t write a one-line stub with no information. Don’t write an essay either. If your entry is longer than the Good example below, it’s too long — the urge to write paragraphs is a signal that you’re trying to capture the conversation instead of the decision.

**Bad — too thin:** `Tweaked contributing.md.` No information.

**Bad — too long:** Paragraph-length recaps of everything discussed, every option weighed, every file touched. The changelog is not a transcript.

**Good:** `Studied MemPalace retrieval system. Decided our exocortex doesn’t need vector search yet — structured files solve 70% of the retrieval problem at zero infrastructure cost.`

## Creating a new project

A project exocortex isn't a special folder — it's emergent from the structure of the project itself. When starting a new project, create these files at the repo root:

| File | What to write | Who maintains it |
|------|--------------|-----------------|
| readme.md | The aspirational description: what is this project, why does it exist, who works on it. This is the dream. | Project lead |
| roadmap.md | Where the project is headed. At least 3 months, at most 3 years. Must align with org roadmap. | Project lead |
| glossary.md | Project-specific vocabulary — terms someone new wouldn't know. | Anyone on the project |
| changelog.md | Project-level changelog with Author field. Append-only, latest on top. | Anyone on the project |
| parking_lot.md | Open questions that need human input before work can proceed. | Anyone on the project |
| src/ | The actual code. | Contributors |
| src/readme.md | AI-generated description of what the code does today. No fluff. Claude maintains this. | Claude |
| src/sprint.md | Current work and next steps. At most a week of work. | Project lead (updated weekly) |

Each contributor symlinks the project into their personal exocortex:
```bash
ln -s ~/project-repo ~/my-exocortex/projects/project-name
```
