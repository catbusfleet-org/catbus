# Failure modes / runbook

Operational playbook for hub/peer failures. Keep live contacts and mailbox IDs fleet-private (your private fleet-ops repository) — not in this public repository.

Related: [`threat-model.md`](threat-model.md), [`signing.md`](signing.md), [`interop-conformance.md`](interop-conformance.md), [`faq-anti-patterns.md`](faq-anti-patterns.md).

---

## Severity

| Sev | Meaning | Typical response |
|-----|---------|------------------|
| S1 | Bus unsafe (credential leak, keys on wire, GO bypass) | Stop machine sends; human-only; rotate off-bus secrets |
| S2 | Trust broken (bad sig floods, tag squatting, seating confusion) | Quarantine senders; tighten allowlist; alert human |
| S3 | Degraded (mail delay, schema drift, soft TTL expiry) | Retry/backoff; telemetry; no consequential acts |
| S4 | Noise (unknown event from unknown sender) | Liveness-only or drop; log |

---

## Catalog

### Mail / transport

| Failure | Sev | Detect | Mitigate |
|---------|-----|--------|----------|
| Filter miss (tag mail in inbox noise) | S3 | Hub never sees REQ | Re-arm filter; confirm subject form `[TAG] REQ\|RES: event` |
| Auth failure / send denied | S2 | Send API errors | Refresh off-bus creds; never paste creds on bus |
| Spoofed From | S2 | DKIM fail / unexpected From | Treat as hostile; prefer self-mail |
| Delivery delay / loss | S3 | No pong within soft TTL | Resend with **new** correlation_id if initiating; don't reuse across tasks |
| Mailbox quota / flood | S2 | Rate spike | Rate-limit; alert; consider temporary tag rotate (ops) |

### Envelope / schema

| Failure | Sev | Detect | Mitigate |
|---------|-----|--------|----------|
| Missing required fields | S3 | Schema validate fail | `error` or drop; do not execute |
| Unknown event | S4/S3 | Not in hub vocabulary | Drop or `error`; peers must not invent events |
| Oversized body | S3 | Size cap | Cap; alert on repeat |
| Second JSON fence / chatty dump | S3 | Parse ambiguity | Reject; require single fence |
| Secret-shaped string in payload | S1 | Scan hit | Quarantine thread; human review; rotate if real secret |

### Correlation / sessions

| Failure | Sev | Detect | Mitigate |
|---------|-----|--------|----------|
| Reply without echoed `correlation_id` | S3 | Mismatch | Treat as unrelated; request proper ack |
| ID reuse across tasks | S3 | Hub state collision | Soft-drop duplicate; educate peer |
| Orphan telemetry | S4 | Unknown id | Log; ignore for authority |

### Signing / chain (when enabled)

| Failure | Sev | Detect | Mitigate |
|---------|-----|--------|----------|
| Bad signature | S2 | Verify fail | Drop; no side effects; alert if seated peer |
| Unknown `key_id` | S3 | Not in seat map | Liveness-only until human seats |
| `parent_hash` mismatch | S2 | Chain break | Do not extend trust; alert human |
| Missing sig when required | S2 | Policy | Reject machine traffic |
| Key material on bus | S1 | Content scan | Incident: stop; rotate; scrub |

### Secure envelope (if ever enabled — discouraged)

| Failure | Sev | Detect | Mitigate |
|---------|-----|--------|----------|
| Opaque blob blocks human GO | S2 | Owner cannot skim | Disable opaque path; fall back to cleartext + signing |
| Decrypt fail | S3 | Recipient error | `error`; do not retry forever |
| GO only inside ciphertext | S1 | Policy violation | Treat GO as invalid; require cleartext GO |

### Protocol / governance

| Failure | Sev | Detect | Mitigate |
|---------|-----|--------|----------|
| Stale protocol pin | S3 | Startup / heartbeat / schedule / `protocol-check` | Proactively report delta; explicit GO before any hub or seat adopts, compatible or breaking |
| Peer invents events | S3 | Unknown event from seated peer | Correct via hub; demote if repeat |
| Social-engineered GO | S1 | Out-of-band pressure or a claimed approval without a verifiable record | For memory/governance, use the human-controlled channel in [`memory.md`](memory.md); for other consequential acts, follow the established human GO procedure and hold if its origin cannot be verified |
| Unsigned content acted on as a command | S1 | Free text, or an unsigned or malformed message, caused action | Reject and log. Only an intake-signed structured message may cause action ([`secure-intake.md`](secure-intake.md)) |
| Docs authority spoof | S2 | Wrong URL / TLS fail | Pin canonical GitHub; don't apply |

### Memory / governance

| Failure | Sev | Detect | Mitigate |
|---------|-----|--------|----------|
| Candidate or pending tier item treated as adopted | S2 | No recorded human GO or status says candidate | Hold affected behavior; retain adopted rules; ask hub/human to resolve |
| Durable memory or T0–T2 changed without ratification | S2 | Missing approval record or unexplained version-control change | Reject the change as unratified; restore last approved state; surface to human |
| Stale memory used for a changing fact | S3 | Source date or current system disagrees | Refresh from authoritative source; retain the discrepancy and update memory through its lifecycle |
| Conflicting memory silently collapsed | S2 | Competing sources or edits without supersession trail | Preserve both with provenance; compare authority, recency, scope, and evidence; escalate unresolved conflict |
| Bus Mail vs. Governance Assent (Confusion) | S1 | Assent claimed in self-mail or no verifiable human approval record | Treat Bus Mail as transport only; do not activate or ratify; require the human-controlled repository approval or enrolled-key signature defined in [`memory.md`](memory.md) |
| Ratification forgeable by seat | S1 | Machine-only approval, unprotected governed-path change, or unverifiable signature | Reject the change as unratified; require enforced required-review branch protection with human CODEOWNER approval or a verified enrolled human signature |

---

## Immediate actions (cheat sheet)

1. **Stop consequential side effects** if trust is in doubt.
2. **Preserve thread** for audit (don't mass-delete).
3. **Classify sev**; page human for S1/S2.
4. **Quarantine** sender or tag as needed (ops).
5. **Rotate** only off-bus secrets that actually leaked.
6. **Record** sanitized incident note in private ops — never paste secrets into git.

## Recovery validation

- [ ] Ping/pong green on intended tag
- [ ] Schema validate on recent packets
- [ ] If signing on: chain verify on last N messages
- [ ] GO gate restated in-thread by human
- [ ] Interop level still accurate ([`interop-conformance.md`](interop-conformance.md))
