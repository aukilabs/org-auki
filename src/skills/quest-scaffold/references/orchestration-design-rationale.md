# Design Rationale — Orchestration Defaults

Why the orchestration defaults in `SKILL.md` are what they are. If a future
session is tempted to change one, read this first.

## Why "the orchestrator" is a role, not a tool

Anyone can be the orchestrator: a Hermes instance, a teammate driving tmux by
hand, a tiny webhook glue script on someone's laptop. The skill describes the
*role* — fan merge events out to all quest agents, keep prefix discipline,
maintain the audit trail. Whoever owns the role for a given quest writes the
webhook glue once and forgets about it.

## Shape 1 vs 2 vs 3 (where do the agents live?)

| | Shape 1: tmux + Claude Code CLI | Shape 2: separate Hermes profiles per repo | Shape 3: Cursor + parallel headless agents |
|---|---|---|---|
| Orchestrator can talk to agents | Yes, `tmux send-keys` | Yes, message their channel | Yes, `claude --print` to a worktree |
| Human can talk to same agent | Yes, `tmux attach` | Yes, same channel | Cursor pane is human-only, headless is orch-only |
| Shared conversation history | Yes (tmux scrollback) | Yes (channel log) | No (two parallel agents) |
| Cursor IDE niceties (inline diff, hover-edit) | Lost | Lost | Kept |
| Setup overhead | Low | High (profile per repo) | Medium |
| Best for | Sprint-scale ≤1 week | Long-running, agent needs durable memory | Quests where review UX matters more than orchestration |

**Default: Shape 1 for ≤1-week quests.** Shape 2 if memory across days matters.
Shape 3 if the human strongly prefers Cursor's review surface.

## Notify-all vs dependency map

At N=3 repos, the cost of "skipped: not relevant" Status-log lines is much
lower than the cost of maintaining a static dependency map or enforcing per-PR
`Unblocks:` declarations.

Crossover point is roughly N=5. Above that, noise dominates and you want one of:

- **Static dependency block in the Notion page** under a `## Dependencies` h2:
  ```
  repo-a depends on: repo-b, repo-c
  repo-b depends on: repo-c
  repo-c depends on: (none)
  ```
- **Per-PR `Unblocks: <list>`** parsed from PR body. Self-maintaining but
  trusts the author.
- **Hybrid: union of static spine + PR-declared overrides.** Most accurate,
  most code.

Keep the `Unblocks:` line in PR bodies even in notify-all mode — it's for the
human reading the PR, not the orchestrator.

## Audit trail — Notion Status log is canonical

Earlier versions of this skill used a per-repo `.quest/relay-log.md` file
committed in the sub-repo. With the Notion-first redesign, the canonical
audit trail is the `Status log` section on the Notion quest page — agents
append entries there with `<repo> claude — ` prefixes, and `Ctrl+F` finds
both the inbound relay and the agent's planned-vs-actual response without
hopping repos.

The `.quest/relay-log.md` per-repo file is optional and lives only inside the
git mirror (Step 4 of SKILL.md) when that mirror exists.

## Echo-back is non-negotiable

Without forcing the agent to echo the verbatim message:
- Agent could silently misread the message and act on a corrupted version.
- The audit trail captures intent (what orch sent) and outcome (what agent did)
  but not the agent's *understanding* — the place where errors creep in.

The echo costs one line of response. Cheap insurance.

## Interrupt-style vs queue-style delivery

| | Interrupt: `tmux send-keys` immediately | Queue: write to inbox file, agent polls |
|---|---|---|
| Reaction latency | Instant | Until next agent checkpoint |
| Mid-thought disruption | Possible | Never |
| Works on idle/finished panes | Best — interrupts the input box | Only triggers if agent runs |

**Default: interrupt-style.** Sprint scale rewards responsiveness. If we see
agents derailing mid-task, switch.

**Important caveat:** `tmux send-keys` to a session sitting on a Claude Code
permission prompt ("Allow this tool? [y/N]") will deliver the relay text as
the prompt answer. Before sending, run
`tmux capture-pane -t <session> -p | tail -5` if the session may be in a
modal state.

## Why notify the merging agent too

It's tempting to skip self-notification. Don't:

- Post-merge follow-up work is often only obvious from the merged state ("now
  I should update README", "now I can close the tracking issue", "CI on main
  passed, time to tag").
- Symmetric flow is simpler to reason about.
- The Status-log entry on the merging agent gives a complete record on that
  side too.

## Why merge-only, not PR-open

PR-open notifications give downstream agents a chance to preview the API and
start prep work. They also create noise on PRs that change substantially
before merge (downstream did wasted prep). For sprint scale with mostly small
PRs, merge-only wins. Revisit if agents complain about being under-informed.

## Cursor / Claude Code extension specifics

People typically run Claude Code as a Cursor extension. Shape 1 means
convincing them to switch to the CLI-in-tmux flavor for the quest duration.
Tradeoffs:

- They lose Cursor's inline diff and hover-edit.
- They gain a shared session that the orchestrator can drive.
- For a 1-week sprint this is usually worth it. For long-term work, Shape 3
  (keep Cursor, run parallel headless agents) may win even with the
  duplication cost.

## Verifying a branch claim

Frequent pitfall: user (or another agent) says "I pushed feature/X to repo Y"
but the branch is local-only. Before assuming the branch exists for the
orchestrator to read:

```bash
gh api repos/<owner>/<repo>/branches --paginate -q '.[].name' | grep -F "<branch>"
```

Or just `git fetch --all` on the local clone and `git branch -r`. Don't take
"I pushed it" at face value — confirm with the remote.

## Default branch is not always `main`

`aukilabs/org` uses `develop`. Several SDK repos do too. Always check with:

```bash
gh repo view <owner>/<repo> --json defaultBranchRef -q .defaultBranchRef.name
```

before naming the webhook trigger branch or before diffing against `main`.
