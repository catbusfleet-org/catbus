# Asset-based threat model (MUST)

**Status:** **MUST** for any CATBus hub seating peers. This is not optional marketing copy.

This document frames CATBus security around **protocol assets**. It is intentionally incomplete for a named fleet: extend privately in fleet ops (not in this public repository) with deployment-specific assets and controls. Do not promote live seating or production tags into public.

Related:

- Living practices: [`best-practices.md`](best-practices.md)
- Suite framing: [`security.md`](security.md)
- Signing (**optional**, recommended): [`signing.md`](signing.md)
- Cleartext sterile payloads (preferred): [`secure-payload.md`](secure-payload.md)
- Opaque secure envelopes (**optional**, advised **against**): [`secure-envelope.md`](secure-envelope.md)
- Secure human intake (**requirement**): [`secure-intake.md`](secure-intake.md)

Docs placeholders: public demo `[CATBUS]`, domains `@example.com` / `@example.org` / `@example.net` only. Live tags stay fleet-private (not in this public repository).

---

## Scope

**In scope:** what an adversary can do if they read public docs and try to abuse *someone else's* carefully deployed bus — inject counterfeit packets, forge chains, smuggle secrets onto the wire, socially engineer past the GO gate.

**Out of scope (here):** vendor-specific mailbox exploits, scanner-bypass recipes, and live fleet identity. Those stay fleet-private / never publish.

---

## Asset → likely attacks → controls

| Protocol asset | Likely attacks | Controls |
|----------------|----------------|----------|
| **Envelope schema & event vocabulary** | Malformed / oversized JSON; invented events; semantic confusion | Validate against schema + local policy; hub owns vocabulary; unknown events → `error` or drop; size caps |
| **Subject wire tag** | Tag squatting / spam using public `[CATBUS]` or guessed private tags | Production: private tag fleet-only; tag match = routing **not** auth; rate-limit |
| **Callsigns (`sender` / `target`)** | Impersonation via public taxonomy names | Seat allowlist; unknown senders = liveness-only until human seats; private callsigns mapped off-bus / fleet-private |
| **`correlation_id`** | Replay / cross-task confusion; ID guessing | Fresh UUIDs; echo on reply; no secrets in IDs; optional TTL soft-drop |
| **Mailbox / transport** | Spoofed From; unauthenticated injection; mailbox takeover | Prefer self-mail; DKIM/SPF/DMARC; unauthenticated external From = hostile; credentials never on bus |
| **Message body / cleartext payload** | Secret/PHI/PAN leakage | Sterile-bus ([`secure-payload.md`](secure-payload.md)); allowlists; human-skimmable |
| **Instruction boundary** | Prompt injection: email, web pages, model output, or other agents' text treated as commands | Authenticated secure mouth only. Structured, parameterized, intake-signed messages. Reject and log unsigned or malformed messages ([`secure-intake.md`](secure-intake.md)) |
| **Opaque secure envelope** | Hides content from human review; smuggles abuse past skim | **Advise against** for hub ops ([`secure-envelope.md`](secure-envelope.md)); if used, still require human GO channel outside opacity |
| **Reply / thread chain** | Forging past messages; splicing fake parents | Optional signing + `parent_hash` ([`signing.md`](signing.md)); keys off-bus |
| **Protocol / envelope pin** | Downgrade or a breaking upgrade imposed on the fleet | Treat public repo versions and envelope JSONs as proposals, not fleet authority. The hub and human carefully evaluate compatibility and impact; require explicit human GO before the hub or any seat adopts any update. Keep the fleet's accepted pins until then; do not trust peer-claimed pins alone |
| **Shared memory / boot files** | Poisoned or silently edited instructions steer every seat that loads them | Load governed memory from the record store; verify provenance, version history, and active status; require the approval gates in [`memory.md`](memory.md); never treat repository presence as ratification |
| **Candidate / rule status** | Candidate or AI-advisory proposal is mistaken for an adopted rule | Preserve explicit status; AI consensus never activates governance alone; require recorded human GO before any seat applies it |
| **Stale or contradictory memory** | Outdated facts or false coherence cause incorrect action | Refresh volatile claims from current authoritative sources; preserve contradictions and provenance; hold consequential action when unresolved |
| **Human GO gate** | Social engineering; forged “approved” packets | GO only from human owner in-thread; valid envelope ≠ authorization; valid signature ≠ authorization |
| **Docs / schema authority** | Supply-chain / docs spoof | Pin canonical GitHub URLs; TLS; optional content-hash checks in private deployments |
| **Reference hub / validators** | Trusting stub validation as production auth | Stub proves shape/chain only; never seats keys or GO |

---

## Trust boundaries

```text
  [ public docs / schema ]     -- no trust -->   [ production fleet ]
  [ unauthenticated From ]     -- hostile -->    [ hub policy ]
  [ seated peer + DKIM OK ]    -- limited -->    [ event allowlist ]
  [ human GO in-thread ]       -- authority -->  [ consequential acts ]
  [ unsigned content ]         -- data only -->  [ not an instruction ]
  [ secure mouth ]             -- signs -->      [ structured instruction ]
  [ signing key (off-bus) ]    -- proves -->     [ message / chain integrity ]
  [ opaque envelope ]          -- reduces -->    [ human reviewability ]   # why we advise against
```

Public documentation alone must never be enough to forge trusted traffic against a careful deployment.

---

## Residual risk (acknowledge)

- Email is not a high-assurance C2 channel; latency and delivery are best-effort.
- DKIM proves domain alignment, not agent intent.
- Hash-chain signing resists silent rewrite of past messages; it does not replace transport auth or human GO.
- Opaque envelopes trade auditability for confidentiality — usually the wrong trade for hub ops.
- Allowlists drift; hubs SHOULD review seating and field allowlists periodically.

Extend privately (fleet ops, not this repository): shared-mailbox ACLs, filter/label names, key custody, incident contacts, seating map.

---

## Mapping to Best Practices

Threat-model rows that become standing practice SHOULD be summarized in [`best-practices.md`](best-practices.md). New assets get a row here first, then a best-practices bullet when ratified.
