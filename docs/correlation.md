# Correlation IDs

CATBus ties request and response packets with an opaque `correlation_id`.

## Rules

1. **Issuer creates the ID.** Initiating event (`ping`, `ask`, …) gets a fresh UUID.
2. **Responder echoes it.** Matching `pong` / `ack` / result / `error` reuses the same id.
3. **Optional `in_reply_to`.** Prior event name for skimability; correlation_id remains authoritative.
4. **TTL is soft.** `ttl_seconds` is a hint.
5. Keep convention consistent within a fleet; do not encode secrets in IDs.

## Example

Request:

```json
{
  "v": "2",
  "event": "ask",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440002",
  "sender": "dispatcher",
  "target": "worker-node",
  "payload": { "task": "summarize" }
}
```

Response:

```json
{
  "v": "2",
  "event": "ack",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440002",
  "sender": "worker-node",
  "target": "dispatcher",
  "in_reply_to": "ask",
  "payload": { "status": "accepted" }
}
```

## Anti-patterns

- Reusing a correlation_id across unrelated tasks
- Responding without echoing the ID
- Putting secrets inside correlation_id strings

## Optional event: `protocol-check`

Sender includes local protocol and envelope pins in `payload`; responder echoes `correlation_id`. Never auto-apply a pin update, compatible or breaking. Proactively `ask` the human with the delta and wait for explicit GO before the hub or any seat adopts it.
