# src/

This directory contains the public organizational context files. Each external contributor symlinks this directory into their personal exocortex as `org-auki/`.

## What's here

| File | Contents |
|------|----------|
| organization.md | Auki Labs mission, protocol (Domains, four questions), economy (credits, $AUKI, staking), products (Real World Web, Cactus), perception-first strategy with deployment examples (vineyards, retail), company values. |
| skills/ | Shared procedural skills that auto-load into Claude Code when relevant — NASA, LEIA, Why-How-What, investor update, meme fitness, project/quest scaffolding, task generation. See `skills/README.md`. |
| methods.md | Thin pointer to `skills/` (kept for compatibility with exocortices that still reference it). |
| contributing.md | Logging rules for changelogs (append-only, tight entries). |
| glossary.md | Shared vocabulary: Domain, credit, $AUKI, staking, slash, intercognitive, exocortex, and other Auki-specific terms. |
| projects.md | Canonical list of public Auki project repos with clone URLs and one-line descriptions. Source of truth for "what projects exist at Auki". |


## Project structure goal

`projects.md` is the canonical list of Auki project repos. Every project follows the standard exocortex scaffolding (see `contributing.md` § Creating a new project). The goal is to restructure the GitHub org so that every piece of work is cleanly filed under one of these projects — no orphan repos, no uncategorized work. Adding a new project means adding a row to `projects.md` first, then scaffolding the repo from the template.
