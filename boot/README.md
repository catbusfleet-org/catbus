# CATBus local first-mint boot pack (0.5.0)

Flat file set. Paste the whole folder where your model can open files by name. Point the seat at `00_BOOT.md` and tell it to boot.

No minter in this mint. You place and update files. Author replacements as intended post-save state. Present tense only.

## How to place

1. Copy every file in this directory into one folder the assistant can read.
2. Keep filenames as shipped. Do not rename `00_BOOT.md`.
3. Fresh session. Give only the path or link to `00_BOOT.md` and the instruction to follow it.
4. First boot: review seed IDs. None start promoted. `GO {ID} candidate to adopted` (or clearer) per item; leave the rest candidate.
5. Run `BOOT_PEER_TEST.md` with a peer grader when you want a real PASS (human calls PASS).

## Load order

`00_BOOT.md` → `T0.md` (adopted only bind) → `STATE.md` → `INDEX.md` → hop-2 by LOCATOR. Parables are hop-2 only, not always-on.

## Compact envelope (agents always write this)

```
{ID} — {Title} ::
{plain-text body}
[{STATUS} | c:{date} u:{date} | rev:{x} | SHARE:{x} | SENS:{x} | src:{x} | app:{x}]
```

Missing SHARE means NONE. Missing SENS means RESTRICTED. Item beats header. Header SHARE inheritance needs app GO on the header.

## Files

00_BOOT.md — boot root / operating instructions  
INDEX.md — card catalog with LOCATORs  
T0.md — seed T0 candidates  
T1_SEED.md / T2_SEED.md / T3_SEED.md — seed candidates  
PARABLES.md — sample parables (non-binding; hop-2)  
STATE.md — seat card  
NOTICE.md — disclosure digest  
WHOAMI.md — peer edge introduction + SHARE_LINK  
LAKE_SAMPLE.md / THREAD_SAMPLE.md / EDGE_REPORT_SAMPLE.md — EXAMPLE — not loaded  
BOOT_PEER_TEST.md — peer-graded boot test  

Docs: docs/memory.md, docs/memory-lake-and-threads.md, docs/edge-share.md, docs/why.md

Never GLOMAR: exists but redacted → say so → ask human need-to-know.
