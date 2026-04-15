# Roadmap — Auki Labs

> **DRAFT — not yet reviewed by Nils.** Assembled from project roadmaps, sprints, goals, and strategy docs. Treat as a starting point for discussion, not a commitment.

## Mission

Increase the intercognitive capacity of civilization. Make the physical world browsable, searchable, and navigable to AI, robots, and humans.

## Strategy

Start with perception. Collapse deployment cost. Capture territory. Enable co-embodiment.

Phones pre-deploy environments. Glasses add passive perception. Robots add autonomous coverage. Each form factor runs the same SDK on the same Domains. Revenue scales with form factors: $500/location/month (phones) → glasses and robots add per-device revenue on top.

---

## Q2 2026 (Apr–Jun): SDK v1, robot deployment, revenue growth

### Protocol & SDK

Ship SDK v1 across all components by June. The SDK must support the full loop: init, discovery, recruitment, transport, spatial reasoning, and economic settlement.

| Milestone | Target |
|-----------|--------|
| SDK local bootstrap (`init`, `initDomain`, core types) | Mid-April |
| Discovery Service v1 — MAC lookup, transport provider recruitment | Mid-April |
| Networking — WebRTC, multi-peer clusters, `convert_pose`/`convert_time` across peers | May |
| Credit Mint + Reward Pool deployed to Base | May |
| Credit Service — settlement loop, payout, audit surface | May |
| Detectors, Extractors, credit wallet integration | June |
| Full JoinBundle, service listings, vacancy matching in Discovery | June |

See [auki/roadmap.md](../../auki/roadmap.md) for component-level detail.

### Cactus (product)

Revenue-generating product. Proves perception-first in retail.

| Milestone | Target |
|-----------|--------|
| Expand live deployments — daily attention to clients | Ongoing |
| Glasses rollout — task-generating perception while staff are on the move | Q2 |
| Robot pilot — autonomous store audit, shelf scanning, task generation off-hours | Q2 |
| Cactus messaging finalized — NASA/WHW-structured positioning | April |

### Reconstruction node

First non-perception test of the co-embodiment model. Proves third-party compute recruitment.

| Milestone | Target |
|-----------|--------|
| Legacy node keeps running | Now |
| Phase 1 — connect and be found via SDK (replaces DDS registration) | When SDK ships init + discovery + networking |
| Phase 2 — data flows through SDK transport | When SDK ships transport streams + map writes |

See [reconstruction/roadmap.md](../../reconstruction/roadmap.md) for full porting plan.

---

## Q3 2026 (Jul–Sep): scale deployments, prove co-embodiment

| Theme | What it means |
|-------|--------------|
| **Retail scale** | Cactus in hundreds of locations. Phones + glasses + robots operating in the same Domains. |
| **Reconstruction ported** | Reconstruction node running on SDK, recruitable through Discovery, paid in credits. First proof that third-party compute works. |
| **Network economics live** | Credits flowing, nodes earning, staking enforced. The real world web has a working economy. |
| **Co-embodiment** | Multiple intelligence providers sharing a robot. The mechanical substrate thesis tested in production. |

---

## 2027–2030: capture territory

The bull case from the strategy doc:

- 100,000 robots generating $100/day revenue
- 1,000,000 glasses generating $10/day revenue
- Phone copilot at $500/location/month
- These devices become infrastructure — the mechanical substrate for increasingly intelligent agents

This timeline depends on: SDK adoption beyond internal use, third-party developers building on the protocol, and the token economy creating self-sustaining incentives for network participation.

---

## Dependencies between workstreams

```
SDK v1 (protocol)
  ├── Discovery v1 → Networking → Full Discovery
  ├── Credit Mint → Credit Service → Reward Pool → Production economy
  └── Spatial + Detectors + Extractors → Cactus glasses/robots
  
Cactus (product + revenue)
  ├── Phones (live, generating revenue now)
  ├── Glasses (depends on Spatial module)
  └── Robots (depends on glasses + autonomous perception pipeline)

Reconstruction (co-embodiment proof)
  └── Depends on SDK init, discovery, networking, transport, economics (in phases)
```

---

## What this roadmap does not cover

- Specific sprint-level tasks — those live in each project's `src/sprint.md`
- Token distribution strategy or treasury management
- Hiring plan (parked until exocortex onboarding proves out)
- Specific customer contract timelines
