# Quest: Fehu

This quest is building towards a world where CTRL-R, a third-party developer, can be the first project using the new [Auki SDK](https://github.com/aukilabs/auki).

The target shape:

- CTRL-R WEB should be able to connect to a domain and fetch its map.
- CTRL-R ROBOT should be able to connect to a domain and fetch its map.
- WEB and ROBOT should be able to speak to each other through a RELAY.
- RELAY should be recruitable into the domain cluster.
- DOMAIN VIEWER should be able to connect to a domain and fetch its map.
- DOMAIN VIEWER should be able to render the ROBOT's pose in real time.
- WEB should be able to pull product locations from CACTUS.

### Cast

- **CTRL-R WEB** — A browser client using the Auki SDK where users pay to teleoperate robots. They can pilot the robots manually, as well as send them to points of interest (fetched from CACTUS). The user can see the robot's camera stream.
- **CTRL-R ROBOT** — The robot's application with the Auki SDK. The robot can fetch the domain map, write its poselog, and stream its video over the Auki network — or log its camera stream through the SDK and bulk-send afterwards.
- **RELAY** — An app that community members can run on a machine to get paid for relaying data between Auki nodes.
- **DOMAIN VIEWER** — An open-source first-party app for rendering the domain and the robots inside it.
- **CACTUS** — A first-party AI copilot for retailers that is assumed to already be using the domain that CTRL-R ROBOT is visiting.

Build the Auki network's canonical transport layer — four recruitable networking capabilities (`networking:message-forwarding`, `networking:bulk-data-channel`, `networking:turn`, `networking:sfu`) and a first-party deployable app that bundles them as a single container.

This is the first concrete use case of the new Auki SDK. Success here turns the capability-composition model from a spec into a thing you can deploy. The first real demo lands on top: CTRL-R's pay-to-teleoperate platform (third-party), with a first-party open-source Domain Viewer rendering robot poses live in the browser.

See [roadmap.md](roadmap.md) for phasing, [sprints.md](sprints.md) for what's active in each sub-repo, [changelog.md](changelog.md) for the full aggregated decision log across all four repos, [parking_lot.md](parking_lot.md) for the open questions no single repo can answer alone.

## Repos

### Active

| Repo | Role |
| ---- | ---- |
| [`aukilabs/auki`](https://github.com/aukilabs/auki) | SDK definitions + reference implementations. Defines the four networking capability interfaces. First real `.ts` landing via [PR #44](https://github.com/aukilabs/auki/pull/44). |
| [`aukilabs/relay`](https://github.com/aukilabs/relay) | First-party Relay bundle app. Implements all four capabilities as a single deployable. Scaffolded Apr 18, 2026; no implementation yet. |
| [`aukilabs/hagall`](https://github.com/aukilabs/hagall) | Legacy Go Relay server (in production). Ships the ROS2 topic relay bounty via [PR #63](https://github.com/aukilabs/hagall/pull/63). Keeps serving its legacy modules indefinitely; the SDK-native Relay is its spiritual successor, not a forced replacement. |
| [`aukilabs/hagall-common`](https://github.com/aukilabs/hagall-common) | Shared protobuf / utilities for hagall. ROS relay protobuf defs landed via [PR #22](https://github.com/aukilabs/hagall-common/pull/22). |
| [`aukilabs/broodsugar`](https://github.com/aukilabs/broodsugar) | Nils's personal exocortex. Where early-phase design thinking lives before it's promoted to public repos. Listed for traceability. |


### Upcoming

| Repo | Role |
| ---- | ---- |
| `aukilabs/domain-viewer` | First-party open-source browser app — renders domain maps + live robot poses. Part of the CTRL-R demo's five-node cast. Not yet scaffolded. |


### External (not in the org)

| Repo | Role |
| ---- | ---- |
| CTRL-R | Third-party pay-to-teleoperate application. Prototype exists on the old SDK. First real SDK consumer once this quest lands. Integration direction TBD — see [parking_lot.md](parking_lot.md). |


## Collaborators

| Person | Role on the quest |
| ------ | ----------------- |
| **Nils** | Quest driver. Scope, direction, cross-repo coordination. |
| **Matthieu** | SDK networking capability specs (`message-forwarding`, `bulk-data-channel`, `turn`, `sfu`). Owns the recruitment mechanic (Vacancy / ServiceListing / Booking). |
| **Arshak** | DevRel. Paired with Nils on the `sdk.init()` bootstrap. Developer-facing surface of the Relay app. |
| **Shuning** | SDK architect. Cross-capability API shape, composition ergonomics. |
| **Phil** | Robotics. Robot-side integration for the CTRL-R demo — how the robot joins a cluster, how ROS topics bridge into SDK data products. |
| **Robin** | Spatial Intelligence. `spatial` + `map` capability specs. Not directly built in this quest, but the demo depends on `map (reader)` being available to multiple nodes. |
| **CTRL-R team** | Third-party app developer. Direction on their integration is a [parking_lot.md](parking_lot.md) item. |
