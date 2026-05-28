---
name: harvest
description: Sub-skill called by /presentation and /presentation-external (the router skills). Auto-populates presentation context from a contributor's work in the current ISO week — reads CHANGELOG entries, merged PRs, closed issues, and skill diffs since the most recent past Friday. Returns a structured digest that the router passes down to /slides or /page. Reduces user-prompting burden by pre-filling "what shipped, what's in progress, what's next".
---

# /harvest

Pre-fills presentation content from a contributor's work in the current ISO week so the router skills (`/presentation`, `/presentation-external`) can pass a ready digest down to `/slides` or `/page`.

This is a **sub-skill** — it is not invoked directly by users. The router skills call it during their harvest step, then pass the result when handing off to the sub-skill.

---

## When to use

Call this skill when a presentation-family skill needs to enumerate a contributor's recent work and the contributor has at least one Git-backed source. Skip it for sales / ops / non-repo contributors — fall back to the calling skill's conversational prompts.

---

## Inputs

| Param | Default | Notes |
|---|---|---|
| `author` | required | GitHub handle or full name. Maps to commit author / PR author. |
| `repos` | auto-discover | List of repo slugs to scan. If omitted, discover from the contributor's exocortex `projects.md`. |
| `since` | most-recent-past-Friday | YYYY-MM-DD. Use `scripts/week-scope.sh` to compute. |
| `until` | today | YYYY-MM-DD. |
| `include_skill_diffs` | true | Surface skill changes separately from regular PRs. |

---

## Step 1 — Resolve the time window

```bash
eval "$(scripts/week-scope.sh)"
# Now: $HARVEST_WEEK, $HARVEST_WEEK_LABEL, $HARVEST_SINCE, $HARVEST_UNTIL
```

If the user specified a custom range, pass `--since` and/or `--week` to the script.

---

## Step 2 — Discover repos (if not provided)

If `repos` is not given, look in `~/agents/<contributor>/projects.md` (or the symlinked `org/projects.md` if no personal projects file) and extract repo slugs from the canonical projects table.

---

## Step 3 — Harvest per repo

The contributor's **personal exocortex CHANGELOG** (`~/agents/<name>/CHANGELOG.md`) is the authoritative source. It records only work the contributor personally did, in their own words, with their own justifications. Read it first.

**Do not use merged PRs as the primary source.** A contributor may merge PRs they didn't author (e.g. scaffolding quests for others, landing team members' work). Merged-by ≠ authored-by.

For each repo in scope, collect:

1. **Exocortex CHANGELOG entries** since `$HARVEST_SINCE` — rows where Author matches the contributor. This is the primary signal.
2. **Merged PRs** where the contributor is explicitly the PR *author* (not just the merger) — use only to catch anything the CHANGELOG missed.
   ```bash
   gh pr list --repo <slug> --state merged --author <author> \
     --search "merged:>=$HARVEST_SINCE" \
     --json number,title,mergedAt,url,body
   ```
   Cross-reference against the CHANGELOG: if a PR already has a CHANGELOG entry, don't list it twice. If a PR has no CHANGELOG entry, include it only if the PR body confirms it's the contributor's own work.
3. **Skill diffs** — commits touching `src/skills/**` in the org repo, attributed to the contributor. These get a separate section because skill changes are often the most leveraged work of the week.

---

## Step 4 — Return a structured digest

Return the following shape (JSON-ish; the calling skill decides format):

```yaml
window:
  week: 20
  since: 2026-05-09
  until: 2026-05-12
author: alice
repos_scanned: [aukilabs/org, aukilabs/posemesh-sdk-rs]

shipped:
  - title: "Quest-scaffold skill: Constraints + Tests sections, brief Status log"
    repo: aukilabs/org
    pr: 35

  - title: "..."
    ...

in_progress:
  - title: "Pulse → org skill migration"
    pr: 42
    repo: aukilabs/org
    state: open

skill_changes:
  - skill: quest-scaffold
    pr: 35
    subject: "Constraints + Tests sections, brief Status log"
```

---

## Pitfalls

- **GitHub 504s.** `gh` occasionally returns transient 5xx, especially on broad `--search` queries. Retry up to 3 times with exponential backoff (2s, 4s, 8s) before failing.
- **CHANGELOG format drift.** Not every Auki repo uses the same table schema. If the personal exocortex CHANGELOG can't be parsed, flag it — don't silently fall back to PRs, which may include work the contributor didn't do.
- **Author identity.** GitHub handle vs. full name vs. exocortex slug. Take a list and try each; the first that returns rows wins.
- **Skill diffs in non-org repos.** Some contributors keep skills in their personal exocortex (`~/agents/<name>/skills/`). If the contributor's projects.md lists a personal repo, include it in the scan.
- **Time-zone fuzziness.** `gh` returns merge dates in UTC. The contributor probably thinks in their local week. Use UTC for matching, render local in the calling skill's output.

---

## Files in this skill

- `SKILL.md` (this file)
- `scripts/week-scope.sh` — resolves ISO week + since/until cutoffs

