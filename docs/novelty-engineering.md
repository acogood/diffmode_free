# Novelty engineering: why the output isn't default LLM answer

Internal reference. Answers one question in full: **what stops this pipeline from returning
the averaged growth playbook any LLM produces when asked "give me growth tactics"?**

Source for buyer-facing copy (README §"Why it's different", landing pages, posts) — every
claim below is backed by a specific line in a shipped skill, cited so the doc can be
re-verified after edits. Does not ship (`docs/` stays out of `plugin/`).

## The problem being solved

"Come up with growth tactics for X" is answered from parametric memory. The model retrieves
the centroid of everything it read about growth marketing and paraphrases it: build in
public, write SEO content, post on LinkedIn, do cold outreach, start a newsletter. The
answer is fluent, plausible, and identical to what every competitor gets from the same
prompt. Prompt-level fixes ("be creative", "be unconventional", "think outside the box")
don't help — they change the adjectives, not the core action.

## The core inversion

**The pipeline never asks the model to invent a tactic.** It asks it to research, mine,
combine, and reject. Generation sits downstream of a research corpus and a combinatorial
draw; novelty is not produced, it is *what survives* a stack of rejection gates.

Seven layers, in execution order.

---

## Layer 1 — The input is research, not memory

`growth-factors-mining` builds a fresh LIGHT vector DB every run from public case studies.

- **Memory is banned as a source.** "You MUST build this **only** from freshly researched
  public sources" — `plugin/skills/growth-factors-mining/SKILL.md:17`. Web research is
  "the ONLY source of vectors" (`:38-39`).
- **Each vector carries real evidence + a reachable `source_url`**; fabricated sources or
  metrics are a checklist failure (`:116`, `:157`, `:205`).
- **Distillation is to the atomic mechanism**, not the tactic: one case study yields 1-3
  vectors describing *why* it worked, with transferability and `saturation_risk` (`:80`,
  `:181-183`). Failure modes stay in the record — that's what makes a later combination able
  to close one.
- **Cross-industry examples are forced** — 2-3 examples in *different* industries than the
  source (`:155`), which is what makes a mechanism transferable rather than a war story.

Net effect: the raw material of synthesis is ~20-40 evidence-backed mechanisms mined this
week, not a compressed memory of 2019 growth blogs.

## Layer 2 — Constraints are pre-committed before synthesis opens

`lite-constraints` writes `synthesis-constraints.json` *before* any tactic exists. The
synthesis stages read it as input, so they cannot negotiate with it.

- **`prohibited_combinations`** — pairings banned a priori because their outcome is
  conventional no matter which vectors land in them
  (`plugin/skills/lite-constraints/SKILL.md:56-67`): customer-research + content-flywheel →
  "talk to customers and write content"; build-demo + share → "build demos and share them";
  community-join + audience-borrowing → "join communities and participate"; content-flywheel
  + any SEO vector → "create content to rank"; behavioral-cohort + content-funnel → "segment
  and optimize". Each carries an `alternative` (keep one vector, swap the other).
  **This is the layer that pre-empts the default answer** — those five patterns *are* the
  default answer, and they're excluded before the model gets a turn.
- **Three mandatory pools** (`:43-54`) — A: white space; B: cross-category synergy; C:
  founder leverage (exploits this founder's rare assets, both vectors High transferability,
  ≥1 Emerging). A and B are `must_include`.
- **`unconventional_anchors`** (`:86-89`) — the most Emerging vectors, each with
  `good_partners` and explicit `avoid_partners` (the over-represented ones).
- **`anti_patterns`** (`:78-84`) — the clean-room replacement for the proprietary
  anti-vector tracking: fabricated scarcity, astroturfing, fake-door pages,
  product-dev-disguised-as-marketing, retention-not-acquisition, DIY cannibalization.
- **`category_diversity_requirements`** (`:69-74`) — no category prefix may exceed 60% of
  vectors used in synthesis.
- **Degraded-DB check** (`:119-123`) — if mined vectors collapse into <5 distinct mechanism
  verbs or one category holds >70%, the run marks `db_quality: degraded` and widens pools.
  A warning that changes behavior, not a gate that halts.

## Layer 3 — The wall (blind draw before analysis)

The strongest structural guarantee, and the only one a reader can audit from the output.

`synthesis-explore` runs two phases and **the section order in the output file is the proof
the ordering held**: `## Blind Draw (IDs only)` must physically precede
`## Vector Combinations`, which must precede `## Validated Mechanisms`
(`plugin/skills/synthesis-explore/SKILL.md:22-28`, enforced again in the output-format spec
at `:250-251` and in the checklist at `:330`).

- The blind draw commits to 15 combinations **as bare vector IDs**, drawn from the three
  pools, before any enrichment is read deeply or any tactic is considered (`:88-106`).
- Phase 1 is explicitly forbidden from naming tactics, describing execution, or picking
  channels (`:53-61`).
- `synthesis-build` has its own wall: all 4-5 white-space tactics must be written **in full,
  ignoring founder constraints**, before Phase 2 may adapt or reject anything —
  "you have NOT earned the right to reject a tactic for impracticality during Phase 1"
  (`plugin/skills/synthesis-build/SKILL.md:31-35`). The `## Pass 1 Disposition` table can
  only dispose of tactics Phase 1 already wrote, which is that wall's structural proof.

Why it matters: without the wall, a model reaches the familiar tactic first and then
back-fills a justification from whatever vectors are handy. Committing blind makes
combinatorics primary and rationalization impossible.

## Layer 4 — The negative gates

Applied to every combination and every mechanism. All blocking.

| Gate | Where | Rule |
|------|-------|------|
| **Mechanism Preview Test** | explore `:68-71` | "What mechanism results, in plain English?" Sounds like standard marketing advice → REJECT. |
| **Prohibited-combination match** | explore `:72-77` | Any pair matching a `prohibited_combinations` theme → REJECT. |
| **Replacement Rule** | explore `:84-86` | Don't skip a conventional pair — keep one vector, swap the other for an `unconventional_anchor`, re-test. |
| **Stripped Core Action** | explore `:123-125` | State the raw action in ≤5 words, **no adjectives**. Kills "compelling contrarian content"-style disguises at the source. |
| **Marketer Test** | explore `:127-129` | Would a generic B2B marketer recommend this exact raw action? "Obviously do that" → REJECT. "Risky / unusual / why would you?" → ACCEPT. |
| **Structural Rescue** | explore `:130-134` | The one override: a conventional-looking action survives if `competitor-gaps.md` Tier 1 shows a real structural barrier stopping competitors. **Max 2 per run**, tagged in the output. |
| **Emergence Proof** | explore `:136-138` | Can vector A alone produce the action? Can B alone? If **both** can → REJECT — no synthesis happened. |
| **Conventional Detection Gate** | explore `:160-164` | Re-run on the derived mechanism: strip the IDs, would a traditional marketer say "yes, obviously"? YES → derive a different capability. |
| **Reframing Test** | explore `:166-172` | Remove the adjectives (compelling, authentic, contrarian, compounding). If the core action is conventional, REJECT regardless of wording. Six named core actions are permanently conventional however dressed up. |
| **Unconventional Element Rule** | explore `:174-176` | The mechanism text must *contain* what makes it non-obvious, not merely imply it. |
| **Prototype gates Q1-Q3** | explore `:193-197` | Q1: would any marketer recommend Step 1? Q2: would Step 1 feel weird/risky? NO → conventional. Q3: can a competitor copy Steps 1-3 in 30 days with no structural barrier? YES → downgrade to "Execution Lead". |
| **Demand-gen purity** | build `:241` | Blocking pre-check: it's acquisition, not retention/product work. |
| **Competitor self-harm check** | build `:248` | Rejects tactics that only work by damaging the founder. |
| **Journalist test** | build `:189-190` | "If a journalist investigated how we execute this, would it be embarrassing?" YES → reframe or DROP. |
| **Anti-pattern validation** | build `:191-192`, `:297` | No HIGH-severity `anti_patterns` match, or an explicit exception. |

## Layer 5 — Anti-sameness (the LLM's other failure mode)

Passing the novelty gates individually still permits ten variations of "publish something".
Three mechanical diversity gates prevent it:

- **Mid-generation diversity check** after mechanisms #5, #10, #15
  (`plugin/skills/synthesis-explore/SKILL.md:218-223`): group core actions; if 3+ share one,
  a crutch is detected — keep the best 2, kill the rest. Targets ≥4 distinct core actions by
  #5, ≥7 by #10, ≥10 by #15.
- **Verb-group deduplication** (`:225-244`) — **output invalid if failed**. The first verb of
  each Day-1 action maps to one of 8 semantic groups (WRITE / BUILD / SHARE / JOIN / EXPORT /
  OPTIMIZE / PRE-SELL / ANALYZE). Hard gates: **max 2 per group**, **≥7 distinct groups**
  across 12-18 mechanisms. Violations regenerate from the same combination with a different
  first verb, favouring the underrepresented groups.
- **Category diversity** — no prefix over 60% of synthesis vectors (constraints `:69-74`,
  enforced in build).

WRITE and SHARE are exactly where a default LLM answer piles up. Capping them at 2 each
forces the tail.

## Layer 6 — The positive lens

The gates above are all negative (they subtract). Two constructs push *toward* structural
asymmetry rather than merely away from cliché:

- **Structural advantage types** (`plugin/skills/synthesis-explore/SKILL.md:178-184`) —
  Platform Arbitrage (12-24 mo) · Competitor Lockout (permanent) · Network Effect
  (compounding) · Counterintuitive (variable) · **Execution Lead (3-6 mo), explicitly flagged
  as NOT a real advantage**. "We'll just do it better" is named and demoted.
- **Guerrilla Lens** (`:199-217`) — each mechanism is tagged with 1-3 of six principles that
  work *because* the founder is small: Surprise, Intimacy, Judo, Counter-cyclical,
  Transparency/Absurdity, Compounding. Each row also states why a funded competitor
  structurally can't copy it. Zero tags → flagged `Guerrilla: none — execution lead`.

## Layer 7 — The reviewer gate

Synthesis `build` is one of two reviewer-gated stages (the other is enrichment
`competitors`). Score ≥7 to pass, max 3 retries, `blocking_issues` injected into a **fresh**
worker — never a continuation of the one that failed, so it can't defend its own output.

The rubric scores the unconventional ratio directly
(`plugin/skills/growth-reviewer/references/demand-gen-synthesis.md:176-181`):

| Score | Band |
|-------|------|
| 9-10 | ≥65% unconventional, real structural advantages, clean scope |
| 7-8 | 50-65% unconventional, clear advantages (**pass threshold**) |
| 5-6 | 35-50%, mostly execution leads, some scope creep |
| 3-4 | <35%, vectors listed rather than synthesized |

It also checks that adaptation didn't sand the edges off: preserved/adapted tactics must
still carry their unconventional core, and dropping most of the white-space exploration is
called out as a serious quality problem (`:149-152`). Final enforced mix: 3-4 white-space +
4-5 synergy/founder-fit = 7-9 tactics, ≥50% unconventional
(`plugin/skills/synthesis-build/SKILL.md:237-238`).

---

## Honest limits

State these when the mechanism claims get pushed on:

- **The free LIGHT DB is deliberately weaker** than the paid database — ~20-40 vectors mined
  per run vs. a curated, saturation-tracked corpus. Same method, thinner substrate.
- **Structural Rescue is a hole, bounded on purpose** — max 2 per run, and each must name the
  Tier-1 barrier in the output.
- **"Unconventional" is a model judgment**, scored by another model. The gates make it
  *auditable and hard to fake*, not objectively measured. The wall and the verb-group caps
  are the only fully mechanical checks.
- **It stops at ideas.** No prioritization, no sequencing, no rollout plan — that's the paid
  product. Tactics are unranked by design.

## Claims usable in public copy

Each is directly backed above:

1. "The model is never asked to invent a tactic" — generation is downstream of mining +
   a blind combinatorial draw.
2. "Combinations are committed before analysis, and the output proves it" — section ordering
   is enforced and reader-auditable in `synthesis-explore.md`.
3. "Some pairings are banned before the run opens" — `prohibited_combinations`, and those
   five patterns are precisely the default LLM answer.
4. "Novelty isn't generated, it's what survives" — a stack of blocking gates, Emergence
   Proof being the sharpest (if both mechanisms could produce it alone, it dies).
5. "Ten tactics can't all be 'write content'" — max 2 per verb group, ≥7 groups, hard fail.
6. "'We'll do it better' is not an advantage" — Execution Lead is explicitly demoted.
7. "A second model has to agree, and the first one doesn't get to argue" — reviewer gate at
   ≥7, retries go to a fresh worker.
