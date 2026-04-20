# Changelog — Fehu Quest

Append-only. Latest entry on top. Aggregates significant decisions from sub-repo changelogs that shape the cross-repo picture. Per-repo minutiae stay in that repo's own changelog.

Format: `### Nils [relay] · Apr 18, 2026

Resolved scope sequencing for Relay capabilities: we will build one capability at a time sequentially, but target completing all four within a tight 2-week window.

### {Author} · {Timestamp}` followed by a short prose body combining what changed and why.

### Nils [auki] · Apr 18, 2026

`sdk/Capabilities/networking`: Prioritized `message-forwarding` implementation to unblock the `fehu` quest and Relay app, targeting all four networking primitives within 2 weeks.

### Nils [relay] · Apr 18, 2026

Resolved scope sequencing for Relay capabilities: Minimum scope for Phil's demo is `message-forwarding` to stabilize connectivity. The perfect demo adds live video streaming and offline RGB upload. SDK must ship networking support first so the Relay deployable can consume it. Sequence one by one, targeting all four within 2 weeks.

### Tracy's Hermes [relay] · Apr 18, 2026

Experiment: testing the dual-write behavior. If this is working correctly, this changelog entry should appear in this repo, and the quest-sync cron job will automatically pick it up and append it to the `fehu` quest changelog in the org repo in less than 12 hours.

### broodsugar's claude · Apr 18, 2026 12:27 +0800

README rewritten from the top with a user-facing narrative: CTRL-R as the first third-party SDK consumer, a bulleted "target shape", and a cast of characters (CTRL-R WEB, CTRL-R ROBOT, RELAY, DOMAIN VIEWER, CACTUS). Claude fixed the markdown-rendering bugs introduced during the rewrite (broken repo links, placeholder URL, hardbreak lines) and parked the open question of whether the old "canonical transport layer" paragraph still earns its place.

### broodsugar's claude · Apr 18, 2026 09:30 +0800

Quest created — precedent-setting, first quest in `org-auki/src/quests/`. Captures the cross-repo project for building the Auki network's canonical transport layer: SDK networking capabilities in `aukilabs/auki`, bundle app in the new `aukilabs/relay` repo, Go bounty work in `aukilabs/hagall` + `aukilabs/hagall-common`, early design docs in `aukilabs/broodsugar`. Seeded README, roadmap, sprints, changelog, parking lot. Also added `org-auki/src/quests/README.md` documenting the quest convention for future additions.

### broodsugar's claude · Apr 18, 2026 09:15 +0800

Scaffolded [`aukilabs/relay`](https://github.com/aukilabs/relay) — the first-party reference implementation that joins the network and offers all four Auki SDK networking capabilities from a single deployable. Tagline: *join the network and relay data*. Separate repo, not part of the SDK. First commit is docs-only; implementation is blocked on the SDK prerequisites landing.

### broodsugar's claude · Apr 18, 2026 08:40 +0800

Decomposed the Auki network's transport layer into four recruitable capabilities — `networking:message-forwarding` (control + small binaries), `networking:bulk-data-channel` (large non-real-time streams), `networking:turn` (real-time media, peer-fallback), and `networking:sfu` (real-time media, one-to-many fan-out). Only `message-forwarding` has implementation in flight today. Parking lot entry in `aukilabs/auki/projectrosrelay_parking_lot.md` flags the three-of-four-unowned-primitives gap.

### broodsugar's claude · Apr 18, 2026 08:05 +0800

First real TypeScript in the Auki SDK landed in `aukilabs/auki` [PR #44](https://github.com/aukilabs/auki/pull/44): `AukiSdk` class + `init()` factory. Wallet identity (viem) + peer identity (UUID). No network / Domain yet. Unblocks the rest of the SDK capability sprints (they all need `sdk.init()` underneath). Kicked off in a live call with Arshak.

### broodsugar's claude · Apr 18, 2026 05:14 +0800

Go rosrelay shipped in `aukilabs/hagall` [PR #63](https://github.com/aukilabs/hagall/pull/63) with protobuf defs in `aukilabs/hagall-common` [PR #22](https://github.com/aukilabs/hagall-common/pull/22). Delivers the ROS2 topic relay bounty on the Go side. Sets the parity target (six tests: fan-out, targeted delivery, size cap, isolation, auth, feature flag) for the SDK-native Relay implementation.
