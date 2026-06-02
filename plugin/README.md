# diffmode-growth-tactics (Claude Code plugin)

The **Diffmode free growth-ideation pipeline**, expressed as **agent skills + sub-agents**
that run inside a coding-agent runtime — portable, invokable, and composable. This directory
is the Claude Code plugin: a `/run-growth-tactics` orchestrator drives the full DAG, web
research routed through **Perplexity MCP** (model-agnostic by design), and every run writes
into a `./<slug>/` workspace **in the user's current directory** — no host repo required.

> This is the **shipped plugin**. `marketplace.json` at the repo root declares
> `source: ./plugin`, so Claude Code copies **only this directory** to its plugin cache. The
> bundled channel menu (`reference/`) and the 12 skills travel with it; the repo's `docs/`,
> `codex/`, and root README do **not** ship. Internal design notes live in the repo's
> `docs/` (architecture, eval methodology, build log) and are not part of the install.

## What it does — and where it stops

`/diffmode-growth-tactics:run-growth-tactics` takes a founder from a **2-minute intake** to a
final `synthesis.md` of **7-9 novel demand-gen tactic IDEAS**, then **STOPS at synthesis**.

```
diagnostics-intake            (URL research → prefill founder-input.md, else minimal Q&A)
        ↓
enrichment                    (2-wave DAG: competitors → audience ‖ acq-tactics)
        ↓                  ╲
        │                   ╲  growth-factors mining (‖, starts right after the competitors
        │                    ╲ gate and runs concurrently through enrichment + the think-tanks)
        │                     ╲  deep-research public case studies → distill ~20-40 atomic
        │                      ╲ vectors → growth-factors.json  (per-run LIGHT DB, clean-room)
think-tank research (×3, ‖)     │
  competitor-gaps               │
  cross-industry                │
  platform-arbitrage            │
        ↓                       ↓
        └────────────┬──────────  lite-constraints (skill, replaces the Python script)
                     ↓
        synthesis  explore → build  →  synthesis.md   (7-9 tactic ideas, STOP)
```

**The moat is DB breadth + paid downstream — not the method.** The synthesis *method* is
free; what's paid (and what defends the product) is the **proprietary 576-vector database**
(breadth) + intelligence layer + saturation/anti-vector tracking, **and** the downstream
**prioritization + week-by-week implementation** stages. This free plugin runs the same
method on a deliberately weaker **per-run LIGHT DB** mined fresh from public case studies and
**stops at synthesis** — full-depth *ideas*, but visibly lighter than the paid product.

**The novelty engine** is the synthesis chain — it cross-references the per-run LIGHT vector
DB against the founder's constraints and combines 2-3 vectors at a time into tactics that
didn't exist in any single playbook. Because a public plugin ships every file to the user's
disk, it **cannot** bundle the proprietary DB; instead, `growth-factors-mining` builds a
**clean-room, per-run substitute** (a deliberately weaker LIGHT DB) from freshly researched
public case studies, and `lite-constraints` replaces the Python constraints generator with
in-context reasoning. Nothing here reads the proprietary `tactics_DB/`.

## Design constraints (see the repo's `docs/architecture.md`)

1. The orchestrator runs in the **main thread**, never as a sub-agent (sub-agents are one
   level deep and could not then spawn workers). It is also the only place that talks to the
   human (AskUserQuestion, for intake).
2. **Skills are passive** instruction docs. Fan-out, waiting, and retry are the
   orchestrator's job, via Agent-tool calls.
3. **State passes through the filesystem** (`./<slug>/…` in the user's cwd). Workers return
   only a small JSON summary + output path, keeping orchestrator context lean.
4. The **reviewer→retry quality gate is a main-thread loop** (re-dispatch the worker with
   the reviewer's blocking issues injected), capped at 3 iterations — the threshold-7 /
   max-3 norm. In v2.3.0 only **enrichment `competitors`** and the **final synthesis
   (`build`)** are reviewer-gated; everything else (audience + acquisition-tactics, the 3
   think-tanks, the LIGHT-DB / constraints / intermediate `explore` stage) gets a structural
   check instead.

## What's here

```
plugin/                          ← the shipped Claude Code plugin (source: ./plugin)
  README.md                      ← this file
  .claude-plugin/plugin.json     ← plugin manifest (name: diffmode-growth-tactics, v2.3.0)
  reference/
    Marketing-Channel-Menu-2026.md   ← BUNDLED channel taxonomy (100+ channels, 2026 edition)
  skills/                        ← the 12 SKILL.md sources (single source of truth)
    diagnostics-intake/                              (entry: URL prefill or minimal Q&A)
    enrichment-competitors|audience|acquisition-tactics/
    competitor-gaps | cross-industry | platform-arbitrage/   (think-tank research)
    growth-factors-mining/                           (⚠ moat-critical clean-room LIGHT DB)
    lite-constraints/                                (no-Python synthesis-constraints generator)
    synthesis-explore/                               (blind combinations → emergent mechanisms)
    synthesis-build/                                 (white-space ideation → founder-fit → final synthesis.md)
    growth-reviewer/  (+ references/ — 7 rubrics bundled; v2.3.0 gates only competitors + synthesis)
  agents/                        ← 4 sub-agent workers
    research-worker.md           tools: Read,Write,Edit,Glob,Grep,Skill,WebFetch,perplexity_research,_search; sonnet
    analysis-worker.md           tools: Read,Write,Edit,Glob,Grep,Skill (NO research MCP)
    synthesis-worker.md          tools: Read,Write,Edit,Glob,Grep,Skill (NO MCP); model: opus
    reviewer.md                  tools: Read,Glob,Grep,Skill
  commands/                      ← the orchestrators
    run-growth-tactics.md        (full DAG — the main entry)
    run-enrichment.md            (standalone enrichment-only entry)
```

All external paths the skills/agents need are resolved at runtime via
`${CLAUDE_PLUGIN_ROOT}` (the plugin's install dir) — the bundled channel menu and the
reviewer rubrics travel inside this directory, so the plugin is self-contained.

## Install

The repo root is a Claude Code plugin marketplace. Add it, then install:

```bash
# from a local clone …
claude plugin marketplace add /path/to/growth_tactics_plugin
# … or directly from GitHub:
claude plugin marketplace add acogood/diffmode_free

claude plugin install diffmode-growth-tactics@diffmode-free
```

Or interactively: `/plugin` → marketplace `diffmode-free` → install `diffmode-growth-tactics`.
Restart Claude Code, then from **any directory** (the run writes into your cwd):

```
/diffmode-growth-tactics:run-growth-tactics --url https://your-product.com
/diffmode-growth-tactics:run-growth-tactics --product <slug>          # use an existing workspace
/diffmode-growth-tactics:run-enrichment    --product <slug>           # enrichment only
```

The research stages (enrichment research dims, `platform-arbitrage`, `growth-factors-mining`,
`diagnostics-intake` URL mode) require a **Perplexity MCP server** in the host; the audience,
think-tank-analysis, and synthesis stages run with **no MCP** by design.

## Cost / latency note (per-run LIGHT DB)

`growth-factors-mining` does a bounded deep-research sweep (12-20 public case studies, one
pass) **every run** — the deliberate price of "fresh, clean-room, no proprietary DB." It is
the slowest/priciest stage. Mitigations: it **caches** `growth-factors.json` and reuses it on
re-run unless `--remine`, and research breadth is bounded.

## Caveats / open items

- **Reviewer-model calibration.** The rubrics ran on gemini-pro/claude in the source
  pipeline; the plugin reviewer is Sonnet. Scores may calibrate slightly differently — lean
  on `blocking_issues` over the raw number near the gate.
- **Per-run cost/latency (measured, theona.ai v2.3.0, 2026-06-02):** **~75–85 min** wall-clock
  (85 min including one transient synthesis socket-death respawn; ~75–80 min clean) and
  **~5 deep `perplexity_research` + ~50 `perplexity_search` calls ≈ $2–3** (Perplexity-plan
  dependent; the deep-research calls dominate, hence the search-first ≤1–2-deep/stage cap).
  `growth-factors` mining (~10 min) and the 3 think-tanks (~12 min) overlap, so they stay off
  the critical path. See the repo `README.md` "Cost & runtime" for the per-stage table.
- **Codex port** is scaffolded-not-built — see the repo's `codex/CODEX.md`. The 12 skill
  bodies are runtime-neutral and consumed unchanged by Codex; only the orchestration layer
  is Claude-specific.

For full version history, see the repo's `docs/STATUS.md`.
