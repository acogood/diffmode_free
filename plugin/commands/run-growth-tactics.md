---
description: Full Diffmode free growth-ideation pipeline — intake → enrichment → think-tanks → per-run clean-room LIGHT vector DB → 4-step synthesis of 7-9 novel demand-gen tactic ideas. Writes to ./<slug>/ in your cwd; stops at synthesis.
---

# Run Growth Tactics

Main-thread orchestrator for the **Diffmode free growth-ideation pipeline** — from a fast
founder intake all the way to a final `synthesis.md` of **7-9 novel demand-gen tactic
IDEAS**, and it **STOPS there**. Prioritization, implementation guides, and the proprietary
576-vector database are the paid product; this command never attempts them.

It runs the workflow as skills + worker sub-agents. It owns the DAG, the parallel fan-out,
the reviewer-retry quality gate, and the stage-boundary checks, and supersedes
`run-enrichment.md` (which remains a standalone entry for running enrichment alone).

> **This command runs in the main thread.** It dispatches worker sub-agents via the
> Agent/Task tool, and it is the only place that may talk to the human (via AskUserQuestion,
> for intake). It must NOT itself be run as a sub-agent — sub-agents are one level deep and
> could not then spawn the workers. (See the repo's `docs/architecture.md` — internal design
> notes, not shipped in the plugin.)

> **Naming under the plugin.** Ships in the `diffmode-growth-tactics` plugin; invoked as
> `/diffmode-growth-tactics:run-growth-tactics`. Use these exact plugin-namespaced ids in
> Agent-tool dispatches:
> - skills: `diffmode-growth-tactics:diagnostics-intake`,
>   `diffmode-growth-tactics:enrichment-<dimension>`,
>   `diffmode-growth-tactics:competitor-gaps` · `:cross-industry` · `:platform-arbitrage`,
>   `diffmode-growth-tactics:growth-factors-mining`, `diffmode-growth-tactics:lite-constraints`,
>   `diffmode-growth-tactics:synthesis-step1-combinations` · `:synthesis-step2-mechanisms` ·
>   `:synthesis-pass1-whitespace` · `:synthesis-pass2-founder`
> - workers: `diffmode-growth-tactics:research-worker`,
>   `diffmode-growth-tactics:analysis-worker`, `diffmode-growth-tactics:synthesis-worker`,
>   `diffmode-growth-tactics:reviewer`
> The plugin is **self-contained**: it reads its bundled channel menu from
> `${CLAUDE_PLUGIN_ROOT}/reference/` and writes all run outputs to a `./<slug>/` workspace in
> the user's current directory. No host repo is required.

## Arguments

`$ARGUMENTS`:

- `--url <site>` — research a website to prefill diagnostics (e.g.
  `--url https://theona.ai`). The workspace slug is derived from the host (`theona.ai`)
  unless `--product` is also given.
- `--product <slug>` — names the workspace at `./<slug>/` in the current directory. Required
  if no `--url`. With both, `--url` feeds intake and `--product` names the workspace.
- `--from <stage>` — resume from a stage, reusing earlier outputs on disk.
- `--only <stage>` — run just one stage (its inputs must already exist).
- `--remine` — force `growth-factors-mining` to re-research instead of reusing a cached
  `growth-factors.json`.
- `--scratch` — write stage outputs to `*-scratch/` sibling dirs, preserving known-good
  originals (honors the "never edit originals" rule for dry-runs / parity checks).
- `--fast-intake` — in URL mode, skip the founder Q&A and accept the researched prefill
  with `[NEEDS FOUNDER INPUT]` placeholders left in (useful for demos; quality is lower).

**Stage names** (for `--from` / `--only`): `diagnostics`, `enrichment`, `think-tanks`,
`growth-factors`, `lite-constraints`, `synthesis` (or finer synthesis steps `step1`,
`step2`, `pass1`, `pass2`).

## Pre-flight

1. **Resolve the workspace** — `WS = ./<slug>` under the user's **current working directory**
   (slug from `--product`, else derived from the `--url` host, e.g. `theona.ai`). Create
   `WS/01-diagnostics`, `WS/02-enrichment`, `WS/03-think-tanks/demand-generation` as needed
   (or the `*-scratch` variants under `--scratch`). **No host repo is required** — the plugin
   is self-contained and writes the run into the cwd.
2. **Confirm the channel menu** — `${CLAUDE_PLUGIN_ROOT}/reference/Marketing-Channel-Menu-2025-Extended.md`
   exists (it is bundled in the plugin; `${CLAUDE_PLUGIN_ROOT}` expands to the plugin's
   install directory at runtime). All stages that need the channel taxonomy read it from
   there.
3. **Confirm the plugin is active** — its skills/agents (`diffmode-growth-tactics:*`) exist
   whenever the plugin is enabled. If a dispatch reports an unknown agent/skill, the plugin
   isn't enabled — run `/plugin` → enable `diffmode-growth-tactics` (or
   `claude plugin install diffmode-growth-tactics@diffmode-free`).
4. **Reviewer gate** — score **≥ 7**, **max 3** iterations per gated stage (the pipeline norm).

## The DAG

```
Stage 0    diagnostics-intake        → WS/01-diagnostics/founder-input.md
Stage 1    enrichment (2 waves)      → WS/02-enrichment/*.md
              Wave 1 (gate):  competitors
              Wave 2 (‖):     audience ‖ acquisition-tactics
Stage 1.5  growth-factors mining     → …/growth-factors.json  (LIGHT DB)
              ↑ starts right after Wave-1 competitors is APPROVED and runs
                CONCURRENTLY through the rest of enrichment + Stage 2; structural
                check only (no reviewer gate); collected/validated at the Stage-3 boundary.
Stage 2    think-tank ×3             (parallel, after enrichment)
              competitor-gaps · cross-industry · platform-arbitrage
Stage 3    lite-constraints          → WS/03-think-tanks/demand-generation/synthesis-constraints.json
              precondition: growth-factors.json present + valid
Stage 4    synthesis  step1 → step2 → pass1 → pass2   → synthesis.md   (STOP)
```

Filesystem state is the contract between stages (same pattern as the enrichment pilot).
**`growth-factors-mining` is deliberately hoisted to Stage 1.5** — it strictly needs only
`founder-input.md` (its enrichment inputs are optional search seeds), so overlapping it with
enrichment + the think-tanks takes its ~40-min runtime off the critical path.

## The per-stage routine (generate → check → reviewer loop)

For each generating stage `S` with worker `W`, output `O`, and (where it has one) rubric
dimension `D` + spec `Spec`:

1. **Dispatch the worker** — Agent tool, `subagent_type = W`, with a self-contained brief:
   ```
   skill:   diffmode-growth-tactics:<skill>
   inputs:  [ …paths… ]
   output:  <O>
   blocking_issues: <none on first pass; reviewer items verbatim on a retry>
   ```
   The worker loads the skill, reads inputs, (researches/reasons), writes `O`, returns
   `{status, outputPath, summary}`. **Capture wall-clock:** before dispatching, run `date +%s`
   (you have Bash) and remember it as the stage's `started_at`; after the attempt resolves,
   run `date +%s` again and compute `duration_s = end − start`. **After every attempt** (this
   one and each retry below), append a row to the run-ledger (`WS/.run-state.json`):
   `{stage, attempt, verdict, score, started_at, duration_s}` — see *Run-ledger* near the end
   of this file. (Timing is additive instrumentation: never block a stage on it.)

   > **Worker lifecycle (read this — it prevents two bugs).** Workers are **stateless and
   > NOT addressable after they return.** Every retry (for ANY reason — gap, reviewer
   > rejection, or a dispatch failure) **spawns a FRESH worker** with the same brief plus any
   > injected `blocking_issues`. **Never `SendMessage` a worker that has already returned** —
   > there is no "re-dispatch the same worker." (The single-shot pattern: "retry that single
   > agent ONCE" via a fresh spawn.) This keeps the architecture reproducible: no main-thread
   > content fallback.

   **Three dispatch outcomes** (handle each):
   - **`ok`** → go to step 2.
   - **`error`** (worker returned `{status:"error", reason}`) → surface `reason` and stop
     this branch (the input it named must be fixed).
   - **dispatch failed / worker died mid-run** (API/socket error, no JSON returned at all) →
     **re-spawn a FRESH worker** with the identical brief, up to **2×** (transient socket
     deaths usually clear on a fresh spawn). If it still dies after 2 fresh spawns, mark `S`
     FAILED with code **`worker-dispatch-failed`** and **print the exact resume command**
     (`--from <stage>` or `--only <stage>`) so the user can resume cheaply from disk. Do NOT
     do the worker's content work in the main thread.
2. **Stage-boundary completeness check** (replaces Python `verify_outputs`): confirm `O`
   exists and is non-empty (`test -s`), AND — critically — that it is **not truncated**.
   `test -s` + a first-header grep both pass on a file that died mid-write, so for markdown
   stages require the stage's **LAST** required section to be present (a worker that crashed
   mid-write won't have reached it), plus a sane **min-line floor** for the large stages.
   For JSON stages: parses + has the required keys + expected counts. Per-stage anchors:

   | Stage | Last-required-section anchor | Min-line floor |
   |-------|------------------------------|----------------|
   | step1 (`synthesis-step1-combinations.md`) | `## Summary Statistics` | ~80 |
   | step2 (`synthesis-step2-mechanisms.md`) | the dedup/verb-group result section | ~80 |
   | pass1 (`synthesis-pass1.md`) | `## Generated Tactics` (with ≥4 `### ` tactic blocks) | ~60 |
   | pass2 (`synthesis.md`) | `## Post-Synthesis Self-Review` | ~150 |
   | enrichment / think-tank `.md` | the skill's final section | per skill |

   If the worker returned `ok` but `O` is missing / empty / **lacks its last-required section
   or falls under the floor** (i.e. truncated — a mid-write death), treat it like a dead
   worker: **spawn a fresh worker** once noting the gap (a full regenerate, since a truncated
   file has no sections to `Edit` onto).
3. **Reviewer loop** (only for stages with a rubric — see table): dispatch
   `diffmode-growth-tactics:reviewer` with `{dimension: D, spec_path: Spec, output_path: O,
   context_paths: […upstream…]}`; read the JSON verdict. If `APPROVED` (score ≥7, format
   PASS) → done. If `REJECTED` and `iter < 3` → **spawn a FRESH worker** `W` with the same
   brief plus `blocking_issues` injected verbatim; re-check; `iter++`. If `REJECTED` at
   `iter = 3` → mark `S` FAILED, record blocking_issues, stop dependents.

   > **Smaller-retry rule (format-only fixes on a large existing file).** When the rejection
   > is **format-only** (missing sections, missing checklist) and `O` already exists and is
   > large, the re-dispatch brief MUST set `retry_mode: format-only` and instruct the fresh
   > worker: **"use the `Edit` tool to ADD the missing sections in place; do NOT
   > Read-then-Write the whole file."** The three writing workers now carry the `Edit` tool,
   > so this is a real, small in-place patch — not a full regenerate. (A full rewrite of a
   > ~900-line file is what repeatedly hit socket deaths in the field; a targeted `Edit` is
   > far smaller and safer.) Fail-clean is unchanged: a worker that dies twice is still
   > `worker-dispatch-failed` with a resume hint — **the orchestrator never does the worker's
   > content work in the main thread, including never patching `O` itself.**

Stages **without** a rubric (growth-factors, lite-constraints, and synthesis step1/step2/
pass1) get a **structural check only** (step 2) — see each stage below. Only the enrichment
dimensions, the 3 think-tanks, and the final `pass2` synthesis are reviewer-gated.

## Stage 0 — Diagnostics intake (the entry point)

Goal: produce `WS/01-diagnostics/founder-input.md`. If it already exists and `--from` is
past `diagnostics`, skip. **Human interaction happens HERE, in the main thread.**

**Collect the must-ask fields** (the things a website can't reveal) via `AskUserQuestion`.
Recommended batching (≤4 questions/call; founders pick "Other" to free-type):

- *Call 1 (structured):* **Stage** [pre-launch / early / traction / growth]; **Monthly
  marketing budget** [$0 / under $500 / $500-2k / $2k+]; **Biggest growth problem** [Not
  enough traffic (demand gen) / Traffic doesn't convert (CRO) / Both]; **Skills you can do**
  (multiSelect) [landing pages / content / ad campaigns / analytics].
- *Call 2 (free-form, founders use "Other"):* **Current traction** (visitors/signups/MRR/
  paying customers — or "pre-launch"); **Primary goal + deadline**; **Where users/traffic
  come from today** (the Q8 acquisition signal); and — **only if no `--url`** — **product
  one-liner + business model/pricing + target-audience hypothesis**.

(Skip Call 2 / accept placeholders if `--fast-intake`.)

Then dispatch **`research-worker`** with skill `diffmode-growth-tactics:diagnostics-intake`:
- URL mode: pass `--url <site>` + the collected `answers`. The worker scrapes homepage/
  pricing/about + a Perplexity pass to fill researchable fields, folds in `answers`, marks
  any remaining gaps, writes `founder-input.md`.
- No-URL mode: pass the `answers` (incl. product/model/audience). The worker formats them
  into the schema (light research allowed to enrich product description + competitive
  alternatives), writes `founder-input.md`.

**Check:** `founder-input.md` exists, non-empty, has the 7 `## N.` sections (grep
`## 1. Product`, `## 4. Challenge Separation`, `## 5. Resources`, `## 7. Module Routing`).
If a `## Confirmation Gaps` block lists must-ask fields and not `--fast-intake`, ask the
founder those specific gaps (one more `AskUserQuestion`) and patch the file in the main
thread. No reviewer rubric for diagnostics (it's capture, not analysis).

## Stage 1 — Enrichment (2 waves)

Run the enrichment DAG exactly as `run-enrichment.md` specifies (that file is the detailed
reference and the standalone entry). Compactly:

```
Wave 1 (blocking gate):  competitors
Wave 2 (parallel):       audience  ‖  acquisition-tactics     (depend on competitors)
```

Per-dimension wiring (worker · inputs · reviewer spec):

| Dim | Worker | Inputs | Reviewer spec_path | rubric dim |
|-----|--------|--------|--------------------|-----------|
| competitors | research-worker | founder-input; channel menu | `${CLAUDE_PLUGIN_ROOT}/skills/enrichment-competitors/SKILL.md` | competitors |
| audience | **analysis-worker** (no MCP) | founder-input; competitors-analysis; channel menu | `${CLAUDE_PLUGIN_ROOT}/skills/enrichment-audience/SKILL.md` | audience |
| acquisition-tactics | research-worker | founder-input; competitors-analysis; channel menu | `${CLAUDE_PLUGIN_ROOT}/skills/enrichment-acquisition-tactics/SKILL.md` | acquisition-tactics |

Skills: `diffmode-growth-tactics:enrichment-<dim>`. Outputs in `OUT = WS/02-enrichment/`:
`competitors-analysis.md`, `audience-jtbd.md`, `acquisition-tactics.md`. Each runs the full
per-stage routine (reviewer-gated). **Wave 1 is a blocking gate** — if `competitors` FAILS,
abort (the rest of enrichment, Stage 1.5 mining, the think-tanks, and all synthesis depend on
`competitors-analysis.md`). (`acquisition-tactics` is a leaf within enrichment, but its output
feeds the think-tanks, so let it complete.)

> **Kick off Stage 1.5 the moment `competitors` is APPROVED** — see the next section. The
> mining branch runs concurrently with Wave 2 and Stage 2; do not wait for the rest of
> enrichment before starting it.

## Stage 1.5 — Start growth-factors mining (overlaps enrichment + Stage 2)

The slowest single stage (~40 min) is `growth-factors-mining`. Its enrichment inputs are
**optional search seeds** — per its own skill it strictly needs only `founder-input.md` — so
hoist it out of the Stage-2 fan-out and **start it the moment Wave-1 `competitors` is
APPROVED**, then let it run concurrently through Wave 2, Stage 2, and the think-tank reviewer
loops. It is **structural-check-only** (no reviewer gate), so it does not block anything until
the Stage-3 boundary, where it is collected and validated.

**Dispatch** (a single Agent call, fired right after the competitors gate; do NOT await it
before moving on to Wave 2 / Stage 2):

| Stage | Worker | Skill | Inputs | Output |
|-------|--------|-------|--------|--------|
| growth-factors | **research-worker** | `:growth-factors-mining` | founder-input (required); competitors-analysis (seed, ready after Wave 1); acquisition-tactics (optional seed — pass it if Wave 2 has produced it, otherwise omit) | `WS/03-think-tanks/demand-generation/growth-factors.json` |

- Pass `--remine` into the brief if present. Otherwise the skill's **cache rule is unchanged**:
  if `growth-factors.json` already exists and `--remine` is absent, the worker reuses it.
- Record the long-running branch in the run-ledger as `growth-factors` (one row when dispatched,
  one when it resolves, with `started_at`/`duration_s`).
- The `acquisition-tactics.md` seed is "optional but recommended" — if mining is dispatched
  before Wave 2 finishes it simply won't have that seed yet, which the skill explicitly allows.

**Collection happens at the Stage-3 boundary** (see Stage 3) — the orchestrator runs the
growth-factors structural + clean-room check there, NOT here. This stage just launches the
branch and keeps a handle on it.

## Stage 2 — Think-tank research (parallel)

After enrichment outputs exist, **dispatch all three think-tanks in a single message** (three
Agent calls) so they run concurrently (alongside the still-running Stage-1.5 mining branch):

| Stage | Worker | Skill | Inputs | Output |
|-------|--------|-------|--------|--------|
| competitor-gaps | analysis-worker | `:competitor-gaps` | founder-input; competitors-analysis; audience-jtbd; acquisition-tactics; channel menu | `…/competitor-gaps.md` |
| cross-industry | analysis-worker | `:cross-industry` | founder-input; competitors-analysis; audience-jtbd; acquisition-tactics | `…/cross-industry.md` |
| platform-arbitrage | **research-worker** | `:platform-arbitrage` | founder-input; competitors-analysis; acquisition-tactics; channel menu | `…/platform-arbitrage.md` |

(`…` = `WS/03-think-tanks/demand-generation/`.)

**Gating:** the **3 think-tanks** are reviewer-gated (rubric dims `competitor-gaps`,
`cross-industry`, `platform-arbitrage`; spec_path = each stage skill's `SKILL.md`). Run their
reviewer loops (the three reviewer dispatches may be batched).

**Concurrent-partial-failure handling (the 3-way fan-out).** The three think-tanks are
dispatched in one message and return independently, so handle them as a batch: **after the
batch returns, classify each branch** and record each in the run-ledger —

- **`ok`** (think-tank APPROVED by its reviewer) → resolved.
- **`rejected`** (reviewer REJECTED, score < 7) → run that branch's reviewer-retry loop
  (fresh worker, blocking_issues injected, max 3) → resolves to ok or failed.
- **`died`** (dispatch failed / no JSON) → re-spawn a FRESH worker up to 2× per the worker
  lifecycle rule → resolves to ok or `worker-dispatch-failed`.
- **`failed`** (still rejected at iter 3, or still dead after 2 respawns) → record FAILED.

**Gate Stage 3 on all three think-tanks RESOLVED + `ok`**: a failed think-tank **blocks
synthesis** (pass1/step1/pass2 read all three think-tank reports). If any think-tank ends
`failed`, stop before Stage 3, surface its `blocking_issues`, and print the resume command
(`--from think-tanks` or `--only <branch>`). The Stage-1.5 `growth-factors` branch is gated
separately, at the Stage-3 boundary below.

## Stage 3 — Lite constraints

**Stage-3 boundary precondition — collect + validate the Stage-1.5 mining branch (BLOCKING).**
Before dispatching `lite-constraints`, the `growth-factors` branch launched in Stage 1.5 must
have RESOLVED and passed its check. Classify it like any concurrent branch (record in the
run-ledger): `ok` if it passes the check below; `died` → re-spawn a FRESH worker up to 2×;
`failed` → still bad after 2 respawns. A failed `growth-factors.json` **blocks everything**
(synthesis needs the LIGHT DB → the constraints), so on `failed`, stop here, surface
`blocking_issues`, and print the resume command (`--only growth-factors` or `--remine`).

**growth-factors.json check** (no rubric → **structural + clean-room check only**): it parses
as JSON; `metadata.total_vectors` matches `vectors.length` and is **15-40**; `category_counts`
sums to total and no prefix > ~60%; every vector has `vector_id` (matching `{prefix}-NNN-slug`),
`category`, `mechanism`, `transferability`, `saturation_risk`, `examples`, and a real
`source_url`. **Clean-room spot-check:** confirm the worker did not read `tactics_DB/` (its
summary should say so; the schema requires real source URLs). If the check fails and the
worker returned ok, re-dispatch once with the specific gap; max 2 attempts.

**Then dispatch lite-constraints.** Worker **`synthesis-worker`** with a **per-dispatch model
override** (see Stage 4's *Model tiering* note):

| Step | Worker | Model | Skill | Inputs | Output |
|------|--------|-------|-------|--------|--------|
| lite-constraints | synthesis-worker | **sonnet** | `:lite-constraints` | growth-factors.json; founder-input.md | `WS/03-think-tanks/demand-generation/synthesis-constraints.json` |

`lite-constraints` is a deterministic JSON build from the LIGHT DB, so dispatch it with
`model: sonnet` (the Agent/Task tool's `model` param overrides the worker's `opus` default).

**Structural check only** (no rubric): parses as JSON; has `diverse_white_space` (≥5 pairs),
`mandatory_combinations` (pools A/B/C present), `prohibited_combinations` (the 5 generic
conventional patterns), `anti_patterns`, and `category_diversity_requirements`
(`max_single_category_pct: 60`). **Every vector ID referenced must exist in
`growth-factors.json`** (cheap cross-check of a sample of ids). Re-dispatch once on failure.

## Stage 4 — Synthesis chain (step1 → step2 → pass1 → pass2)

**ID-consistency precheck (BLOCKING — run BEFORE step1).** `synthesis-constraints.json` is
built against a specific `growth-factors.json`. If the LIGHT DB was re-mined (`--remine`)
without rebuilding constraints — e.g. `--remine` then `--from synthesis`, which skips Stage 3
— the on-disk constraints reference vector IDs that no longer exist, and synthesis would
emit broken traceability silently. So before dispatching step1: collect every vector ID
referenced anywhere in `synthesis-constraints.json` (`diverse_white_space`,
`mandatory_combinations`, `prohibited_combinations.vectors_if_present`,
`unconventional_anchors`) and confirm **each one exists in the CURRENT `growth-factors.json`**.
On ANY mismatch, **ABORT** with code **`constraints-stale`** and the hint: *"`synthesis-constraints.json`
references vector IDs absent from the current `growth-factors.json` — re-run
`--from lite-constraints` to rebuild constraints against the current LIGHT DB."* Do not
proceed to step1 with stale constraints.

All four on **`synthesis-worker`** (no MCP, clean-room), sequentially — but **model-tiered**
(see the *Model tiering* note below the table):

| Step | Model | Skill | Inputs | Output | Gate |
|------|-------|-------|--------|--------|------|
| step1 | **sonnet** | `:synthesis-step1-combinations` | founder-input; growth-factors.json; synthesis-constraints.json; audience-jtbd; the 3 think-tank reports | `…/synthesis-step1-combinations.md` | structural |
| step2 | **sonnet** | `:synthesis-step2-mechanisms` | step1 output; growth-factors.json; founder-input | `…/synthesis-step2-mechanisms.md` | structural |
| pass1 | **opus** | `:synthesis-pass1-whitespace` | synthesis-constraints.json; step2 output; growth-factors.json; founder-input; the 3 think-tank reports; channel menu | `…/synthesis-pass1.md` | structural |
| pass2 | **opus** | `:synthesis-pass2-founder` | synthesis-pass1.md; synthesis-constraints.json; growth-factors.json; founder-input; audience-jtbd; competitors-analysis; competitor-gaps; cross-industry; platform-arbitrage; channel menu | `…/synthesis.md` | **reviewer-gated** |

> **Model tiering (cost/latency tuning, no quality change expected).** The mechanical steps —
> `lite-constraints` (Stage 3), `step1` (blind vector combinations + strip test), and `step2`
> (3-step mechanism prototypes + conventional-detection gate) — run on **sonnet**; the
> creative/novelty engine (`pass1` white-space) and the final reviewer-gated deliverable
> (`pass2`) stay on **opus**. Pass the tier with a **per-dispatch `model` override** on the
> Agent/Task call (e.g. `model: sonnet` for step1/step2) — that param takes precedence over
> `synthesis-worker`'s `opus` frontmatter default, so no extra worker file is needed.
> **`step2` is the riskier downgrade** (mechanism novelty): if a run's strip-test pass-rate or
> unconventional ratio visibly drops, revert just `step2` to `opus` (one-line change).
> *(Fallback if a runtime ever ignores the per-dispatch override: add a 5th worker
> `agents/synthesis-fast-worker.md` — `model: sonnet`, same tools + clean-room rule — and route
> lite-constraints/step1/step2 to it instead.)*

**Structural checks** for step1/step2/pass1: file exists, non-empty, has the skill's required
sections (step1 → `## Vector Combinations` + `## Stripped Core Action Test`; step2 →
`## Validated Mechanisms` + the dedup result; pass1 → `## Generated Tactics`), and — quick
novelty smell-test — that referenced vector IDs exist in `growth-factors.json` and no tactic
names leak into step1/step2. If a step's own validation marks it INVALID (e.g. step2 verb
groups < 7), spawn a fresh worker once with the gap.

**`must_include` enforcement gate — Bug-C fix (hardened).** Skill self-checks alone were
shown to be skippable, so the orchestrator enforces this deterministically. Parse
`synthesis-constraints.json` for the `must_include` pairs (`mandatory_combinations` pools
A + B). A raw whole-file grep only proves *line-presence*, which is too weak — the two IDs
could appear in unrelated combinations. So enforce **block-level co-occurrence**:

- **After step1 writes its output:** split the file into `### Combination #N` blocks (parse
  per-block, not whole-file). For EACH `must_include` pair, a pair is **validly used** only
  if **both** of its vector IDs appear **within a single `### Combination #N` block**. A pair
  is **validly substituted** only if there is an explicit substitution note that (i) names
  that pair AND (ii) **names a replacement vector that EXISTS in `growth-factors.json`**
  (validity, not mere presence of the word "substituted"). If any pair is neither validly
  used nor validly substituted, spawn a fresh step1 worker **ONCE** with the specific pairs
  in `blocking_issues` (e.g. "Pool-B pair `lever-NNN`+`struct-NNN` is not co-located in any
  one combination and has no valid substitution — co-locate both IDs in one combination, or
  substitute with a replacement vector that exists in growth-factors.json").
- **After pass2 writes the final `synthesis.md` (closing check WITH remediation):** apply the
  same block-level test per *tactic* — for each Pool-B `must_include` pair, both IDs must
  appear within a single tactic's `**Source:** … Vectors` line/block, OR a valid substitution
  note (naming an existing replacement vector) must be present. If any Pool-B pair is neither
  validly used nor validly substituted, **re-dispatch pass2 ONCE** with `blocking_issues`
  listing exactly the missing pairs (this is a real remediation, not just a re-grep). If a
  pair is still uncovered after that single pass2 retry, record it as a known gap in the
  run-ledger and the final report — do not silently pass.

**pass2 reviewer gate:** dispatch `diffmode-growth-tactics:reviewer` with
`{dimension: "demand-gen-synthesis", spec_path:
"${CLAUDE_PLUGIN_ROOT}/skills/synthesis-pass2-founder/SKILL.md", output_path: "…/synthesis.md",
context_paths: [growth-factors.json, synthesis-constraints.json, founder-input.md,
audience-jtbd.md, competitors-analysis.md, competitor-gaps.md, cross-industry.md,
platform-arbitrage.md]}`.
Score ≥7 / max 3 retries, blocking_issues injected verbatim on re-dispatch. The reviewer
applies the demand-gen-synthesis rubric WITH the clean-room adjustments noted in the
growth-reviewer skill (score against the per-run LIGHT DB; do not require Week-1 depth;
synthesis is the final stage).

## Output / report — and STOP

When the run finishes, report a compact summary (do not paste file contents). Include a
**timing column** (`duration_s` per stage, read from the run-ledger rows) so the run prints
exactly where the wall-clock went — the `growth-factors` row shows its concurrent duration,
which should overlap (not add to) enrichment + the think-tanks:

```
Growth Tactics — <slug>                                                          duration
  diagnostics          OK                                  …/founder-input.md           42s
  enrichment           3/3 APPROVED                        WS/02-enrichment/*.md       18m
  growth-factors       OK  (31 vectors, 6 categories)      …/growth-factors.json  [‖ 38m, clean-room]
  think-tanks          3/3 APPROVED                        …/{competitor-gaps,cross-industry,platform-arbitrage}.md  22m
  lite-constraints     OK                                  …/synthesis-constraints.json  3m
  synthesis            APPROVED (score 8, 1 pass)          …/synthesis.md  (8 tactics, 5 unconv.)  19m
  ── total wall-clock ──────────────────────────────────────────────────────────  ~1h52m
```

(Durations are illustrative; print the real `duration_s` from `WS/.run-state.json`. Mark the
`growth-factors` row `‖` to signal it ran concurrently with enrichment + Stage 2, so its time
is hidden under the critical path rather than added to it.)

Then tell the founder explicitly:

> This is where the **free** pipeline stops — you have 7-9 novel demand-gen tactic IDEAS,
> generated by combining mechanisms from a per-run LIGHT growth database. The **paid**
> Diffmode adds prioritization, full week-by-week implementation guides, and the
> proprietary 576-vector database + intelligence layer (deeper, more durable tactics).

For any FAILED stage, list its final `blocking_issues`.

## Failure modes

| Code | Where | Meaning | Recovery |
|------|-------|---------|----------|
| `missing-channel-menu` | pre-flight | bundled channel menu absent from `${CLAUDE_PLUGIN_ROOT}/reference/` | reinstall the plugin |
| `plugin-not-enabled` | any dispatch | a `diffmode-growth-tactics:…` id doesn't resolve | enable the plugin |
| `worker-dispatch-failed` | any stage | worker died mid-run (API/socket error, no JSON) after 2 fresh re-spawns | stage FAILED; resume with the printed `--from <stage>`/`--only <stage>` — no main-thread fallback |
| `intake-incomplete` | Stage 0 | founder-input has unresolved must-ask gaps | ask the founder the Confirmation Gaps |
| `competitors-gate-failed` | Wave 1 | competitors REJECTED ×3 | inspect blocking_issues; downstream can't run |
| `dimension-failed` | enrichment | a dim REJECTED ×3 | list blocking_issues; dependents skipped |
| `growth-factors-invalid` | Stage 1.5 / Stage-3 boundary | JSON/schema/clean-room check failed ×2 | inspect; synthesis can't run without the LIGHT DB |
| `constraints-invalid` | Stage 3 | synthesis-constraints schema/id check failed | re-dispatch lite-constraints |
| `constraints-stale` | Stage 4 precheck | `synthesis-constraints.json` references vector IDs absent from the CURRENT `growth-factors.json` (e.g. `--remine` then `--from synthesis`) | re-run `--from lite-constraints` to rebuild constraints against the current LIGHT DB |
| `synthesis-failed` | Stage 4 | pass2 REJECTED ×3 | list blocking_issues |
| `clean-room-violation` | Stage 1.5/3/4 | a worker read `tactics_DB/` | re-dispatch; the LIGHT-DB stages must never touch the proprietary DB |

## Idempotency

Overwrite-on-rerun for stage outputs, EXCEPT `growth-factors.json`, which is **cached and
reused** unless `--remine` (the deliberate cost mitigation for per-run mining — it is the
slowest/priciest stage). `--scratch` writes to `*-scratch/` dirs and preserves originals.

**`--remine` invalidates `synthesis-constraints.json`.** The constraints file is derived from
a specific LIGHT DB, so re-mining makes the cached constraints stale (its vector IDs may no
longer exist). Whenever `--remine` runs, the orchestrator **must also force `lite-constraints`
to re-run** (rebuild `synthesis-constraints.json` against the fresh `growth-factors.json`)
before any synthesis step. The Stage-4 `constraints-stale` precheck is the backstop that
catches a resume which skipped this (e.g. `--remine` then `--from synthesis`).

**Run-ledger.** The orchestrator maintains a workspace-local `WS/.run-state.json` (see
*Run-ledger* below) recording each stage attempt's verdict. On a `--from` / `--only` resume,
read it first to know which stages are done / failed / mid-retry. It is per-run workspace
state (git-ignored), and is **best-effort** recovery aid, not a hard guarantee.

## Run-ledger (durability across a multi-hour run)

A full run can take ~2.5h and span context compaction. To survive that and make
`--from`/`--only` resumes reliable, maintain a small, human-readable, **workspace-local**
ledger at `WS/.run-state.json` and **append to it after every stage attempt**:

```json
{ "stage": "enrichment:competitors", "attempt": 1, "verdict": "APPROVED", "score": 8, "started_at": 1717200000, "duration_s": 1080, "output": "WS/02-enrichment/competitors-analysis.md" }
{ "stage": "growth-factors", "attempt": 1, "verdict": "OK", "started_at": 1717200200, "duration_s": 2280, "output": "WS/03-think-tanks/demand-generation/growth-factors.json" }
{ "stage": "synthesis:pass2", "attempt": 2, "verdict": "REJECTED", "score": 6, "started_at": 1717206000, "duration_s": 900, "blocking": ["…"] }
```

(JSON-lines, or an equivalent `WS/RUN-LOG.md` table — append-only, one row per attempt.)

- **Write a row after EVERY attempt** of every gated/structural stage: the verdict
  (`APPROVED` / `REJECTED` / `OK` / `FAILED` / `died→respawn`), the score where there is one,
  the **`started_at`** (epoch seconds from `date +%s` before dispatch) and **`duration_s`**
  (epoch seconds after the attempt resolves, minus `started_at`), and the output path. The
  per-stage `duration_s` is what the final report's timing column and the *Output/report*
  total wall-clock are read from — the first instrumented run replaces the rough minute
  estimates in this file with real numbers. (The `growth-factors` branch runs concurrently, so
  its `duration_s` overlaps enrichment + Stage 2 rather than adding to the critical path.)
- **On resume** (`--from` / `--only`), read the ledger FIRST to learn which stages are done,
  which failed, and which were mid-retry — then resume from the right point instead of
  re-deriving state from scratch.
- This is **best-effort durability.** The orchestrator is an LLM following prose, so the
  ledger is a recovery *aid*, not a transactional guarantee — if it and the filesystem
  disagree, trust the on-disk stage outputs (the contract between stages) and reconcile.
- The ledger is **per-run workspace state** — it is git-ignored (see repo `.gitignore`).

## Acceptance check (user runs after the orchestrator finishes)

1. `synthesis.md` exists with **7-9 tactics**, ≥50% unconventional, every tactic traceable
   to a vector combination from `growth-factors.json`.
2. `growth-factors.json` is a clean-room LIGHT DB (20-40 vectors, correct schema, real
   source URLs, nothing traceable to `tactics_DB/`).
3. Spot-check that tactics are **non-generic** (the novelty test the whole pipeline exists
   for) — strip the tactic name + adjectives; a traditional marketer should NOT say "obviously
   do that" for the majority.
4. Enrichment (3 dims) + think-tank outputs reached APPROVED (score ≥7); note any that needed
   2-3 passes.
5. `WS/.run-state.json` carries a `duration_s` for every stage attempt, and the run report
   printed the per-stage timing column — confirm `growth-factors` overlapped enrichment +
   Stage 2 (its row started right after the competitors gate) rather than serializing after them.
6. (Optional moat check) Compare a light-DB synthesis run against a proprietary-DB run for
   the same workspace — the free output should be **useful but visibly weaker**.
