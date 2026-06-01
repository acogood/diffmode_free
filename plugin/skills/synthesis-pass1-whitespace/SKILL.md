---
name: synthesis-pass1-whitespace
description: Synthesis Pass 1 of 4 for the Diffmode growth-tactics pipeline (TT-DG-PASS1) — generates 4-5 genuinely unconventional demand-gen tactics from diverse white-space vector pairs, in exploration mode (IGNORES founder constraints; practicality is Pass 2's job). Reads synthesis-constraints.json diverse_white_space + the step2 mechanisms + growth-factors.json + the think-tank reports, applies the kill list and the unconventional self-audit. Use after step2; feeds pass2.
metadata:
  version: "1.0.0"
---

# Synthesis — Pass 1: White Space Exploration

Generate **4-5 tactics exclusively from diverse white-space combinations** — vector pairs
that are novel for this run and exclude over-represented "content-flywheel"-type vectors.
**This pass prioritizes unconventional exploration over practicality and IGNORES founder
constraints** (Pass 2 applies them).

Vector definitions come from `growth-factors.json`. Do NOT read `tactics_DB/`.

## Philosophy: Exploration Mode

Mindset: "What interesting mechanisms emerge from these never-combined vectors?" / "What
would a founder do with unlimited resources?" — NOT "can this founder do this?" The goal is
to discover unconventional approaches Pass 2 can refine or preserve.

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

## Inputs & Output

- `WS/03-think-tanks/demand-generation/synthesis-constraints.json` (PRIMARY —
  `diverse_white_space`)
- `WS/03-think-tanks/demand-generation/synthesis-step2-mechanisms.md` (the validated
  emergent mechanisms — draw on these, not just for format)
- `WS/03-think-tanks/demand-generation/growth-factors.json` (vector definitions)
- `WS/01-diagnostics/founder-input.md` (READ but DO NOT filter by constraints)
- Think-tank context (use if present): `competitor-gaps.md`, `platform-arbitrage.md`,
  `cross-industry.md` — for open channels, timing windows, and transferable angles
- `${CLAUDE_PLUGIN_ROOT}/reference/Marketing-Channel-Menu-2025-Extended.md` (bundled channel menu)
- **OUTPUT**: `WS/03-think-tanks/demand-generation/synthesis-pass1.md`

## Process

1. **Load diverse white space** from `synthesis-constraints.json` (`diverse_white_space`).
   These are pre-filtered to exclude content-flywheel-type vectors and limit repetition
   (max 2 per anchor). Display the loaded pairs in a table. **Category awareness:** aim for
   ≥2 different category prefixes across your 4-5 tactics (soft target here; Pass 2 enforces
   hard minimums from `category_diversity_requirements`).
2. **For each combination, derive the emergent mechanism** (reuse/extend the matching Step-2
   mechanism where one exists): "What UNUSUAL capability emerges?" It must differ from what
   either vector produces alone and feel uncomfortable/counterintuitive. Do NOT consider
   whether the founder can execute it.
3. **Design a complete tactic from each mechanism.** Name MUST reflect the unconventional
   mechanism, not generic marketing. No practicality filtering — include tactics even if
   they need skills/budget the founder lacks or feel risky.

## Kill List (still applies in exploration mode)

Skip combinations whose core action is: start a newsletter · write SEO content · build
community (join Discord/Slack) · demo the product · interview customers · improve the core
product · re-engage churned users · upgrade existing customers · improve onboarding · build
a tool/dashboard/calculator (engineering, distribution as afterthought) · create a feature
and announce it · develop an integration. If the white-space pair only produces a kill-list
action, it didn't yield anything novel — skip it.

## Output Format

Save to `WS/03-think-tanks/demand-generation/synthesis-pass1.md`:

```markdown
# Pass 1: White Space Exploration Results
## Overview
- Method: Two-Pass Synthesis — Pass 1 (White Space only) · Tactics Generated: N · Practicality Filtering: DISABLED

## White Space Combinations Used
| # | Vector A | Vector B | Status (Used / Skipped + reason) |

## Generated Tactics (Exploration Mode)
### Tactic #N: <Name reflecting the unconventional mechanism>
**Source:** Vectors `id-1` + `id-2` · White-space reason
**Emergent Mechanism:** 2-3 sentences
**Why This Is Unconventional:** 1 sentence (why a marketer hesitates)
**Structural Advantage:** Type / Duration / Why competitors can't copy
**How to Execute (Ideal, unconstrained):** 1. … 2. … 3. …
**Required Resources (Unconstrained):** Time / Budget / Skills (do NOT filter) / Tools
**Success Metrics:** Early signal (Wk 1-2) / Key metric (Month 1)
**Practicality Assessment (for Pass 2):** Difficulty / Resource intensity / Risk / Pass-2 action (Preserve / Adapt / Consider dropping)

## Pass 1 Summary
- Unconventional ratio (target 100% here) · Tactics-ready-for-Pass-2 table · White-space utilization

## Notes for Pass 2
- High-potential tactics to preserve / tactics needing adaptation / tactics at risk of being conventional
```

## Self-Audit (per tactic)

1. **Remove all vector references** — does the tactic still sound unusual? NO → vectors are
   labels on a conventional action (regenerate from a different pair).
2. **Day-1 action on the Kill List?** YES → kill & regenerate.
3. **Marketer Test** — would a B2B marketer recommend this unprompted? YES → too
   conventional, reconsider.
4. **Cannibalization Test** — does it teach customers to DIY what the product does? YES →
   reframe (emphasize the PAIN of manual methods, don't teach the method).

## Validation Checklist (before pass2)

- [ ] 4-5 tactics, each from a `diverse_white_space` pair (IDs exist in growth-factors.json).
- [ ] Each passes all 4 self-audit tests; 100% unconventional target.
- [ ] ≥2 category prefixes represented across the tactics (soft target).
- [ ] Demand-gen only (no CRO/retention/product-dev tactics).
- [ ] Each tactic carries a Practicality Assessment for Pass 2.
