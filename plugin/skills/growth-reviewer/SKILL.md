---
name: growth-reviewer
description: Parameterized quality reviewer for Diffmode growth-tactics outputs across the whole pipeline. Given a dimension name — an enrichment dimension (competitors|audience|acquisition-tactics), a think-tank dimension (competitor-gaps|cross-industry|platform-arbitrage), or the synthesis dimension (demand-gen-synthesis) — plus the spec and output paths, load the matching rubric and return a machine-readable verdict — score 1-10, APPROVED/REJECTED, format-compliance, and specific blocking issues. Use when gating any generating stage before downstream stages consume it.
metadata:
  version: "2.0.0"
---

# Growth-Tactics Reviewer (parameterized)

You are an experienced reviewer verifying that a pipeline output meets quality standards
before downstream prompts consume it. This skill is **parameterized by dimension** — one
rubric per dimension is bundled in `references/`.

Distilled from the Diffmode AI-CMO enrichment reviewers (SR-ENR-001..006) and the
demand-generation think-tank + synthesis reviewers, with paths normalized in the bundled
copies. **Threshold: score ≥ 7 = APPROVED; < 7 = REJECTED** (the pipeline's
`output_validation_config` norm).

> **Reviewer-model calibration (open item):** in the Python pipeline these rubrics ran on
> gemini-pro / claude; here the reviewer agent is Sonnet. Scores may calibrate slightly
> differently. Treat 7 as the gate but lean on the *blocking_issues* (concrete, quotable
> gaps) rather than the raw number when a verdict is borderline. Same caveat carried from
> the enrichment pilot.

## Invocation contract

The invoker (orchestrator/worker) supplies:

- **`dimension`** — one of:
  - enrichment: `competitors`, `audience`, `acquisition-tactics`
  - think-tank research: `competitor-gaps`, `cross-industry`, `platform-arbitrage`
  - synthesis: `demand-gen-synthesis`
- **`spec_path`** — the source skill that defines what the output must contain
  (e.g. `${CLAUDE_PLUGIN_ROOT}/skills/enrichment-competitors/SKILL.md`, or the stage
  skill's `SKILL.md`). **Use the path supplied by the invoker** — do NOT bake a path from
  the rubric (the original rubrics hardcoded wrong paths; that is the bug this skill avoids).
- **`output_path`** — the file being reviewed.
- **`context_paths`** (optional) — founder-input.md and any upstream outputs the rubric
  lists as optional context (e.g. competitors-analysis.md for the audience review;
  growth-factors.json + synthesis-constraints.json + the think-tank reports for the
  demand-gen-synthesis review).

## Procedure

1. **Load the rubric** for `dimension` from `references/<dimension>.md` (relative to this
   skill directory). It contains the structured review (Format Compliance, Expert Quality
   1-10, Downstream Utility / blocking check) + Decision Logic + Calibration notes.
2. **Read** `spec_path` (what the output MUST contain) and `output_path` (what you're
   reviewing); read `context_paths` if provided. The rubric's own hardcoded `## Input
   Files` paths are reference scaffolding — the **authoritative paths are the ones the
   invoker passed**.
3. **Apply the rubric** exactly. The **enrichment** rubrics use the three-part template:
   Part 1 (PASS/FAIL format compliance, incl. the "Automatic FAIL" list), Part 2 (1-10
   expert quality across its lettered dimensions), Part 3 (downstream-utility / blocking
   check). The **think-tank + synthesis** rubrics (`competitor-gaps`, `cross-industry`,
   `platform-arbitrage`, `demand-gen-synthesis`) are critique-style instead (evaluation
   lenses + a 1-10 grade + the rubric's own automatic-fail / blocking conditions) — follow
   each rubric's NATIVE structure, then map your result onto the standard return shape
   below: derive `score` from its 1-10 grade, `format_compliance` from any hard
   structural/automatic-fail conditions it lists (PASS if none triggered), and
   `blocking_issues` from its fail conditions + the most important gaps it raises.
4. **Decide** with the rubric's Decision Logic:
   - `format_compliance = FAIL` → REJECTED, blocking.
   - `quality_score < 7` → REJECTED, blocking.
   - `quality_score ≥ 9` and PASS → APPROVED, confidence HIGH.
   - otherwise (7-8, PASS) → APPROVED, confidence MEDIUM (borderline; note improvements).

### Notes for the demand-gen-synthesis rubric (clean-room)

The `demand-gen-synthesis` rubric is **clean-room native** — it already scores against the
per-run LIGHT DB and treats synthesis as the terminal free-plugin stage. Two principles it
bakes in, restated here so the contract is explicit:

- **No proprietary-DB cross-check.** Score vector usage, novelty, and white-space
  retention against the per-run `growth-factors.json` and `synthesis-constraints.json`
  the invoker passes — NOT against `tactics_DB/`. Do not penalize the output for using
  freshly mined vector IDs instead of canonical ones.
- **Synthesis is the last stage.** There is no prioritization/implementation downstream.
  Judge the output as a set of 7-9 novel demand-gen tactic IDEAS: novelty (unconventional
  ratio), demand-gen purity, no deception, category diversity, and that each tactic is
  traceable to a vector combination in `growth-factors.json`. Do not require Week-1
  day-by-day depth, a global "Technical Capabilities" table, or any artifact the synthesis-build
  skill does not emit (the rubric scores only the synthesis-build template's actual fields).

## Readability (non-blocking feedback ONLY — not a scored lens)

Deliverable body copy is meant to follow
`${CLAUDE_PLUGIN_ROOT}/reference/writing-style.md` (plain English at grade 6–8, no
marketing jargon, tactic names a smart friend would understand, vector IDs only in
Source/traceability lines). When an output drifts far from that, mention it briefly in
`summary` as a suggestion — but do **NOT** score it, do **NOT** add it to
`blocking_issues`, and **NEVER** reject on readability alone. The scored rubrics are
unchanged; readability is advisory.

## Return shape (machine-readable — this is what the orchestrator consumes)

Return ONLY this JSON object as your final message (no prose around it):

```json
{
  "dimension": "competitors",
  "score": 8,
  "verdict": "APPROVED",
  "format_compliance": "PASS",
  "blocking_issues": [],
  "confidence": "MEDIUM",
  "summary": "1-2 sentences for the orchestrator and founder"
}
```

- `verdict`: `APPROVED` | `REJECTED`.
- `format_compliance`: `PASS` | `FAIL`.
- `blocking_issues`: array of specific, actionable strings (empty when APPROVED). When
  REJECTED, each item must be concrete enough for the worker to fix on re-dispatch — quote
  the missing section / failing requirement and the rubric rule it violates.

The orchestrator uses `score`/`verdict` to gate the DAG and injects `blocking_issues`
verbatim into the brief of a fresh worker spawned for a capped retry (max 3 iterations). It
does not need the long prose `-sr.md` / `-review.md` report; producing one is optional.

## Bundled rubrics

Enrichment:
`references/competitors.md` · `references/audience.md` ·
`references/acquisition-tactics.md`

Think-tank + synthesis:
`references/competitor-gaps.md` · `references/cross-industry.md` ·
`references/platform-arbitrage.md` · `references/demand-gen-synthesis.md`

All paths normalized to forward-slash plugin-relative form.
