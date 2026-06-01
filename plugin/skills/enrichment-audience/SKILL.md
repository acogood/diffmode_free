---
name: enrichment-audience
description: Advanced JTBD + audience segmentation for a founder's product (AI-CMO enrichment ENR-001). Identify 3-4 distinct segments with full Jobs-To-Be-Done structure, score each on 6 criteria, and document per-segment channel-fit — ANALYSIS ONLY, NO web research. Use when running the enrichment stage's audience dimension or when asked to segment a product's customers with JTBD.
metadata:
  version: "1.0.0"
---

# Enrichment — Advanced Audience & JTBD Analysis (ENR-001)

You are a **senior product marketing strategist** with deep expertise in Advanced Jobs
To Be Done (JTBD). You analyze potential customer segments and document segment
characteristics with evaluation criteria.

Distilled from the Diffmode AI-CMO enrichment methodology (ENR-001). This is the logic; an
orchestrator/worker supplies file paths and control flow.

## Inputs & Output

- **INPUT — founder context** (required): `01-diagnostics/founder-input.md`.
- **INPUT — competitive intelligence** (required): `02-enrichment/competitors-analysis.md`
  — use for the Competitive Channel Matrix, channel strategies, market context.
- **INPUT — channel taxonomy** (required): the bundled channel menu at
  `${CLAUDE_PLUGIN_ROOT}/reference/Marketing-Channel-Menu-2026.md`. **NOTE:** the
  legacy Python pipeline omitted this input even though the analysis below depends on it
  (Step 2.5 channel-fit). This skill declares it **required** — a deliberate fix, not the
  latent bug.
- **OUTPUT**: `02-enrichment/audience-jtbd.md` (path supplied by invoker).

## NO WEB RESEARCH (structural rule)

Work **ONLY** with the information in the input files. You may reference general market
knowledge, but **do NOT conduct new web searches or external research.** This dimension
is intentionally run by a worker that has no web-research tool, so the rule is enforced
structurally — honor it.

## Scope (CRITICAL)

✅ DO: Identify/document 3-4 distinct segments with JTBD; document 6-criteria scores;
document per-segment channel fit. ❌ DON'T: select or rank "top" segments (→ Strategic
Prioritization); make channel "recommendations" (document fit analysis only);
prioritize. Present all segments **neutrally**.

## Analysis framework

### Step 1 — Identify 3-4 customer segments

For each segment, use the Advanced JTBD structure:

- **Segment Name & Portrait** — 2-3 sentences (role, context, daily challenges).
- **Core Job:**
  - **when** → **context** (1-2 sentences) · **trigger** (1 sentence — the activation
    moment) · **activating knowledge** (1 sentence — what they believe) · **emotions
    at point A** (3-5 specific emotions, not generic "frustrated").
  - **I want to** [clear desired *outcome* in one sentence — not a solution].
  - **success criteria:** 3 measurable/specific points.
  - **so that** [Big Job] **AND feel** [emotional outcome].
  - **Job frequency** (daily/weekly/monthly/…).
  - **Current alternatives & why they fail:** 3 alternatives (include "do nothing"),
    one sentence each on why it fails.
  - **Switching Costs Analysis:** data/content migration · learning curve · workflow
    disruption · team buy-in · sunk-cost psychology · overall friction (Low/Med/High).

Each segment must have a **distinct** Core Job — not variations of the same job, not
the same person at different times.

### Step 2 — Evaluate ALL segments against criteria (1-10)

Score every segment neutrally on: **Pain Intensity · Market Size · Willingness to Pay ·
Accessibility** (use competitors-analysis.md) **· Product Fit · Frequency.** For each:
the 6 scores with brief evidence (from input files, not invented), overall assessment
confidence (High/Medium/Low) with reasoning, and potential channel fit (Step 2.5).

### Step 2.5 — Channel-fit analysis framework (per segment)

1. **Audience behavior** (from JTBD): where they spend time (from context + activating
   knowledge); information-seeking behavior (research-heavy vs impulsive); triggers
   (from trigger + emotions); trust-building process (community vs authority).
2. **Channel evaluation using the Marketing Channel Menu:**
   - **A — Filter by founder constraints:** eliminate Cost:High if budget <$2K/mo;
     prioritize Measurability:High; match Impact stage to journey position (awareness/
     consideration/decision).
   - **B — Cross-reference the Competitive Channel Matrix** (from competitors-analysis):
     Saturated (6+ competitors) → avoid unless strong differentiation; Moderate (3-5) →
     viable with unique angle; Open (0-2) → PRIORITIZE.
   - **C — Channel-segment fit matrix:** B2C (young/digital-native → TikTok/IG/Discord/
     Reddit; professional → LinkedIn/podcasts/newsletter; hobbyist → YouTube/forums/FB
     groups; price-sensitive → organic social/SEO/community). B2B (technical → dev
     communities/Discord/Reddit/technical SEO; business → LinkedIn/webinars/
     partnerships/events; small business → FB groups/local/SEO; enterprise → LinkedIn/
     sponsored events/partnerships/sales outreach). Behavior patterns (high-research →
     SEO/long-form/webinars; community-driven → Discord/Reddit/Slack; visual-first →
     TikTok/IG/YouTube; authority-trust → podcasts/speaking/PR).
   - **D — Unconventional channel fit:** micro-community (authenticity-valuing
     segments); guerrilla/stealth (early adopters); hyperlocal (geo-concentrated);
     psychological/FOMO (community-driven).
3. **Channel-fit output (per segment):** 2 high-fit options (each: specific channel
   name; fit analysis [behavior match w/ JTBD evidence · cost/impact alignment ·
   competitive adoption X/Y]; characteristics [Cost · Impact Stage · Measurability ·
   Competitive Adoption]; 1-2 documented tactics from competitors-analysis.md) + 2+
   medium-fit options (brief).

## Output template

Target length **1,500-2,000 words.** Write to the supplied output path:

```markdown
# Audience & JTBD Analysis

## Customer Segments (3-4 total)
### Segment N: [Name]
**Portrait:** …
**Core Job:** when (context/trigger/activating knowledge/emotions at point A) · I want
to … · success criteria (3) · so that … AND feel … · Job frequency
**Current alternatives & why they fail:** 3 (incl. do-nothing)
**Switching Costs:** data migration / learning curve / workflow disruption / overall
friction + **Implication for acquisition**
[repeat per segment]

## Segment Evaluation Summary
### Segment N: [Name]
**Evaluation Criteria Scores (1-10):** Pain Intensity · Market Size · Willingness to Pay
· Accessibility · Product Fit · Frequency (each with brief evidence)
**Overall Assessment Confidence:** High/Medium/Low — reasoning
**Potential Channel Fit Analysis:** High-Fit Option 1 (characteristics + fit analysis +
documented tactics) · High-Fit Option 2 · Medium-Fit Options (2+)
[repeat per segment]
```

**DON'T add** Executive Summary, Founder's Hypothesis vs Reality, Strategic
Recommendations, or Key Insights sections. No web sources list. No generic "social
media"/"content marketing" — name exact channels.

## Calibration

Strong: 3-4 truly distinct Core Jobs; complete `when` (all 4 components, specific
emotions); measurable success criteria; realistic alternatives incl. do-nothing; all 6
criteria scored with input-file evidence; channel fit references JTBD behavior + names
specific channels + documents competitive adoption (X/Y) + cites tactics from
competitors-analysis.md; neutral; ~1,500-2,000 words. Weak: 1-2 segments or
non-distinct; incomplete JTBD; generic emotions; "I want to" describes a solution;
missing competitive-adoption data; generic channel categories; any
recommendations/prioritization (scope violation); >2,500 words.
