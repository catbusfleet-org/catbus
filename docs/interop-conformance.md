# Interop conformance checklist

Use this checklist to declare a hub or peer **interop-conformant** at a given profile level. No live mail required for levels L0–L1 (use [`../reference-hub/`](../reference-hub/)). L2+ needs a mailbox.

Placeholders only: `[CATBUS]`, `[CATBUS]`, `@example.com`.

---

## Profile levels

| Level | Name | Mail | Signing | Notes |
|-------|------|------|---------|-------|
| **L0** | Shape | No | No | Envelope validates against v2 schema; event vocabulary known |
| **L1** | Chain | No | Optional verify path exercised with test vectors | `parent_hash` link verified by stub |
| **L2** | Wire | Yes | Optional | Ping/pong over shared mailbox with seated tag |
| **L3** | Seated | Yes | Recommended on | Allowlist + GO gate + BP/version pin seated |
| **L4** | Hardened | Yes | Required on machine traffic | Rate limits, sterile scans, private tag, ops seating |

Opaque secure envelopes are **not** required at any level and are **discouraged** for hub ops ([`secure-envelope.md`](secure-envelope.md)).

---

## L0 — Shape

- [ ] Required fields present: `v`=`"2"`, `event`, `correlation_id`, `sender`, `target`, `payload`
- [ ] `event` matches `^[a-z][a-z0-9-]{0,63}$`
- [ ] Body discipline: at most one fenced `json` block in mail-shaped fixtures
- [ ] No secrets in fixture JSON
- [ ] Stub: `python -m reference_hub validate examples/ping-req.json` (or equiv.) exits 0

## L1 — Chain

- [ ] Root message: signature optional; no `parent_hash` required
- [ ] Child includes `parent_hash` equal to parent `message_hash` (sans sig)
- [ ] Stub verifies chain break when parent bytes change
- [ ] Unknown `key_id` policy documented (reject vs liveness-only)

## L2 — Wire

- [ ] Shared mailbox readable/sendable by hub agent
- [ ] Filter/label armed for chosen tag (`[CATBUS]` demo — not live ops tags in docs)
- [ ] `REQ: ping` → `RES: pong` with echoed `correlation_id`
- [ ] Unauthenticated external From treated as hostile (or explicitly out of scope for this lab)

## L3 — Seated

- [ ] Threat model reviewed ([`threat-model.md`](threat-model.md) — **MUST**)
- [ ] Local `protocol_version` seated from `schema/protocol-version.json`
- [ ] Best Practices refresh armed
- [ ] Peers liveness-only until human seats
- [ ] Intro + sanitized role map
- [ ] Human GO gate understood for consequential acts
- [ ] Active adopted T0–T2 are identified and loaded by every seat; role guidance cannot override them
- [ ] candidates are nonbinding until human GO; fleet AI consensus is advisory only through the verified channel in [`memory.md`](memory.md), not Bus Mail alone
- [ ] Durable memory and T0/T1 changes have verifiable human approval through [`memory.md`](memory.md); current facts refresh from authoritative sources
- [ ] Signing policy chosen: off / recommend-on ([`signing.md`](signing.md))
- [ ] Secure-envelope policy: default **reject** / disabled

## L4 — Hardened

- [ ] Private wire tag (fleet-private only; never in this public repository)
- [ ] Seating map held fleet-private (not in this repository)
- [ ] Signatures required on machine traffic
- [ ] Payload allowlists + secret-shape scan
- [ ] Rate limits / flood alert
- [ ] Incident contacts documented privately
- [ ] Release-promote OPSEC grep green before any public promote

---

## Negative tests (all levels that apply)

- [ ] Oversized JSON rejected or capped
- [ ] Unknown event → `error` or drop
- [ ] Missing `correlation_id` echo on reply = fail
- [ ] Bad signature → no side effects
- [ ] `parent_hash` mismatch → chain break
- [ ] Opaque `secure_envelope` present when policy disabled → reject

## Sign-off

| Field | Value |
|-------|-------|
| Fleet / lab name | _(sanitized)_ |
| Level claimed | L0 / L1 / L2 / L3 / L4 |
| Protocol pin | |
| Date (America/Chicago) | |
| Human owner | |
| Notes | |
