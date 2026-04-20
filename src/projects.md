Canonical list of public Auki project repos and cross-repo quests. Source of truth for what projects exist at Auki — adding a new project or quest means adding a row here first.

# Repos

## External repos (clone and symlink)

| Repo | Clone from | What it is |
|------|-----------|------------|
| [org-auki](https://github.com/aukilabs/org-auki) | `git clone https://github.com/aukilabs/org-auki.git` | Shared org brain — mission, methods, team, conventions |
| [exocortex](https://github.com/aukilabs/exocortex) | `git clone https://github.com/aukilabs/exocortex.git` | Exocortex template for onboarding new contributors |
| [auki](https://github.com/aukilabs/auki) | `git clone https://github.com/aukilabs/auki.git` | The $AUKI SDK repo |
| [relay](https://github.com/aukilabs/relay) | `git clone https://github.com/aukilabs/relay.git` | First-party Relay bundle app — joins the network and offers all four SDK networking capabilities from a single deployable |
| [cactus (frontend)](https://github.com/matterless/cactus) | `git clone https://github.com/matterless/cactus.git` | Cactus retail AI copilot — frontend |
| [cactus-backend](https://github.com/matterless/cactus-backend) | `git clone https://github.com/matterless/cactus-backend.git` | Cactus retail AI copilot — backend |
| [gotu-web](https://github.com/matterless/gotu-web) | `git clone https://github.com/matterless/gotu-web.git` | Web editor for the GoTu navigator app |



## Quests (inside the org repo)

Quests are cross-repo projects — work that spans multiple repos where no single repo can own the state. They live inside this `org-auki` repo at `src/quests/{slug}/`, so cloning `org-auki` includes every quest. Symlink a quest into your exocortex root for top-level access, the same way you would a project repo.

| Quest | Path | What it is |
|-------|------|------------|
| [fehu](quests/fehu/) | `org-auki/src/quests/fehu/` | Build the Auki network's canonical transport layer — four SDK networking capabilities + a first-party Relay bundle app |