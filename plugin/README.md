# diffmode-growth-tactics (Claude Code plugin)

The **Diffmode free growth-ideation pipeline**, packaged as a Claude Code plugin. One command —
`/diffmode-growth-tactics:start your-product.com` — takes a product from a **2-minute intake** to a
**Your Growth Tactics** report of **7–9 novel demand-gen tactic ideas**, then stops at ideas.
Every run writes into a `./<slug>/` folder in your current directory; no host repo, no account,
no API key.

> **This is the shipped plugin.** `marketplace.json` at the repo root declares `source: ./plugin`,
> so Claude Code copies **only this directory** to its plugin cache. The bundled channel menu
> (`reference/`) and the 13 skills travel with it; the repo's `docs/`, `codex/`, and root README do
> **not** ship.

## What you get

The run builds a **growth strategy** in three parts — a read on your competition (who you're up
against and how each rival gets users), a map of your buyers (your segments and the job each is
hiring you to do), and **7–9 unconventional acquisition tactics** built for the founder's budget,
stage, and team. The tactics land in the **Your Growth Tactics** report — plain cards, one per
tactic: what it is, why rivals can't copy it, how to start this week, and when to kill it. The
full engineering write-up behind each tactic ships alongside as a working paper.

The competitor read, the buyer map, and the acquisition audit behind them stay in the workspace
as briefs you can reuse. It **stops at synthesis** — prioritization and a week-by-week rollout
are the paid product (see the bottom of this file).

The run ends with a **styled HTML report** at `<slug>/report/index.html` — every deliverable as
a readable page that opens in your browser, no markdown viewer or extra installs needed (the
`.md` sources stay alongside).

## The pipeline

```
diagnostics-intake     URL research → prefill, else a 2-minute Q&A
        ↓
enrichment             competitors → audience ‖ acquisition-tactics
        ↓              ↘ growth-factors mining runs concurrently from right here
think-tank research     three angles in parallel — competitor gaps · cross-industry ·
        ↓               platform opportunities
lite-constraints       in-context constraints generator (no Python)
        ↓
synthesis  explore → build  →  synthesis.md   (7–9 tactic ideas, then STOP)
        ↓
packaged as "Your Growth Tactics"  →  plain-language tactic cards (best-effort)
```

Research stages use a **Perplexity MCP server** when present and **fall back to the built-in
WebSearch** otherwise (zero setup; fallback citations are auto-verified for reachability); the
analysis and synthesis stages run with **no MCP** by design. A parameterized reviewer gates two
stages — enrichment `competitors` and the final synthesis `build` — and every other generating
stage gets a structural check. The orchestration model (a main-thread orchestrator, passive
skills, and thin worker sub-agents, and why each runs where it does) is documented in
[`../docs/architecture.md`](../docs/architecture.md).

## Install and run

The repo root is a Claude Code plugin marketplace named `diffmode-free`.

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
/diffmode-growth-tactics:start your-product.com
```

That's the whole interface: run it bare and it asks for your product's website (or takes
"I don't have a site yet"); run it again in the same folder and it offers to continue an
unfinished run right where it stopped.

**Claude Cowork:** install through the app, not in a session — **Cowork tab → Customize →
Plugins → Add from repository** → `acogood/diffmode_free` → install `diffmode-growth-tactics`,
then start a new session. Don't ask the in-session agent to install it: sessions are sandboxed,
so an in-session install is wiped on relaunch; the Customize menu is the install that persists.

## What's in this directory

```
plugin/
  README.md                      this file
  .claude-plugin/plugin.json     plugin manifest (name: diffmode-growth-tactics)
  reference/                     bundled 2026 marketing-channel menu (100+ channels)
  skills/                        the 13 skill files — the single source of truth
  agents/                        4 worker sub-agents (research / analysis / synthesis / reviewer)
  commands/                      the start orchestrator
```

All paths the skills and agents need are resolved at runtime via `${CLAUDE_PLUGIN_ROOT}` (the
plugin's install dir), so the plugin is self-contained.

## Notes

- **Cost / runtime:** about **1–1.5 hours** per run; free on the built-in web search, or roughly
  **$2–3** with Perplexity (a few deep-research calls are the only paid part). Measured runtimes
  and the per-stage breakdown live in [`../docs/STATUS.md`](../docs/STATUS.md).
- **Codex:** the skill bodies are runtime-neutral and Codex reads them unchanged; only the
  orchestration layer is Claude-specific. See the repo's [`../codex/CODEX.md`](../codex/CODEX.md).

## Free vs. the full Diffmode

This plugin gives you the **ideas**. [**Diffmode**](https://diffmode.app) ranks them and turns the
top picks into a **week-by-week rollout plan**, drawn from a much larger, curated growth-mechanism
database than the fresh, per-run research each run does here. Free audit, no credit card; full plan
with a **30-day money-back guarantee** → **[diffmode.app](https://diffmode.app)**.
