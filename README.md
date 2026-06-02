# Diffmode Growth Tactics

A free, open growth-ideation pipeline for teams that can't outspend their competitors —
solo founders, first marketing hires, small bootstrapped teams. It takes a product from a
**2-minute intake** to a `synthesis.md` of **7-9 novel demand-gen tactic IDEAS**, and stops
there.

Generic AI marketing tools stop at *retrieval* — they hand you a list of known channels. This
pipeline runs the **synthesis** step: it cross-references documented growth *mechanisms*
against a founder's constraints and combines 2-3 at a time into tactics that didn't exist in
any single playbook before.

It ships as **one repo, one physical copy of the skills**, consumable from two runtimes:

- **Claude Code** — a packaged plugin (`plugin/`) with a `/run-growth-tactics` orchestrator.
- **OpenAI Codex** — a scaffold (`codex/`) that reads the *same* skills (see status below).

## The method is free; the moat is not

The synthesis **method** is what this repo gives away. What stays paid — and what actually
defends the product — is:

1. the **proprietary 576-vector growth database** (breadth), its intelligence layer, and
   saturation / anti-vector tracking; and
2. the downstream **prioritization + week-by-week implementation** stages.

This free pipeline runs the same method on a deliberately weaker **per-run LIGHT database**,
mined fresh from public case studies every run (`growth-factors-mining`), and **stops at
synthesis**. The output is genuinely useful — full-depth *ideas* — but visibly lighter than
the paid product. Nothing here reads or ships the proprietary database.

## The pipeline

```
diagnostics-intake            (URL research → prefill, else a minimal Q&A)
        ↓
enrichment                    (competitors → audience ‖ acquisition-tactics)
        ↓                       ↘ growth-factors mining (‖, the clean-room LIGHT DB) starts
        ↓                          right after the competitors gate and overlaps the rest
think-tank research (×3, ‖)        of enrichment + the think-tanks
  competitor-gaps · cross-industry · platform-arbitrage
        ↓
lite-constraints              (in-context constraints generator, no Python)
        ↓
synthesis  explore → build  →  synthesis.md   (7-9 tactic ideas, STOP)
```

A parameterized **reviewer** gates **two stages** — enrichment `competitors` and the final
synthesis (`build`) — at score ≥ 7, max 3 retries; every other generating stage gets a
structural check. Research stages need a **Perplexity MCP server**; analysis + synthesis
stages run with no MCP by design. Every run writes into a `./<slug>/` workspace **in your current directory** — no
host repo required.

## Cost & runtime (measured)

Measured end-to-end on **theona.ai** (v2.3.0, `--fast-intake`, 2026-06-02):

- **Runtime: ~75–85 min** wall-clock. The reference run took **85 min** *including* one transient
  socket-death respawn on synthesis; a clean run is **~75–80 min**. Stages overlap heavily —
  `growth-factors` mining (~10 min) and Wave-2 enrichment run concurrently and stay off the
  critical path, and the 3 think-tanks run in **parallel** (~12 min, not ~36).
- **Perplexity: ~5 deep `perplexity_research` + ~50 `perplexity_search` calls** per run
  (**≈ $2–3**, depending on your Perplexity plan/model). The few **deep-research calls dominate
  the cost**, so the pipeline is search-first and caps deep research at ~1–2 calls/stage. Only
  the research stages (diagnostics URL prefill, competitors, acquisition-tactics, growth-factors
  mining, platform-arbitrage) call Perplexity; analysis + synthesis use no MCP.

Rough per-stage wall-clock (overlapping stages share a start time):

| Stage | ~Time | Notes |
|-------|-------|-------|
| diagnostics intake | 8 min | URL research + prefill |
| enrichment: competitors (gate) | 15 min | the one reviewer-gated enrichment dim |
| enrichment: audience ‖ acquisition-tactics | 4 / 17 min | concurrent (Wave 2) |
| growth-factors mining | 10 min | concurrent — hidden under the critical path |
| think-tanks ×3 | 12 min | parallel, not 3× |
| lite-constraints | 4 min | |
| synthesis: explore → build | 12 + 7 min | +~8 min if a socket death respawns |

Point-in-time numbers from one product — treat as rough. `growth-factors.json` is cached
(re-mined only on `--remine`), so a `--from synthesis` re-run is minutes, not the full hour.

## Repo layout

```
.claude-plugin/marketplace.json   ← Claude marketplace (source: ./plugin)
plugin/                           ← the Claude Code plugin (the only thing Claude installs)
  skills/                         ← the 12 SKILL.md sources — SINGLE SOURCE OF TRUTH
  agents/  commands/  reference/  README.md
codex/                            ← Codex scaffold (reads the same skills via symlink)
  .agents/skills/* → ../../plugin/skills/*
  AGENTS.md  agents/*.toml  CODEX.md
docs/                             ← internal design notes (not shipped to either runtime)
LICENSE                           ← Apache-2.0
```

The 12 skills live **once**, in `plugin/skills/`. Codex consumes them through relative
symlinks under `codex/.agents/skills/`, so there is no second copy and no drift.

## Install — Claude Code

The repo root is a plugin marketplace named `diffmode-free`.

```bash
# from a local clone …
claude plugin marketplace add /path/to/growth_tactics_plugin
# … or directly from GitHub once published:
claude plugin marketplace add <owner>/<repo>

claude plugin install diffmode-growth-tactics@diffmode-free
```

Restart Claude Code, then from **any directory** (the run writes into your cwd):

```
/diffmode-growth-tactics:run-growth-tactics --url https://your-product.com
```

You'll need a **Perplexity MCP server** configured in Claude Code for the research stages.
See `plugin/README.md` for the full command reference.

## Install — OpenAI Codex (scaffolded, verify-at-build-time)

The skill bodies are **runtime-neutral** — Codex reads the same `SKILL.md` files Claude does.
The Codex orchestration layer is **scaffolded, not yet built** (Codex's surface moves fast;
treat it as runnable-soon). To try a single skill today, clone the repo and follow
[`codex/CODEX.md`](codex/CODEX.md): it covers registering the Perplexity MCP
(`codex mcp add perplexity …`), the **`KEY`/`TOKEN` env-stripping gotcha**, how the Claude
orchestrator maps to an `AGENTS.md` + `PLANS.md` ExecPlan, and how to load
`.agents/skills/`.

## License

[Apache-2.0](LICENSE). © 2026 Anton Kogut.
