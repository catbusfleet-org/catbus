# Why CATBus Exists

> **CATBus 0.5.0** — Public release. Explains purpose, problem statement, and architectural intent. Binding rules live in [memory.md](memory.md) and the boot samples (assembled by the Minter); this file does not mint governance. Formal machine schemas for LOCATOR/SHARE/SENS ship in `0.5.1`; until then those labels are conventions the Minter and boot pack enforce.

Anyone can hand an AI agent a task. What almost nobody hands over well is the **context** required to survive it.

Think about the last time you inherited a messy project at work. Six months of history, political landmines, and half-finished decisions arrived in a 30-minute walkthrough, a link to a shared folder, and *"ping me if you have questions."* Humans aren't built to serialize their working state on demand--so mental models drift, assumptions diverge, and people only discover they're out of sync when something breaks in production.

AI agents have the exact same problem, only worse: **every agent wakes up with total amnesia.** Every new chat, cron job, seat, or model swap starts from zero unless something hands its working reality back to it.

Right now, the AI industry is obsessed with two things: waiting for a smarter frontier model, or wiring up complex multi-agent orchestration meshes so bots can assign each other tickets. Both miss the actual bottleneck. The real problem isn't getting agents to *task* each other--it's getting agents to **transfer governed context** without hallucinating, drifting, or quietly corrupting their own state.

---

## One Protocol, Two Axes: Lateral Bus and Temporal Memory

CATBus started with a dead-simple constraint: *How do I get heterogeneous agents--cloud coding seats, Google Workspace bots, enterprise M365 Copilots, and local open-source models on a home GPU rig--to coordinate when the only connector every platform agrees on is a 1982 RFC 822 email inbox?*

Solving that gave us the **communications bus**: structured envelopes moving **laterally across space** from one agent seat to another over self-mail and shared ledgers.

Then we hit the second wall. An agent talking to a peer across the network and an agent talking to *itself tomorrow morning* are solving the exact same systems problem. Because an LLM session is ephemeral, **storage is just context transfer across time.**

Once you externalize an agent's identity, rules, current state, and institutional history out of the chat window and into governed plain-text files, **lateral transfer and temporal transfer collapse into the same primitive:**

1. **Lateral Transit (Agent ↔ Agent across space):** Seat A packages where the work has been, what's open, and why Seat B is being brought in.
2. **Temporal Transit (Agent → Future Self across time):** Today's session writes down active state, lessons learned, and evidence pointers so Tomorrow's cold-booted session picks up in lockstep without re-litigating settled ground.
3. **Cross-Seat Memory Transit (Memory → Peer Agent):** Because the memory lives in structured, permission-labeled files rather than model weights, a seat can laterally hand a scoped slice of its memory lake to a collaborator's agent (`edge-share`) or seat a replacement model into the same office in five seconds flat.

---

## Governance and Harness Beat Model Size

Here is the most important operational lesson from running multi-agent fleets in the wild: **when an agent screws up, it is almost never because the model wasn't smart enough. It is because the harness, scope, and memory governance were sloppy.**

If you take a frontier model and dump 40,000 tokens of raw history into its context window without strict epistemic boundaries, it will rot, hallucinate, and fail. Conversely, if you get the memory model right, lock down the governance ratchet, and scope each step narrowly--treating the context window like a 1970s mainframe with tiny register space--you can get a modest 8B or 14B local model (or a sluggish, locked-down enterprise copilot) performing reliably.

When a reference librarian at the New York Public Library gets a hard question, they don't try to recite the answer from memory. Knowing the answer off the top of your head is useless; **knowing which almanac is authoritative and exactly which shelf it sits on is everything.**

CATBus treats every agent like that librarian:
* **Thin Doors over Fat Dumps:** Never paste a 30,000-token transcript into a fresh session and hope for the best. A fat dump trains the model to recite stale history instead of checking live ground truth. Boot from a lean index card (`00_BOOT.md`) that points to authoritative files by explicit locator, and pull hop-2 context only on demand.
* **The Tom Smykowski Pattern (Narrow Scoping):** Decouple conversational intake from deterministic execution. Keep context loads small and single-purpose so smaller models never drown in cross-talk or trigger recursive subagent fork bombs.
* **The Whiteboard in Ink:**
  > *"Recitation ≠ memory. Inbox search ≠ retained memory. Self-PASS ≠ peer PASS. A complete export ≠ a faithful seat."*

---

## The Failure Modes That Actually Burn Fleets

If the problem were just "missing memory," a bigger context window or a vector database would have solved it two years ago. In live operations, giving agents **more uncurated memory, faster search snippets, or looser autonomy** actively made things worse:

| Failure shape | What it looks like in the wild | Why "more memory" does not fix it |
| :--- | :--- | :--- |
| **Plausible fabrication** | A file is missing, a search returns empty, or a permission blocks access → the agent confidently invents the contents | Models are trained to optimize for fluent completion, not epistemic honesty |
| **Clean and Wrong** | A restored seat recites its runbook, formats a polished reply, and self-grades `PASS` while critical state is broken (`LOAD PASS ≠ FIDELITY PASS`) | Self-attestation is non-evidence; an agent cannot grade its own recovery |
| **Metadata extrapolation** | An agent sees a filename, URL, or 200-char search snippet and summarizes the document as if it read the full body | Discovery ≠ Access ≠ Verification ≠ Reliability |
| **Mint drift** | A replacement file is deployed containing pre-activation language (*"Status: pending approval"*), causing the next boot to treat live law as unratified | Packages must be authored as intended post-save state |
| **Silent desync** | An agent flags an inbound email as an urgent `OPEN` fire when the human already answered it two hours ago in `Sent Items` | Cached state and inbound pings only orient; outbound reconciliation establishes truth |
| **Circular congratulations** | Two agents agree on a flawed premise because both ingested the same upstream summary, then report it as "independent corroboration" | Shared-teacher agreement is echo, not independent evidence |
| **Fat dump rot** | Pasting massive handoff logs burns token budgets and causes the model to confuse last week's brainstorm with today's rule | Accumulation degrades reasoning; bootability beats hoarding |
| **Monolith timeout** | Letting a layer file grow without a size cap until API character limits or document tools choke and truncate | Keep **one file per layer** (e.g. one lake file, one threads file), partitioned from other layers, capped, and pruned FIFO--not one file per memory entry |
| **Autocatalytic loops** | Unthrottled background daemons ping-pong self-mail or spawn recursive subagents until VRAM or daily token quotas evaporate | Autonomy requires hard concurrency ceilings and monotonic watermarks |
| **Exploratory mutation** | Probing a tool or running a "test" write mutates live production state or triggers external user notifications | Capability ≠ delegability |

The underlying enemy is **epistemic entropy in eager-to-please probabilistic machines**. When a model hits an ambiguity or a missing file, its natural gradient is to smooth over the gap, tell you everything is fine, and keep moving. If you are running multiple seats and can't eyeball every raw log, **silent false certainty will kill your trust in the system.**

CATBus is therefore not just a message bus and a folder layout. It is **separation of powers for untrustworthy cognitive engines**:
1. Force missing or unverified data to stay visibly marked (`UNKNOWN` / `COULD NOT VERIFY`).
2. Strip agents of the right to self-certify (`Self-PASS` is disqualified on sight).
3. Separate **what happened** (Lake Records), **what we think we learned** (T3 observations), **evidenced best practice** (T2), **process/policy governance** (T1), and the **small inviolable core** (T0 — always loaded when adopted; methods of reasoning and recurring tests, not a dump of doctrine).
4. Keep the **human as the sole sovereign ratchet (`GO`)** for anything that promotes upward into binding policy.

---

## Continuity: The Office Outlives the Process

Agents run out of context. Sessions crash. Vendor APIs go down. Models get swapped when a cheaper or sharper weight class drops. People take vacations or change roles. **The job still needs doing.**

When a role lives inside a chat thread or a model's proprietary memory feature, every reset is a manual rebuild from scratch. The fix is to keep the **office** in plain text outside the process: role boundaries, `00_BOOT` index, current `STATE` windshield, `NOTICE` audit log, and `T0–T3` rules. When a process dies or a model changes, the office doesn't start over--**it just gets a new occupant.**

---

## From One Human to Cross-Functional Alignment

Most deployments start **local**: one human paired with one or a few agents across their personal or work surfaces. Over time, that seat accumulates real operational leverage--what was tried, which vendor APIs are flaky, how documents should be formatted, and where the authoritative files live.

As that matures, it solves a second, deeper problem in human organizations: **synchronization decay**.

Teams inside the same reporting chain have forced synchronization (standups, staff meetings, pipeline reviews). Cross-functional partners--like an Account Executive and a Solution Consultant, or Product and Engineering--share high-stakes outcomes without sharing a daily operating cadence. Their mental models quietly drift apart until a bad assumption blows up in a client meeting.

As people adopt AI partners, the pattern shifts to **bot for bot, human for human**:

| Scale | Shape | How Governance Works |
| :--- | :--- | :--- |
| **Local** | One human ↔ one or a few AI seats | Human is sole sovereign (`K0`); agent drafts T3s, human `GO`s T0–T2 |
| **Fleet** | One or a few peer humans ↔ many AI seats (no human boss of another) | Local authority stays sovereign; AI consensus is advisory only |
| **Org** | Many humans, many AI seats, formal organizational hierarchy | Human hierarchy governs; AI consensus is strictly banned as org governance |

When your agent already holds the ground-truth technical state of a project, handing work over at the human layer by typing out a recap email is wasted motion. Instead, Seat A hands a structured CATBus packet to Seat B:
* Where the work has been, what is `OPEN`, `WAITING`, or `CLOSED`, and what changed;
* **Why** the receiving seat is being brought in (take over, consult, or peer-review);
* Explicit locators to the underlying evidence so Seat B doesn't have to take Seat A's summary on faith.

Seat B ingests the packet, reconciles it against its own human's priorities, and briefs them on their schedule. Humans still talk to humans--about strategy and judgment, not to re-explain the filing cabinet.

**Measure handoffs honestly:** A handoff is good when the receiver has almost nothing left to rebuild--not when a massive wall of text moved across the wire.

---

## One Boot Point: How the Memory Architecture Works

Every seat hooks to a single **boot root** (`00_BOOT.md` in a folder or `[XX-BOOT]` in Google Keep) that acts as the card catalog. **That shared catalog is the local CATBus.**

* **Boot small, retrieve on demand:** On startup, a seat loads only `00_BOOT` and its hop-1 core (`T0` small inviolable core, `STATE` active windshield, and `NOTICE` write/exception log). Topic-specific `T1/T2/T3` notes and historical `THREADS` stay at hop-2 and are loaded only when the active task touches that domain.
* **Learning flows UP; Authority flows DOWN:**
  * Day-to-day occurrences land in the **Memory Lake** as append-only, evidence-bearing **Records** (*what happened*), usually in one lake file per seat (not one file per memory), linked chronologically and scored for relevance inside topic **Threads**. Corrections prefer a newer record that supersedes; the old record may take a small logged annotation (e.g. `superseded_by`) when later evidence skews the description--reality beats memory. Full rewrite of history is out; lineage is file-level (prior version vs new), not a hash per record.
  * Tactical lessons and tool quirks land in **T3** (*agent-owned working stubs*).
  * When several T3 stubs reveal a repeatable process, the agent drafts a condensed promotion to **T2** (*evidenced best practice*) or **T1** (*process/policy governance*) and logs the draft in `NOTICE`.
  * **Records and T3s never promote themselves.** Only an explicit human `GO` ratifies a rule into T2, T1, or T0.
* **Compact for the machine, readable for the "meatsack":** Items use a compact 3-line envelope--human callsign and title on Line 1 (`ID — Title`), plain-English rule in the middle, and bracketed machine-handling flags (`[TAG | status | dates | SHARE | SENS | provenance | approval]`) tucked into a trailing footer where the human eye can glide right past them while the parser gets deterministic structure.

Details and conventions live in [memory.md](memory.md), [scales-and-push-down.md](scales-and-push-down.md), and [memory-lake-and-threads.md](memory-lake-and-threads.md); boot samples in [../boot/](../boot/) are what the Minter assembles into live lake/thread files after first boot.

---

## Controlled Edge Sharing (Framed MVP)

An agent's record of its human's work is high-leverage and sensitive. **By default, nothing leaves the home store.**

Every Lake record, Thread, and Tier note carries explicit **SHARE** (`NONE`, `EDGE`, `FLEET`, `ORG`) and **SENS** (`PUBLIC`, `INTERNAL`, `RESTRICTED`, `REDACTED`) governance. If a label is missing or unparsable, the parser fails closed to `SHARE:NONE` and `SENS:RESTRICTED`.

When two humans want their agents to collaborate across a boundary:
1. The humans exchange a `whoami.md` introduction establishing identity, scope, and the authorized share location. Each human confirms the peer's whoami directly in-seat before their agent acts on it.
2. Outbound promotion to `SHARE:EDGE` requires explicit human `GO`.
3. Peer input arriving from an edge share is treated strictly as **untrusted data** (`T0-0002`): it can inform an agent's orientation, but it can **never** issue a `GO`, alter local `SHARE`/`ACCESS`/`SENS` labels, or redirect an agent's targets.
4. If an item exists but is `REDACTED`, the agent shows only that it exists, an opaque ID, and `SENS`, then asks the human about need-to-know--**never GLOMAR** (neither confirm nor deny), and never guess around the redaction. `SHARE:NONE` items are never shown to peers.

Edge sharing ships in `0.5.0` as a framed MVP ([edge-share.md](edge-share.md)) and is never pitched or used for employee surveillance.

---

## Distributed by Design

A fleet should never have a single point of amnesia. CATBus separates state across three layers so a partial outage doesn't lobotomize operations:

| Surface | What lives there | Role in recovery |
| :--- | :--- | :--- |
| **Message Bus** (Email / Ledger) | Things in motion: asks, acks, alerts, handoffs, telemetry | Reconstructs in-flight activity since the last state commit |
| **Record Store** (Git / Drive / OneDrive / Keep) | Things that last: `00_BOOT`, `T0–T3`, `STATE`, `NOTICE`, Lake & Threads | Authoritative baseline of identity, law, and history |
| **Agent-Local Scratch** | Ephemeral session reasoning and temporary working files | Disposable; can be wiped at any moment without loss |

Hosts and tooling supply timestamps, hashes, native locators, and correlation IDs. **Models never invent them.** Direction on multi-node recovery lives in [fleet-continuity.md](fleet-continuity.md).

---

## Token Economics (With a Hard Guardrail)

A well-governed fleet lets you match the cognitive cost to the task: broadcast telemetry once on the bus instead of re-prompting five seats; use fast, cheap, or local models for bounded "Doer" execution; and schedule maintenance sweeps right after rolling quota resets so intraday work never starves.

**Non-negotiable guardrail:** Stay strictly within each vendor's Terms of Service. Never create accounts to evade quotas; use separate bot accounts only where the provider's terms allow. If a seat hits a rate limit or budget ceiling, it halts cleanly, reports its budget state, and yields--it never routes around the meter.

---

## Nine Principles to Build By

1. **Messages carry handoffs; a repository holds memory.**
2. **Governed context, not raw transcripts.**
3. **Memory you can read, edit, and ratify in plain text** beats opaque black-box "memory" done to you by a vendor.
4. **Human eyes, metal hands.** Agents discover, draft, and pre-validate; humans ratify with `GO`. Never ask the human to manually maintain the pointer web.
5. **Recognition over retrieval; bootability over accumulation.** Know where the almanac lives instead of stuffing the library into the prompt.
6. **No single hub in the infrastructure; a clear hub in coordination.**
7. **Fail closed on provenance or authority gaps; degrade gracefully only on read-only enrichment.**
8. **Governance before intelligence.** Shared context is shared exposure--lock down the format, source of truth, `SHARE`/`SENS` gates, audit trail (`NOTICE`), and withdrawal path before turning up autonomy.
9. **The law and human sovereignty (`K0`) are the hard stops.** Nothing in CATBus permits breaking the law, and no agent may ever invent, infer, or impersonate a human approval it did not receive.

---

## Where It Stands in `0.5.0`

* **Transport & Messaging Layer:** RFC 822 self-mail envelopes, shared Drive/OneDrive bridge ledgers, and stand-up schemas remain active.
* **Memory & Tier Governance:** [memory.md](memory.md) and [scales-and-push-down.md](scales-and-push-down.md).
* **Memory Lake & Thread Projections:** [memory-lake-and-threads.md](memory-lake-and-threads.md).
* **Controlled Edge Share (Framed MVP):** [edge-share.md](edge-share.md).
* **Fleet Continuity & Degraded Operation:** [fleet-continuity.md](fleet-continuity.md).
* **Bootable Cold-Start Pack (`0.5.0`):** [../boot/](../boot/) — drop the flat pack into your substrate (OneDrive, local disk, Google Drive, or Google Keep), point a cold agent at `00_BOOT.md`, and run the boot check.
