# Roadmap — Fehu Quest

Where the cross-repo work is headed. Sequenced by dependency — each phase depends on previous phases landing across all involved repos.

## Now

- **SDK TS bootstrap** landing in `aukilabs/auki`: `AukiSdk` class + `sdk.init()` ([PR #44](https://github.com/aukilabs/auki/pull/44)).
- **Go rosrelay bounty work** awaiting merge: `aukilabs/hagall` [PR #63](https://github.com/aukilabs/hagall/pull/63) + `aukilabs/hagall-common` [PR #22](https://github.com/aukilabs/hagall-common/pull/22).
- **Project docs** landing in `aukilabs/auki` ([PR #43](https://github.com/aukilabs/auki/pull/43)): projectrosrelay.md, projectrosrelay_demo.md, projectrosrelay_parking_lot.md.
- **Relay app repo scaffolded** at [aukilabs/relay](https://github.com/aukilabs/relay) — README, parking lot, roadmap, src/ placeholders. No code yet.

## Phase 1 — SDK prerequisites + first capability

SDK team lands: `sdk.initDomain()`, `manager` (admission + signed tokens), `cluster-registry` (capability ads + reachability), `networking` (outbound-WS transport + message handler registration). Relay app in `aukilabs/relay` implements `networking:message-forwarding` on top. Achieves parity with the Go rosrelay's six test cases ([hagall#63](https://github.com/aukilabs/hagall/pull/63)).

**Exit:** a TS Relay node joins a cluster, advertises `networking:message-forwarding`, and carries messages between two recruited peers. Six parity tests pass.

## Phase 2 — Relay app, containerized

Docker image published. Operator runs one container, joins the network as a general infrastructure provider. Supports `networking:message-forwarding` initially, with env-var-controlled capability advertisement (so operators can disable what they don't want to offer).

**Exit:** published container image. One operator runs it in production and earns credits.

## Phase 3 — CTRL-R demo + live RGB via `sfu`

Add `networking:sfu` to both the SDK and the Relay. CTRL-R demo works end-to-end: the user pays, drives a robot, watches it move in the Domain Viewer, and sees live camera feed. First real third-party SDK consumer.

**Exit:** CTRL-R demo recorded + published. At least one live teleop session.

## Phase 4 — Recorded RGB via `bulk-data-channel`

Add `networking:bulk-data-channel` to both SDK and Relay. Teleop sessions can upload recorded RGB for review, audit, training-data collection.

**Exit:** CTRL-R can store recordings from a teleop session in the Auki network and retrieve them later.

## Phase 5+ — Production concerns

- Prometheus metrics endpoint with per-capability counters.
- Capability-level capacity advertisement (graceful degradation when one capability is overloaded).
- Helm chart for K8s operators.
- Multi-region deployment pattern.
- Specialist operators competing with the bundle on specific capabilities (the bundle is the starter pack, not the only shape).
