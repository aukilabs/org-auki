---
name: quest-scaffold
description: Use when creating a cross-repo quest. Everything lives in a single GitHub Project created from the Auki Kanban Template ([REDACTED - link to your organization's Kanban template]). The project README holds the demo definition, demo script, constraints, tests, and repos overview. Questions and Tasks are cards on the Kanban board. No git mirror, no Notion, no separate changelog/relay files. Minimal token footprint.
---

# Quest Scaffolding (GitHub Project Only)

A **quest** is a sprint-sized, multi-repo project working towards a clearly defined demo. The **only** coordination surface is a GitHub Project created from the Auki Kanban Template.

This is the lightest possible version — agents read the project README and the board cards directly. No local files, no Notion dumps, no extra Markdown mirrors.

## Where everything lives

- **Single GitHub Project** (created from the Auki Kanban Template #4)
  - Must have the custom `Status` single-select field with these exact options:
    - `Questions`
    - `Exploring`
    - `Tasks`
    - `In progress`
    - `In review`
    - `Done`
  - **Project README** contains:
    - Demo definition (top)
    - `## Demo script` (numbered sequential steps)
    - `## Scope`
    - `## Constraints`
    - `## Repos` (overview table)
    - `## Tests`
  - **Questions** = cards with Status = "Questions"
  - **Tasks** = cards using the other Status values
  - All other state lives in card fields (`Repo`, `Owner`, etc.)

No `CHANGELOG.md`, no `relay_log.md`, no `AGENTS.md`, no `org/src/quests/{slug}/` folder.

## Step 1 — Define the demo

Ask the user for the demo definition. This becomes the first paragraph in the **project README**.

## Step 2 — Create the GitHub Project

The agent should create the project using the `copyProjectV2` GraphQL mutation (this preserves the custom `Status` field from the template).

**Template project ID**: `[REDACTED - insert your organization's Kanban template project ID]` (Auki Kanban template at [REDACTED - link to your organization's Kanban template])

**Mutation example** (run via `gh api graphql`):

```graphql
mutation {
  copyProjectV2(input: {
    projectId: "[REDACTED - insert your organization's Kanban template project ID]",
    ownerId: "[REDACTED - insert your organization's owner ID]",   # aukilabs organization global ID
    title: "Quest: {Quest Name}"
  }) {
    projectV2 {
      id
      number
      url
    }
  }
}
```

After creation, immediately set:
- `shortDescription` via `updateProjectV2`
- `readme` via `updateProjectV2` (containing the full demo definition + `## Demo script`, Scope, Constraints, Repos, and Tests)

**Note**: Using plain `gh project create` produces a blank project missing the custom Status column and should be avoided.

## Step 3 — Add initial cards

- Create one card per participating repo in the `## Repos` section of the README (or as repo cards).
- Seed any known high-level constraints and tests into the README.
- Leave **Questions** and **Tasks** empty until agents start surfacing them as cards.

## Step 4 — Spawn agents

Use the spawn helper:

```bash
bash scripts/spawn-quest.sh {slug} {repo1} {repo2} ...
```

Kickoff prompt for each agent:

> You are {repo} claude for the {quest-name} quest. The quest lives entirely in this GitHub Project: {project-url}. Read the project README, locate your repo, report current status by updating the Repos overview, and surface questions by creating new cards in the Questions / Parking Lot area. Do not pre-resolve questions.

Agents use the GitHub web UI or `gh` CLI to read the README and manage cards.

## Step 5 — Human answers questions

When the human answers a question card, they convert it into a Task card (change status / move to Tasks column, or create a linked task card). The original question card can be closed or moved to "Answered".

## Step 6 — Orchestrator

The existing `relay-merge.sh` + webhook setup still works. On merge events, the orchestrator sends `[orchestrator]` messages to the tmux sessions. Agents react by checking the project board for newly unblocked cards.

Receipts can be left as comments on the relevant cards or in the project activity log (no separate `relay_log.md` needed).

## Card conventions

- **Question cards**: Use a consistent label (e.g. `question`) or a dedicated column. Include `Repo`, short description, and any recommendation in the card body.
- **Task cards**: Use Status columns. Include originating question (if any), dependencies, and `Repo` in the card.
- **Tests**: Live in the project README (under `## Tests`). They are only binding once the human approves them.

## Why this version?

- Lowest possible token usage (agents only read the project README + card lists)
- Single source of truth
- Visual Kanban + structured cards
- No maintenance of parallel git mirrors or Notion pages

## Implementation Notes (from real usage)

- Always create the project using the `copyProjectV2` GraphQL mutation (or instruct the agent to do so). This preserves the custom `Status` field from the template.
- The template project ID is `[REDACTED - insert your organization's Kanban template project ID]`.
- After creation, the README and shortDescription must be set via the `updateProjectV2` mutation.
- The custom Status field options (`Questions`, `Exploring`, `Tasks`, `In progress`, `In review`, `Done`) are critical for the workflow.
- Never use plain `gh project create` — it produces a project without the required Status column.
- Only create Question cards for things that are genuinely unresolved. Most items in an implementation plan are already answered and should become Task cards instead.
- Use `addProjectV2DraftIssue` for rapid population of the board.
- Always set the Status field explicitly when creating cards so they land in the correct column.

## References

- `scripts/spawn-quest.sh` — spawn helper (no Notion dependency)
- `scripts/relay-merge.sh` — orchestrator relay (unchanged)
- `templates/repo-agents-md-snippet.md` — Quest Mode instructions to paste into each repo's AGENTS.md / CLAUDE.md (updated version that points to the project URL instead of a local folder)