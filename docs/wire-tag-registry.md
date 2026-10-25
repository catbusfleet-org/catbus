# Wire-tag registry convention (pattern doc)

**Purpose:** Define *how* fleets register subject tags — not a dump of live household tags.

**Promotable placeholders only** in this file:

| Context | Tag | Publish? |
|---------|-----|----------|
| Public / LinkedIn demo | `[CATBUS]` | Yes |
| Live production | _(not listed here)_ | **No** — fleet-private (not in this public repository) |

If you discover a live tag in private notes, record it in your private fleet-ops repository, never in this public repository. Do not invent or leak household production tags into promotable docs.

---

## Subject form

```text
[<TAG>] REQ: <event>
[<TAG>] RES: <event>
```

Examples:

```text
[CATBUS] REQ: ping
[CATBUS] RES: pong
```

Rules:

1. Tag match is **routing**, not authentication.
2. One primary tag per fleet lane (demo vs prod).
3. Do not reuse the public demo tag for high-security production.
4. Filter/label names that capture the tag stay fleet-private (not in this repo).

---

## Registry record shape (private fleet template)

Keep live values in private fleet ops — **do not commit live values into this docs file**.

```yaml
# fleet-private wire-tags.yaml (example shape only — not stored here)
tags:
  - id: demo-public
    subject_tag: "[CATBUS]"
    lane: public-demo
    auth_meaning: none  # routing only
  # - id: prod
  #   subject_tag: "[REDACTED]"
  #   lane: production
  #   filter_label: "(fleet-private only)"
  #   auth_meaning: none
```

---

## Anti-patterns

- Publishing live production tags in README, LinkedIn, or public schema comments
- Treating tag presence as proof of hub authenticity
- Running production traffic on `[CATBUS]` because docs used it
- Mixing multiple live tags without a private fleet registry
- Documenting any live household production tag as if it were the public CATBus demo tag (live values stay fleet-private only)

## Related

- Stand-up: [`00-stand-up-order.md`](00-stand-up-order.md)
- Security: [`security.md`](security.md)
