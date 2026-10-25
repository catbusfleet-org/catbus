# Security notes

## Threat we care about

An adversary who reads public (or leaked) docs and tries to **inject a counterfeit hub** (or peer) into someone else's CATBus fleet.

CATBus is designed so that **public documentation alone is not enough** to forge trusted traffic against a careful deployment.

## Optional security suite (default stance)

| Component | Status | Doc |
|-----------|--------|-----|
| Asset-based threat model | **MUST** | [`threat-model.md`](threat-model.md) |
| Secure human intake | **requirement** | [`secure-intake.md`](secure-intake.md) |
| Sterile cleartext payloads | Preferred baseline | [`secure-payload.md`](secure-payload.md) |
| Message signing + chain hash | **OPTIONAL**, **recommend** | [`signing.md`](signing.md) |
| Opaque secure envelope | **OPTIONAL**, **advise against** | [`secure-envelope.md`](secure-envelope.md) |

**Prefer cleartext-reviewable payloads + signing over opaque envelopes for hub ops.** Opacity knocks down human reviewability.

Living practices: [`best-practices.md`](best-practices.md).

## Public vs private surface

| Published / promotable | Kept private (never publish) |
|------------------------|------------------------------|
| Conceptual architecture | Real mailbox addresses |
| Public envelope schema (v2) | Production subject tags / labels |
| Sanitized roles & `@example.*` | Live callsign registries / peer lists |
| Demo tag `[CATBUS]` | Live household production tags (fleet-private, not in this repository) |
| Generic signing & sterile-payload schemas | Live key IDs, fingerprints, seating maps |
| Asset-based threat model | Event catalogs of a specific fleet |
| Secure-envelope doc **with advise-against** | Credentials, app passwords, tokens |
| | Scanner-bypass or “armor” recipes |

## Defender principles (non-exhaustive)

1. **Transport binding.** DKIM/SPF/DMARC; self-mail or tightly allowlisted From; unauthenticated external From = hostile.
2. **Private wire tag.** Production tags must not match public placeholders. Tag match ≠ auth.
3. **Hub owns live seating state.** Unknown senders = liveness-only until human seats. The repository record store is authoritative for governed memory and its promotion status ([`memory.md`](memory.md)).
4. **Schema is not trust.** Validate shape, then policy.
5. **Least privilege cleartext payloads.** No secrets/PHI/PANs on bus.
6. **Optional hash-based signing.** Keys off-bus; `parent_hash` on replies.
7. **Avoid opaque envelopes for hub ops.** Reviewability is a control.
8. **Rate and volume.** Rate-limit and alert on floods.
9. **Human GO for consequential acts.** Even when envelope verifies.
10. **Self-mail for machine traffic.** Prefer shared-mailbox self-mail over open From spoofing.
11. **Governed memory.** Load adopted tiers and their recorded provenance from the authorized record store; never execute candidates or let a memory document grant access. Require the verifiable human-controlled approval channel for ratification and T0–T2 activation defined in [`memory.md`](memory.md); Bus Mail and authorship claims alone are insufficient.
12. **Secure human intake.** Treat prompt injection like SQL injection. Free text is accepted only at the authenticated secure mouth. Only its signed, structured messages can cause action. Unsigned content is data. Downstream rejects unsigned or malformed messages and logs the rejection ([`secure-intake.md`](secure-intake.md)).

## Never publish

- Live wire tags or filter rules
- Live callsigns or role maps of a real fleet
- Mailbox credentials or OAuth tokens
- Signing private keys or live key ceremonies
- Real addresses (examples: `@example.com` only)
- Branding guidelines
- Live fleet OPSEC (kept outside this public repository)

## Reporting

Documentation leaks that would help forge traffic: open a security-marked issue on `github.com/catbusfleet-org/catbus` with **no** exploit payload against third parties. Private deployment issues stay in private channels.
