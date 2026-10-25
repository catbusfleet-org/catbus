# Roles (sanitized public taxonomy)

Public docs and minted cards use **only** these role names unless the human seated custom callsigns in the stand-up interview. Do not publish live callsigns.

| Role | Responsibility |
|------|----------------|
| `orchestrator` | Hub. Owns protocol, seating, intro/role map, memory-governance status, and GO-gate enforcement. |
| `dispatcher` | Routes tasks; tracks ask/ack lifecycle; follows active fleet governance. |
| `worker-node` | Executes accepted tasks under active fleet governance; sparse finished packets. |
| `audit-node` | Observes bus traffic and memory-governance transitions; does not invent protocol or activate candidates. |

All seats load and follow adopted T0–T2 regardless of role. Role-specific guidance cannot override these fleet-wide tiers. Promotion gates and candidate status are defined in [`memory.md`](memory.md).

## Seating (primary path)

1. Human pastes [`00-stand-up-order.md`](00-stand-up-order.md) into hub model.
2. Hub interviews + mints cards ([`../prompts/hub.md`](../prompts/hub.md)).
3. Ping/pong; human seats peers; hub emits `intro`.

## Domains in examples

`@example.com`, `@example.org`, `@example.net` only.

## Wire tags (placeholders)

```text
[CATBUS] REQ: <event>
[CATBUS] RES: <event>
```

Production: private tag fleet-only (not published here).
