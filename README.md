# Auki Org Context

This is the shared organizational context for Auki Labs. Every employee's exocortex symlinks to this repo as `org/`, giving their AI partner the same foundational context about the company — mission, strategy, values, methods, vocabulary, and the canonical list of projects.

One copy on disk. Everyone reads it. When leadership updates a file here, every exocortex sees the change.

## What's here

- `src/` — the org context files that get symlinked into personal exocortices. See [`src/readme.md`](src/readme.md) for the full list, including [`src/projects.md`](src/projects.md) — the canonical pointer to every Auki project repo.
- `roadmap.md` — the org-level strategic plan (all project roadmaps must align to this)
- `sprint.md` — what we're working on this week
- `changelog.md` — org-level changelog

## How to use

Symlink `src/` into your personal exocortex as `org/`:

```bash
ln -s ~/aukilabs-org/src ~/my-exocortex/org
```

Your AI partner will read `org/organization.md`, `org/methods.md`, `org/projects.md`, etc. alongside your personal files.

## Project structure

Every Auki project lives in its own GitHub repo, listed in [`src/projects.md`](src/projects.md). Projects follow the standard exocortex scaffolding (`readme.md`, `roadmap.md`, `glossary.md`, `changelog.md`, `parking_lot.md`, `src/` with `readme.md` and `sprint.md`) — see [`src/contributing.md`](src/contributing.md) § Creating a new project for the template.

The goal is to restructure the GitHub org so that every piece of work is cleanly filed under one of these canonical projects, with no orphan repos. `src/projects.md` is the source of truth for what exists and what it's for — adding a new project means adding a row there first.
