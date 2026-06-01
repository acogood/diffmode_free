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
synthesis  step1 → step2 → pass1 → pass2  →  synthesis.md   (7-9 tactic ideas, STOP)
```

A parameterized **reviewer** gates every generating stage (score ≥ 7, max 3 retries).
Research stages need a **Perplexity MCP server**; analysis + synthesis stages run with no MCP
by design. Every run writes into a `./<slug>/` workspace **in your current directory** — no
host repo required.

## Repo layout

```
.claude-plugin/marketplace.json   ← Claude marketplace (source: ./plugin)
plugin/                           ← the Claude Code plugin (the only thing Claude installs)
  skills/                         ← the 14 SKILL.md sources — SINGLE SOURCE OF TRUTH
  agents/  commands/  reference/  README.md
codex/                            ← Codex scaffold (reads the same skills via symlink)
  .agents/skills/* → ../../plugin/skills/*
  AGENTS.md  agents/*.toml  CODEX.md
docs/                             ← internal design notes (not shipped to either runtime)
LICENSE                           ← Apache-2.0
```

The 14 skills live **once**, in `plugin/skills/`. Codex consumes them through relative
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
