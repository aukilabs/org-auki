---
name: generate-tasks
description: Use when the user asks for tasks, a weekly plan, or "what should I work on." Combines user.md, user_role.md, goals.md, and every linked project's sprint.md into a role-filtered task list written to tasks.md.
---

# Generate tasks

Combine four inputs to produce a weekly task list.

## Inputs

1. **`user.md`** — what this person can do (skills, background).
2. **`user_role.md`** — what this person should do (responsibilities, routines).
3. **`goals.md`** — personal habits, routines, responsibilities, non-project goals.
4. **All `sprint.md` files** in linked projects — what needs doing.

## Procedure

1. Scan `goals.md` and every `sprint.md` in linked projects.
2. Filter through the person's role. Only surface work that matches their responsibilities.
3. Group by responsibility.
4. Write the result to `tasks.md`.

A developer gets code tasks. A manager gets alignment and review tasks. Same sprints, different output.

## Relevance check

For each task, evaluate:

- Is it in alignment with the current attention (`attention.md`)?
- Does the attention map to a stated goal?
- Does the goal align with the organization's mission and the person's role?

Push back on anything that doesn't.
