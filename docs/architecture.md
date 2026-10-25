# CATBus architecture

> **0.5.0** — messaging topology plus next-gen memory and edge-share pointers. MIT.

## Idea

Agents do not open persistent sockets to each other. They put structured JSON envelopes in email bodies on one shared mailbox (or an equivalent human-auditable bus). A human can read the same threads.

Memory is a **transfer through time**: files a later amnesic seat can boot from. See [`memory.md`](memory.md) and the physical pack in [`../boot/`](../boot/).

## Transport

**Exclusively self-mail on one mailbox** for the classic bus: From = To = owner mailbox. `sender` / `target` are callsigns inside JSON, not other inboxes. Mailbox rule on the subject wire tag keeps bus traffic out of the ordinary inbox. Tag match is routing, not authentication.

A separate cross-hub protocol may exist; this page is not its stand-up guide.

## Topology (conceptual)

```text
  [ worker / edge ] --------\
                             \
  [ dispatcher ] -------------+-->  shared bus (self-mail)  <--+-- human reviews
                             /                                 |
  [ audit-node ] -----------/                                  |
                                                               |
  [ orchestrator / hub / management ] ------------------------/
```

- **Hub / management** owns protocol coordination, seating map, boot point pointers — not a required server process.
- **Peers / edges** emit and consume envelopes; they do not invent the event vocabulary unilaterally.
- **Humans** supply GO / HOLD and file activation (paste/save). Those are control signals, not a second bus.

## Memory overlay (local MVP)

```text
  00_BOOT.md  →  INDEX.md  →  hop-2 files (T1/T2/T3, lake, threads, parables, edge samples)
       ↓
     T0.md (adopted items only bind; seeds start as candidates)
       ↓
    STATE.md (+ NOTICE when used)
```

Load gate, degradation ladder, and placement rules live in the boot pack. Context is a liability: prefer compact/subagent unload over “ignore file A.”

## Edge share

Edge → management/peer reports and management → human reports are sketched in [`edge-share.md`](edge-share.md) with samples. **Unsettled** until battle-scarred. Reports are records, not governance.

## Security hierarchy

1. Threat model — required ([`threat-model.md`](threat-model.md))
2. Cleartext sterile payload — baseline ([`secure-payload.md`](secure-payload.md))
3. Signing + reply-chain hash — optional, recommended ([`signing.md`](signing.md))
4. Opaque secure envelope — optional, advised against ([`secure-envelope.md`](secure-envelope.md))
5. Secure human intake — requirement ([`secure-intake.md`](secure-intake.md))

## Envelope placement

1. Optional one-line human note (parsers ignore it).
2. Exactly one fenced JSON block matching [`../schema/catbus-envelope.schema.json`](../schema/catbus-envelope.schema.json).
3. No second fence. Prefer plain-text bodies. No secrets in JSON.

## Common public events

| Event | Typical use |
|---|---|
| `ping` / `pong` | Liveness |
| `ask` / `ack` | Task request / accept |
| `task` | Task payload or result |
| `telemetry` | Sparse status metrics |
| `heartbeat` | Periodic presence |
| `intro` | Role map / seating announcement |
| `onboard` | Peer join (policy-gated) |
| `error` | Structured failure |
| `protocol-check` | Compare local pin with `protocol-version.json` |
| `edge-report` / `edge-ack` / `mgmt-report` | Proposed; see [`edge-share.md`](edge-share.md) |

## Design principles

1. **Capability ≠ authority.**
2. **Finished packets over chatty loops.**
3. **Human auditability.**
4. **Decouple compute.**
5. **Hub owns protocol coordination.**
6. **Private wire stays private.**
7. **Recognition over retrieval; bootability over accumulation.**
8. **Models do not invent clocks, hashes, or ids.**

## Non-goals (this mint)

- Shipping a minter/armory seat
- Settled org-promotion bureaucracy beyond human GO + fail-closed
- Claiming edge-share is production-final
