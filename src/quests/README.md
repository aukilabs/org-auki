# Quests

A **quest** is a cross-repo project. It spans more than one repo and no single repo can own the state.

Quests live under `org-auki/src/quests/{slug}/` so every project lead has visibility, not just whoever is driving each leg.

Use a quest when a single project doesn't fit cleanly in one repo. Otherwise prefer the standard project structure in the owning repo.

## Folder convention

```
quests/{slug}/
  README.md          ← Landing page (identity file). Pitch, repos involved, collaborators.
  AGENTS.md          ← Entry point for an AI agent loaded into this quest.
  CONTRIBUTING.md    ← Logging conventions for this quest.
  roadmap.md         ← Phased plan across all repos — milestones, dependencies.
  sprints.md         ← Links + tight summaries of each sub-repo's current sprint.
  changelog.md       ← Full aggregated decision log — cross-repo decisions + duplicates of per-repo decisions from each sub-repo. Append-only, latest on top.
  parking_lot.md     ← Cross-repo open questions (per-repo opens stay in the sub-repo for now).
```

The quest is an **aggregation layer**. Per-repo code and implementation detail stay in the sub-repos, but decisions are duplicated here so the quest changelog is the full view — you can stand in the quest dir and see everything that happened across all participating repos. Sprints.md summarizes per-repo sprint content with links back.

## Current quests


