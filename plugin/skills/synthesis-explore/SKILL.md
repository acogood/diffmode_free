---
name: synthesis-explore
description: Synthesis EXPLORE stage for the Diffmode growth-tactics pipeline (fuses the blind-combination draw + emergent-mechanism derivation — formerly two separate synthesis steps — into ONE structural-check-only stage). Reads the per-run growth-factors.json (LIGHT vector DB) + synthesis-constraints.json + founder-input + audience-jtbd + the 3 think-tank reports; draws vector combinations BLIND (IDs only, before any analysis), runs the Stripped Core Action Test + prohibited-combination + must_include checks, then derives the NOVEL MECHANISM that EMERGES from each (Reframing Test, structural-advantage classification, 3-step prototype, verb-group dedup). Outputs synthesis-explore.md — 15-20 blind combinations + 12-18 validated mechanisms, NO tactic names. Feeds synthesis-build.
metadata:
  version: "1.0.0"
---

# Synthesis — Explore (Phase 1 Blind Combinations → Phase 2 Emergent Mechanisms)

This is the FIRST synthesis stage. It fuses two jobs that MUST stay ordered: **Phase 1** draws
vector combinations BLIND (vector-first, before any tactic exists), and **Phase 2** derives the
NOVEL MECHANISM that emerges from each combination. Vector-first thinking is the novelty
engine: you commit to combinations BEFORE knowing what tactic they might produce, which is how
you escape conventional playbooks. **Output: 15-20 raw vector combinations + 12-18 validated
mechanisms. NO TACTIC NAMES. NO EXECUTION STEPS.** (Tactic design is synthesis-build's job.)

Vectors and their definitions come from the per-run `growth-factors.json` (the LIGHT DB). Do
NOT read `tactics_DB/` (clean-room — moat-critical). The category structure and
`{prefix}-NNN-slug` ID format are shared conventions; the specific IDs are whatever this run
mined.

## The two phases are WALLED — do them strictly in order

**You MUST complete Phase 1 (blind draw + combinations) in FULL before starting Phase 2
(mechanisms).** The output must physically PROVE this ordering: the section
`## Blind Draw (IDs only)` must precede `## Vector Combinations`, which must precede
`## Validated Mechanisms`. If you catch yourself deriving a mechanism (Phase 2) before the
blind draw and combinations (Phase 1) are written, STOP — you have broken the wall; go back.

## Inputs & Output

The invoker provides (do not hardcode absolute paths):

- `WS/01-diagnostics/founder-input.md`
- `WS/03-think-tanks/demand-generation/growth-factors.json` (LIGHT vector DB — vector IDs,
  categories, mechanisms, transferability, saturation_risk)
- `WS/03-think-tanks/demand-generation/synthesis-constraints.json` (mandatory pools, white
  space, prohibited combinations, category diversity)
- `WS/02-enrichment/audience-jtbd.md` (trigger events + emotions)
- Think-tank context (use if present): `WS/03-think-tanks/demand-generation/cross-industry.md`
  (transferable mechanisms worth combining), `competitor-gaps.md` (open channels/segments),
  `platform-arbitrage.md` (emerging-platform timing windows)
- **OUTPUT**: `WS/03-think-tanks/demand-generation/synthesis-explore.md`

═══════════════════════════════════════════════════════════════════════════
# PHASE 1 — BLIND VECTOR COMBINATIONS  (no tactics, no execution)
═══════════════════════════════════════════════════════════════════════════

Force exploration of vector combinations WITHOUT thinking about tactics yet. **Output of this
phase: 15-20 raw vector combinations with synergy rationale. NO TACTIC NAMES. NO EXECUTION
STEPS.**

## Critical Rules

**YOU MUST NOT:** name tactics · describe execution · pick channels · think "what marketing
to do" · generate combinations that produce CONVENTIONAL outcomes.

**YOU MUST ONLY:** explore vector synergies · explain WHY vectors combine · identify white
space · document founder leverage · **REJECT combinations that produce conventional marketing.**

If you find yourself writing a tactic name or execution step, STOP and delete it.

## Conventional Outcome Detection (BLOCKING)

Some combinations ALWAYS produce conventional outcomes regardless of framing. REJECT them
before they reach Phase 2.

**The Mechanism Preview Test** — before accepting a combination, ask:
> "If I combine these vectors, what mechanism results, in plain English?"
> If it sounds like standard marketing advice, REJECT.

**Apply `synthesis-constraints.json` → `prohibited_combinations`.** Those are theme-level
rules (e.g. customer-research + content-flywheel = "talk to customers, write content";
build-demo + share = "build demos and share them"; community-join + audience-borrowing =
"join communities and participate"; content-flywheel + any SEO vector = "write content to
rank"; behavioral-cohort + content-funnel = "segment and optimize"). Any pair whose mined
vectors match a prohibited theme is REJECTED.

**What makes a combination UNCONVENTIONAL** — its mechanism (1) a marketer would advise
AGAINST ("that's risky/unusual"), (2) competitors structurally CAN'T copy (not just won't),
(3) exploits a timing window (first-mover in an emerging space), or (4) requires a specific
founder constraint (solo founder can do what enterprise can't).

**The Replacement Rule** — don't skip a conventional pair, REPLACE it: keep ONE vector,
swap the other for a partner (ideally an `unconventional_anchor` from the constraints file)
that produces an unconventional mechanism; re-run the Mechanism Preview Test.

## Blind Vector Selection (BEFORE ANY ANALYSIS)

Complete this BEFORE reading enrichment deeply or thinking about tactics — commit to
combinations blind. Draw from the three mandatory pools in `synthesis-constraints.json`,
listing ONLY vector IDs (no descriptions/previews yet), into the output's
`## Blind Draw (IDs only)` section:

- **Pool A — White Space (5):** from `diverse_white_space` / `mandatory_combinations`
  pool `A_white_space`.
- **Pool B — Cross-Category Synergy (5):** from `mandatory_combinations` pool `B_synergy`
  (one per high-synergy category pair).
- **Pool C — Founder Leverage (5):** from pool `C_founder_leverage` — both vectors
  transferability "High", at least one "Emerging", each exploiting a specific unfair
  advantage the founder possesses.

**Checkpoint:** 15 combinations drawn blind. If any pool is short (the LIGHT DB is smaller
than the paid DB), fill from the nearest cross-category Emerging/High-transferability pairs
in `growth-factors.json` and note the substitution. **Only AFTER this may you analyze** what
the combinations might produce.

## Process

1. **Load founder context** — Industry, Budget, Team, Skills, Stage (brief).
2. **Select 2-3 category clusters that fit** — from the categories present in
   `growth-factors.json` (Structural Arbitrage, Leverage, Resource Optimization,
   Psychological, Positioning, Conversion), pick the 2-3 best-fit for this founder and say
   why (e.g. low budget + high technical skill → Structural/Resource lean).
3. **Identify synergistic pairs** — cross-category pairs from Pool B; explain which fit.
4. **Find white space** — 5-8 uncommon pairs (Pool A + others); for each: why unexplored?
   brilliant or foolish? fits constraints?
5. **Extract buyer psychology** — from `audience-jtbd.md`: Trigger Event (what happens
   24-48h before they search) + Primary Emotion; note which vectors align.

## Stripped Core Action Test (BLOCKING — run for EVERY combination)

**Part 1 — Raw Action (≤5 words, NO adjectives, no vector IDs).** Describe what the
combination produces using only verbs + nouns. ("Publish raw failure data" ✓; "Create
compelling contrarian content" ✗ — has adjectives.)

**Part 2 — The Marketer Test.** Would a generic B2B marketer recommend this EXACT raw
action? "Obviously do that" → REJECT. "That's risky / unusual / why would you?" → ACCEPT.

**Part 2b — Structural Rescue (on REJECT only).** If the Marketer Test says REJECT but the
competitor analysis (`competitor-gaps.md` Tier 1) shows a genuine structural barrier
preventing competitors from executing this exact action, OVERRIDE the reject → ACCEPT with
note `[STRUCTURAL RESCUE: <barrier>]`. The action looks conventional but competitors
structurally can't do it. Max 2 rescues per run.

**Part 3 — Emergence Proof (accepted only).** Can Vector A ALONE produce the action? Can
Vector B ALONE? If BOTH can independently → REJECT (no emergence). If EITHER alone CANNOT →
ACCEPT (true synthesis).

═══════════════════════════════════════════════════════════════════════════
# PHASE 2 — EMERGENT MECHANISMS  (what NEW thing emerges)
═══════════════════════════════════════════════════════════════════════════

Transform the Phase-1 vector combinations into the NOVEL MECHANISM that emerges from each.
**Output of this phase: 12-18 validated mechanisms with structural-advantage analysis. No
tactic names yet.**

**The test:** if you can't explain what EMERGES from the combination that neither vector
provides alone, the combination is weak — skip it.

Vector definitions come from the per-run `growth-factors.json` (each vector's `mechanism`
field — copy it into the "Vector Mechanisms" block for traceability). Do NOT read `tactics_DB/`.

## Critical Rules

**MUST NOT:** name tactics · name channels/platforms · write execution steps · jump to "how
to do this marketing." **MUST:** describe the emergent MECHANISM · explain what's NOVEL ·
identify the STRUCTURAL ADVANTAGE type · skip weak combinations.

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

## Guerrilla Lens (tag each mechanism — positive novelty, not a gate)

After the prototype gates, tag each mechanism with 1-3 guerrilla principles it exploits.
This is a POSITIVE lens — it pushes toward mechanisms that work *because* of structural
asymmetries between small and large players, complementing the negative anti-conventional
tests above. A mechanism does NOT need all six; 1-2 strong tags is fine.

| Principle | Why it works for a small player | Why a funded competitor can't copy it |
|-----------|--------------------------------|---------------------------------------|
| **Surprise** | Unexpected format, timing, or channel gets disproportionate attention | Big players plan campaigns months ahead; can't be spontaneous |
| **Intimacy** | Personal, 1:1, hand-crafted outreach converts at 10× mass marketing | Can't scale intimacy; delegating it makes it fake |
| **Judo** | Uses a competitor's size, brand, or compliance burden against them | Their size IS the vulnerability; they can't shrink |
| **Counter-cyclical** | Going against the grain (timing, pricing, positioning) buys cheap attention | Big players follow industry norms; deviating is career risk |
| **Transparency / Absurdity** | Doing something "unprofessional" works because it's honest or weird | Corporate brands get fired for this; founders get celebrated |
| **Compounding** | Many small consistent actions build an asset nobody can buy | Big players buy results; they don't build them patiently |

Write the tags as `Guerrilla: Surprise + Judo` (etc.) in each mechanism block. If a
mechanism has zero applicable tags, note `Guerrilla: none — execution lead` as a warning
(it may still pass the structural-advantage test, but it lacks the asymmetry multiplier).

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

═══════════════════════════════════════════════════════════════════════════
# Output Format  (one file — Phase 1 sections, THEN Phase 2 sections)
═══════════════════════════════════════════════════════════════════════════

Save to `WS/03-think-tanks/demand-generation/synthesis-explore.md`. The section ORDER is the
structural proof that Phase 1 preceded Phase 2 — keep it exactly:

```markdown
# Synthesis Explore — Blind Combinations & Emergent Mechanisms

## Founder Context Summary
- Industry / Budget / Team / Key Skills / Stage

## Blind Draw (IDs only)
> Drawn BEFORE any analysis (Phase 1, step 1). IDs only — no descriptions, no tactics.
- Pool A — White Space (5 pairs): `id`+`id` · `id`+`id` · … (Pool A entries are PAIRS, same as B and C)
- Pool B — Cross-Category Synergy (5): `id`+`id` · … (one per high-synergy pair)
- Pool C — Founder Leverage (5): `id`+`id` · …
- Substitutions (if the LIGHT DB was short): <pair> → <replacement id that exists in growth-factors.json>

## Selected Category Clusters
1. Primary: <category> — why; key vectors (5-7 IDs from growth-factors.json)
2. Secondary: <category> — why; key vectors
3. Tertiary (optional)

## Buyer Psychology Alignment
- Trigger Event / Primary Emotion / vectors that intercept the trigger / address the emotion

## Stripped Core Action Test
| Combination | Raw Action (≤5 words) | Marketer Test | Emergence Proof |
|-------------|----------------------|---------------|-----------------|
| A1 | ... | ACCEPT/REJECT | PASS/FAIL |

## Vector Combinations (15-20)
> **Length budget — this file has a hard ceiling.** Keep each combination to roughly 10 lines;
> if the file passes ~600 lines, stop adding combinations and move to Phase 2. This is a working
> paper the build stage reads for signal, not an essay. A one-shot write of an oversized version
> of this file has exceeded the response output limit and killed the worker outright, producing
> no file at all.

### Combination #N
- **Vectors:** `id-1` + `id-2` [+ `id-3`]   (2-3 vectors max, never 4+)
- **Pool Source:** A / B / C
- **Synergy Type:** <Category + Category>
- **White Space Status:** <occurrence note / "novel pairing in this run">
- **Raw Action (≤5 words):** ...
- **Marketer Test:** ACCEPT  · **Emergence Proof:** PASS
- **Why These Combine:** what each vector contributes (1 sentence each) + Together (2-3 sentences)
- **Why Unconventional:** reference the Raw Action
- **Founder Leverage:** 2 sentences — what unfair advantage does this exploit?
- **Buyer Psychology Fit:** intercepts trigger? addresses emotion?

## White Space Combinations
| # | Combination | Why Unexplored? | Brilliant or Foolish? |

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
**Guerrilla Lens:** <1-3 principles: Surprise / Intimacy / Judo / Counter-cyclical /
Transparency-Absurdity / Compounding — or "none — execution lead">
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

## Summary Statistics
| Total combos | Validated mechanisms | White space | Synergistic pairs | Unique vectors |
| 15-20 | 12-18 | 5-8 | 10+ | 25+ (or as many as the LIGHT DB allows) |
```

## Validation Checkpoint (before synthesis-build)

**Phase 1 (combinations):**
- [ ] `## Blind Draw (IDs only)` physically precedes `## Vector Combinations` (the wall held).
- [ ] Pools A/B/C each contributed (5 each, or noted substitutions for a small LIGHT DB).
- [ ] **Every `must_include` pair (pools A + B in `synthesis-constraints.json`) is validly
      used OR validly substituted.** Validly used = **both** of the pair's vector IDs appear
      together **inside one `### Combination #N` block** (not merely somewhere in the file —
      block-level co-occurrence). Validly substituted = an explicit one-line note that names
      the pair AND names a replacement vector **that exists in `growth-factors.json`** (use
      the Replacement Rule). A silently dropped pair, or a "substitution" whose replacement
      isn't in `growth-factors.json`, is a FAIL.
- [ ] 15-20 combinations, each with 2-3 vectors (not 4+), each explaining WHY they synergize.
- [ ] Stripped Core Action Test done for every combination: Raw Action ≤5 words no adjectives,
      Marketer Test ACCEPT, Emergence Proof PASS.
- [ ] ZERO combinations matching any `prohibited_combinations` theme.
- [ ] NO tactic names, NO execution steps anywhere.

**Phase 2 (mechanisms):**
- [ ] 12-18 validated mechanisms; each has a real emergent explanation (not vector restatement).
- [ ] Each copies its vectors' `mechanism` fields from `growth-factors.json` (traceability).
- [ ] Each has a structural-advantage type + duration; ≥50% are Arbitrage/Lockout/Network.
- [ ] ≥60% UNCONVENTIONAL (Reframing Test applied — adjectives stripped, conventional core REJECTED).
- [ ] Each has a 3-step Execution Prototype passing Q1/Q2/Q3.
- [ ] Each has a Guerrilla Lens tag (1-3 principles); mechanisms tagged "none — execution
      lead" are flagged but allowed (they still need a structural-advantage type).
- [ ] **Verb groups ≥7 and ≤2 mechanisms per group** (else OUTPUT INVALID — regenerate).
- [ ] Weak combinations documented; NO tactic names.
- [ ] Every vector ID used exists in `growth-factors.json`.

This feeds **synthesis-build** (white-space ideation → founder-fit adaptation → final
synthesis.md). Do not proceed until both phases' validation passes.
