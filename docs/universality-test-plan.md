# Universality Test Plan

The pipeline has been tested on SaaS, mobile apps, a Lightroom plugin, and an edtech
service — all digital products. The universality claim (physical businesses, local
services, consumer products) is unproven. This plan documents how to test it.

## Test subjects (run the full pipeline for each)

| Product | Type | Why this one |
|---------|------|-------------|
| A local coffee shop (pick a real one with a website) | Physical / local / hyperlocal | Stresses the channel menu's hyperlocal section, tests whether mining finds non-digital case studies |
| A mobile game (indie, small team) | Consumer digital / app store | Tests ASO, community, viral-loop vectors; different from B2B SaaS |
| A fitness studio or yoga studio (local, with a site) | Physical / local / subscription | Tests whether the pipeline handles "foot traffic" as a channel and local competition |

## What to watch for (per run)

### diagnostics-intake
- Does the Q&A mode ask relevant questions? (e.g., "foot traffic" vs "visitors/mo")
- Does the "unfair advantage" prompt elicit useful answers for a non-technical founder?

### growth-factors-mining
- Are the case studies relevant to the industry, or do they default to SaaS/tech?
- Does the breadth check (added 2026-07-31) catch gaps?
- Do the guerrilla search seeds pull in physical-world case studies?

### enrichment-competitors
- Does the competitor analysis find real local competitors, or only online ones?
- Does the channel matrix cover physical/local channels?

### competitor-gaps
- Does Tier 1 (structural advantage) produce relevant gaps for a local business?
  (e.g., "authentic community presence" vs "corporate brand can't be local")
- Are the "unconventional channel gaps" from the channel menu's Section 6 relevant?

### synthesis-explore / synthesis-build
- Do the tactics make sense for a non-digital product?
- Do the execution prototypes (Day 1 / Day 7 / Day 30) reference realistic actions?
- Does the Guerrilla Lens (added 2026-07-31) tag mechanisms with relevant principles?
- Are the examples in the skill prompts (which reference "B2B SaaS," "PLG," "free trial")
  causing the LLM to anchor on SaaS?

### founder-report
- Does the report read naturally for a non-technical founder?
- Are the "Execute this" tool pointers relevant? (A coffee shop owner doesn't need
  the `cold-email` skill — they need "walk into 10 businesses and talk to the manager.")

## Decision criteria

After 2-3 test runs:

- **If it works with minor tweaks:** Add industry-aware search seeds to
  growth-factors-mining (e.g., "for local/physical businesses, also search for: foot
  traffic, local partnerships, in-store experience, local press, word-of-mouth"). Expand
  the channel menu's Section 7 "What to Focus On First" with a local-business variant.

- **If it breaks significantly:** Consider adding an industry-type classifier to
  diagnostics-intake (digital product / local business / consumer app / physical product)
  that adjusts mining search themes and channel menu emphasis.

- **If it's fundamentally digital-only:** Say so in the README. "Built for digital
  products and services" is honest and fine. Don't force universality that isn't there.

## Known SaaS-anchoring points to check

These are places in the skill prompts where SaaS-specific language might bias the LLM:

1. `synthesis-explore` — examples reference "B2B SaaS," "free trial," "PLG"
2. `growth-factors-mining` — search themes default to "growth case studies" (tech-biased)
3. `Marketing-Channel-Menu-2026.md` Section 7 — "What to Focus On First" is written for
   "a solo or bootstrapped B2B founder"
4. `lite-constraints` — the `generated_for` schema assumes digital-product fields
5. `diagnostics-intake` — "visitors/mo" and "signups/mo" as primary metrics
