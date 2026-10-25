# Secure payload — sterile cleartext (preferred)

**Naming:** This document is about **cleartext, human-reviewable payloads** on a sterile bus. It is **not** an opaque “secure envelope.” For the optional opaque construct (advised against), see [`secure-envelope.md`](secure-envelope.md).

**Suite status:** Recommended baseline for all hubs (pairs with threat model **MUST**). Signing is optional-but-recommended on top; opaque envelopes are optional-and-discouraged.

Related: [`threat-model.md`](threat-model.md), [`signing.md`](signing.md), [`secure-envelope.md`](secure-envelope.md), [`security.md`](security.md), schema [`../schema/secure-payload.schema.json`](../schema/secure-payload.schema.json).

Placeholders: `[CATBUS]` / `[CATBUS]`; `@example.com` / `@example.org` / `@example.net`.

---

## Sterile-bus principles

1. **No secrets on the wire.** API keys, OAuth tokens, cookies, app passwords, recovery codes, private keys, seeds — forbidden in subjects, bodies, and JSON.
2. **No PHI / PANs / credentials.** Reference by opaque handles off-bus if linkage is required.
3. **Allowlisted fields.** Small documented set of payload keys per event; reject/strip unknown keys in high-security fleets.
4. **Pointers, not payloads.** Large or sensitive blobs stay off-bus; envelopes carry IDs, hashes, or placeholder URLs.
5. **Human-skimmable.** If a human cannot safely read the thread on a phone, the packet is too sensitive or too chatty — **this is why we prefer cleartext over opaque envelopes.**

---

## Forbidden content (non-exhaustive)

| Class | Examples (do not put on bus) |
|-------|------------------------------|
| Credentials | Passwords, API keys, bearer/refresh tokens, app passwords |
| Key material | Private keys, JWKs with `d`, seed phrases, raw HMAC secrets |
| Payment | Full PAN, CVV, magnetic-stripe equivalents, secret bank pairs |
| Health / identity abuse | PHI beyond mailbox owner acceptance; ID images; biometrics |
| Live fleet identity in promotable docs | Production wire tags, live callsign registries, real mailboxes |
| Bypass recipes | Scanner defeat / From forgery recipes |

Out-of-band for the above; on-bus send only opaque `ref_id` or status.

---

## Allowlisted envelope fields (public v2)

Required: `v`, `event`, `correlation_id`, `sender`, `target`, `payload`.

Optional: `timestamp`, `in_reply_to`, `ttl_seconds`, `message`, optional `signature` ([`signing.md`](signing.md)).

| Event | Example allowlisted payload keys |
|-------|----------------------------------|
| `ping` / `pong` | (empty), optional `nonce` |
| `ask` / `ack` | `task`, `status`, `reason` |
| `task` | `task`, `status`, `result_summary`, `ref_id` |
| `telemetry` / `heartbeat` | `local_version`, `envelope_v`, `ok`, `metrics` |
| `intro` / `onboard` | `roles` (sanitized), `note` |
| `protocol-check` | `local_version`, `envelope_v`, `authority` |
| `error` | `code`, `message` (no secret stack traces) |

---

## Example (sterile cleartext)

Subject: `[CATBUS] REQ: ask` 

```json
{
  "v": "2",
  "event": "ask",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440020",
  "sender": "dispatcher",
  "target": "worker-node",
  "payload": {
    "task": "summarize",
    "ref_id": "doc-example-001"
  }
}
```

---

## Anti-patterns

- Pasting `.env` or cloud keys into a task body
- Embedding PANs or auth cookies in `payload`
- Using `message` as a free-form PII dump
- Publishing real domains or live tags in promotable examples
- Assuming schema validation alone = safe
- Wrapping ordinary hub traffic in opaque envelopes “for security” (see [`secure-envelope.md`](secure-envelope.md))

---

## Validation hint

1. Validate envelope shape.
2. Validate payload against per-event allowlist.
3. Scan for high-entropy token-like strings; quarantine on hit.
4. Optionally require signatures when seated.
5. Still demand human **GO** for consequential side effects.
