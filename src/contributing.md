# Contributing

Every change to any document in this repo should be logged in changelog.md.
If we are editing a file in a loaded repo, make sure to respect the changelog conventions of that repo. Project-level repos use an **Author** field in their changelogs, since they have multiple contributors.

---

## Changelog

Append-only, prepend latest entry on top. Each entry is a level-3 heading followed by 1–2 sentences: what changed and the decision behind it. Blank line between entries.

Heading format: `### {Author} · {Timestamp}` — e.g. `### Nils · Apr 2, 21:03 HKT, 2026`.
Body: tight — 1–2 sentences. The changelog captures the decision, not a transcript.

Shared repos use the Author field because multiple people contribute.

### Good changelog entries

Each change should produce a changelog entry. Write the decision in 1–2 tight sentences — not a transcript.

Don't write "Updated contributing.md." as the whole entry. Don't write an essay either. If your entry is longer than the Good example below, it's too long — the urge to write paragraphs is a signal that you're trying to capture the conversation instead of the decision.

**Bad — too thin:** `Fixed typo.` No information.

**Bad — too long:** Paragraph-length recaps of everything discussed, every option weighed, every file touched. The changelog is not a transcript.

**Good:** `Studied MemPalace retrieval system. Decided our exocortex doesn't need vector search yet — structured files solve 70% of the retrieval problem at zero infrastructure cost.`

## Creating a new project

See the [`project-scaffold`](skills/project-scaffold/SKILL.md) skill. For cross-repo work see [`quest-scaffold`](skills/quest-scaffold/SKILL.md).
