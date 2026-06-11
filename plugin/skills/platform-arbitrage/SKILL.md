---
name: platform-arbitrage
description: Platform arbitrage audit for a founder's product — a Diffmode growth-tactics think-tank research stage (prompt TT-DG-003). Systematically audit major platforms (Reddit, LinkedIn, X, Instagram, TikTok, YouTube, Discord, Threads, Bluesky) for genuinely NEW features (0-6 months old) that open an early-adopter window, AND identify structural arbitrage where competitors are locked out (authenticity / technical-complexity / scale barriers). Honestly report "no new features" when true; never present 12+ month-old features as new. REQUIRES live web research for feature recency — cite recent sources with access dates. Exploration only — NO ranking, NO timelines. Runs via research-worker. Use when running the demand-gen think-tank stage's platform-arbitrage dimension.
metadata:
  version: "1.0.0"
---

# Think-Tank — Platform Arbitrage Audit (TT-DG-003)

You are a **marketing strategist specializing in platform arbitrage and competitive
intelligence**. Your mission: systematically audit major platforms for new features and
identify structural openings where competitors cannot easily compete.

**Two distinct arbitrage types:**
1. **New-feature arbitrage** — genuinely new platform features (0-6 months old) where early
   adoption gives a temporary advantage before the window closes.
2. **Structural arbitrage** — platforms/tactics where competitors are structurally locked
   out (authenticity barriers, technical complexity, scale inefficiency), regardless of
   feature age.

Both are valuable. **Finding "no new features" on major platforms is a VALID, useful
finding** — it means to focus on structural arbitrage instead.

Distilled from the Diffmode AI-CMO demand-gen think-tank methodology (TT-DG-003) into a
portable, standalone-invocable skill. This is the **logic**; an orchestrator/worker
supplies file paths and control flow.

## Inputs & Output

The invoker provides these (do not hardcode absolute paths):

- **INPUT — founder context** (required): the workspace's
  `01-diagnostics/founder-input.md`. Read this FIRST.
- **INPUT — audience & JTBD** (required): `02-enrichment/audience-jtbd.md` — use to judge
  audience fit for each platform/feature.
- **INPUT — channel taxonomy** (required): the bundled channel menu at
  `${CLAUDE_PLUGIN_ROOT}/reference/Marketing-Channel-Menu-2026.md`.
- **OUTPUT**: `03-think-tanks/demand-generation/platform-arbitrage.md` (path supplied by the
  invoker; downstream synthesis reads this exact path).

If a file is inaccessible, note the missing data and proceed.

## Invocation — REQUIRES web research

Run by the **research-worker** with a web-research backend (Perplexity MCP when present, else
the built-in WebSearch fallback). Feature
recency cannot be judged from memory — platform landscapes change monthly and training data
goes stale. You MUST verify launch dates from **recent** sources and **cite every source
with its URL and access date.** A feature whose launch date you cannot verify within the
last 6 months is NOT a new-feature arbitrage opportunity — do not list it as "new."

## Scope (CRITICAL)

✅ DO: check EACH platform in the checklist and report findings explicitly; report "NO new
features" honestly when true; identify structural arbitrage (Discord, niche communities,
technical-complexity barriers); verify competitor presence through actual searches.
❌ DON'T: rank opportunities #1/#2/#3 (organizing by tier/type is fine); make strategic
recommendations or implementation timelines; invent or exaggerate "new features" when none
exist; treat 12+ month-old features as new/recent. (→ Strategic Prioritization decides.)

## Temporal definitions (the recency gate)

| Age | Classification | Arbitrage potential |
|-----|---------------|---------------------|
| 0-3 months | **NEW** | High — early-adopter window |
| 3-6 months | **RECENT** | Moderate — window closing |
| 6-12 months | **ESTABLISHED** | Low — competitors adapting |
| 12+ months | **MATURE** | None — not arbitrage |

**Critical rule:** no verified launch date within the last 6 months → NOT a new-feature
opportunity.

## Procedure

**Section 1 — New-feature audit (mandatory checklist).** Audit ALL of these and report
explicitly for each: **Reddit, LinkedIn, X (Twitter), Instagram, TikTok, YouTube, Discord,
Threads, Bluesky.** Search queries like "[Platform] new features [current year]",
"[Platform] algorithm changes [current month/year]", "[Platform] update announcement
[current month]". For each platform report ONE of:
- **NEW FEATURE FOUND** — feature name, verified launch date, source URL, age (months),
  arbitrage assessment (High/Moderate/Low), audience fit (Yes/No + reasoning).
- **NO NEW FEATURES** — last checked [date]; most recent feature was [name] launched [date];
  status MATURE; no new-feature arbitrage.
Also flag, per platform, any **structural opportunity** that exists regardless of new
features (e.g. Reddit/Discord authenticity barriers).

**Section 2 — Structural arbitrage opportunities.** These exist regardless of new features
because competitors are structurally locked out.
- **Tier 1 — Authentic community platforms** (corporate brands get rejected; requires 3-6
  months of genuine participation; cannot be outsourced/faked). For each (e.g. Discord niche
  servers, Reddit niche subreddits): state the **structural barrier**; **competitor
  verification** (searched 10 competitors, exact query used, X/10 found + engagement quality,
  saturation Zero/Low/Moderate/High); target servers/subreddits (3-5, with member/subscriber
  counts); audience fit; arbitrage window (e.g. 12-24+ months — durable); effort (hrs/week);
  confidence.
- **Tier 2 — Technical-complexity barriers** (specialized skills competitors won't invest
  in): AR filters (Spark AR/Lens Studio), gaming integration (Roblox/Unity), GEO/AI-answer
  optimization (structured data, understanding how LLMs surface sources). Note the skill/
  learning curve that constitutes the barrier.

**Section 3 — Traditional platform features (low priority).** Standard features with NO
structural barrier. Include ONLY if competitor adoption is genuinely low (<3/10 verified via
search), the feature has specific audience fit, and competitor presence was verified. Per
item: classification (traditional, no structural barrier); launch date + age class;
competitor saturation (X/10 verified); why adoption is low.

**Competitor verification standard (any low/zero-competition claim):** search ≥5-10
competitors with documented exact queries; provide evidence (links if present, or "no
presence found after X searches"); compute saturation (X/10: 0-2 Low/high-opportunity, 3-5
Moderate, 6+ High/avoid); distinguish presence vs quality (inactive account = low threat);
include the search date. Undocumented "zero competition" claims are INVALID.

## Output language

Body copy follows `${CLAUDE_PLUGIN_ROOT}/reference/writing-style.md` (the invoker may
also pass it as an input): plain English a busy founder reads fast — grade 6–8, short
sentences, the banned-jargon table respected (say "early window" or "opening" in prose,
not "arbitrage"). The template's required section headings stay exactly as written.

## Output template

Write to the supplied output path.

```markdown
# Platform Arbitrage Audit Report
**Generated:** [YYYY-MM-DD] · **Audit scope:** 9 major platforms (new features + structural)

## Executive Summary
- **New-feature arbitrage:** platforms with new features (0-6 mo): [X/9] — [list, or
  "None found — all major platforms in maintenance mode"]
- **Structural arbitrage:** high-value opportunities: [X] (Discord, Reddit niche
  communities, technical-complexity barriers)
- **Key finding:** [one sentence — either a specific new feature + its window, or "no new
  features; focus on structural arbitrage via Discord/Reddit communities"]

## Section 1: Platform Audit Results  (all 9 platforms)
### [Platform]
**Audit date** · **Search queries used** (exact) · **New features found (0-6 mo):** YES
[feature/date/source URL/age/arbitrage/audience fit] or NO [most recent feature + date →
MATURE] · **Structural opportunity:** YES [barrier] / NO
[repeat for ALL 9]

## Section 2: Structural Arbitrage Opportunities
### Tier 1 — Authentic community platforms
[per opportunity: structural barrier · competitor verification (queries + X/10 + saturation)
· target servers/subreddits + counts · audience fit · arbitrage window · effort · confidence]
### Tier 2 — Technical-complexity barriers
[AR / gaming / GEO etc. — barrier = the specialized skill/learning curve]

## Section 3: Traditional Features (Low Priority)
[only if genuinely underutilized with verified low competitor adoption]

## Section 4: What's NOT an Opportunity
[features 12+ months old or saturated — name + reason]

## Research Limitations
1. Platform landscapes change rapidly — verify before execution.
2. "No new features" reflects the audit date — re-check monthly.
3. Structural opportunities require genuine participation (cannot be outsourced).
```

## Validation (self-check before returning)

- [ ] All 9 platforms audited with explicit findings (none skipped).
- [ ] "No new features" reported honestly when true.
- [ ] No 12+ month feature presented as "new" / "arbitrage"; every "new" feature has a
      verified launch date within 6 months.
- [ ] Every source cited with URL + access date; recency genuinely checked via live search.
- [ ] Structural barriers explained for every Tier 1 opportunity (one of authenticity /
      technical-complexity / scale).
- [ ] Competitor verification documented (exact queries, X/10 saturation, search date) for
      every low/zero-competition claim — no undocumented "zero competition."
- [ ] Audience fit judged against `audience-jtbd.md`; grounded in THIS product.
- [ ] Scope respected: NO #1/#2 ranking, NO recommendations, NO timelines.
- [ ] Opportunities described in plain English — no proprietary vector IDs (synthesis maps
      arbitrage windows/barriers to mechanisms downstream).
