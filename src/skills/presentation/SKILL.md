---
name: presentation
description: Starting point for creating an internal Auki Labs presentation. Use when any team member wants to create a weekly update, work summary, or team presentation. Always internal audience — no audience question asked. Offers two formats: slides (reveal.js deck) or one-pager (scrollable HTML document). Employees always start here for internal work; use /presentation-external for investor, client, or community-facing output.
---

# /presentation

The starting point for internal Auki presentations. One question — what format — then hand off immediately. No audience question. Internal is the default and only audience for this skill.

---

## Step 1 — What do you want to create?

Ask:

> "What would you like to create?"
>
> - **Weekly update — Slides** — a deck covering your work for the week. Good for all-hands, team syncs, or sharing a visual walkthrough.
> - **Weekly update — One-pager** — a scrollable document of your work for the week. Good for written update posts and project summaries.
> - **Product deck** — a standalone product or pitch presentation, not tied to a specific week. Good for investor conversations, partner meetings, or product overviews.

Wait for the answer before doing anything else.

---

## Step 2 — Theme

Ask which brand theme to apply. Keep this to one line:

> "Which theme? **Auki** (default). [Cactus and Gotu themes redacted for public sync]"

Default to `auki` if the user doesn't specify.

---

## Step 3 — Find the work

**Skip entirely if the user chose Product deck** — route straight to Step 4. Product decks skip harvest.

**For weekly updates:** run `/harvest` silently, then present a 2–6 bullet summary of what you found and ask the user to confirm before routing.

```
/harvest --author <name> --since <YYYY-MM-DD>
```

**Fall back to a conversational prompt only if** harvest returns empty or the contributor has no Git-backed repos (sales, ops, etc.):

> "Where can I find the work this presentation covers? A GitHub repo, Linear project, Discord channel, or just tell me what you worked on."

When you have the digest, group related PRs and commits into named initiatives (drop PR numbers and hashes), then confirm:

> "Here's what I found: [2–6 bullets]. Does this look right? Anything to add or change?"

Wait for their response.

---

## Step 4 — Route to the right sub-skill

Hand off immediately. Don't ask anything else.

| Choice | Sub-skill | Pass |
|---|---|---|
| Weekly update — Slides | `/slides` | `audience = internal`, `theme`, harvest digest |
| Weekly update — One-pager | `/page` | `audience = internal`, `theme`, harvest digest |
| Product deck | `/slides` | `type = product-deck`, `theme` (no digest) |

---

## Notes

**For external presentations** (investor, client, or community), use `/presentation-external` instead. That skill handles audience selection and the redaction/framing rules that go with each external audience.

**If someone calls `/page` or `/slides` directly**, that's fine — the sub-skills work standalone.
