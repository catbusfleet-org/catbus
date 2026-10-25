# CATBus

**AI agents wake up with amnesia, and the people who hand work to each other aren't much better.**
**CATBus is an open protocol for recovering and transferring working state, so when a session ends, a model runs out of tokens, or a role changes hands, the next owner picks up instead of starting over.**
Messages carry the handoffs; a repository holds the memory. [Why CATBus exists](docs/why.md)

```
 /\\  /\\     [CATBUS]
/  --  \\    Cross-Agent Transfer Bus
(  o  o  )   Self-mail JSON on one mailbox
 \\  ==  /
```

<p align="center">
  <img src="assets/logo-mark.svg" alt="CATBus mark" width="160" />
</p>

**CATBus (Cross-Agent Transfer Bus)** is a free, open-source protocol for serverless, asynchronous tasking and telemetry among agents over ordinary email — plus a governed plain-text memory model so cold seats can boot. No broker. No extra infrastructure. There is still a hub, but it's a coordination role (protocol owner, role registry, boot point), not a server, so it can be re-seated like any other role ([`docs/fleet-continuity.md`](docs/fleet-continuity.md)). The documents and schemas in this repository are free to use under the MIT license.

| Pin | Value |
|-----|-------|
| Protocol | `catbus` **0.5.0** ([`schema/protocol-version.json`](schema/protocol-version.json)) |
| Envelope | `v: "2"` |
| License | MIT |
| Repo | [`github.com/catbusfleet-org/catbus`](https://github.com/catbusfleet-org/catbus) |

## What's new in 0.5.0

- **T0–T3 governance** at **local / fleet / org** scales ([`docs/memory.md`](docs/memory.md), [`docs/scales-and-push-down.md`](docs/scales-and-push-down.md))
- **Memory lake + threads** with SHARE/SENS labels (fail-closed) ([`docs/memory-lake-and-threads.md`](docs/memory-lake-and-threads.md))
- **Physical first-mint boot pack** ([`boot/`](boot/)) — paste flat files, open `00_BOOT.md`, boot
- **Edge share** framed MVP ([`docs/edge-share.md`](docs/edge-share.md)) — whoami is data, not proof
- **Secure human intake** required ([`docs/secure-intake.md`](docs/secure-intake.md))
- AI consensus: **moot locally**, may **advise in fleet**, **banned as org governance**

## How do I use this?

Humans do **not** need to learn CATBus. It is **model-to-model** architecture. Hand [`docs/00-stand-up-order.md`](docs/00-stand-up-order.md) to your shared-mailbox central agent. It interviews, configures, mints hub and peer cards, and maintains topology. You answer short questions and reply **GO** only when the hub surfaces a predictable gate.

For a single seat without the mail bus yet: drop [`boot/`](boot/) into a folder the model can open, point it at `00_BOOT.md`, and run the boot check. Seed items start as candidates; none bind until you GO them.

Hub contract: [`prompts/hub.md`](prompts/hub.md). Why (amnesia **and** anti-fabrication): [`docs/why.md`](docs/why.md).

## Transport

Bus traffic is **exclusively self-mail on one shared mailbox** that the agents can send to and read (Gmail, or another mailbox with that access).

- **From = To = the owner's mailbox.**
- There are **no external SMTP recipients** for bus packets.
- `sender` and `target` are callsigns inside the JSON, not other inboxes.

Production deployments keep private wire tags, private callsigns, and binding checks **out** of this repository. Public examples use `[CATBUS]` and `@example.com` / `@example.org` / `@example.net`.

## Mailbox rules

Create an inbox filter or mailbox rule on the subject wire tag so bus and bot traffic does not bury the human inbox.

- Pattern: subject contains the wire tag.
- Public demo: subject contains `[CATBUS]`. Gmail-style query: `subject:[CATBUS]`.
- A private tag, if you use one, is not published here.

Tag match is routing, not authentication.

## Will this work for your AI agent fleet?

The go/no-go is the **Will this work?** table in [`docs/peer-capability-matrix.md`](docs/peer-capability-matrix.md).

| Mark | Meaning |
|------|---------|
| 🟢 YES | Closes the hub loop unattended |
| 🟡 YES (but …) | Does, if the caveat on that row is true |
| 🟠 Maybe (why) | Not a yes |
| 🔴 NO (why) | Cannot |

Ping/pong before you depend on a seat.

## Security hierarchy

| Order | Component | Status | Doc |
|-------|-----------|--------|-----|
| 1 | Asset-based threat model | **MUST** before production peers | [`docs/threat-model.md`](docs/threat-model.md) |
| 2 | Secure human intake | **Required** | [`docs/secure-intake.md`](docs/secure-intake.md) |
| 3 | Cleartext sterile payload | Preferred baseline | [`docs/secure-payload.md`](docs/secure-payload.md) |
| 4 | Message signing + reply-chain hash | **OPTIONAL**, **recommended** | [`docs/signing.md`](docs/signing.md) |
| 5 | Opaque secure envelope | **OPTIONAL**, **advised against** | [`docs/secure-envelope.md`](docs/secure-envelope.md) |

Readable JSON plus optional signing is the path. Opaque envelopes are not a stronger default. Summary: [`docs/security.md`](docs/security.md).

## Memory and governance

Memory is a governed publishing system, not an automatic side effect of conversation.

- **Local:** human rules; local T3 is self-keep + disclose (nonbinding).
- **Fleet:** AI consensus may **advise**; humans judge.
- **Org:** AI consensus **banned** as governance; humans govern humans.

Records (lake + threads) never promote into tiers. Lessons become new T3s/proposals that cite them. Ratification uses the verifiable human channel in [`docs/memory.md`](docs/memory.md). Free text becomes an instruction only at the secure mouth.

## What's in this repo

| Path | Purpose |
|------|---------|
| [`boot/`](boot/) | Cold-start first-mint pack (`00_BOOT.md` entry) |
| [`docs/why.md`](docs/why.md) | Purpose, failure modes, architectural intent |
| [`docs/memory.md`](docs/memory.md) | T0–T3 governance model |
| [`docs/memory-lake-and-threads.md`](docs/memory-lake-and-threads.md) | Lake records, threads, SHARE/SENS |
| [`docs/scales-and-push-down.md`](docs/scales-and-push-down.md) | Local / fleet / org overlays |
| [`docs/edge-share.md`](docs/edge-share.md) | Peer edge share (framed MVP) |
| [`docs/00-stand-up-order.md`](docs/00-stand-up-order.md) | Interview, liveness, cards, topology |
| [`docs/peer-capability-matrix.md`](docs/peer-capability-matrix.md) | Seat fit check |
| [`docs/best-practices.md`](docs/best-practices.md) | Living practices |
| [`docs/threat-model.md`](docs/threat-model.md) | Asset-based threat model (**MUST**) |
| [`docs/secure-intake.md`](docs/secure-intake.md) | Secure mouth (**required**) |
| [`schema/protocol-version.json`](schema/protocol-version.json) | Protocol pin |
| [`schema/catbus-envelope.schema.json`](schema/catbus-envelope.schema.json) | Envelope schema (v2) |
| [`prompts/`](prompts/) | Drop-in hub and peer prompts |
| [`examples/`](examples/) | ping/pong and ask/ack samples |
| [`CHANGELOG.md`](CHANGELOG.md) | Keep a Changelog |

## Envelope (public v2)

Minimum fields:

```json
{
  "v": "2",
  "event": "ping",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440001",
  "sender": "orchestrator",
  "target": "worker-node",
  "payload": {}
}
```

Body: optional one-line note; exactly one fenced `json` block; no secrets in JSON.

## Subject line (illustrative)

```text
[CATBUS] REQ: ping
[CATBUS] RES: pong
```

`[CATBUS]` is the **public demo** tag. Matching the pattern is not authentication.

## What this repo does not publish

- Real mailbox addresses or account identifiers
- Production subject tags or filter-rule names
- Live callsign lists or hub peer lists
- Credentials, app passwords, tokens, or routine identifiers

See [`docs/security.md`](docs/security.md) and [`docs/threat-model.md`](docs/threat-model.md).

## Status

**Public release 0.5.0.** Envelope major stays `v: "2"`. Formal machine schemas for LOCATOR/SHARE/SENS follow in `0.5.1`; until then those labels are conventions the boot pack (and later the Minter) enforce.

## License

MIT — see [`LICENSE`](LICENSE).
