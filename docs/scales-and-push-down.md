# Scales and push-down

> **0.5.0** — companion to [`memory.md`](memory.md).

CATBus memory runs at three scales. Use the scale that matches who can boss whom — not how many GPUs you own.

## Scale definitions

| Scale | Humans | Agents | Human hierarchy |
|---|---|---|---|
| **Local** | One human (sometimes a few co-equal collaborators on one seat) | One AI, or a few AIs under that human | No human is another human’s boss in this scope |
| **Fleet** | One human, or a few humans | Many AIs | Flat among humans: no human is the boss of another human |
| **Org** | Many humans | Many AIs | A company or organization: clear human hierarchy; humans have bosses |

If a human can fire, override, or assign another human in the same governance scope, you are in **org**, not fleet.

## What belongs where (push-down guideline)

Push **down** (toward local) anything that is preference, surface quirk, or pair-specific workflow. Push **up** (toward fleet/org) only what must bind more than one seat or protect the entity.

| Kind of material | Local | Fleet | Org |
|---|---|---|---|
| Inviolable methods of reasoning (Discovery≠Access, claim≠proof, present-tense mint, fail-closed on provenance) | Yes (human-approved T0) | Shared copy or pointer OK if identical | Org T0 may mandate minimums |
| Process / policy (how mail is handled, who may mint, promotion channel) | Pair-specific T1 | Fleet T1 when every seat must match | Org T1 for entity policy |
| Evidenced best practice | Local T2 + deviation→T3 | Fleet T2 when scars are shared | Org T2 with human concurrence |
| Sticky notes / local judgment | Local T3 (self-keep + disclose) | Not pushed as binding; may advise | Org T3 only if human-approved and binding |
| Secrets, wire tags, host maps, personal data | Local private store / never in shared boot | Fleet ops lumber room if needed; never public | Org secrets vault; never in agent lake |
| Cross-seat telemetry / edge reports | Optional local log | Fleet shared records (human-gated publish) | Org reporting systems |
| Preferences (tone, schedule windows, tool quirks) | Local T3 / state | Share as advisory only | Org style guides only if human policy |
| Legal / compliance / security veto lanes | Local stricter OK | Fleet security seat veto | Org security + counsel; law hard-stops |

**Local may only add stricter controls** compatible with fleet/org overlays. It may not weaken them.

**Org wins over fleet wins over local** on conflict, unless a higher scale explicitly delegates a decision down.

## AI consensus by scale

| Scale | AI consensus |
|---|---|
| **Local** | Moot. One human, their AIs. The human rules. |
| **Fleet** | May **advise**. Humans judge. Silence, absence, and abstention are not assent. AI consensus never governs humans. |
| **Org** | **Banned** as a governance step. Orgs govern from **human** consensus (and hierarchy). A fleet under an org may still use AI consensus to advise that fleet’s humans; it still cannot govern humans. |

## Committee of two

**Fleet only:** for a fleet-scoped promotion recommendation, a proposer and a different seconder (different principals) may recommend; human GO still required.

**Org:** promotion is more complex (lanes, vetoes, human hierarchy). Not specified as “committee of two” here; see [`memory.md`](memory.md) org section and future org-promotion design.

## Edge share (pointer)

Edges report facts upward as **records**. Management aggregates and reports. Telemetry does not become T0–T3 by volume or agreement. See [`edge-share.md`](edge-share.md).
