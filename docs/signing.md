# Signing protocol (OPTIONAL — recommended)

**Suite status:** **OPTIONAL**. CATBus hubs MAY run without signatures.  
**Recommendation:** For seated machine traffic, **prefer** hash-based message signing + reply-chain linking. Signing keeps payloads **cleartext-reviewable** while proving integrity — unlike opaque secure envelopes ([`secure-envelope.md`](secure-envelope.md)), which we advise against for hub ops.

Related: [`threat-model.md`](threat-model.md) (**MUST**), [`secure-payload.md`](secure-payload.md), [`security.md`](security.md), schema [`../schema/signing.schema.json`](../schema/signing.schema.json), stub [`../reference-hub/`](../reference-hub/).

---

## Goals

1. **Prove** a seated agent produced a given envelope body (integrity + authenticity relative to a known public key).
2. **Link** replies to parents so an adversary cannot silently splice forged history (**hash-into-hash** / `parent_hash`).
3. Keep **signing private keys off-bus** — never in envelope JSON, mail bodies, or repos.

Non-goals: replacing DKIM/SPF; providing confidentiality (use out-of-band channels for secrets); publishing live key IDs of a real fleet in public docs.

---

## When to require signatures

| Mode | Policy |
|------|--------|
| Demo / early UAT | Signatures off; still validate envelope shape |
| Seated production peers | **Recommend** require `signature` on machine traffic |
| Human GO threads | May be plain text per policy; do not confuse GO with machine sig |

**Signature ≠ authorization.** Even a verified signature does not authorize spends or third-party outbound mail — human GO still gates consequential acts.

---

## Private keys off-bus

| On bus / repo (OK) | Off bus (required) |
|--------------------|--------------------|
| `key_id` (opaque handle) | Private signing key material |
| Algorithm name (`ed25519`, …) | Key generation / HSM / agent secret store |
| Public key fingerprint (optional, truncated) | Live key ceremony details in public materials |
| Signature bytes (base64) | Passphrases, seeds, recovery material |

---

## Canonical message hash

1. Build the **unsigned envelope object**: all fields except `signature` (and any private binding fields).
2. Canonicalize JSON (recommend: UTF-8, sorted object keys, no insignificant whitespace — document exact rule in private runbook; keep stable).
3. `message_hash = HASH(canonical_bytes)` (recommend SHA-256; declare `hash_alg`).
4. `signature = Sign(private_key, message_hash)` (or over canonical bytes — pick one; stay consistent).

Receivers recompute and verify with the sender's seated public key.

---

## Reply chain linking (hash-into-hash)

```text
  H0 = hash(parent_envelope_sans_sig)
  reply includes parent_hash = H0  (inside signed material)
  H1 = hash(reply_envelope_sans_sig)   # covers parent_hash
```

Changing the parent breaks verification of every descendant that linked it.

See diagram: [`diagrams/signing-chain.md`](diagrams/signing-chain.md).

---

## Suggested envelope attachment (illustrative)

```json
{
  "v": "2",
  "event": "ack",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440010",
  "sender": "worker-node",
  "target": "orchestrator",
  "in_reply_to": "ask",
  "payload": { "status": "accepted" },
  "signature": {
    "alg": "ed25519",
    "hash_alg": "sha256",
    "key_id": "worker-node-2026q3",
    "parent_hash": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
    "sig": "BASE64_SIGNATURE_BYTES_HERE"
  }
}
```

- `parent_hash` omitted on chain roots (first `ping` / `intro`).
- `key_id` is opaque, not a secret.
- Example domains only: `@example.com` style identities.

---

## Verification checklist

1. Parse envelope; strip `signature` before hashing.
2. Canonicalize → `message_hash`.
3. Resolve `key_id` → seated public key (unknown → reject or liveness-only).
4. Verify `sig`.
5. If `parent_hash` present: match stored parent hash (or policy-allow missing parent for out-of-order delivery).
6. Apply hub policy + GO gate.

---

## Failure modes (signing)

| Failure | Suggested hub behavior |
|---------|------------------------|
| Bad signature | Drop or `error`; no payload side effects |
| Unknown `key_id` | Liveness-only until human seats key |
| `parent_hash` mismatch | Chain break; alert human; do not extend trust |
| Missing signature when policy requires it | Reject machine traffic; allow human plain-text GO per policy |

Full runbook: [`failure-modes.md`](failure-modes.md).

---

## Distinct from the secure mouth

The secure mouth ([`secure-intake.md`](secure-intake.md)) holds its own key and signs the structured form the human confirmed. That intake signature is how free text becomes an instruction.

A peer `signature` on machine traffic does not mint an intake signature. Downstream components must not accept unsigned free text as an instruction. Intake signing keys are held only by the intake.

## Relation to transport auth and envelopes

Signing **complements** DKIM/SPF/DMARC and private wire tags. It does **not** replace them.

Prefer **cleartext sterile payload + signing** over **opaque secure envelopes**. See [`secure-envelope.md`](secure-envelope.md).
