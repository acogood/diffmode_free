---
description: (advanced — pipeline testing) Run the Diffmode enrichment stage only — competitors → audience ‖ acquisition-tactics, reviewer-gated, into a ./<slug>/ workspace in your cwd.
---

# Run Enrichment

Main-thread orchestrator for the **enrichment** stage, run as skills + worker
sub-agents. Owns the DAG, the parallel fan-out, the reviewer-retry quality gate, and the
stage-boundary existence checks, following the same single-shot worker / main-thread
orchestration pattern as the full pipeline (`start.md`).

> **This command runs in the main thread.** It dispatches worker sub-agents via the
> Agent/Task tool. It must NOT itself be run as a sub-agent — sub-agents are one level
> deep and could not then spawn the workers. (See the repo's `docs/architecture.md`.)

Design refs (internal, not shipped in the plugin):
`docs/enrichment-pilot.md` (corrected DAG, inputs, bug fixes),
`docs/architecture.md` (roles, state contract).

> **Naming under the plugin.** This command ships in the `diffmode-growth-tactics` plugin and
> is invoked as `/diffmode-growth-tactics:run-enrichment`. Its skills and worker agents are
> plugin-namespaced — use these exact ids in Agent-tool dispatches:
> skills `diffmode-growth-tactics:enrichment-<dimension>`; workers
> `diffmode-growth-tactics:research-worker`,
> `diffmode-growth-tactics:analysis-worker`, `diffmode-growth-tactics:reviewer`.
> The plugin is **self-contained**: it reads its bundled channel menu from
> `${CLAUDE_PLUGIN_ROOT}/reference/` and writes outputs to a `./<slug>/` workspace in the
> user's current directory. No host repo is required.

## Welcome (print BEFORE any tool call)

Print this first, verbatim — markdown only, no ASCII art / ANSI:

> # Diffmode — researching your market
>
> This is the research-only run (~30–40 minutes, hands-off): it studies your
> **competitors**, maps your **buyers**, and audits **what's already working** in your
> market. You get 3 reusable research briefs at the end — they open in your browser.

During the run, follow the full pipeline's **User-facing voice** rules
(`start.md`): one plain start line with an ETA and one done line per
dimension; no reviewer mechanics, check internals, or ledger JSON in the narration.

## Arguments

`$ARGUMENTS`:

- `--product <slug>` (required) — names the workspace at `./<slug>/` in the current directory.
  Example: `/run-enrichment --product theona.ai`.
- `--only <dimension[,dimension…]>` (optional) — run a subset (e.g. `--only competitors`).
  Dependencies must already exist on disk for any dimension not in the subset.
- `--scratch` (optional) — write outputs to `02-enrichment-scratch/` instead of
  `02-enrichment/`, preserving any existing originals (use for dry-runs / parity checks,
  honoring the "never edit originals" rule for known-good outputs).

The three dimensions: `competitors`, `audience`, `acquisition-tactics`.

## Pre-flight

1. **Resolve the workspace** — `WS = ./<slug>` under the user's **current working directory**.
   Confirm `WS/01-diagnostics/founder-input.md` exists and is non-empty. If missing, abort with
   `missing-founder-input` (diagnostics must run first). **No host repo is required** — the
   plugin is self-contained.
2. **Confirm the channel menu** — `${CLAUDE_PLUGIN_ROOT}/reference/Marketing-Channel-Menu-2026.md`
   exists (bundled in the plugin; required by competitors, acquisition-tactics, audience).
   `${CLAUDE_PLUGIN_ROOT}` expands to the plugin's install directory at runtime.
3. **Resolve the output dir** — `OUT = WS/02-enrichment` (or `WS/02-enrichment-scratch`
   under `--scratch`). Create it if missing.
4. **Confirm the plugin is active** — the `diffmode-growth-tactics` plugin's skills
   (`diffmode-growth-tactics:enrichment-*`) and worker agents are present whenever the plugin
   is enabled, so no install step is needed here. If a worker dispatch later reports an
   unknown agent, the plugin is not enabled — run `/plugin` and enable `diffmode-growth-tactics`
   (or `claude plugin install diffmode-growth-tactics@diffmode-free`).
5. **Detect the research backend (capability note — no hard gate).** Check whether a
   Perplexity MCP server is available (the `mcp__perplexity__*` tools resolve). The research
   dims (`competitors`, `acquisition-tactics`) use it when present. **If no Perplexity MCP is
   detected, print one line —** *"WebSearch fallback mode — no Perplexity MCP detected;
   research quality slightly lower, citations auto-verified."* **— and proceed.** The
   `research-worker` falls back to the built-in `WebSearch` (see its Step 3 + Step-6
   citation-integrity check); there is no hard gate. `audience` runs on `analysis-worker`
   (no MCP) regardless.
6. **Confirm the reviewer threshold** — score **≥ 7**, **max 3** iterations, applied to
   **`competitors` only** (the Wave-1 blocker). `audience` + `acquisition-tactics` get a
   **structural completeness check only**, no reviewer (v2.3.0 reviewer cut — they proved
   reliable enough in the field that gating them added latency + retry risk without changing
   the result).

## The DAG (waves)

```
Wave 1 (blocking reviewer gate):           competitors
Wave 2 (parallel, structural check only):  audience          ‖ acquisition-tactics   (both depend_on competitors)
```

`acquisition-tactics` is a leaf (nothing downstream in enrichment consumes it). Wave 2 is the
last enrichment wave — there is no Wave 3. (Enrichment is intentionally lean: dimensions whose
output no downstream stage reads are not run. See the repo's `docs/enrichment-pilot.md` for the
removal history.)

### Per-dimension input wiring (the worker's `inputs`)

| Dimension | Worker (plugin-namespaced) | Inputs | Gate |
|-----------|--------|--------|------|
| competitors | `diffmode-growth-tactics:research-worker` | `WS/01-diagnostics/founder-input.md`; `${CLAUDE_PLUGIN_ROOT}/reference/Marketing-Channel-Menu-2026.md` | **reviewer-gated** — spec `${CLAUDE_PLUGIN_ROOT}/skills/enrichment-competitors/SKILL.md` |
| audience | **`diffmode-growth-tactics:analysis-worker`** (no MCP) | `WS/01-diagnostics/founder-input.md`; `OUT/competitors-analysis.md`; `${CLAUDE_PLUGIN_ROOT}/reference/Marketing-Channel-Menu-2026.md` | structural check only (no reviewer) |
| acquisition-tactics | `diffmode-growth-tactics:research-worker` | `WS/01-diagnostics/founder-input.md`; `OUT/competitors-analysis.md`; `${CLAUDE_PLUGIN_ROOT}/reference/Marketing-Channel-Menu-2026.md` | structural check only (no reviewer) |

Output filenames in `OUT/`: `competitors-analysis.md`, `audience-jtbd.md`,
`acquisition-tactics.md`.

> **Channel-menu fix:** the audience worker DOES receive the channel menu, unlike the
> legacy Python config — a deliberate correction (`enrichment-pilot.md` bug fix #1).
> **Audience no-search:** audience uses `analysis-worker`, which has no
> research MCP, so ENR-001's no-new-web-search rule is structurally enforced.

## The per-dimension routine (generate → existence-check → reviewer loop)

For each dimension `D` with worker `W`, output `O = OUT/<file>.md`, rubric spec `S`:

### 1. Dispatch the worker

Call the Agent tool with `subagent_type = W` (the plugin-namespaced worker id from the
table, e.g. `diffmode-growth-tactics:research-worker`) and a self-contained brief:

```
skill:   diffmode-growth-tactics:enrichment-<D>
inputs:  [ …the paths from the table above… ]
output:  <O>          (absolute or repo-relative)
blocking_issues: <none on the first pass>
```

The worker loads the skill, reads inputs, (researches), writes `O`, and returns
`{status, outputPath, summary}`.

### 2. Stage-boundary existence check (replaces Python `verify_outputs`)

After the worker returns, confirm deterministically:

- `O` exists and is **non-empty** (`test -s <O>`).
- `O` contains the dimension's required top-level sections (a cheap grep, e.g.
  competitors → `## Competitor Overview` and `## Competitive Channel Matrix`; audience →
  `## Customer Segments` and `## Segment Evaluation Summary`; acquisition-tactics →
  `## Tactics Summary Dashboard`).

If the file is missing/empty/structurally incomplete and the worker returned `ok`,
treat as a failed attempt and re-dispatch once with the specific gap noted; if the
worker returned `error`, surface its `reason` and stop this dimension's branch.

### 3. Reviewer loop — `competitors` only (score ≥ 7, max 3 iterations)

**Run this loop ONLY for `competitors`** (the Wave-1 blocker). `audience` +
`acquisition-tactics` skip the reviewer entirely — their step-2 structural existence check IS
their gate (re-dispatch once on a structural gap, then accept). For `competitors`:

```
iter = 1
loop:
  dispatch Agent(subagent_type = "diffmode-growth-tactics:reviewer", brief = {
      dimension: <D>, spec_path: <S>, output_path: <O>,
      context_paths: [ WS/01-diagnostics/founder-input.md, …upstream outputs… ] })
  read verdict JSON { score, verdict, format_compliance, blocking_issues[] }

  if verdict == APPROVED (score ≥ 7 and format PASS):
      mark D done; record score; break

  else:  # REJECTED
      if iter >= 3:
          mark D FAILED; append blocking_issues to the run summary; STOP D's branch
          (do not dispatch dimensions that depend on D)
      else:
          re-dispatch W with the SAME brief plus blocking_issues injected verbatim;
          re-run step 2 (existence check); iter += 1; continue
```

The reviewer's `blocking_issues` are passed unchanged into the worker's re-dispatch
brief — the worker's procedure addresses them first. This is the repo's threshold-7 /
max-3 norm.

## Execution order (the actual run)

1. **Wave 1 — competitors.** Run the per-dimension routine for `competitors`. **This is
   a blocking gate** — if it ends FAILED, abort the whole run (both other dimensions depend
   on `competitors-analysis.md`).

2. **Wave 2 — audience ‖ acquisition-tactics (parallel).** Dispatch BOTH workers in a
   **single message containing two Agent tool uses** so they run concurrently:
   - `diffmode-growth-tactics:analysis-worker` for `audience` (no MCP),
   - `diffmode-growth-tactics:research-worker` for `acquisition-tactics`.
   Then run each dimension's **existence-check only** — there is **no reviewer loop** for
   Wave-2 dims in v2.3.0 (structural check only); if a dim's structural check fails,
   re-dispatch it once with the gap noted, then accept. `acquisition-tactics` is a leaf;
   nothing in enrichment depends on it. Wave 2 is the last enrichment wave — there is no
   Wave 3.

## Output / report

When the run finishes:

1. **Render the HTML report (best-effort, never blocks):** find a Python ≥3.8 by probing
   `python3` / `python` / `py -3` with `-c "import sys; assert sys.version_info >= (3,8)"`,
   then run `"${CLAUDE_PLUGIN_ROOT}/scripts/render_html.py" "<WS>"`; with no Python, fall
   back to `bash "${CLAUDE_PLUGIN_ROOT}/scripts/render_html.sh" "<WS>"`. The renderer
   skips files that don't exist, so an enrichment-only workspace yields the 3 briefs (+
   the product brief) at `WS/report/index.html`.
2. **Lead with the deliverables** — one line per brief with its plain-English value and
   the HTML link (or the `.md` path if rendering was skipped): Competitor Research (who
   you're up against and how each rival gets users) · Audience Map (your buyer segments
   and what each hires you for) · Acquisition Audit (the plays already working in your
   market). Then offer to open `WS/report/index.html` in the browser (macOS `open`,
   Linux `xdg-open`, Windows/git-bash `explorer.exe "$(cygpath -w …)"`).
3. **Do not print scores/verdicts by default** — say each brief is done; keep the
   compact verdict summary for when the user asks or a dimension FAILED:

```
Enrichment — <slug>
  competitors          APPROVED  (score 8, 1 pass)        OUT/competitors-analysis.md
  audience             OK        (structural)             OUT/audience-jtbd.md
  acquisition-tactics  OK        (structural)             OUT/acquisition-tactics.md
```

For any FAILED dimension, list its final `blocking_issues`.

## Failure modes

| Code | Where | Meaning | Recovery |
|------|-------|---------|----------|
| `missing-founder-input` | pre-flight | `WS/01-diagnostics/founder-input.md` absent/empty | run diagnostics first |
| `missing-channel-menu` | pre-flight | bundled channel menu absent from `${CLAUDE_PLUGIN_ROOT}/reference/` | reinstall the plugin |
| `plugin-not-enabled` | any dispatch | a worker/skill id (`diffmode-growth-tactics:…`) doesn't resolve | enable the plugin: `/plugin` → `diffmode-growth-tactics`, or `claude plugin install diffmode-growth-tactics@diffmode-free` |
| `competitors-gate-failed` | Wave 1 | competitors REJECTED after 3 iterations | inspect blocking_issues; the 2 downstream dims cannot run |
| `worker-error` | any | a worker returned `{status:"error"}` | surface `reason`; fix the input it named |
| `output-missing` | existence check | worker returned ok but file missing/empty/incomplete | re-dispatched once; if still bad, stop that branch |
| `dimension-failed` | Wave-2 structural check | `audience`/`acquisition-tactics` still structurally incomplete after the single re-dispatch (no reviewer loop for Wave-2 dims in v2.3.0) | list the gap in the run summary |

## Idempotency

Overwrite-on-rerun for `OUT/*.md`, matching the current CLI. A re-run regenerates the
three files from scratch. Use `--scratch` to write into `02-enrichment-scratch/` and
preserve known-good originals (dry-runs / output-parity checks).

## Acceptance check (user runs after the orchestrator finishes)

1. All three `OUT/*.md` exist, non-empty, with the required sections.
2. `competitors` reached APPROVED (score ≥ 7); `audience` + `acquisition-tactics` passed
   their structural completeness check (required sections present). Note anything that needed
   a re-dispatch.
3. Spot-check `OUT/*.md` for completeness — every required section present, every
   required field populated, sources cited where the skill demands them.
4. Confirm the audience worker performed **no** web lookups (no research MCP available
   to it) and that a research worker actually cited real, retrieved URLs.
