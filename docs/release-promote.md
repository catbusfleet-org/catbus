# Release process (maintainers)

How public CATBus releases are cut. **No promote-patch files.** Live identity, production wire tags, and branding guidelines stay out of this repository.

---

## 1. Pre-release gate

- [ ] Protocol/envelope pin changes have human GO before hub/seat adoption
- [ ] `schema/protocol-version.json` bump decided (semver)
- [ ] `CHANGELOG.md` entry drafted for the release
- [ ] Memory/governance docs and examples contain no private fleet memory or personal context
- [ ] Interop level still accurate for claimed demos
- [ ] Security stance unchanged or intentionally updated:
  - Threat model = **MUST**
  - Secure human intake = **required** ([`secure-intake.md`](secure-intake.md))
  - Signing = optional, **recommended**
  - Secure envelopes = optional, **advised against** (human reviewability)

## 2. What does not ship here

| Path / material | Why |
|-----------------|-----|
| Live production wire tags, seating maps, callsigns | Fleet-private OPSEC |
| Brand guidelines / private review packets | Not product protocol |
| Secrets, keys, mailbox addresses | Never |

## 3. OPSEC grep (run on the release tree)

```bash
rg -n -i \
  -e '@gmail\\.com' \
  -e '@googlemail\\.com' \
  -e 'AGENT-HANDSHAKE' \
  -e 'Outseer' \
  -e 'outseer' \
  -e 'BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY' \
  -e 'api[_-]?key\\s*[:=]' \
  -e 'xox[baprs]-' \
  -e 'ghp_[A-Za-z0-9]+' \
  -e 'sk-[A-Za-z0-9]{20,}' \
  .
```

Manual skim: no real emails, no live production subject tags, no fleet callsigns as if public, domains only `@example.com` / `@example.org` / `@example.net` in examples, wire tags only `[CATBUS]` (and private tags named as a *concept*, not a value).

## 4. Ship

1. Open or merge the release PR into the public working tree.
2. Run stub validate if present (`reference-hub`).
3. Tag if releasing.
4. Record source SHA notes in `CHANGELOG.md` when promoting from a private SoR.

## 5. Rollback

If a leak ships: scrub public history or force-fix only with explicit maintainer approval; rotate anything exposed; treat as S1 in [`failure-modes.md`](failure-modes.md).
