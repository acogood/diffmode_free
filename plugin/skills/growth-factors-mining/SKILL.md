---
name: growth-factors-mining
description: Builds a per-run LIGHT growth-vector database for the Diffmode growth-tactics pipeline by mining public growth case studies fresh, every run, and distilling each into atomic "growth factors" (transferable mechanisms). Clean-room — NEVER reads the proprietary tactics_DB. Outputs growth-factors.json (~20-40 vectors across the 6 categories) in the schema the synthesis chain + lite-constraints consume. Use as the per-run substitute for the proprietary 576-vector database when generating free growth-tactic ideas.
metadata:
  version: "1.0.0"
---

# Growth-Factors Mining (per-run LIGHT vector DB)

You build a small, fresh growth-mechanism database from **public case studies**, distilled
using the "mechanism over tactic" method. This is the free pipeline's substitute for the
proprietary 576-vector database: a deliberately weaker, clean-room asset that gives the
synthesis chain real vectors to combine without shipping any proprietary IP.

## ⚠️ Clean-room rule (moat-critical — non-negotiable)

You MUST build this **only** from freshly researched public sources. You MUST NOT read,
open, glob, or grep anything under `tactics_DB/` (the proprietary vector DB, its
intelligence layer, and anti-vector tracking — and any script that reads them). No content
here may be traceable to that database. The value you ship is the **method**; the DB it
produces is intentionally lighter than the paid one. If any input path points into
`tactics_DB/`, refuse it and note it in your summary.

## Inputs & Output

The invoker provides (do not hardcode absolute paths):

- **INPUT — founder context** (required): `WS/01-diagnostics/founder-input.md`. Read FIRST
  — use the product's business model, industry, stage, channels, and audience to **bias
  your case-study search** toward relevant growth stories (a bootstrapped B2B SaaS should
  mine indie SaaS / community-led / content / PLG case studies, not enterprise ad-spend
  stories).
- **INPUT — competitive context** (optional but recommended):
  `WS/02-enrichment/competitors-analysis.md` and `WS/02-enrichment/acquisition-tactics.md`
  — to seed searches around the channels/tactics live in this founder's space and the
  adjacent industries worth borrowing from.
- **WEB RESEARCH** (required capability): your web-research backend (Perplexity MCP when
  present, else the built-in WebSearch fallback — deep multi-source research + targeted
  search). This is the ONLY source of vectors.
- **OUTPUT**: write `WS/03-think-tanks/demand-generation/growth-factors.json`.

## Caching & bounded research (cost control — surface this tradeoff)

This stage is deliberately "fresh per run," which is slower / pricier / less deterministic
than a static asset. Mitigate:

- **Cache:** if `growth-factors.json` already exists at the output path AND the brief does
  NOT set `remine: true`, do NOT re-research. Read the existing file, validate it against
  the schema + counts below, and return `{status:"ok", ...,"summary":"reused cached growth-factors.json (N vectors)"}`.
  Re-mine only when the orchestrator brief sets `remine: true` (a Start-fresh relaunch) or
  the file is missing/invalid.
- **Resume-partial (socket-death recovery — do NOT re-pay for deep research):** if the brief
  includes **`resume_partial: true`** (the orchestrator sets this only when re-spawning after a
  mid-mine death) AND a partial `growth-factors.json` exists that PARSES but is short of target
  (e.g. < 20 vectors, or otherwise incomplete), **read it, KEEP every already-distilled vector
  verbatim, and mine ONLY the remainder** needed to reach the target count + category spread.
  Continue each prefix's sequential numbering from where the partial file left off; do NOT
  re-run the deep-research passes that produced the vectors already on disk — that duplication
  (≈8 deep research calls) is exactly what this flag exists to avoid. `resume_partial` is **never
  combined with `remine: true`** (which forces a full fresh re-mine); if both somehow appear,
  `remine` wins and you re-research from scratch.
- **Bound breadth + cap deep research (the run's biggest cost lever):** review **12-20
  public case studies** using **at most ~1-2 deep-research passes** (a `perplexity_research`
  call when Perplexity is present; otherwise iterate your search tool + `WebFetch`) — seed
  them from the founder context for the initial case-study landscape, then gather the
  remaining case studies + their specific metrics with cheaper search-tool calls
  (`perplexity_search`, or the built-in WebSearch fallback).
  Do NOT open-ended crawl. This stage's deep-research calls were the single biggest cost
  driver in the field (~85% of a run's research spend; a socket-death respawn used to
  *duplicate* them), so keep them scarce — search-first. Stop when you have enough distinct
  mechanisms to hit the target count.

## Method — adapt the proven extraction methodology

Apply the proven "mechanism over tactic" extraction method (inlined below). For each case
study:

1. **Mechanism, not tactic.** Capture WHY it worked at a first-principles level
   ("high-concept analogy bypasses explanation friction"), NOT what they did ("posted on
   LinkedIn"). One case study yields 1-3 atomic vectors.
2. **Transferability test.** Would this work in a *completely different* industry? Give 2-3
   cross-industry `examples` proving it transfers. Drop "Low transferability" / very
   context-specific findings.
3. **Dedup.** Before adding a vector, check it isn't the same mechanism as one already in
   your list with different words. Merge duplicates; keep the cleaner statement.
4. **No generic advice.** Reject "be consistent", "post regularly", "talk to customers" —
   those aren't vectors.
5. **Demand-gen lean.** Prefer `lever-` / `resource-` / `struct-` (acquisition/distribution
   mechanisms). `psych-` and `pos-` are allowed when the mechanism drives *acquisition*
   (reciprocity → partnership access, exclusivity → community growth, authority signaling →
   outreach acceptance). `conv-` only for the rare acquisition-adjacent conversion
   mechanism. This is a demand-gen pipeline.

## Categories & ID format (NOT secret — reused so synthesis runs unchanged)

The 6 categories and the `{prefix}-NNN-slug` ID format are public conventions. Reuse them
so the ported synthesis prompts consume your output unchanged. Numbering is **local to this
run** — number sequentially per prefix starting at `001` based on the order you mine them.
Any resemblance to proprietary IDs is incidental; you derive these independently.

| Category | Prefix | Mechanism is about… |
|----------|--------|----------------------|
| Structural Arbitrage | `struct-` | Timing, platform/market gaps, competitive positioning windows |
| Leverage Mechanisms | `lever-` | Compounding, amplification, flywheels, viral loops, network effects |
| Resource Optimization | `resource-` | Efficiency, validation, risk reduction, lean/bootstrapped execution |
| Psychological Mechanisms | `psych-` | Cognitive biases, trust, urgency, social proof (acquisition-side) |
| Positioning Dynamics | `pos-` | Differentiation, framing, anchoring, contrarian positioning |
| Conversion Architecture | `conv-` | Funnel/offer mechanics that drive acquisition (rare here) |

## Target output

- **20-40 vectors total.** Aim for spread: a healthy run has the majority in
  `struct-`/`lever-`/`resource-`, with a few `psych-`/`pos-`. No single prefix should
  exceed ~60% of the vectors. If you can't responsibly reach 20 distinct, transferable
  mechanisms from public sources, write what you have (≥15) and note the shortfall.
- Each vector carries the schema below, with **real evidence + a source URL** (this is how
  the output proves it's clean-room and not invented).

## Output schema (write EXACTLY this JSON shape)

```json
{
  "metadata": {
    "generated_for": "<workspace slug / product>",
    "generated_date": "<YYYY-MM-DD>",
    "method": "clean-room per-run mining from public case studies (mechanism-over-tactic)",
    "source_note": "Diffmode growth-tactics LIGHT DB. Built fresh from public case studies. NOT the proprietary 576-vector database.",
    "case_studies_reviewed": <int>,
    "total_vectors": <int>,
    "category_counts": { "struct-": 0, "lever-": 0, "resource-": 0, "psych-": 0, "pos-": 0, "conv-": 0 }
  },
  "vectors": [
    {
      "vector_id": "struct-001-counter-cyclical-launch-timing",
      "category": "Structural Arbitrage",
      "vector_name": "Counter-Cyclical Launch Timing",
      "mechanism": "Launching against the seasonal grain (when competitors retreat) buys cheap attention and premium positioning.",
      "transferability": "High",
      "saturation_risk": "Emerging",
      "examples": [
        "A fitness app launching a no-resolution campaign in January",
        "A tax tool going premium during the discount-software rush",
        "A B2B SaaS shipping a big release the week competitors go quiet for a holiday"
      ],
      "evidence": "<short quote/metric from the case study, e.g. 'launched Black Friday rejecting discounts; $14,950 pre-sold'>",
      "source_url": "https://<real source>",
      "time_to_signal_weeks": 2
    }
  ]
}
```

Field rules (from the extraction methodology): `mechanism` = 1-2 sentences, transferable,
not case-specific; `transferability` ∈ {High, Medium, Low} (avoid Low); `saturation_risk` ∈
{Emerging, Mature, Oversaturated}; `examples` = 2-3 in DIFFERENT industries than the source;
`evidence` quotes/paraphrases the actual case study (numbers when available — never
fabricate); `source_url` is a real, reachable URL; `time_to_signal_weeks` optional integer.

## Procedure

1. **Read founder context** (+ competitive context if provided). Derive 4-6 search themes
   (business model, primary channels, industry, adjacent industries to borrow from).
2. **Check the cache / resume-partial** (see above). If a valid full file exists and the
   brief does not set `remine: true`, reuse and return. If the brief sets
   `resume_partial: true` and a parseable but
   short partial file exists (and no `remine`), load it, keep its vectors, and mine only the
   remainder — skip the deep-research passes for what's already there.
3. **Deep research pass (search-first, ≤~1-2 deep calls):** run a bounded set of web-research
   calls — at most ~1-2 deep-research passes (`perplexity_research` when present) for the
   initial landscape, then cheaper search-tool calls (`perplexity_search`, or the built-in
   WebSearch fallback) — on growth case studies across those themes + 2-3
   deliberately *different* industries (for transferable mechanisms). Capture source URLs +
   the specific result/metric for each story.
   **Guerrilla search seeds:** alongside the founder-derived themes, include at least one
   search pass using unconventional/guerrilla angles — e.g. "ambush marketing case study,"
   "counter-cyclical launch timing," "secret menu / exclusive offer growth," "community
   infiltration marketing," "mystery benefactor / anonymous giveaway," "reverse review /
   customer-as-hero marketing," "hyperlocal guerrilla tactic," "partnership judo startup."
   These pull in case studies the default "growth case study" query misses (physical-world,
   event-based, psychological, and partnership mechanisms).
4. **Distill** each case study → 1-3 atomic vectors using the method above. Assign category
   + a local sequential `{prefix}-NNN-slug` id. Write `mechanism`, `transferability`,
   `saturation_risk`, 2-3 cross-industry `examples`, `evidence`, `source_url`.
5. **Breadth check.** Map every distilled vector to a mechanism type: content/SEO ·
   partnership/alliance · timing/counter-cyclical · pricing/offer · community/tribe ·
   outbound/direct · event/experiential · platform/technical · psychological/behavioral ·
   structural/regulatory. If any type that the founder's industry could plausibly use has
   ZERO vectors, do one more targeted search for case studies in that type before
   proceeding. This is a check, not a constraint — new vectors still must pass the
   transferability test and the mechanism-over-tactic rule.
6. **Dedup + balance** to 20-40 vectors with category spread (no prefix > ~60%).
7. **Compute `metadata`** (counts, category_counts, case_studies_reviewed) and write valid
   JSON to the output path. Validate it parses (`json.load`-clean).

## Validation checklist (self-check before returning)

- [ ] Output is valid JSON in the exact schema above; `total_vectors` matches `vectors`
      length; `category_counts` sums to `total_vectors`.
- [ ] 20-40 vectors (or ≥15 with a noted shortfall); no single prefix > ~60%.
- [ ] Breadth check ran: vectors span ≥5 distinct mechanism types (content, partnership,
      timing, pricing, community, outbound, event, platform, psychological, structural);
      any plausible type with zero vectors triggered a follow-up search.
- [ ] Every vector is a MECHANISM (WHY), not a surface tactic (WHAT).
- [ ] Every vector has 2-3 cross-industry `examples`, real `evidence`, and a real
      `source_url`. No fabricated sources or metrics.
- [ ] Demand-gen lean (majority struct-/lever-/resource-); psych-/pos- only for
      acquisition-side mechanisms.
- [ ] CLEAN-ROOM confirmed: nothing was read from `tactics_DB/`; nothing is traceable to it.
