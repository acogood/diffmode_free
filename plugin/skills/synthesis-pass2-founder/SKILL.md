---
name: synthesis-pass2-founder
description: Synthesis Pass 2 of 4 — the FINAL stage of the Diffmode growth-tactics pipeline (TT-DG-PASS2). Reviews Pass-1 white-space tactics and adapts them for founder constraints (preserving the unconventional core), generates 4-5 more from the synergy + founder-fit pools, and merges into a final synthesis.md of 7-9 novel demand-gen tactic ideas (target 50%+ unconventional). Reads synthesis-pass1 + synthesis-constraints.json + enrichment + the think-tank reports; uses the lite anti_patterns (NOT a proprietary anti-vectors DB). The free plugin STOPS here.
metadata:
  version: "1.0.0"
---

# Synthesis — Pass 2: Founder Fit & Merge (FINAL stage)

1. **Review Pass-1 tactics** and adapt for founder constraints — **preserving the
   unconventional core.**
2. **Generate 4-5 additional tactics** from the synergy + founder-fit pools.
3. **Merge** into a final synthesis of **7-9 total tactics** (target 50%+ unconventional).

This is the **last stage of the free pipeline.** It produces a portfolio of novel demand-gen
tactic IDEAS and stops. (Prioritization, implementation guides, and the proprietary
576-vector DB are the paid product — do not attempt them here.)

Vector definitions come from `growth-factors.json`; pools/anti-patterns from
`synthesis-constraints.json`. Do NOT read `tactics_DB/` (no proprietary anti-vectors DB —
use the lite `anti_patterns` field instead).

## Philosophy: Preserve the Unconventional Core (CRITICAL)

The #1 goal of Pass 2 is to PRESERVE Pass-1's unconventional mechanisms. What makes a tactic
unconventional: the **positioning** (contrarian / anti-establishment), the **structural
advantage** (competitor lockout, platform arbitrage), and the **uncomfortable edge** that
makes traditional marketers hesitate.

When adapting for constraints: **DO** reduce budget/time, simplify execution, scale down
scope — while keeping the uncomfortable positioning, the structural advantage, and the
rebellious/contrarian angle. **DON'T** remove words like "rebellion / anti- / contrarian" to
make it "safer," replace a structural advantage with an execution advantage, or sand down
the edge that creates the lockout. The unconventional NAME and POSITIONING must survive.

- BAD: "Anti-Enterprise Citation **Rebellion**" → "Technical Citation Authority" ❌ (lost the rebellion → lost the lockout)
- GOOD: "Anti-Enterprise Citation **Rebellion** (Lean Version)" ✅ (only budget/time reduced)

Aim for **≥60% Pass-1 preservation** with unconventional edges intact.

## Scope Enforcement — DEMAND GENERATION ONLY

Before any tactic: "Does this bring NEW PEOPLE who've never heard of the product?" YES =
include; NO = delete (CRO territory).

## Inputs & Output

- `WS/03-think-tanks/demand-generation/synthesis-pass1.md` (PRIMARY — Pass-1 output)
- `WS/03-think-tanks/demand-generation/synthesis-constraints.json` (pools `B_synergy` +
  `C_founder_fit`; `anti_patterns`; `category_diversity_requirements`)
- `WS/03-think-tanks/demand-generation/growth-factors.json` (vector definitions)
- `WS/01-diagnostics/founder-input.md` (constraints to apply; goal + deadline)
- `WS/02-enrichment/audience-jtbd.md`, `WS/02-enrichment/competitors-analysis.md`
- Think-tank context: `competitor-gaps.md`, `platform-arbitrage.md` (channel selection,
  structural advantage), `cross-industry.md` (transferable mechanisms / adaptation angles for
  the new Phase-2 synergy + founder-fit tactics)
- `${CLAUDE_PLUGIN_ROOT}/reference/Marketing-Channel-Menu-2025-Extended.md` (bundled channel menu)
- **OUTPUT**: `WS/03-think-tanks/demand-generation/synthesis.md`

## Phase 1: Review Pass-1 Tactics (PRESERVE / ADAPT / DROP)

| Decision | Criteria | Action |
|----------|----------|--------|
| PRESERVE | founder can execute with minor adaptation | keep, small resource adjustments |
| ADAPT | mechanism valuable, execution needs rework | redesign execution, keep mechanism |
| DROP | requires capabilities the founder fundamentally lacks | remove (counts toward the ≤40% drop allowance) |

**Timeline gate:** if a structural-advantage timeline (6-24 mo) exceeds the founder's
deadline by >3x AND the founder has a ≤90-day deadline → ADAPT so the tactic produces
observable acquisition signal (traffic/signups/trials) within the deadline, even while the
moat builds over time. If it fundamentally can't signal within 3x the deadline → DROP.

**Adaptation rules:** budget too high → reduce scope, not approach; skill missing → add a
learning curve or no-code/vibe-code path BUT keep distribution as the primary effort (if
80%+ becomes building, reframe around the distribution mechanism); time-intensive → phase
it; positioning feels risky → KEEP IT (the risk IS the advantage).

**DROP threshold:** at most 2 Pass-1 tactics dropped (preserve ≥60%).

## Deception veto (NEVER allowed — binary, non-scored)

Reject any tactic relying on: fabricated scarcity/urgency · multi-account astroturfing /
fake social proof · fake-door pages for nonexistent features · manipulating AI search via
seeded fabricated discussions · consensus loops of fake accounts · any tactic whose core
mechanism is deception (even if effective). Also reject: targeting existing users for
upsells (retention, not acquisition). **Journalist test:** "If a journalist investigated how
we execute this, would it be embarrassing?" YES → reframe or DROP. Cross-check every tactic
against `synthesis-constraints.json` `anti_patterns` (the clean-room replacement for the
proprietary anti-vectors DB) — any HIGH-severity match is blocking.

## Phase 2: Generate Synergy & Founder-Fit Tactics

From `synthesis-constraints.json`: **Pool B** (synergy pairs) + **Pool C** (founder-fit).
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

These MUST pass founder-constraint checks: budget in range; skills available or a clear path;
timeline realistic. Apply the **Complexity Budget** (inlined — the paid pipeline kept this in
a monolith):

| Team capacity | Max vectors/tactic | Max external dependencies |
|---------------|--------------------|---------------------------|
| Solo, <10 hrs/wk | 2 | 1 |
| Solo, 10-25 hrs/wk | 2-3 | 1-2 |
| Small team | 3 | 2 |

Tactics exceeding budget are flagged `[HIGH COMPLEXITY]`. Apply the **Kill List** (inlined
from the tactic-design step): start a newsletter · write SEO content · build community ·
demo the product · interview customers · improve the core product · re-engage churned ·
upgrade existing · improve onboarding · build a tool/dashboard · create-and-announce a
feature · develop an integration. A Day-1 action matching these = not novel demand gen.

## Phase 3: Merge, Dedup, and the Final Mix

Combine preserved/adapted Pass-1 + new Pass-2 tactics. **Dedup:** if two tactics share the
same Day-1 action, keep the one with the stronger structural advantage.

**Target final mix (ENFORCED):** 3-4 from Pass 1 (white space) + 4-5 from Pass 2
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

## Output Format

Save to `WS/03-think-tanks/demand-generation/synthesis.md`:

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
- [ ] White-space retention ≥60%; unconventional ≥50% (Core Action Strip Test).
- [ ] Phase 3.5 purity: 0 failures (every tactic brings NEW people; building ≤40%).
- [ ] Deception veto: 0 tactics fail the journalist test / match a HIGH anti_pattern.
- [ ] Category diversity respected (no prefix > 60% of vectors used).
- [ ] Every vector ID exists in `growth-factors.json`; every tactic traces to a combination.
- [ ] Every Pool-B `must_include` pair is validly used (both IDs co-located in one tactic) or
      validly substituted (replacement named and present in `growth-factors.json`).
- [ ] STOP here — no prioritization, no implementation guides (paid).
