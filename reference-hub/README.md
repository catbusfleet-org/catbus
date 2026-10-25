# Minimal reference hub (stub)

**No live mail.** This stub validates CATBus envelope **shape** and optional **chain hash** / signature object structure for L0–L1 interop ([`../docs/interop-conformance.md`](../docs/interop-conformance.md)).

It does **not** authenticate peers, seat keys, or satisfy the threat model by itself.

## Run

```bash
cd /path/to/catbus
python3 -m reference_hub validate ../examples/ping-req.json
python3 -m reference_hub chain-demo
```

From repo root:

```bash
python3 -m reference_hub validate examples/ping-req.json
python3 -m reference_hub chain-demo
```

(Package lives in this directory; set `PYTHONPATH=reference-hub` or run as below.)

```bash
cd reference-hub && python3 -m reference_hub validate ../examples/ping-req.json
```

## What it checks

- Required fields: `v`=`"2"`, `event`, `correlation_id`, `sender`, `target`, `payload`
- Event pattern kebab-case
- Optional `signature` object shape (alg, hash_alg, key_id, sig, optional parent_hash)
- Demo chain: parent hash binds into child `parent_hash`; mutating parent breaks the link check

## What it deliberately skips

- Cryptographic verify with real keys (optional future)
- SMTP/IMAP
- Opaque secure envelopes (discouraged for hub ops)
- GO gate / seating policy
