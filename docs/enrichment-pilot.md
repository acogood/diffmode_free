# Enrichment pilot: corrected DAG, distillation map, file layout

The enrichment stage is the pilot because it is **script-free** and **vector-DB-free**
— the cleanest possible mapping. This doc is the build spec for the enrichment dimension
skills + reviewer + the worker agents + 1 orchestrator. (It originally mapped 5 dimension
skills; `demographics` and `purchase-objections` were since dropped — see the callout below —
leaving **3 live dimensions**: competitors, audience, acquisition-tactics.)

## The corrected enrichment DAG

Verified against `manual_test_automation/workflow-config.yaml` lines 30–133.
Thresholds: **score ≥ 7, max 3 iterations** (`output_validation_config`).

```
competitors            (gate, blocking; execution_group 1)
   ├─► audience              (depends_on: competitors)              ┐ Wave 2 (parallel)
   └─► acquisition-tactics   (depends_on: competitors; LEAF)        ┘
```

> **demographics removed (2026-05-28), purchase-objections removed (2026-06-01).**
> `demographics` was dropped because the FREE plugin runs no SSR (the paid/SSR pipeline keeps
> `prompts/enrichment/demographics.md`). `purchase-objections` was a verified **dead leaf** —
> nothing downstream consumed it (no think-tank, no synthesis step, no `pass2`) — so it was
> dropped to take a whole reviewer-gated stage off the critical path. Enrichment is now **2
> waves**: `competitors → audience ‖ acquisition-tactics`. (If objections are wanted later
> they'd need wiring into `pass2` first.)

### Corrections vs. prior assumptions (and the old memory)

- **acquisition-tactics is a leaf** — nothing downstream in *enrichment* consumes it.
  (Think-tanks consume it later, out of pilot scope.)

### Per-dimension inputs (the real context wiring)

| Dimension | Inputs (workspace-relative unless noted) | Web research? | Output |
|-----------|------------------------------------------|---------------|--------|
| competitors | `01-diagnostics/founder-input.md`; `Marketing-Channel-Menu-2025-Extended.md` (repo root) | **yes** | `02-enrichment/competitors-analysis.md` |
| audience | `01-diagnostics/founder-input.md`; `02-enrichment/competitors-analysis.md`; **`Marketing-Channel-Menu-2025-Extended.md` (root) — added, see bug fix #1** | **NO** | `02-enrichment/audience-jtbd.md` |
| acquisition-tactics | `01-diagnostics/founder-input.md`; `02-enrichment/competitors-analysis.md`; `Marketing-Channel-Menu-2025-Extended.md` (root) | **yes** | `02-enrichment/acquisition-tactics.md` |

`competitors-analysis.md` is the true gatekeeper — shared by the other 2 dimensions
(audience + acquisition-tactics).

## Distillation map (prompt → skill)

Each dimension skill is ≈90% of the existing prompt, restructured as a standalone,
runtime-agnostic instruction doc. **Removed** on distillation: hardcoded absolute save
paths (`/ai-cmo-workspace/02-enrichment/…`) — replaced by an `## Inputs & Output`
contract where the orchestrator/worker supplies paths. **Kept verbatim:** the scope
guardrails (✅DO/❌DON'T), the analysis frameworks, the output templates, the
self-validation checklists.

| Skill | Source prompt | Core logic distilled |
|-------|---------------|----------------------|
| `enrichment-competitors` | `prompts/enrichment/competitors.md` (ENR-002 v2.1) | tier taxonomy (`market_leader`/`indie_direct`/`indirect`), indie-tier verification gate (both-halves), 11-category acquisition breakdown, growth-loop + trajectory analysis, channel matrix, mix-verification line. Documentary only. |
| `enrichment-audience` | `prompts/enrichment/audience.md` (ENR-001 v3.1) | Advanced JTBD (3–4 segments), 6-criteria scoring, per-segment channel-fit framework. **Analysis only — no web research.** |
| `enrichment-acquisition-tactics` | `prompts/enrichment/acquisition-tactics.md` (ENR-004 v2.3) | 25–35 tactics (competitor/adjacent/unconventional), scrappy-competitor playbook, required-fields schema, effort-to-signal matrix, loop-potential. |
| `growth-reviewer` | `prompts/reviewers/enrichment/*.md` (SR-ENR-00x) | parameterized: loads the named dimension rubric (bundled in `references/`), emits `{score, verdict, format_compliance, blocking_issues}`. |

> `enrichment-purchase-objections` (ENR-005 — 7-category objection mining) was also distilled
> here originally, but the dimension was removed 2026-06-01 (dead leaf — see the DAG callout),
> so its skill + rubric no longer ship.

## File layout (canonical sources in this repo)

```
pipeline-skills/
  skills/
    enrichment-competitors/SKILL.md
    enrichment-audience/SKILL.md
    enrichment-acquisition-tactics/SKILL.md
    growth-reviewer/
      SKILL.md
      references/
        competitors.md            ← copied from prompts/reviewers/enrichment/, paths fixed
        audience.md
        acquisition-tactics.md
  agents/
    enrichment-research-worker.md   tools: Read,Write,Glob,Grep,mcp__perplexity__perplexity_research,_search; model: sonnet
    enrichment-analysis-worker.md   tools: Read,Write,Glob,Grep (NO research MCP) — audience only
    growth-reviewer.md          tools: Read,Glob,Grep
  commands/
    run-enrichment.md               --product <slug>
```

## Worker → dimension assignment

| Wave | Dimension | Worker | Reviewer rubric |
|------|-----------|--------|-----------------|
| 1 | competitors | `enrichment-research-worker` | competitors |
| 2 | audience | **`enrichment-analysis-worker`** (no MCP) | audience |
| 2 | acquisition-tactics | `enrichment-research-worker` | acquisition-tactics |

## Bug fixes (corrections made during distillation — NOT copied forward)

1. **Audience / channel-menu omission.** `workflow-config.yaml` passes only
   `founder-input.md` + `competitors-analysis.md` to `enrichment-audience`, but the
   audience prompt body (Step 2.5, Constraints "use ALL input files: …
   Marketing-Channel-Menu-2025-Extended.md") *relies on* the channel menu. The
   `enrichment-audience` SKILL.md declares the channel menu as a **required input**,
   and the orchestrator passes it. A strict improvement over the latent pipeline bug.
2. **Reviewer path bugs.** The rubrics hardcode Windows-style / wrong spec paths
   (`prompts\02-enrichment\enrichment-competitors.md`) and backslash workspace paths
   (`ai-cmo-workspace\02-enrichment\…`). Two-part fix: (a) the **orchestrator passes
   spec + output paths as arguments** to the reviewer worker — paths are not baked
   into the reviewer skill; (b) the **bundled rubric copies** in
   `growth-reviewer/references/` have all paths normalized to forward-slash,
   repo-relative form so the reference material is internally correct.

## Idempotency

Overwrite-on-rerun for `02-enrichment/*.md`, matching the current CLI. A re-run of
`/run-enrichment --product <slug>` regenerates the three files from scratch. The
dry-run procedure (`../../pipeline-skills/README.md` → verification, and `full-pipeline-map.md`) writes
into a scratch copy to honor the repo's "never edit originals" rule for known-good
outputs.
