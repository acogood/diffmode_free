# CLAUDE.md

Guidance for AI agents working in the **Diffmode Growth Tactics** standalone repo.

## What this repo is

The free Diffmode growth-ideation pipeline, packaged as a portable **Claude Code plugin**
(+ a **Codex** scaffold). It takes a founder from a 2-minute intake to a `synthesis.md` of
**7-9 novel demand-gen tactic IDEAS** and **stops at synthesis**. It is an *extract* of the
private `ai-cmo` monorepo's `pipeline-skills/` — re-pointed so it runs **standalone**, leaking
none of the paid product.

This is a **prompt-based system, not traditional software**: no build, no runtime. The
"code" is Markdown (`SKILL.md` bodies, agent defs, orchestrator commands) executed by a
coding-agent runtime. Outputs are Markdown/JSON files written to a per-run workspace.

Buyer-facing essence / moat framing lives in `README.md` and `plugin/README.md`.

## The moat (do not erode it)

The synthesis **method** is what this repo gives away. **Paid + proprietary** (never ship,
never reference content of): the **576-vector growth database** (`tactics_DB/` in the private
repo), its intelligence layer + saturation/anti-vector tracking, and the downstream
**prioritization + implementation** stages. The free pipeline runs the same method on a
deliberately weaker **per-run LIGHT DB** mined fresh from public case studies, and stops.

**Clean-room rule (moat-critical):** `growth-factors-mining` and the whole synthesis chain
MUST NOT read anything under `tactics_DB/`. Mentions of `tactics_DB/` in this repo are only
*prohibitions* / moat framing — never actual DB content, vector counts (no `542`/`8,238`), or
`prompts/` source files. Keep it that way.

## Architecture — single source of truth + what ships

- **One repo, one physical copy of the skills.** The 14 skills live **once** in
  `plugin/skills/`. **Edit them there.** `codex/.agents/skills/*` are relative symlinks
  (`../../../plugin/skills/<name>`) — Codex reads the same files; do NOT create a second copy.
- **Only `plugin/` ships to Claude users.** `marketplace.json` (repo root) declares
  `source: ./plugin`, so Claude copies just that dir to its cache. `docs/`, `codex/`, and the
  root `README.md` do **not** ship — put internal notes there, not in `plugin/`.
- **Codex reads a checked-out repo** (not a copy), so the symlinks resolve. Codex side is
  **scaffold + guide only (verify-at-build-time)** — see `codex/CODEX.md`; the full Codex
  orchestrator is not built.

| Path | Role | Ships to Claude? |
|------|------|------------------|
| `plugin/skills/` | 14 SKILL.md — canonical methodology | yes |
| `plugin/agents/` | 4 worker sub-agents (research/analysis/synthesis/reviewer) | yes |
| `plugin/commands/` | `run-growth-tactics`, `run-enrichment` orchestrators | yes |
| `plugin/reference/` | bundled `Marketing-Channel-Menu-2025-Extended.md` | yes |
| `codex/` | `AGENTS.md` + worker `.toml` + symlinked skills + `CODEX.md` | no |
| `docs/` | architecture, eval-methodology, STATUS, full-pipeline-map | no |

## Portability rules (the whole point of the extract — don't regress)

1. **No host-repo dependencies.** Never reintroduce a "confirm repo root / `ai-cmo-workspace/`
   / `prompts/` present, abort if not" pre-flight. Runs write to **`./<slug>/`** in the user's
   current directory.
2. **Resolve bundled files via `${CLAUDE_PLUGIN_ROOT}`** (expands to the install dir at
   runtime): the channel menu is `${CLAUDE_PLUGIN_ROOT}/reference/…`; reviewer `spec_path`s are
   `${CLAUDE_PLUGIN_ROOT}/skills/<skill>/SKILL.md`. Never point at `prompts/…`.
3. **Skill bodies stay runtime-neutral** — no Claude-only tool ids baked in (say "your
   web-research tool (Perplexity via MCP)", not `mcp__perplexity__*`). The concrete tool
   binding belongs in `plugin/agents/*.md` (Claude) / `codex/agents/*.toml` (Codex). Skills
   treat input paths (incl. the channel menu) as **invoker-supplied**.
4. **Plugin name stays `diffmode-growth-tactics`** — the `diffmode-growth-tactics:*` namespaced
   dispatch ids in commands/agents depend on it.

## The pipeline (DAG)

```
diagnostics-intake → enrichment (competitors → audience ‖ acq-tactics)
  → think-tank ×3 (competitor-gaps · cross-industry · platform-arbitrage)
  ‖ growth-factors-mining (LIGHT DB; starts right after the competitors gate, overlaps enrichment + think-tanks)
  → lite-constraints → synthesis (step1 → step2 → pass1 → pass2) → synthesis.md  (STOP)
```

A parameterized **reviewer** gates the 3 enrichment dims, the 3 think-tanks, and final `pass2`
(score ≥ 7, max 3 retries, `blocking_issues` injected into a FRESH worker). Non-gated stages
get structural checks. Workers are **single-shot and stateless** — every retry is a fresh
spawn; never `SendMessage` a returned worker. Research stages need a **Perplexity MCP**;
analysis + synthesis run with **no MCP** by design (structurally enforces no-web-search).

## Common tasks

- **Edit a skill / agent / command** → edit under `plugin/`. After editing, reinstall the
  plugin to pick up changes. Codex symlinks need no action.
- **Validate** → `claude plugin validate plugin` (must pass before publishing / community
  submission).
- **Check nothing external leaked back in** →
  `grep -rn "prompts/\|ai-cmo-workspace\|repo root" plugin/` should return nothing but the
  README's references to this repo's own root.
- **Confirm Codex symlinks resolve** → `ls -L codex/.agents/skills/` lists all 14.

## Pointers

- Repo landing + install (both runtimes) → `README.md`
- Plugin internals + command reference → `plugin/README.md`
- Codex setup, MCP `KEY`/`TOKEN` gotcha, porting guide → `codex/CODEX.md`
- Codex orchestration model (DAG, gates, clean-room) → `codex/AGENTS.md`
- Design rationale / state contract → `docs/architecture.md`
- Reviewer methodology / scoring → `docs/eval-methodology.md`
- Build/version history → `docs/STATUS.md`

## Open decisions (carry these forward)

1. **Marketplace name** is `diffmode-free` (in `marketplace.json` + install strings as
   `@diffmode-free`) — deliberately NOT `diffmode`, to avoid colliding with / squatting the
   paid `diffmode` CLI + skill (github.com/agentic-builders/diffmode-cli). The plugin name
   stays `diffmode-growth-tactics`.
2. **Source of truth** between this repo and the private `ai-cmo/pipeline-skills/` dev origin is
   **undecided** — keep edits here in sync deliberately until that's settled.
3. **`claude-community` marketplace submission** — optional, after the repo is verified.
