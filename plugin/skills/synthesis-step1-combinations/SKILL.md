---
name: synthesis-step1-combinations
description: Synthesis Step 1 of 4 for the Diffmode growth-tactics pipeline (TT-DG-004a) — forces blind, vector-first exploration of growth-factor combinations BEFORE any tactic exists. Reads the per-run growth-factors.json (LIGHT vector DB) + synthesis-constraints.json + enrichment, draws from mandatory pools, runs the Stripped Core Action Test, and outputs 15-20 raw vector combinations (no tactic names, no execution). Use as the first synthesis step; its output feeds step2 mechanisms.
metadata:
  version: "1.0.0"
---

# Synthesis — Step 1: Vector Combination Exploration

Force exploration of vector combinations WITHOUT thinking about tactics yet. Vector-first
thinking is the novelty engine: you commit to combinations BEFORE knowing what tactic they
might produce, which is how you escape conventional playbooks. **Output: 15-20 raw vector
combinations with synergy rationale. NO TACTIC NAMES. NO EXECUTION STEPS.**

Vectors and their definitions come from the per-run `growth-factors.json` (the LIGHT DB).
Do NOT read `tactics_DB/`. The category structure and `{prefix}-NNN-slug` ID format are
shared conventions; the specific IDs are whatever this run mined.

## Critical Rules

**YOU MUST NOT:** name tactics · describe execution · pick channels · think "what marketing
to do" · generate combinations that produce CONVENTIONAL outcomes.

**YOU MUST ONLY:** explore vector synergies · explain WHY vectors combine · identify white
space · document founder fit · **REJECT combinations that produce conventional marketing.**

If you find yourself writing a tactic name or execution step, STOP and delete it.

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
- **OUTPUT**: `WS/03-think-tanks/demand-generation/synthesis-step1-combinations.md`

## Conventional Outcome Detection (BLOCKING)

Some combinations ALWAYS produce conventional outcomes regardless of framing. REJECT them
before they reach Step 2.

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
listing ONLY vector IDs (no descriptions/previews yet):

- **Pool A — White Space (5):** from `diverse_white_space` / `mandatory_combinations`
  pool `A_white_space`.
- **Pool B — Cross-Category Synergy (5):** from `mandatory_combinations` pool `B_synergy`
  (one per high-synergy category pair).
- **Pool C — Founder Fit (5):** from pool `C_founder_fit` — both vectors transferability
  "High", at least one "Emerging", each addressing a specific founder constraint.

**Checkpoint:** 15 combinations drawn blind. If any pool is short (the LIGHT DB is smaller
than the paid DB), fill from the nearest cross-category Emerging/High-transferability pairs
in `growth-factors.json` and note the substitution. Only AFTER this may you analyze what
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

**Part 3 — Emergence Proof (accepted only).** Can Vector A ALONE produce the action? Can
Vector B ALONE? If BOTH can independently → REJECT (no emergence). If EITHER alone CANNOT →
ACCEPT (true synthesis).

## Output Format

Save to `WS/03-think-tanks/demand-generation/synthesis-step1-combinations.md`:

```markdown
# Vector Combination Exploration

## Founder Context Summary
- Industry / Budget / Team / Key Skills / Stage

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
### Combination #N
- **Vectors:** `id-1` + `id-2` [+ `id-3`]   (2-3 vectors max, never 4+)
- **Pool Source:** A / B / C
- **Synergy Type:** <Category + Category>
- **White Space Status:** <occurrence note / "novel pairing in this run">
- **Raw Action (≤5 words):** ...
- **Marketer Test:** ACCEPT  · **Emergence Proof:** PASS
- **Why These Combine:** what each vector contributes (1 sentence each) + Together (2-3 sentences)
- **Why Unconventional:** reference the Raw Action
- **Founder Fit:** 2 sentences
- **Buyer Psychology Fit:** intercepts trigger? addresses emotion?

## White Space Combinations
| # | Combination | Why Unexplored? | Brilliant or Foolish? |

## Summary Statistics
| Total combos | From Primary cluster | White space | Synergistic pairs | Unique vectors |
| 15-20 | 8-10 | 5-8 | 10+ | 25+ (or as many as the LIGHT DB allows) |
```

## Validation Checkpoint (before Step 2)

- [ ] Pools A/B/C each contributed (5 each, or noted substitutions for a small LIGHT DB).
- [ ] **Every `must_include` pair (pools A + B in `synthesis-constraints.json`) is validly
      used OR validly substituted.** Validly used = **both** of the pair's vector IDs appear
      together **inside one `### Combination #N` block** (not merely somewhere in the file —
      block-level co-occurrence). Validly substituted = an explicit one-line note that names
      the pair AND names a replacement vector **that exists in `growth-factors.json`** (use
      the Replacement Rule). The LIGHT DB is smaller than the paid DB, so legitimate
      substitution is allowed — but a silently dropped pair, or a "substitution" whose
      replacement isn't in `growth-factors.json`, is a FAIL.
- [ ] 15-20 combinations, each with 2-3 vectors (not 4+), each explaining WHY they synergize
      and founder fit.
- [ ] Stripped Core Action Test done for every combination: Raw Action ≤5 words no
      adjectives, Marketer Test ACCEPT, Emergence Proof PASS.
- [ ] ZERO combinations matching any `prohibited_combinations` theme.
- [ ] ≥80% would make a marketer say "that's unusual."
- [ ] NO tactic names, NO execution steps anywhere.
- [ ] Every vector ID used exists in `growth-factors.json`.

This feeds **Step 2: Mechanism Synthesis**. Do not proceed until validation passes.
