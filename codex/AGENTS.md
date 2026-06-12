# AGENTS.md — Diffmode Growth Tactics (Codex runtime)

Durable instructions for running the **Diffmode free growth-ideation pipeline** under OpenAI
Codex. Codex merges `AGENTS.md` files walking the tree (nearest wins), so keep this scoped to
the pipeline.

> **STATUS: built + A/B-validated (2026-06-04).** The skill bodies (`.agents/skills/`) are the
> real IP and are runtime-neutral — Codex consumes them unchanged. The *orchestration* below is
> re-expressed from the proven Claude orchestrator (`../plugin/commands/start.md`)
> and now runs end-to-end as a deterministic Python driver, **`codex/orchestrate.py`** — the full
> DAG from Stage 0 URL intake through synthesis, dispatching each stage as a `codex exec` worker
> and gating it with the structural checks in `codex/checks.py`. It passed a full A/B quality test
> on theona.ai (2026-06-04, gpt-5.5, Perplexity OFF) on par with the Claude baseline. The `.toml`
> field names + `codex exec` dispatch flags reflect **codex-cli 0.136** — re-confirm against your
> installed Codex if it has drifted. See `CODEX.md` for setup + the run command.

## What this produces — and where it stops

From a fast founder intake to a final `synthesis.md` of **7-9 novel demand-gen tactic IDEAS**,
then it **STOPS**. Prioritization, implementation guides, and the proprietary 576-vector
database are the paid product — never attempt them here.

## Workspace convention

All run state lives on the filesystem (the contract between stages). Resolve `WS = ./<slug>`
under the **current working directory** (slug from the product name, else the URL host, e.g.
`theona.ai`). Create `WS/01-diagnostics`, `WS/02-enrichment`,
`WS/03-think-tanks/demand-generation`. No host repo is required.

The bundled **channel menu** is at `../plugin/reference/Marketing-Channel-Menu-2026.md`
relative to this directory (i.e. `plugin/reference/…` from the repo root). The skill bodies
refer to it as `${CLAUDE_PLUGIN_ROOT}/reference/…` — that is a Claude-runtime token; under
Codex the orchestrator simply passes the checkout-relative path as an input. Skills treat the
channel menu as **invoker-supplied**, so no skill edit is needed.

## Skills (single source of truth)

The 13 skills are symlinked into `.agents/skills/` from `../plugin/skills/` (the
`founder-report` packaging skill is symlinked too, but the Codex driver does not dispatch
it — the report renderer falls back to `synthesis.md` for Codex runs). Load a skill by
reading `.agents/skills/<skill>/SKILL.md` and following it step-by-step — the skill is the
authority on scope, frameworks, output template, and validation. Reviewer rubrics live at
`.agents/skills/growth-reviewer/references/<dimension>.md`.

## Orchestration model

1. **One level of agents.** The orchestrator (the `codex/orchestrate.py` driver) runs at the
   top and dispatches worker agents (`codex/agents/*.toml`). Workers do NOT spawn workers.
   Each worker is its own `codex exec` batch call — requested per stage by the driver, never
   self-spawned. **Each dispatch is a separate `codex exec` call that scopes its own web access:**
   the `research-worker` dispatch adds `-c web_search="live"` (and attaches Perplexity if
   registered) plus `-c sandbox_workspace_write.network_access=true` so its citation-integrity
   re-fetch can `curl` full URLs; every other dispatch adds nothing and inherits the
   `web_search = "disabled"` baseline (CODEX.md §4). There is no `codex exec --agent` flag — agents are delegated in-prompt,
   one `codex exec` per worker.
2. **Workers are stateless and single-shot.** A worker loads one skill, reads inputs, writes
   one output, returns a small JSON summary `{status, outputPath, summary}`. It is not
   addressable after it returns. Every retry is a FRESH worker with the same brief plus any
   injected `blocking_issues`.
3. **State passes through the filesystem.** Workers return only the JSON summary + output path
   — keep orchestrator context lean.
4. **The orchestrator is the only thing that talks to the human** (for intake).

### Workers

| Worker (`codex/agents/*.toml`) | Web access | Used for |
|--------------------------------|-----------|----------|
| `research-worker` | native `web_search` (built-in) + Perplexity MCP (optional) | diagnostics-intake (URL), enrichment research dims, platform-arbitrage, growth-factors-mining |
| `analysis-worker` | **none (enforced)** | enrichment-audience, competitor-gaps, cross-industry (analysis mode) |
| `synthesis-worker` | **none (enforced)** | lite-constraints, synthesis explore → build |
| `reviewer-worker`  | none | every reviewer-gated stage |

The no-web workers deliberately have **no `mcp_servers`** **and are dispatched with
`web_search = "disabled"`** — both halves are required on Codex (the native `web_search` tool
defaults to `cached`, i.e. web-cache, so "no `mcp_servers`" alone would still leave a web path
open). `research-worker` declares **no** `mcp_servers` array — on Codex that field is a *map* keyed
by server name (a bare list silently voids the whole agent file); instead it **inherits a
globally-registered Perplexity MCP** (`codex mcp add perplexity`) when present, and is the only
worker dispatched with web enabled (`-c web_search="live"`). Absent Perplexity it falls back to the
native `web_search` tool — Perplexity-optional on Codex, mirroring the Claude plugin (v2.4.0).

## The DAG

```
Stage 0    diagnostics-intake        → WS/01-diagnostics/founder-input.md
Stage 1    enrichment (2 waves):
             Wave 1 (reviewer gate):            competitors
             Wave 2 (‖, structural check only): audience ‖ acquisition-tactics    (depend on competitors)
Stage 1.5  growth-factors mining     → …/growth-factors.json (LIGHT DB)
             starts right after Wave-1 competitors is APPROVED; runs concurrently through
             the rest of enrichment + Stage 2; structural-check-only; collected at the Stage-3 boundary
Stage 2    think-tank ×3             (parallel, after enrichment; structural check only)
             platform-arbitrage (research) · competitor-gaps · cross-industry
Stage 3    lite-constraints          → WS/03-think-tanks/demand-generation/synthesis-constraints.json
             precondition: growth-factors.json present + valid
Stage 4    synthesis  explore → build   → synthesis.md   (STOP)
```

## The quality gate (reviewer → retry loop)

For each **reviewer-gated** stage (in v2.3.0: enrichment `competitors` and the final synthesis
`build`): after the worker writes its output, dispatch `reviewer-worker` with
`{dimension, spec_path, output_path, context_paths}`. Read the JSON verdict.

- **APPROVED** (score ≥ 7, format PASS) → done.
- **REJECTED** and iterations < 3 → spawn a FRESH worker with the same brief plus the reviewer's
  `blocking_issues` injected verbatim; re-check; increment.
- **REJECTED** at iteration 3 → mark the stage FAILED, record blocking_issues, stop dependents.

The non-gated stages (growth-factors-mining, lite-constraints, synthesis `explore`, enrichment
`audience` + `acquisition-tactics`, and the 3 think-tanks) get a **structural check only** (file
exists, non-empty, required sections present, JSON parses with expected keys/counts, referenced
vector IDs exist in `growth-factors.json`). Re-dispatch once on a structural failure.

## Clean-room rule (moat-critical)

`growth-factors-mining` and the whole synthesis chain MUST NOT read any proprietary growth
database (`tactics_DB/` and the like). `growth-factors-mining` builds a per-run LIGHT vector DB
**only from freshly researched public case studies**; synthesis reasons over that LIGHT DB and
the lite constraints. If any brief points a worker at a proprietary DB, it refuses and notes it.
The moat is the proprietary DB's breadth + the paid downstream stages — not the method, which
this repo ships.

## Acceptance check

`synthesis.md` has 7-9 tactics, ≥50% unconventional, each traceable to a vector combination from
`growth-factors.json`; the LIGHT DB is clean-room (20-40 vectors, **real, resolvable source URLs**
— Perplexity- or native-`web_search`-sourced, 0 NXDOMAIN/404 — nothing traceable to a proprietary
DB); enrichment + think-tank outputs reached APPROVED (≥7).
