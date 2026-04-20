# Skills

Procedural skills for Auki work. Each skill is a directory with a `SKILL.md` file containing YAML frontmatter (`name`, `description`). Your AI agent auto-loads skills whose description matches the current task.

This directory is the **agent-neutral canonical library**. Discovery paths differ per agent, so each exocortex symlinks this directory into the paths its agents watch:

| Agent | Discovery path |
|-------|----------------|
| Claude Code | `.claude/skills/` (project) or `~/.claude/skills/` (user) |
| Codex | `~/.agents/skills/` (user) |
| OpenCode | `.opencode/skills/` (project) or `~/.config/opencode/skills/` (user) |
| Hermes | *(confirm per your install)* |

Wire whichever agents you use by symlinking each skill (or the whole skills directory) into that agent's path.

## Current skills

| Skill | When to use |
|-------|-------------|
| [nasa-persuasion](nasa-persuasion/SKILL.md) | Writing persuasive content — pitches, blog posts, sales copy |
| [leia-ui-review](leia-ui-review/SKILL.md) | Evaluating a UI design change |
| [story-why-how-what](story-why-how-what/SKILL.md) | Crafting a launch story, pitch, or talk opening |
| [investor-update](investor-update/SKILL.md) | Writing an investor update |
| [evaluate-meme](evaluate-meme/SKILL.md) | Scoring content for memetic fitness |
| [project-scaffold](project-scaffold/SKILL.md) | Creating a new Auki project exocortex |
| [quest-scaffold](quest-scaffold/SKILL.md) | Creating a cross-repo quest |
| [quest-sync](quest-sync/SKILL.md) | Aggregating missed changelog entries from sub-repos to a quest |
| [generate-tasks](generate-tasks/SKILL.md) | Producing a weekly task list from role, goals, and sprints |

## Personal overrides

Personal skills — or overrides of an org skill by slug — go in the user-level path for your agent (e.g. `~/.claude/skills/` for Claude Code, `~/.agents/skills/` for Codex). User-level beats project-level, so a same-slug personal skill overrides the org one.

## Contributing

Add a new skill by creating a directory with a `SKILL.md` file. The `description` field is what triggers auto-loading, so write it precisely (when to use, what it produces). Then add a row to the table above.
