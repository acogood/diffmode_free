---
name: synthesis-step2-mechanisms
description: Synthesis Step 2 of 4 for the Diffmode growth-tactics pipeline (TT-DG-004b) — derives the NOVEL MECHANISM that EMERGES from each Step-1 vector combination. Reads step1 combinations + growth-factors.json (for vector definitions), writes a 3-step execution prototype per mechanism, runs the conventional-detection gate and action-deduplication (verb-group) check, and outputs 12-18 validated mechanisms with structural-advantage classification. Use after step1; feeds pass1.
metadata:
  version: "1.0.0"
---

# Synthesis — Step 2: Mechanism Synthesis

Transform raw vector combinations into the NOVEL MECHANISM that emerges from each. **Input:**
Step-1 combinations. **Output:** 12-18 validated mechanisms with structural-advantage
analysis. No tactic names yet.

**The test:** if you can't explain what EMERGES from the combination that neither vector
provides alone, the combination is weak — skip it.

Vector definitions come from the per-run `growth-factors.json` (each vector's `mechanism`
field). Do NOT read `tactics_DB/`.

## Critical Rules

**MUST NOT:** name tactics · name channels/platforms · write execution steps · jump to "how
to do this marketing." **MUST:** describe the emergent MECHANISM · explain what's NOVEL ·
identify the STRUCTURAL ADVANTAGE type · skip weak combinations.

## Inputs & Output

- `WS/03-think-tanks/demand-generation/synthesis-step1-combinations.md` (PRIMARY)
- `WS/03-think-tanks/demand-generation/growth-factors.json` (vector definitions — copy each
  vector's `mechanism` into the "Vector Mechanisms" block)
- `WS/01-diagnostics/founder-input.md`
- **OUTPUT**: `WS/03-think-tanks/demand-generation/synthesis-step2-mechanisms.md`

## Conventional Detection Gate (BLOCKING)

For EVERY mechanism, ask: "If I stripped the vector IDs and described this to a traditional
B2B marketer, would they say 'Yes, obviously do that'?" YES → REJECT (derive a DIFFERENT
emergent capability). NO / "that's unusual" → continue.

**Anti-gaming — same thing, different words (ALL REJECTED).** Reframing a conventional
tactic with fancy language does not make it unconventional. Run the **Reframing Test:**
remove the adjectives (compelling, authentic, contrarian, compounding) — what's the CORE
ACTION? If the core action is conventional, REJECT regardless of wording. Examples of core
actions that stay conventional however they're dressed up: "talk to customers and write
content," "segment users and optimize," "share your work publicly," "build demos and share
them," "join communities and participate," "write content to rank in search."

**The Unconventional Element Rule:** the mechanism description must CONTAIN what makes it
non-obvious (e.g. "released as open datasets," "competitors avoid," "before the platform
saturates"), not merely imply it.

## Structural Advantage Types (classify each mechanism)

- **Platform Arbitrage (12-24 mo):** new platform/algorithm competitors don't grok yet.
- **Competitor Lockout (Permanent):** brand/structural constraints stop competitors copying.
- **Network Effect (Compounding):** value grows with scale; late entrants can't catch up.
- **Counterintuitive (Variable):** traditional marketers advise against it.
- **Execution Lead (3-6 mo):** "we'll do it better" — NOT a real structural advantage (flag).

## Execution Prototype (REQUIRED before validation — plain English, no jargon)

For EACH mechanism write a 3-step prototype:
1. Day 1 — what does the founder PHYSICALLY DO?
2. Day 7 — what happens next?
3. Day 30 — measurable outcome?

Then the prototype gates: **Q1** Is Step 1 something any marketer would recommend? YES →
CONVENTIONAL. **Q2** Would executing Step 1 feel weird/risky to a traditional marketer? NO →
CONVENTIONAL; YES (give the reason) → continue. **Q3** Could a competitor copy Steps 1-3
within 30 days with no structural barrier? YES → downgrade to "Execution Lead"; NO (name the
barrier) → true structural advantage.

## Mid-Generation Diversity Check (after mechanisms #5, #10, #15)

List each mechanism's core action in 3-5 words; group by similarity. If 3+ share the same
core action → crutch detected: keep the 2 with the best structural advantage, kill the rest,
and for remaining combinations deliberately seek a DIFFERENT core action. Targets: ≥4
distinct core actions by #5, ≥7 by #10, ≥10 by #15.

## Action Deduplication (verb-group — OUTPUT INVALID IF FAILED)

Extract the FIRST VERB of each mechanism's Day-1 action and group semantically:

| Group | Verbs |
|-------|-------|
| WRITE | Write, Publish, Create, Produce, Document, Blog, Author, Draft |
| BUILD | Build, Develop, Make, Code, Ship, Implement, Construct, Design |
| SHARE | Share, Post, Distribute, Spread, Release, Broadcast, Announce |
| JOIN | Join, Participate, Engage, Connect, Network, Comment, Reply |
| EXPORT | Export, Extract, Open-source, Expose, Dump, Upload, Provide |
| OPTIMIZE | Optimize, Target, Position, Format, Structure, Configure |
| PRE-SELL | Pre-sell, Validate, Test, Demo, Launch, Pitch, Sell |
| ANALYZE | Analyze, Research, Study, Survey, Investigate, Audit |

**Hard gates:** max 2 mechanisms per verb group; ≥7 distinct verb groups across 12-18
mechanisms. If violated → keep the 1-2 best per group, regenerate the rest from their
combination with a DIFFERENT first verb (favor underrepresented groups: EXPORT, PRE-SELL,
OPTIMIZE).

## Output Format

Save to `WS/03-think-tanks/demand-generation/synthesis-step2-mechanisms.md`:

```markdown
# Mechanism Synthesis
## Input Summary
- Combinations received: N · Mechanisms validated: N · Combinations skipped (weak): N

## Validated Mechanisms
### Mechanism #N (from Combination #X)
**Vectors:** `id-1` + `id-2`
**Vector Mechanisms (from growth-factors.json):**
- `id-1`: <its mechanism field>
- `id-2`: <its mechanism field>
**Emergent Mechanism:** 2-4 sentences — what NEW thing emerges (impossible with either alone)
**Why Novel:** 2-3 sentences
**Structural Advantage:** Type / Duration / Why competitors can't copy (specific barrier)
**Execution Prototype:** 1. Day 1 … 2. Day 7 … 3. Day 30 …
**Novelty Test:** Conventional Detection PASS (marketer would NOT recommend) · Emergence Yes
· Specificity Yes (unconventional element explicit)

## Skipped Combinations (Weak)
### Skipped: Combination #X — vectors — why no novel mechanism emerged

## Mechanism Classification Summary
| Type | Count | Mechanisms |
(target: ≥50% Platform Arbitrage / Competitor Lockout / Network Effect)

## Unconventional Ratio
| UNCONVENTIONAL | CONVENTIONAL |  (target ≥60% unconventional)

## Action Deduplication Result
| Distinct verb groups (≥7) | Max per group (≤2) |
```

## Validation Checkpoint (before pass1)

- [ ] 12-18 validated mechanisms; each has a real emergent explanation (not vector restatement).
- [ ] Each has a structural-advantage type + duration; ≥50% are Arbitrage/Lockout/Network.
- [ ] ≥60% UNCONVENTIONAL.
- [ ] Each has a 3-step Execution Prototype passing Q1/Q2/Q3.
- [ ] **Verb groups ≥7 and ≤2 mechanisms per group** (else OUTPUT INVALID — regenerate).
- [ ] Weak combinations documented; NO tactic names.
- [ ] Every vector ID exists in `growth-factors.json`.

This feeds **Pass 1: White Space Exploration.** Do not proceed until validation passes.
