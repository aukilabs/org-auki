# Sprints — Fehu Quest

Active sprint state across each sub-repo. Link to the actual sprint.md for details; tight summary here.

Refresh weekly, or whenever a sub-repo's sprint changes materially.

## `aukilabs/auki` — SDK sprints

- **[sdk/src/sprint.md](https://github.com/aukilabs/auki/blob/develop/sdk/src/sprint.md)** — `AukiSdk` class + `init()` landed ([PR #44](https://github.com/aukilabs/auki/pull/44)). Next: `sdk.initDomain()`, capability composition hook decision.
- **[sdk/Capabilities/spatial/src/sprint.md](https://github.com/aukilabs/auki/blob/develop/sdk/Capabilities/spatial/src/sprint.md)** — local spatial/time bootstrap, TimeTransforms, Pose Log. Sprint-planned, no code yet.
- **[sdk/Capabilities/manager/src/sprint.md](https://github.com/aukilabs/auki/blob/develop/sdk/Capabilities/manager/src/sprint.md)** — local domain bootstrap + cluster registry seed. Sprint-planned, no code yet.
- **[sdk/Capabilities/cluster-registry/src/sprint.md](https://github.com/aukilabs/auki/blob/develop/sdk/Capabilities/cluster-registry/src/sprint.md)** — cluster-of-one shape + registry store. Sprint-planned, no code yet.
- **[sdk/Capabilities/networking/src/sprint.md](https://github.com/aukilabs/auki/blob/develop/sdk/Capabilities/networking/src/sprint.md)** — transport capabilities, `ProviderAdvertisement` / `ManagerEndpoint` / `TransportProfile` schemas. Sprint-planned, no code yet. Currently WebRTC-first; the quest may push for outbound-WS earlier.
- **[sdk/Capabilities/map/src/sprint.md](https://github.com/aukilabs/auki/blob/develop/sdk/Capabilities/map/src/sprint.md)** — empty canonical map bootstrap, primitive read/insert API. Sprint-planned, no code yet.

## `aukilabs/relay` — Relay app sprint

- **[src/sprint.md](https://github.com/aukilabs/relay/blob/main/src/sprint.md)** — repo scaffolded; waiting on SDK prerequisites. First capability target: `networking:message-forwarding`. Parity target: the six test cases from the Go rosrelay ([hagall#63](https://github.com/aukilabs/hagall/pull/63)).

## `aukilabs/hagall` — Go rosrelay bounty

No formal sprint.md file in this repo. Work tracked via [PR #63](https://github.com/aukilabs/hagall/pull/63) (module + tests) and [hagall-common #22](https://github.com/aukilabs/hagall-common/pull/22) (protobuf defs). Both open, CI green. Awaiting review.
