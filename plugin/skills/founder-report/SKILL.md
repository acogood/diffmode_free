---
name: founder-report
description: Founder-report packaging stage for the Diffmode growth-tactics pipeline — the post-gate step that turns the APPROVED synthesis.md (a reviewer-facing working paper) into growth-tactics.md, the founder-facing "Your Growth Tactics" report. Strict re-packaging per the central writing-style.md — plain tactic cards (what it is, why competitors can't copy it, how to start this week, time to first signal, what you need, kill it if) with ZERO pipeline plumbing — no vector IDs, no Pass labels, no pools, no numeric scores, no self-grading. Adds no new claims, numbers, tactics, or estimates — every sentence traceable to synthesis.md. Use after the synthesis build reviewer gate and before the HTML report render. Best-effort by design — if it fails, the report falls back to synthesis.md.
metadata:
  version: "1.0.0"
---

# Founder Report — package `synthesis.md` into "Your Growth Tactics"

`synthesis.md` is written to pass a reviewer: it carries disposition tables, traceability
lines, pool audits, and self-grades, because downstream checks parse them. That makes it a
**working paper**, not a deliverable. This stage derives the founder view: it reads the
APPROVED `synthesis.md` and re-packages the tactics into `growth-tactics.md` — the page the
founder actually opens first. `synthesis.md` itself is **never modified** (its structure is
a load-bearing contract with the reviewer and the orchestrator's checks).

## The one rule — re-package, never re-author

**Zero new content.** Every sentence in the output must be traceable to something
`synthesis.md` already says. Specifically:

- **No new claims, numbers, estimates, channels, or tactics.** If synthesis.md doesn't say
  it, the report doesn't either.
- **Tactic count and names are preserved exactly** — same tactics, same order, same names —
  minus bracket tags: strip the ` — [Pass 1 White Space]` / ` — [Pass 2 Synergy/Founder-Fit]`
  origin labels from titles, and strip `[HIGH COMPLEXITY]` / `[LOW CONFIDENCE]` flags from
  names. Where such a flag exists, say it in plain words inside the card instead (e.g. "this
  is the heaviest lift in the set" under **What you need**).
- **Allowed transformations:** reorder, merge fields, strip labels and citations, split long
  sentences, and simplify wording to meet `writing-style.md`. Nothing else.

## Inputs & Output

- `WS/03-think-tanks/demand-generation/synthesis.md` (PRIMARY — the APPROVED final
  synthesis; read-only)
- `${CLAUDE_PLUGIN_ROOT}/reference/writing-style.md` (the voice contract — grade 6–8,
  ≤~20 words per sentence, banned-jargon table, the coffee test)
- **OUTPUT**: `WS/03-think-tanks/demand-generation/growth-tactics.md` (write no other files)

## Document skeleton (exactly these sections, in this order)

### 1. `# Your Growth Tactics`

A 2-3 sentence intro: what these tactics are, why they fit THIS founder (pull the budget /
team / stage facts from the Synthesis Overview's Constraint Summary), and how to use the
document (start with the quick wins, read each card before committing).

### 2. `## Start this week`

The tactics whose first signal arrives within ~4 weeks — take them from the Tactical
Clusters quick-wins group. One line each: the tactic name + what you'd do first. No card
detail here; the cards follow.

### 3. `## The tactics`

One card per tactic, in synthesis order. Heading: `### N. <Name>` (sequential number, plain
name, no bracket labels). Each card has **exactly these 7 fields, in this order**:

| Field | Built from (synthesis.md) | Rules |
|-------|---------------------------|-------|
| **What this is** | `In plain English` (+ `Emergent Mechanism` where it clarifies) | 1-3 short sentences; what you actually do |
| **Why competitors can't copy it** | `Structural Advantage` (+ the competitive-adoption note from `Primary Channel(s)`) | strip taxonomy labels ("Type: …") — keep the plain reason and how long the edge lasts. KEEP competitor-adoption lines like "nobody in your market does this yet" |
| **How to start this week** | `How to Execute` steps, kept verbatim where they're already plain | fold in useful `Adapted to Your Constraints` context (e.g. "scaled down to fit your $500/month") |
| **Time to first signal** | `Expected Timeline & Success Metrics` | the early signal + when to expect it; strip any `(per …)` vector citations |
| **What you need** | `Required Resources` (+ `Skills Required` where it adds something) | time / budget / tools, in one or two lines |
| **Kill it if…** | the decision point in `Expected Timeline & Success Metrics` | the concrete number/date that says stop or double down |
| **Execute this** | derived from the tactic's first steps | 2-3 specific tools, skills, or templates that help execute the first steps — see rules below |

**"Execute this" rules.** This field is the ONE exception to the "zero new content" rule —
it names execution aids, not strategic claims. Scope it tightly:

- Name 2-3 concrete tools, agent skills, or templates that help the founder execute the
  tactic's first steps. Match them to what the tactic actually involves:
  - Outreach / cold email → the `cold-email` skill (coreyhaines31/marketingskills) or the
    agent's built-in writing
  - Copy / messaging → the `copywriting` skill or the agent's built-in writing
  - Landing page / demo → v0.dev, the `free-tools` skill, or the agent's code generation
  - Community / social → the `community-marketing` or `social` skill
  - Content / SEO → the `content-strategy` or `ai-seo` skill
  - Design / visual assets → Canva, Figma, or the agent's image generation
  - Tracking / measurement → a simple spreadsheet with columns for the kill-signal metric
- Format as a short bulleted list: `→ <what>: <tool/skill name>`.
- Do NOT invent tactics, channels, or numbers here — only name execution tools.
- If the tactic is purely manual (e.g. "walk into 10 coffee shops"), say
  `→ No tools needed — this is a shoes-on-the-ground play.`

### 4. `## What to avoid`

From the Anti-Portfolio. Per item: why founders try it, why it fails for THIS founder, and
what to do instead (point at the relevant card by number). No severity labels, no
"anti-pattern" vocabulary — just plain warnings.

### 5. `## How to sequence these`

The timeline clusters in plain words (this week / this month / the long game), then the
Top 5 as "if you only run five, run these" — each with a **one-line plain reason** taken
from what synthesis.md already says about it (fit, speed, the edge). **No numeric scores
anywhere** — the founder gets reasons, not grades.

### 6. `## Where these came from`

One short paragraph: these tactics were built by combining growth mechanisms mined from
real, public case studies during this run, and checked against this founder's budget, team,
and stage; the reason they're defensible is that copying them would force a bigger
competitor to work in a way their structure doesn't allow. Then point the curious reader at
the two working papers in the same report: **How These Were Built** (the mechanism
combinations) and **Tactic Engineering Notes** (the full engineering write-up, scores and
traceability included). This must be the LAST section.

## Banned in the output (deterministic — the orchestrator greps for these)

The orchestrator rejects the output if any of these appear. Self-grep before returning:

| Banned | Why |
|--------|-----|
| vector IDs — regex `(struct\|lever\|resource\|psych\|pos\|conv)-[0-9]` | plumbing; lives in synthesis.md only |
| `Pass 1` / `Pass 2` | pipeline phase labels |
| `must_include` | constraints plumbing |
| `Pool A` / `Pool B` | constraints plumbing |
| `white space` / `white-space` (any case) | pipeline vocabulary |
| `growth-factors.json` | internal file name |
| `PASS` / `FAIL` self-grading | the founder report doesn't grade itself |
| `/10` or `/50` scores | no numeric scores in the founder view |
| "anti-pattern" (any case) | jargon; say what to avoid in plain words |

Plus everything `writing-style.md` already bans (leverage, optimize, arbitrage, …).

## Self-check (before returning)

- [ ] Card count under `## The tactics` == the number of `### Tactic #N` blocks in
      synthesis.md, same order, same names (minus bracket tags).
- [ ] Every card has all 7 fields, in the listed order (including "Execute this").
- [ ] Banned-pattern grep over the output is empty.
- [ ] The document's last section is `## Where these came from`.
- [ ] Voice: grade 6–8, ≤~20 words per sentence, passes the coffee test, no banned jargon —
      per `writing-style.md`.
- [ ] Spot-check 2-3 cards: every sentence traces to the matching tactic in synthesis.md —
      no invented numbers, channels, or steps.

This stage is **best-effort by design**: if it can't produce a clean output, the pipeline
ships `synthesis.md` as the main page (old behavior). Never degrade `synthesis.md` to make
this stage pass.
