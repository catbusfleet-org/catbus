"""CLI: python -m reference_hub validate <file.json> | chain-demo"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED = ("v", "event", "correlation_id", "sender", "target", "payload")
EVENT_RE = __import__("re").compile(r"^[a-z][a-z0-9-]{0,63}$")


def canonicalize(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def message_hash(envelope: dict[str, Any]) -> str:
    unsigned = {k: v for k, v in envelope.items() if k != "signature"}
    return hashlib.sha256(canonicalize(unsigned)).hexdigest()


def validate_envelope(env: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for k in REQUIRED:
        if k not in env:
            errors.append(f"missing required field: {k}")
    if env.get("v") != "2":
        errors.append('v must be string "2"')
    if "event" in env and not isinstance(env["event"], str):
        errors.append("event must be string")
    elif "event" in env and not EVENT_RE.match(env["event"]):
        errors.append("event must match kebab-case pattern")
    if "payload" in env and not isinstance(env["payload"], dict):
        errors.append("payload must be object")
    for k in ("correlation_id", "sender", "target"):
        if k in env and (not isinstance(env[k], str) or not env[k]):
            errors.append(f"{k} must be non-empty string")
    sig = env.get("signature")
    if sig is not None:
        if not isinstance(sig, dict):
            errors.append("signature must be object")
        else:
            for req in ("alg", "hash_alg", "key_id", "sig"):
                if req not in sig:
                    errors.append(f"signature missing {req}")
            if "parent_hash" in sig and not isinstance(sig["parent_hash"], str):
                errors.append("signature.parent_hash must be string")
    return errors


def cmd_validate(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print("FAIL: root must be object", file=sys.stderr)
        return 1
    errs = validate_envelope(data)
    if errs:
        print("FAIL:")
        for e in errs:
            print(f"  - {e}")
        return 1
    h = message_hash(data)
    print(f"OK shape  message_hash={h}")
    return 0


def cmd_chain_demo() -> int:
    parent = {
        "v": "2",
        "event": "ping",
        "correlation_id": "550e8400-e29b-41d4-a716-446655440001",
        "sender": "orchestrator",
        "target": "worker-node",
        "payload": {},
    }
    h0 = message_hash(parent)
    child = {
        "v": "2",
        "event": "pong",
        "correlation_id": parent["correlation_id"],
        "sender": "worker-node",
        "target": "orchestrator",
        "in_reply_to": "ping",
        "payload": {},
        "signature": {
            "alg": "ed25519",
            "hash_alg": "sha256",
            "key_id": "demo-worker",
            "parent_hash": h0,
            "sig": "DEMO_NOT_A_REAL_SIGNATURE",
        },
    }
    errs = validate_envelope(child)
    assert not errs, errs
    ok = child["signature"]["parent_hash"] == h0
    print(f"chain link OK={ok} parent_hash={h0}")
    # mutate parent → break
    parent_broken = dict(parent)
    parent_broken["payload"] = {"nonce": "tamper"}
    h0_broken = message_hash(parent_broken)
    broken = child["signature"]["parent_hash"] == h0_broken
    print(f"tamper detected OK={not broken} (child still points at old H0)")
    return 0 if ok and not broken else 1


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in {"-h", "--help"}:
        print(__doc__)
        return 2
    if argv[1] == "validate":
        if len(argv) != 3:
            print("usage: python -m reference_hub validate <file.json>", file=sys.stderr)
            return 2
        return cmd_validate(Path(argv[2]))
    if argv[1] == "chain-demo":
        return cmd_chain_demo()
    print(f"unknown command: {argv[1]}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
