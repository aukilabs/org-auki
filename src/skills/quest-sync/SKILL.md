---
name: quest-sync
description: Use when syncing or aggregating changelog decisions from sub-repos up to a quest's main changelog. Use this on a cron schedule to ensure no human-written sub-repo decisions are missed in the quest's aggregated view.
---

# Quest Sync

Quests are aggregation layers. While AI agents are instructed to dual-write decisions to both the sub-repo and the quest, human contributors sometimes forget. This skill syncs those missed entries.

## Procedure

1. **Identify Scope:** Read the quest's `sprints.md` or `README.md` to identify the participating sub-repos.
2. **Scan Sub-Repos:** For each sub-repo, read its `CHANGELOG.md`. Look at entries from the last few days.
3. **Diff:** Compare the recent sub-repo entries against the quest's `CHANGELOG.md` (`org-auki/src/quests/{slug}/CHANGELOG.md`).
4. **Aggregate:** If any entries in the sub-repos are missing from the quest changelog, append them to the top of the quest changelog (maintaining reverse-chronological order). 
5. **Contextualize:** When importing an entry, prepend the sub-repo name in brackets to the body text (e.g., `[hagall] Moved CTRL-R integration...`) so the quest log remains clear about where the work happened.