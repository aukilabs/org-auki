You are in the **fehu** quest — a cross-repo project tracked at `org-auki/src/quests/fehu/`. This directory is an aggregation layer across four Auki repos: `aukilabs/auki` (SDK), `aukilabs/relay` (first-party bundle app), `aukilabs/hagall` (legacy Go Relay), `aukilabs/hagall-common` (shared protobuf).

At session start, read:

- `README.md` — what this quest is, which repos are involved, who the collaborators are
- `sprints.md` — current activity across sub-repos, with links to each one's `src/sprint.md`
- `roadmap.md` — phasing and cross-repo dependencies
- `changelog.md` — cross-repo decisions
- `parking_lot.md` — cross-repo open questions

Per-repo detail lives in the sub-repos themselves — follow the links in `sprints.md` when you need them. Broader Auki context (mission, team, methods, skills library) lives one level up in the containing `org` repo.

Log cross-repo decisions to `changelog.md` with an **Author** field (not PromptID). See `CONTRIBUTING.md` for the format. Per-repo decisions belong in the sub-repo's own `changelog.md`, not here.
