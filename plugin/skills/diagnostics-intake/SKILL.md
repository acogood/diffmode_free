---
name: diagnostics-intake
description: Fast founder-input capture for the Diffmode growth-tactics pipeline (the diagnostics stage). Produces WS/01-diagnostics/founder-input.md in the exact schema the enrichment + synthesis stages read. Two modes — (A) URL mode researches a product's website (homepage/pricing/about) plus a web-research pass to prefill the researchable fields, then marks founder-only gaps for confirmation; (B) Q&A mode formats a minimal (~2-minute) answer set into the schema. Use as the entry point of run-growth-tactics, or whenever a workspace needs a founder-input.md before enrichment.
metadata:
  version: "1.0.0"
---

# Diagnostics — Intake (fast founder-input)

You produce a single file: `WS/01-diagnostics/founder-input.md`, in the **exact schema**
the rest of the pipeline reads (enrichment, the constraints generator's field parser, and
synthesis all key off these sections and labels). This replaces the slow 20-minute
diagnostic interview with a ~2-minute path: research what's public, ask only what isn't.

This is **capture, not analysis** — no strategy, no recommendations, no channel picks.
That separation is load-bearing: later stages depend on raw, un-editorialized founder
context.

## Inputs & Output

The invoker provides (do not hardcode absolute paths):

- **MODE A — `url`** (a website, e.g. `https://theona.ai`): research the site + company.
- **MODE B — `answers`**: a block of founder answers to the minimal question set below
  (the orchestrator collects these in the main thread; you format them).
- **MODE A+B**: both — research the URL AND fold in any founder answers the brief passed
  (answers always win over researched guesses).
- **OUTPUT**: write to `WS/01-diagnostics/founder-input.md` (path supplied by invoker).

If neither `url` nor `answers` is present, write the schema with every must-ask field as a
`[NEEDS FOUNDER INPUT: …]` placeholder and report it — do not invent a business.

## Field provenance (what to research vs what to ask)

| Field | Provenance |
|-------|-----------|
| Product description, what it does, who it's for | RESEARCHABLE (homepage/about) |
| Business model + pricing (tiers, free trial) | RESEARCHABLE (pricing page) |
| Target-audience hypothesis (segments, ICP) | RESEARCHABLE (site copy) + confirm |
| Competitive alternatives (direct + indirect) | RESEARCHABLE (web research) |
| Product complexity ("explains itself" vs "needs a demo") | RESEARCHABLE + confirm |
| **Stage + current metrics** (visitors, signups, MRR, paying customers) | **MUST ASK** |
| **Current acquisition sources / what's working** (Q8 demand-gen signal) | **MUST ASK** |
| **Demand-gen vs CRO split** (traffic problem vs conversion problem) | **MUST ASK** |
| **Budget** (monthly marketing $, paid-ads yes/no) | **MUST ASK** |
| **Skills / technical capabilities** (landing pages, content, ads, analytics) | **MUST ASK** |
| **Goal + timeline** (target metric, deadline) | **MUST ASK** |
| Tactics ruled out + competitor-dignity constraints | MUST ASK (optional) |

Founder-only fields cannot be guessed from a website. In URL mode, write a researched
best-guess for confirmable fields and a `[CONFIRM: …]` / `[NEEDS FOUNDER INPUT: …]` marker
for every MUST-ASK field not supplied in `answers`, and list them all under a final
**"Confirmation Gaps"** block so the orchestrator can ask.

## Minimal question set (Q&A mode — target ≤ 2 minutes)

These are the ONLY fields a founder must answer (the orchestrator asks them; skip
interview-observation and CRO-deep-dive fields):

1. **Product in one line** — what it does + who it's for (skip if URL covers it).
2. **Business model & pricing** — e.g. "B2B SaaS, $49/mo, free trial" (skip if URL covers).
3. **Target-audience hypothesis** — the 1-3 roles/segments you think you're for.
4. **Stage + rough metrics** — pre-launch / early / traction / growth, plus any of:
   visitors/mo, signups/mo, paying customers, MRR.
5. **Q8 — current acquisition sources** — where today's users/traffic come from, and
   what's working best. *(This is the demand-gen-vs-CRO signal. If traffic is the
   bottleneck → demand gen; if traffic converts poorly → CRO.)*
6. **Biggest growth problem** — "not enough traffic" (demand gen) **or** "traffic doesn't
   convert" (CRO), in the founder's words.
7. **Budget + skills** — monthly marketing $ (and paid-ads yes/no), plus which of
   {landing pages, content creation, ad campaigns, analytics} they can do.
8. **Goal + deadline** — target (e.g. "20 paying teams" / "10k visitors/mo") + timeframe.
   *(Optional 9th: tactics/channels already ruled out + why.)*

Keep each question answerable in a phrase. Never block on the optional one.

## Procedure

### Mode A — URL research → prefill
1. **Fetch the site.** Use your page-fetch tool (a web-fetch capability, or a scrape skill
   if available) on the homepage, the pricing page, and the about/product page. Extract:
   what the product does, who it's for, business model, pricing tiers, free trial,
   positioning language.
2. **Research the company + market** with your web-research backend (Perplexity MCP when
   present, else the built-in WebSearch fallback — deep research + targeted search): confirm
   the category, find direct + indirect
   competitors/alternatives, note stage signals if public (funding, team size, launch
   date). Cite URLs + access dates in a Research Notes footer.
3. **Fill researchable fields** from steps 1-2. For confirmable judgment calls (audience
   hypothesis, product complexity), write your best read AND a `[CONFIRM: …]` marker.
4. **Fold in `answers`** if the brief passed any (founder answers override guesses).
5. **Mark must-ask gaps.** Every MUST-ASK field not covered by `answers` gets a
   `[NEEDS FOUNDER INPUT: …]` marker inline and an entry in the Confirmation Gaps block.

### Mode B — Q&A → format
1. Map the founder's answers to the schema sections below. Light web research is allowed
   to enrich the product description and find competitive alternatives, but do NOT invent
   metrics, budget, or goals — those are founder-only.
2. Any minimal-set field the founder skipped → `[NEEDS FOUNDER INPUT: …]` + Confirmation Gaps.

### Both modes — derive Module Routing (Section 7) mechanically
From Q8 / the stated biggest problem:
- Traffic is the bottleneck (low visitors, channels not working) → **Demand Generation (first)**.
- Traffic converts poorly (decent visitors, low signup→paid) → **CRO (first)**.
- Both unclear / pre-launch → **Demand Generation (first)** (default; you can't optimize
  conversion without traffic). State the rationale in one or two sentences, quoting the
  founder's metrics.

> This plugin's pipeline is demand-gen-focused (it ends at demand-gen tactic synthesis).
> Always capture the routing honestly; if CRO is clearly primary, say so in Section 7 so
> the founder knows the free plugin addresses the demand-gen half.

## Output template (write EXACTLY this structure)

```markdown
# Diagnostic Interview Results
**Interview Date:** <YYYY-MM-DD>
**Source:** Diffmode Diagnostics Intake (<URL mode | Q&A mode | URL+Q&A>)
---
## 1. Product & Market Fundamentals
### Product Description
<2-4 sentences: what it is, core function, the after-state for the user>
### Business Model
**Type:** <e.g. B2B SaaS (usage-based)>
**Target segment:** <e.g. Mid-market teams (HR, Sales, Ops)>
### Pricing
**Primary tier:** <tier + price>
**Free tier/trial:** <Yes/No + detail>
### Target Audience (Founder's Hypothesis)
<roles / segments / industries>
**Ideal customer profile:** <one ICP sentence>
### Competitive Alternatives
**Direct competitors:** <named>
**Indirect alternatives:** <named, incl. "manual work / status quo">
---
## 2. Problem & Validation
### Product Complexity
**Classification:** <Self-explanatory | Requires some explanation | Requires a demo>
**Details:** <1-2 sentences>
### Problem Urgency
**Score:** <1-10 or [NEEDS FOUNDER INPUT]>
**Evidence:** <who feels the pain, when>
---
## 3. Current Growth Situation
### Stage
**Status:** <pre-launch | early | traction | growth — one line>
**Current metrics (last 30 days):**
- Visitors: <n or [NEEDS FOUNDER INPUT]>
- Signups: <n or [NEEDS FOUNDER INPUT]>
- Paying customers / MRR: <n / $ or [NEEDS FOUNDER INPUT]>
### What's Working
**Current acquisition sources:** <Q8 — where users/traffic come from today>
**Early wins:** <best-performing channel(s)>
---
## 4. Challenge Separation (CRITICAL)
### Demand Generation Challenges
**Current visitors/month:** <n>
**Target visitors/month:** <n>
**Traffic blockers:** <what's limiting top-of-funnel>
**Channels Attempted:**
| Channel | Result | Status |
|---------|--------|--------|
| <channel> | <result> | <Continuing/Stopped> |
### Conversion Rate Optimization Challenges
**Visitor → Signup:** <% or [NEEDS FOUNDER INPUT]>
**Signup → Paid:** <% or [NEEDS FOUNDER INPUT]>
**Conversion blockers:** <if known>
---
## 5. Resources & Constraints
### Time
**Founder availability:** <hrs/week on marketing or [NEEDS FOUNDER INPUT]>
**Team availability:** <roles or "solo">
### Budget
**Monthly marketing budget:** <$ / "no paid ads for now" / [NEEDS FOUNDER INPUT]>
**Hard constraints:** <e.g. paid ads ruled out>
### Technical Capabilities
- Landing pages: <Yes/No/Limited>
- Ad campaigns: <Yes/No/Limited>
- Content creation: <Yes/No/Limited>
- Analytics/tracking: <Yes/No/Limited>
### Goal & Timeline
**Primary goal:** <target metric + number>
**Deadline:** <timeframe>
**Stakes:** <why it matters — optional>
---
## 6. Tactical Constraints & White Space
### Tactics Ruled Out by Founder
| Tactic/Channel | Reason Dismissed |
|----------------|------------------|
| <tactic> | <reason> |
### Competitor Dignity Constraints
<things competitors avoid doing — opportunity hints — or "Not specified">
---
## 7. Module Routing
### Primary Focus Recommendation
**Module:** <Demand Generation (first) → then CRO | CRO (first)>
**Rationale:** <1-2 sentences quoting the metrics that drove the call>
### Key Constraints to Honor
- <constraint>
---
## Confirmation Gaps
<Bulleted list of every [NEEDS FOUNDER INPUT] / [CONFIRM] marker above, so the
orchestrator can ask the founder. Empty list = "None — all fields captured.">
---
## Research Notes (URL mode)
<Sources used: URL + access date for each. Mark estimates [Estimated]/[Unverified].>
---
*Diagnostics complete. Ready for Enrichment Stage.*
```

## Validation checklist (self-check before returning)

- [ ] All 7 sections present, in order, with the exact `## N.` headers above.
- [ ] Section 1 product description is specific to THIS product (not generic).
- [ ] Section 4 separates demand-gen (traffic) from CRO (conversion) — the Q8 signal.
- [ ] Section 5 budget + technical capabilities are present (the constraints parser reads
      "Monthly marketing budget", the skills bullets, MRR, and "solo"/team — keep those
      exact labels so the parser finds them).
- [ ] Section 7 routing is derived from the stated problem, with a one-line rationale.
- [ ] Every founder-only field is either filled from `answers` or marked
      `[NEEDS FOUNDER INPUT]` AND listed in Confirmation Gaps — never silently invented.
- [ ] No strategy/recommendations leaked in (capture only).
- [ ] URL mode: Research Notes footer cites real URLs + access dates.
