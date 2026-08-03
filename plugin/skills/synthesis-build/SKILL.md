---
name: synthesis-build
description: Synthesis BUILD stage — the FINAL stage of the Diffmode growth-tactics pipeline (fuses white-space ideation + founder-fit adaptation & merge — formerly two separate synthesis passes — into ONE reviewer-gated stage). Reads synthesis-explore.md (the validated emergent mechanisms) + synthesis-constraints.json + growth-factors.json + founder-input + audience-jtbd + competitors-analysis + the 3 think-tank reports + the bundled 2026 channel menu. Phase 1 IDEATES white-space tactics IGNORING constraints; Phase 2 adapts them for founder constraints (preserving the unconventional core) + generates synergy/founder-fit tactics; Phase 3 merges into a final synthesis.md of 7-9 novel demand-gen tactic ideas (target 50%+ unconventional). Uses the lite anti_patterns (NOT a proprietary anti-vectors DB). The free plugin STOPS here.
metadata:
  version: "1.0.0"
---

# Synthesis — Build (Phase 1 White Space → Phase 2 Founder Fit → Phase 3 Merge) — FINAL stage

This is the **last stage of the free pipeline.** It fuses three jobs that MUST stay ordered:

1. **Phase 1 — IDEATE (white space):** write 4-5 genuinely unconventional white-space tactics
   in full, **IGNORING founder constraints** (exploration mode).
2. **Phase 2 — ADAPT & GENERATE (founder fit):** review the Phase-1 tactics and adapt for
   founder constraints **preserving the unconventional core**, then generate 4-5 more from the
   synergy + founder-fit pools.
3. **Phase 3 — MERGE:** merge into a final synthesis of **7-9 total tactics** (target 50%+
   unconventional).

It produces a portfolio of novel demand-gen tactic IDEAS and **stops**. (Prioritization,
implementation guides, and the proprietary 576-vector DB are the paid product — do not attempt
them here.)

Vector definitions come from `growth-factors.json`; pools/anti-patterns from
`synthesis-constraints.json`; the validated emergent mechanisms come from
`synthesis-explore.md`. Do NOT read `tactics_DB/` (clean-room — no proprietary anti-vectors DB;
use the lite `anti_patterns` field instead).

## The three phases are WALLED — do them strictly in order

**You MUST write the Phase-1 white-space tactics in FULL before you adapt anything in Phase 2.**
You have **NOT earned the right to reject a tactic for impracticality during Phase 1** — that is
Phase 2's job. The output PROVES the ordering held: the `## Pass 1 Disposition` table (Phase 2)
can only dispose tactics that Phase 1 already wrote in full. If you catch yourself filtering a
Phase-1 tactic for "the founder can't do this," STOP — that belongs in Phase 2.

## Inputs & Output

- `WS/03-think-tanks/demand-generation/synthesis-explore.md` (PRIMARY — the validated emergent
  mechanisms + blind combinations; Phase 1 ideates from these + `diverse_white_space`)
- `WS/03-think-tanks/demand-generation/synthesis-constraints.json` (`diverse_white_space`; pools
  `B_synergy` + `C_founder_leverage`; `anti_patterns`; `category_diversity_requirements`)
- `WS/03-think-tanks/demand-generation/growth-factors.json` (vector definitions)
- `WS/01-diagnostics/founder-input.md` (Phase 1 READS but does NOT filter by constraints; Phase
  2 applies them; goal + deadline)
- `WS/02-enrichment/audience-jtbd.md`, `WS/02-enrichment/competitors-analysis.md`
- Think-tank context: `competitor-gaps.md`, `platform-arbitrage.md` (channel selection,
  structural advantage), `cross-industry.md` (transferable mechanisms / adaptation angles for
  the new Phase-2 synergy + founder-fit tactics)
- `${CLAUDE_PLUGIN_ROOT}/reference/Marketing-Channel-Menu-2026.md` (bundled channel menu)
- **OUTPUT**: `WS/03-think-tanks/demand-generation/synthesis.md`

═══════════════════════════════════════════════════════════════════════════
# PHASE 1 — IDEATE (white space; IGNORE founder constraints)
═══════════════════════════════════════════════════════════════════════════

Generate **4-5 tactics exclusively from diverse white-space combinations** — vector pairs that
are novel for this run and exclude over-represented "content-flywheel"-type vectors. **This
phase prioritizes unconventional exploration over practicality and IGNORES founder
constraints** (Phase 2 applies them).

## Philosophy: Exploration Mode

Mindset: "What interesting mechanisms emerge from these never-combined vectors?" / "What would
a founder do with unlimited resources?" — NOT "can this founder do this?" The goal is to
discover unconventional approaches Phase 2 can refine or preserve. **Write all 4-5 tactics in
FULL here, before any adaptation.**

## Scope Enforcement — DEMAND GENERATION ONLY

Before generating ANY tactic: "Does this bring NEW PEOPLE to the site who've never heard of
the product?" YES = include; NO = delete (CRO territory).

**Engineering-as-marketing: allowed but scoped.** Building things to ATTRACT new users is
valid demand gen, but the tactic's PRIMARY purpose must be acquisition, not product
improvement. Test: if you removed the distribution/acquisition channel, would the remaining
work be on the product roadmap anyway? If YES → not demand gen.

| Tactic type | Verdict |
|-------------|---------|
| Build-to-attract (80% distribution / 20% build) | ✅ Demand gen |
| Product improvement with marketing framing | ❌ Product dev |
| Improve onboarding / re-engage churned / upsell existing | ❌ CRO / Retention |

## Process (Phase 1)

1. **Load diverse white space** from `synthesis-constraints.json` (`diverse_white_space`).
   These are pre-filtered to exclude content-flywheel-type vectors and limit repetition
   (max 2 per anchor). Display the loaded pairs in a table. **Category awareness:** aim for
   ≥2 different category prefixes across your 4-5 tactics (soft target here; Phase 2 enforces
   hard minimums from `category_diversity_requirements`).
2. **For each combination, derive the emergent mechanism** (reuse/extend the matching
   `synthesis-explore.md` mechanism where one exists): "What UNUSUAL capability emerges?" It
   must differ from what either vector produces alone and feel uncomfortable/counterintuitive.
   Do NOT consider whether the founder can execute it.
3. **Design a complete tactic from each mechanism.** Name it per the naming rule in
   `${CLAUDE_PLUGIN_ROOT}/reference/writing-style.md`: plain words that tell a smart friend
   what you'd actually do — what you do + the twist — with the unconventional mechanism
   visible in the name (not generic marketing, and not an invented codename either). No
   practicality filtering — include tactics even if they need skills/budget the founder
   lacks or feel risky.

## Kill List (still applies in exploration mode)

Skip combinations whose core action is: start a newsletter · write SEO content · build
community (join Discord/Slack) · demo the product · interview customers · improve the core
product · re-engage churned users · upgrade existing customers · improve onboarding · build
a tool/dashboard/calculator (engineering, distribution as afterthought) · create a feature
and announce it · develop an integration. If the white-space pair only produces a kill-list
action, it didn't yield anything novel — skip it.

## Self-Audit (per Phase-1 tactic)

1. **Remove all vector references** — does the tactic still sound unusual? NO → vectors are
   labels on a conventional action (regenerate from a different pair).
2. **Day-1 action on the Kill List?** YES → kill & regenerate.
3. **Marketer Test** — would a B2B marketer recommend this unprompted? YES → too
   conventional, reconsider.
4. **Cannibalization Test** — does it teach customers to DIY what the product does? YES →
   reframe (emphasize the PAIN of manual methods, don't teach the method).

**Phase-1 gate:** 4-5 white-space tactics, each from a `diverse_white_space` pair (IDs exist in
`growth-factors.json`), each passing all 4 self-audit tests, 100% unconventional target,
demand-gen only. Carry a one-line Practicality Assessment per tactic (Difficulty / Resource
intensity / Risk / Phase-2 action: Preserve / Adapt / Consider dropping) so Phase 2 can act.

═══════════════════════════════════════════════════════════════════════════
# PHASE 2 — ADAPT & GENERATE (founder leverage; ≥60% of Phase 1 PRESERVED)
═══════════════════════════════════════════════════════════════════════════

## Philosophy: Preserve the Unconventional Core (CRITICAL)

The #1 goal of Phase 2 is to PRESERVE Phase-1's unconventional mechanisms. What makes a tactic
unconventional: the **positioning** (contrarian / anti-establishment), the **structural
advantage** (competitor lockout, platform arbitrage), and the **uncomfortable edge** that
makes traditional marketers hesitate.

When adapting for constraints: **DO** reduce budget/time, simplify execution, scale down
scope — while keeping the uncomfortable positioning, the structural advantage, and the
contrarian angle. **DON'T** soften the move itself to make it "safer," replace a structural
advantage with an execution advantage, sand down the edge that creates the lockout, or drop
a tactic because the founder hasn't done it before — unfamiliarity is not a constraint. The
unconventional POSITIONING must survive adaptation — and per the naming rule (*Output
language* below), it survives in PLAIN WORDS: the uncomfortable move stays visible in the
name; the edge lives in the mechanism, never in invented vocabulary.

- BAD: "Call Out Enterprise Tools by Name in Your Docs" → "Technical Citation Authority" ❌ (the confrontation vanished → lost the lockout)
- BAD: "Anti-Enterprise Citation Rebellion" ❌ (edge hidden behind a codename — a smart friend can't tell what you'd do)
- GOOD: "Call Out Enterprise Tools by Name in Your Docs (Lean Version)" ✅ (the uncomfortable move is right in the name; only budget/time reduced)

Aim for **≥60% Phase-1 preservation** with unconventional edges intact.

## Phase 2a: Review Phase-1 Tactics (PRESERVE / ADAPT / DROP)

| Decision | Criteria | Action |
|----------|----------|--------|
| PRESERVE | founder can execute with minor adaptation | keep, small resource adjustments |
| ADAPT | mechanism valuable, execution needs rework | redesign execution, keep mechanism |
| DROP | requires more time or money than the founder has | remove (counts toward the ≤40% drop allowance) |

> **A skill the founder would need to LEARN is NOT a reason to drop.** State the learning
> cost honestly (time to competence, quality of first attempts) and keep the tactic.
> Founders will learn any channel that brings customers — unfamiliarity is not a constraint.

**Timeline gate:** if a structural-advantage timeline (6-24 mo) exceeds the founder's
deadline by >3x AND the founder has a ≤90-day deadline → ADAPT so the tactic produces
observable acquisition signal (traffic/signups/trials) within the deadline, even while the
moat builds over time. If it fundamentally can't signal within 3x the deadline → DROP.

**Adaptation rules:** budget too high → reduce scope, not approach; skill missing → state
the learning cost honestly (time to competence, quality of first attempts) and KEEP the
tactic — a founder will learn any channel that brings customers; time-intensive → phase it;
positioning feels risky → KEEP IT (the risk IS the advantage).

**DROP threshold:** at most 2 Phase-1 tactics dropped (preserve ≥60%).

**Channel-justification rule.** For each tactic, the Primary Channel choice must be
justified against the mechanism — explain WHY this channel amplifies THIS mechanism (not
just "the founder can do content"). If the mechanism would work equally on any channel,
the channel choice is arbitrary — pick the one with the lowest competitive adoption from
the matrix. The channel shapes the execution steps; it is a design input, not a label.

## Deception veto (NEVER allowed — binary, non-scored)

Reject any tactic relying on: fabricated scarcity/urgency · multi-account astroturfing /
fake social proof · fake-door pages for nonexistent features · manipulating AI search via
seeded fabricated discussions · consensus loops of fake accounts · any tactic whose core
mechanism is deception (even if effective). Also reject: targeting existing users for
upsells (retention, not acquisition). **Journalist test:** "If a journalist investigated how
we execute this, would it be embarrassing?" YES → reframe or DROP. Cross-check every tactic
against `synthesis-constraints.json` `anti_patterns` (the clean-room replacement for the
proprietary anti-vectors DB) — any HIGH-severity match is blocking.

## Phase 2b: Generate Synergy & Founder-Leverage Tactics

From `synthesis-constraints.json`: **Pool B** (synergy pairs) + **Pool C** (founder-leverage).
**You MUST generate at least 4 new tactics here** so the final set reaches 7-9 (the founder
gets a portfolio of ideas; this is where free stops, so depth-of-options matters). If you
can't find 4 quality combinations, explain why, still produce your best 4 with caveats, and
flag low-confidence ones `[LOW CONFIDENCE]`.

**`must_include` enforcement (Pool B).** Every **Pool-B `must_include` pair** must be
**validly used or validly substituted** across the FINAL tactic set. Validly used = **both**
of the pair's vector IDs appear together **within a single tactic's** `**Source:** … Vectors`
list (block-level co-occurrence — not the two IDs scattered across different tactics).
Validly substituted = an explicit one-line note that names the pair AND names a replacement
vector **that exists in `growth-factors.json`** (e.g. "B3 `lever-NNN`+`struct-NNN`
substituted — neither vector survived the founder-fit check; replaced with `resource-NNN`
which is in growth-factors.json"). A silently dropped Pool-B pair, or a substitution whose
replacement isn't in `growth-factors.json`, is a defect — list each Pool-B pair and mark it
used (which tactic #) or validly substituted (which replacement). This is in addition to the
"≥4 new tactics" floor, not a replacement for it.

These MUST pass founder-constraint checks: budget in range; time realistic; leverages an
asset the founder possesses (or states honestly what they'd need to learn). Apply the
**Complexity Budget** (inlined — the paid pipeline kept this in a monolith):

| Team capacity | Max vectors/tactic | Max monthly $ on external help |
|---------------|--------------------|--------------------------------|
| Solo, <10 hrs/wk | 2 | $0-100 |
| Solo, 10-25 hrs/wk | 2-3 | $100-300 |
| Small team | 3 | $300+ |

Tactics exceeding budget are flagged `[HIGH COMPLEXITY]`. Apply the **Kill List** (inlined
from the tactic-design step): start a newsletter · write SEO content · build community ·
demo the product · interview customers · improve the core product · re-engage churned ·
upgrade existing · improve onboarding · build a tool/dashboard · create-and-announce a
feature · develop an integration. A Day-1 action matching these = not novel demand gen.

═══════════════════════════════════════════════════════════════════════════
# PHASE 3 — MERGE, DEDUP, AND THE FINAL MIX
═══════════════════════════════════════════════════════════════════════════

Combine preserved/adapted Phase-1 + new Phase-2 tactics. **Dedup:** if two tactics share the
same Day-1 action, keep the one with the stronger structural advantage.

**Target final mix (ENFORCED):** 3-4 from Phase 1 (white space) + 4-5 from Phase 2
(synergy/founder-fit) = **7-9 total (minimum 7)**; unconventional ≥50%. Respect
`category_diversity_requirements` (no single category prefix > 60% of vectors used).

### Phase 3.5: Demand-Gen Purity Pre-Check (BLOCKING)

For EACH final tactic answer: (1) Day-1 action in one sentence; (2) time split BUILDING vs
DISTRIBUTING — if BUILDING > 40%, it's product dev, not demand gen; (3) target = NEW people
(demand gen) or EXISTING users (retention/CRO). Any tactic failing any question → replace.
**Max purity failures in final output: 0.**

### Phase 3.6: Competitor Self-Harm Check

For each tactic vs the top competitors in `competitors-analysis.md`: does it require a
competitor's platform? send traffic to a competitor without capture? educate customers in a
way that benefits competitors equally? → reframe or remove.

═══════════════════════════════════════════════════════════════════════════
# Output Format
═══════════════════════════════════════════════════════════════════════════

## Output language (REQUIRED)

`synthesis.md` is the deliverable the founder actually reads. Its body copy follows
`${CLAUDE_PLUGIN_ROOT}/reference/writing-style.md`: plain English at grade 6–8, ≤~20
words per sentence, the banned-jargon table respected, vector IDs ONLY in the
`**Source:**`/Traceability lines (never in prose), tactic names that pass the
smart-friend test, and an `**In plain English:**` line under every tactic name. The
template's section headings and field labels stay exactly as written below.

Save to `WS/03-think-tanks/demand-generation/synthesis.md`. In the per-tactic origin tags,
**Pass 1 White Space** = a Phase-1 tactic that was preserved/adapted; **Pass 2
Synergy/Founder-Fit** = a Phase-2 generated tactic.

```markdown
# Demand Generation Tactics Synthesis
## Synthesis Overview
- Method: Two-Pass Vector Synthesis over a per-run LIGHT growth-factors DB · Total Tactics: N
- Pass summary table (Pass 1 white space → N; Pass 2 synergy/founder-fit → N)
- White Space Retention Rate: X% (target ≥60%)
- Unconventional Ratio: UNCONVENTIONAL / HYBRID / CONVENTIONAL (target unconv ≥50%, conv ≤30%)
- Constraint Summary (budget / team / skills / stage / goal)
- Channel Selection Summary (Saturated to AVOID / Moderate / Open Opportunity — from the competitive channel matrix)

## Pass 1 Disposition
| Pass 1 Tactic | PRESERVE/ADAPT/DROP | Reason |

## Generated Tactics
### Tactic #N: <Name> — [Pass 1 White Space | Pass 2 Synergy/Founder-Fit]
**In plain English:** <one ≤20-word sentence — what you actually do>
**Source:** Origin · Vectors `id-1` + `id-2` (exist in growth-factors.json)
**Primary Channel(s):** from the channel menu · Competitive adoption (0-2 opportunity / 3-5 moderate / 6+ saturated) · why this channel
**Emergent Mechanism:** what emerges from the combination
**Structural Advantage:** Type / Duration / Why competitors can't copy
**Synthesis Logic:** what each vector contributes + how they interact (2-3 sentences)
**Adapted to Your Constraints:** (if ADAPTED) what changed; how it fits the founder
**How to Execute:** 1. … 2. … 3. … (specific tools/platforms, adapted for constraints)
**Required Resources:** Time / Budget (in range) / Tools
**Skills Required:** table — skill / founder has? / status
**Expected Timeline & Success Metrics:** early signal (Wk 1-2) / key metric (Month 1) / time-to-signal / decision point
**Anti-Pattern Validation:** checked vs synthesis-constraints.json anti_patterns — no HIGH-severity match (or exception noted)
**Scores:** Unfair advantage / Speed / Resource fit / Scalability / Risk (1-10 each) → TOTAL /50

## Anti-Portfolio: Tactics to AVOID
### #N: <name> — why founders try it / why it fails for THIS founder / what to do instead (ref tactic #)

## Tactical Clusters (by origin; by timeline: quick wins / medium / long-term)
## Top 5 Tactics (by score)
## Traceability Summary
| Tactic # | Origin | Vectors | Structural Advantage | Unconventional? |

## Post-Synthesis Self-Review
- White Space Retention (≥60%?) · Unconventional Ratio via Core-Action-Strip Test (≥50%?) · Constraint Compliance (100%?) · No Duplicates · Final Grade: PASS / NEEDS REVISION
```

**Core Action Strip Test** (for the unconventional ratio): write each tactic's Day-1 action
in one sentence, remove ALL adjectives, ask "would a traditional marketing consultant
recommend this exact action?" YES → CONVENTIONAL; NO → UNCONVENTIONAL. Target ≥50%
unconventional; <40% = FAIL (replace conventional tactics).

## Validation Checklist (final)

- [ ] 7-9 tactics (minimum 7); 3-4 from Pass 1 + 4-5 from Pass 2.
- [ ] `## Pass 1 Disposition` present (the structural proof that Phase-1 ideation preceded
      Phase-2 adaptation) — every Phase-1 tactic marked PRESERVE/ADAPT/DROP with a reason.
- [ ] White-space retention ≥60%; unconventional ≥50% (Core Action Strip Test).
- [ ] Phase 3.5 purity: 0 failures (every tactic brings NEW people; building ≤40%).
- [ ] Deception veto: 0 tactics fail the journalist test / match a HIGH anti_pattern.
- [ ] Category diversity respected (no prefix > 60% of vectors used).
- [ ] Every vector ID exists in `growth-factors.json`; every tactic traces to a combination.
- [ ] Every Pool-B `must_include` pair is validly used (both IDs co-located in one tactic) or
      validly substituted (replacement named and present in `growth-factors.json`).
- [ ] Every tactic carries an `**In plain English:**` line (≤20 words, plain words); every
      tactic name passes the smart-friend test; body copy follows
      `reference/writing-style.md` (no banned jargon, no vector IDs in prose).
- [ ] `## Post-Synthesis Self-Review` present with retention %, unconventional %, constraint
      compliance, no-duplicates, Final Grade.
- [ ] STOP here — no prioritization, no implementation guides (paid).
