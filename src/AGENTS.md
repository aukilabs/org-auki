You are in the `org-auki` shared organizational context for Auki Labs. This directory (`src/`) is what every external contributor's personal exocortex symlinks in as `org-auki/`.

At session start, read:

- `organization.md` — mission, strategy, products, values
- `projects.md` — canonical list of Auki project repos and cross-repo quests
- `contributing.md` — logging conventions (referenced by every exocortex as `@org-auki/contributing.md`)
- `quests/README.md` — active cross-repo quests
- `skills/README.md` — shared procedural skills library (auto-loaded by your agent when a skill's description matches the task)

If you're loaded here via an exocortex symlink (the common case), the user-level `AGENTS.md` already knows to read these files at the right moments — this file exists as a fallback entry point for agents opened directly in the org repo (e.g. maintaining mission docs without a personal exocortex).

Log changes to `../changelog.md` (at the repo root) with an **Author** field (not PromptID) — this repo has multiple contributors.
