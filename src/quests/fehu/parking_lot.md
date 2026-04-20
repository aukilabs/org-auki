# Parking Lot — Fehu Quest

Cross-repo open questions. Per-repo opens stay in that repo's own parking lot — this file is the index plus any question that spans multiple repos.

---

## README: does the old "canonical transport layer" paragraph still earn its place?

After the Apr 18 README rewrite, the new narrative (CTRL-R + cast of characters) and the pre-existing paragraph ("Build the Auki network's canonical transport layer — four recruitable networking capabilities…") cover overlapping ground. Options: (a) delete the old paragraph, (b) keep it as a one-line tagline, (c) keep both. Doc-hygiene decision, not a blocker.

**Resolvers:** Nils.

---

## Direct invitation of a known capability provider

When an operator already knows which provider they want (e.g. "this specific relay at 1.2.3.4"), is that a filtered Vacancy, or does the SDK need a separate direct-invitation primitive? Generalizes beyond the relay case to every capability (TURN, signaling, gateways, storage, compute).

Full context: [aukilabs/auki: parking_lot.md](https://github.com/aukilabs/auki/blob/develop/parking_lot.md) item #2.

**Resolvers:** Matthieu, Shuning.

---

## Admission token format

The Manager signs admission tokens; the Relay verifies them. Exact schema and interaction with Booking + credit-service pricing is TBD. Blocks the Relay's first-capability implementation.

Full context: [aukilabs/auki: projectrosrelay_parking_lot.md](https://github.com/aukilabs/auki/blob/develop/projectrosrelay_parking_lot.md).

**Resolvers:** Matthieu.

---

## CTRL-R integration direction

Who writes the robot-side SDK daemon for CTRL-R — us, their team, or do we ship the SDK and let them integrate? How does video transport work in their existing prototype? What's the acceptable end-to-end teleop latency?

Full context: [aukilabs/auki: projectrosrelay_demo.md](https://github.com/aukilabs/auki/blob/develop/projectrosrelay_demo.md) (the ranked Phil-questions at the bottom).

**Resolvers:** Phil + CTRL-R team + Nils.

---

## Canonical container form factor for the Relay app

Single Docker image vs Compose vs Helm. How the bundle handles partial enablement (operator only wants to offer `turn`). First-instinct answer is "one Docker image with env-var capability toggles" but needs operator feedback.

Full context: [aukilabs/relay: parking_lot.md](https://github.com/aukilabs/relay/blob/main/parking_lot.md).

**Resolvers:** ops-minded operator feedback.

## Resolved

- **Three of four network primitives have no sprint coverage**: Resolved by Nils (Apr 18) - Minimum scope for Phil's demo is `message-forwarding` (to fix dropped connections). Perfect demo requires video streaming (`sfu` or `turn`) and offline RGB upload to domain map node (`bulk-data-channel`). We will build one at a time, but target all four in 2 weeks. The SDK must support networking first so Relay can consume it.
