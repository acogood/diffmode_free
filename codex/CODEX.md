# CODEX.md — running Diffmode Growth Tactics under OpenAI Codex

This repo ships the pipeline as a **shared standard**: the 15 `SKILL.md` bodies (the
methodology IP, ~90% of the content) are runtime-neutral and read **byte-for-byte the same**
by Claude Code and Codex. Only the orchestration layer differs per runtime. This guide covers
the Codex side.

> ## ⚠ Status: scaffolded, not yet built — verify at build time
>
> What is **done**: the skills are runtime-neutral and symlinked into `.agents/skills/`; the
> worker stubs (`agents/*.toml`) and the orchestration spec (`AGENTS.md`) are written.
>
> What is **not done**: a turnkey Codex run of the *full* DAG. Codex's agent/skill/plugin
> surface moves fast, so before a production run, **verify** the `.toml` field names, the
> skill-preload mechanism, and the sub-agent dispatch API against the current Codex docs. The
> single-skill smoke test below is the recommended first step — it proves the shared-skill
> seam without depending on the full orchestrator.

## How the runtimes map

| Concern | Claude Code | Codex |
|---|---|---|
| Skills | `plugin/skills/*` (auto-discovered) | `.agents/skills/*` (symlinks to the same files) |
| Orchestrator | `/run-growth-tactics` slash command | a `PLANS.md` ExecPlan + `AGENTS.md` durable instructions |
| Workers | `plugin/agents/*.md` (`tools:` lists `mcp__perplexity__*`) | `agents/*.toml` custom agents (`mcp_servers = ["perplexity"]`) |
| Plugin root | `${CLAUDE_PLUGIN_ROOT}` resolves at runtime | no equivalent — the orchestrator passes checkout-relative paths |

Codex won't honor a Claude slash command, so the orchestrator is **re-authored** (see
`AGENTS.md`), not ported. The skills and the reviewer rubrics are **not** re-authored — they
are the same files.

## Path resolution under Codex

- **Skills** are read from `.agents/skills/<skill>/SKILL.md`. Codex reads a **checked-out
  repo** (not a copied cache), so the relative symlinks into `../plugin/skills/*` resolve
  fine — one physical skill set, both runtimes.
- **The channel menu** is at `plugin/reference/Marketing-Channel-Menu-2025-Extended.md` (from
  the repo root) — i.e. `../plugin/reference/…` relative to this `codex/` directory. The skill
  bodies mention it as `${CLAUDE_PLUGIN_ROOT}/reference/…`; that token is **Claude-only**.
  Skills declare the channel menu as **invoker-supplied** ("the invoker provides these; do not
  hardcode absolute paths"), so under Codex the orchestrator simply passes the checkout-
  relative path as the input — **no skill edit needed**.
- **Reviewer rubrics**: `.agents/skills/growth-reviewer/references/<dimension>.md`.

## Setup

### 1. Register the Perplexity MCP server (research stages only)

```bash
codex mcp add perplexity --env PERPLEXITY_API_KEY="pplx-…" -- npx -y @perplexity-ai/mcp-server
```

Only `research-worker` needs this. `analysis-worker`, `synthesis-worker`, and `reviewer-worker`
deliberately declare **no** `mcp_servers` — the absence of a research tool is what structurally
enforces the "no new web search" rules for those stages.

### 2. ⚠ The `KEY` / `TOKEN` env-stripping gotcha

Codex strips environment variables whose names contain `KEY` / `SECRET` / `TOKEN` by default.
Without a fix, `PERPLEXITY_API_KEY` never reaches the MCP process and **research silently
fails** (empty results, no error). Either, in `config.toml`:

```toml
[shell_environment_policy]
ignore_default_excludes = true
```

…or whitelist just that var via the policy's `env_vars` allowlist. Verify the MCP actually
receives the key before a full run.

### 3. Make the worker agents discoverable

Place the `agents/*.toml` stubs where your Codex install reads custom agents (per current docs,
`~/.codex/agents/*.toml`, or a project-scoped equivalent). Confirm each `name` resolves before
dispatching. The stubs are mirrors of `../plugin/agents/*.md` — read those for the full,
battle-tested worker contracts.

## Smoke test (prove the shared-skill seam first)

Before building the full orchestrator, confirm a single skill loads and runs standalone under
Codex:

1. Ensure `.agents/skills/enrichment-competitors` resolves:
   `ls -L .agents/skills/enrichment-competitors/SKILL.md`.
2. Register the Perplexity MCP (above) and confirm the key reaches it.
3. Drive `research-worker` with a brief: `skill = enrichment-competitors`, `inputs =` a
   `founder-input.md` you supply + the channel menu path
   (`plugin/reference/Marketing-Channel-Menu-2025-Extended.md`), `output =`
   `./<slug>/02-enrichment/competitors-analysis.md`.
4. Verify the output has the required sections (`## Competitor Overview`,
   `## Competitive Channel Matrix`) and cites Perplexity-sourced URLs.

If that works, the shared-skill seam is proven — the remaining work is wiring the DAG + reviewer
loop from `AGENTS.md` into a `PLANS.md` ExecPlan.

## Building the full orchestrator (next pass)

Re-express `../plugin/commands/run-growth-tactics.md` as a `PLANS.md` ExecPlan that owns: the
DAG (Stage 0→4), the parallel fan-outs (Wave-2 enrichment; the 4-way think-tank + growth-factors
batch), the reviewer→retry gate (score ≥ 7, max 3, blocking_issues injected into a fresh
worker), the structural checks for the non-gated stages, and the Stage-4 `constraints-stale`
precheck + block-level `must_include` enforcement. `AGENTS.md` is the durable companion to that
ExecPlan. Keep workers single-shot and stateless; keep the clean-room rule absolute.
