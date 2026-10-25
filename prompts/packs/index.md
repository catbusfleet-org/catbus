# Versioned profile packs (prompts index)

Packs are versioned drop-ins for hub/peer seating. **Primary path** remains: paste [`../../docs/00-stand-up-order.md`](../../docs/00-stand-up-order.md) so the hub interviews and mints cards. Packs below are library copies for humans who prefer fixed files.

| Pack ID | Semver | Files | Notes |
|---------|--------|-------|-------|
| `hub-core` | 0.5.0 | [`../hub.md`](../hub.md) | Hub card; starts interview if unseated |
| `peer-core` | 0.5.0 | [`../peer.md`](../peer.md) | Generic peer |
| `role-orchestrator` | 0.5.0 | [`../orchestrator.md`](../orchestrator.md) | Specialty aligned to hub |
| `role-dispatcher` | 0.5.0 | [`../dispatcher.md`](../dispatcher.md) | Specialty |
| `role-worker` | 0.5.0 | [`../worker-node.md`](../worker-node.md) | Specialty |
| `role-audit` | 0.5.0 | [`../audit-node.md`](../audit-node.md) | Specialty |
| `stand-up` | 0.5.0 | [`../../docs/00-stand-up-order.md`](../../docs/00-stand-up-order.md) | **Preferred single drop-in** |

## Security blurb (every pack)

- Threat model: **MUST**
- Secure human intake: **requirement** — [`../../docs/secure-intake.md`](../../docs/secure-intake.md)
- Signing: optional, **recommended** when seated
- Opaque secure envelopes: optional, **advised against**

## Memory governance (every pack)

- Load and follow adopted T0–T2 across roles; see [`../../docs/memory.md`](../../docs/memory.md).
- Treat T2 candidates awaiting human GO as nonbinding (fleet AI consensus may advise).
- Ratify durable memory or promote T0/T1 content only through the verifiable human-controlled channel in [`../../docs/memory.md`](../../docs/memory.md); Bus Mail alone is not approval.

## Versioning

Bump pack semver when instruction behavior changes; keep aligned with [`../../schema/protocol-version.json`](../../schema/protocol-version.json) when protocol semantics change. Record in [`../../CHANGELOG.md`](../../CHANGELOG.md).
