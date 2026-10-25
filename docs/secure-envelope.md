# Secure envelope protocol (OPTIONAL — advised against)

**Naming clarification:**

| Term | Meaning in CATBus |
|------|---------------------|
| **Envelope** (CATBus v2) | The normal cleartext JSON object (`v`, `event`, `correlation_id`, …) — always human-skimmable. |
| **Secure payload / sterile payload** | Rules for what may appear in cleartext `payload` — [`secure-payload.md`](secure-payload.md). |
| **Secure envelope (opaque)** | An optional wrapper that encrypts or otherwise hides payload bytes from casual inbox review. **This document.** |

CATBus uses `secure-payload` for cleartext sterility rules and **secure envelope** for the optional opaque wrapper, so the two are never confused.

---

## Suite status

| | |
|--|--|
| **Status** | **OPTIONAL** |
| **Recommendation** | **Advise AGAINST** for normal hub ops |
| **Why** | Opaque envelopes **knock down human reviewability** — a core CATBus property (phone-skimmable threads, HITL GO). Prefer **cleartext sterile payloads + optional signing** ([`secure-payload.md`](secure-payload.md), [`signing.md`](signing.md)). |

Threat model (**MUST**): [`threat-model.md`](threat-model.md).

---

## When a secure envelope might still be considered

Rare cases only, with eyes open:

- Regulatory need to transit a short secret pointer that cannot wait for a vault handoff **and** the mailbox is not an acceptable cleartext surface.
- Cross-org handoff where intermediate MTAs must not see a field — still prefer out-of-band vault.

Even then: keep the **outer** CATBus envelope cleartext (event, correlation, sender, target visible); put opacity only in a nested field if you must; document recovery for the human owner; never use opacity to bypass GO.

---

## If you implement anyway (pattern only)

Illustrative — not a recommendation to enable:

```json
{
  "v": "2",
  "event": "task",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440030",
  "sender": "dispatcher",
  "target": "worker-node",
  "payload": {
    "secure_envelope": {
      "alg": "age-recipient-or-equivalent",
      "kid": "opaque-recipient-handle",
      "ciphertext": "BASE64_OPAQUE_BYTES"
    },
    "status": "sealed"
  }
}
```

Rules if enabled:

1. Outer envelope remains schema-valid and skimmable (`event`, parties, correlation visible).
2. Ciphertext carries **no** expectation of hub semantic routing on inner content without decrypt.
3. Human GO for consequential acts must still have a **cleartext** channel (in-thread GO cannot be “inside” ciphertext only).
4. Keys off-bus; never publish live `kid` values in public docs.
5. Default fleet policy: **reject** `secure_envelope` unless explicitly seated by human owner.

---

## Preference hierarchy (hub ops)

1. **Threat model** — must  
2. **Cleartext sterile payload** — prefer  
3. **Message signing + chain hash** — optional, recommend  
4. **Opaque secure envelope** — optional, **advise against**

Do not market opaque envelopes as “more secure CATBus.” For hub ops, reviewability is a security control.
