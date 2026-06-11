# CODEX.md — running Diffmode Growth Tactics under OpenAI Codex

This repo ships the pipeline as a **shared standard**: the 15 `SKILL.md` bodies (the
methodology IP, ~90% of the content) are runtime-neutral and read **byte-for-byte the same**
by Claude Code and Codex. Only the orchestration layer differs per runtime. This guide covers
the Codex side.

> ## ✅ Status: built + A/B-validated (2026-06-04)
>
> The full DAG runs end-to-end as a deterministic Python driver — **`codex/orchestrate.py`**
> (Stage 0 URL intake → enrichment → think-tanks → per-run LIGHT DB → synthesis), dispatching
> each stage as a `codex exec` worker and gating it with the structural checks in
> `codex/checks.py`. It **passed a full A/B quality test on theona.ai** (2026-06-04, gpt-5.5,
> Perplexity OFF): **9 tactics, 78% unconventional, 0 phantom vectors, build reviewer APPROVED 8.0
> first-pass, a 25-vector clean-room LIGHT DB, 18/18 cited URLs live, ~51 min** — on par with the
> Claude v2.3.0 baseline. See **Running the full pipeline** below + `../docs/STATUS.md` Round-7.
>
> The skills are runtime-neutral and symlinked into `.agents/skills/`; the `research-worker` is
> **Perplexity-optional** (prefers Perplexity when registered, else the native `web_search` tool,
> with a citation-integrity re-fetch). The `.toml` field names + `codex exec` dispatch flags in
> §3–§4 are verified against **codex-cli 0.136** (the worker-schema smoke in Round-6 was 0.130) —
> re-confirm against your installed Codex if it has drifted. The single-skill smoke test below
> remains the fastest way to prove the shared-skill seam in isolation.

## How the runtimes map

| Concern | Claude Code | Codex |
|---|---|---|
| Skills | `plugin/skills/*` (auto-discovered) | `.agents/skills/*` (symlinks to the same files) |
| Orchestrator | `/run-growth-tactics` slash command | a `PLANS.md` ExecPlan + `AGENTS.md` durable instructions |
| Workers | `plugin/agents/*.md` (`tools:` lists `mcp__perplexity__*` + `WebSearch`) | `agents/*.toml` custom agents (Perplexity MCP **optional** + native `web_search`) |
| Plugin root | `${CLAUDE_PLUGIN_ROOT}` resolves at runtime | no equivalent — the orchestrator passes checkout-relative paths |

Codex won't honor a Claude slash command, so the orchestrator is **re-authored** (see
`AGENTS.md`), not ported. The skills and the reviewer rubrics are **not** re-authored — they
are the same files.

## Path resolution under Codex

- **Skills** are read from `.agents/skills/<skill>/SKILL.md`. Codex reads a **checked-out
  repo** (not a copied cache), so the relative symlinks into `../plugin/skills/*` resolve
  fine — one physical skill set, both runtimes.
- **The channel menu** is at `plugin/reference/Marketing-Channel-Menu-2026.md` (from
  the repo root) — i.e. `../plugin/reference/…` relative to this `codex/` directory. The skill
  bodies mention it as `${CLAUDE_PLUGIN_ROOT}/reference/…`; that token is **Claude-only**.
  Skills declare the channel menu as **invoker-supplied** ("the invoker provides these; do not
  hardcode absolute paths"), so under Codex the orchestrator simply passes the checkout-
  relative path as the input — **no skill edit needed**.
- **Reviewer rubrics**: `.agents/skills/growth-reviewer/references/<dimension>.md`.

## Setup

### 1. (Optional) register the Perplexity MCP server

Perplexity is **optional**. Register it for lower-cost, higher-quality deep research on the
research stages; **without it, `research-worker` falls back to the native `web_search` tool**
(`-c web_search="live"` at dispatch — zero setup, no API key). This mirrors the Claude plugin,
which prefers Perplexity when present and falls back to the built-in WebSearch (plugin v2.4.0).

```bash
codex mcp add perplexity --env PERPLEXITY_API_KEY="pplx-…" -- npx -y @perplexity-ai/mcp-server
```

Only `research-worker` uses a research backend at all. `analysis-worker`, `synthesis-worker`, and
`reviewer-worker` deliberately declare **no** `mcp_servers` **and** are dispatched with
`web_search = "disabled"` — see §4 "Web search & clean-room" below.

### 2. ⚠ The `KEY` / `TOKEN` env-stripping gotcha (only if you registered Perplexity)

*(Skip this entirely if you're using the native `web_search` fallback — it needs no key.)*

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

Place the `agents/*.toml` stubs where your Codex install reads custom agents — **verified for
codex-cli 0.130: `~/.codex/agents/*.toml`** (or a project-scoped equivalent). Confirm each `name`
resolves before dispatching. ⚠ A malformed agent file is **silently ignored** (Codex logs only a
`warning: Ignoring malformed agent role definition …`) — the most common cause is writing
`mcp_servers` as an **array of names**; on Codex it is a **map keyed by server name**
(`[mcp_servers.<name>]` with a transport — `command`/`args` or `url`). That is why the workers here
declare **no** `mcp_servers` and inherit Perplexity from the parent session instead (see §1 and the
`research-worker.toml` header comment). The stubs mirror `../plugin/agents/*.md` — read those for
the full, battle-tested worker contracts.

### 4. Web search & clean-room (per-invocation)

Codex's native web search is **per-invocation**, controlled by the top-level `web_search` config
key — one of `disabled`, `cached` (the default), or `live`. The default `cached` still serves
**web-cache** results, so it is **not** "no web." That makes the clean-room mapping explicit and
mirrors Claude's per-agent tool grants — the research worker is the only one with a web tool;
every other worker is offline by construction:

- **Baseline `web_search = "disabled"`** in `~/.codex/config.toml`. This is the safe default for
  the no-web stages (analysis, synthesis, reviewer): with it set, omitting `mcp_servers` truly
  means no web. ("No `mcp_servers`" alone is **insufficient** — the native `web_search` tool would
  still default to `cached`.)
- **`research-worker` dispatches opt IN to web:** add `-c web_search="live"` to that worker's
  `codex exec` call (and register + attach Perplexity if you want the lower-cost backend). On
  `codex exec` use the **`-c web_search="live"`** override — the bare `--search` flag is the
  **interactive** `codex` equivalent (`codex --search …`) and is rejected when placed *after* the
  `exec` subcommand (`codex exec --search` errors; use `-c web_search="live"`, or the global
  `codex --search exec …`). Also grant **shell network** for the citation-integrity re-fetch:
  `--sandbox workspace-write -c sandbox_workspace_write.network_access=true`. (The native
  `web_search` tool works without it, but the full-URL `curl` re-fetch that drops dead/404 deep
  links does not — a measured run without network could only verify domains, missing two stale
  deep-link 404s; see STATUS Round-6.)
- **No-web dispatches add nothing** — they inherit the disabled baseline and stay offline.

## Smoke test (prove the shared-skill seam first)

Before building the full orchestrator, confirm a single skill loads and runs standalone under
Codex. Perplexity is optional here — the **native `web_search` fallback path is the one to prove**,
since it is the new zero-setup default:

1. Ensure `.agents/skills/enrichment-competitors` resolves:
   `ls -L .agents/skills/enrichment-competitors/SKILL.md`.
2. Make `research-worker` discoverable (copy `agents/research-worker.toml` into your Codex agents
   dir, e.g. `~/.codex/agents/`).
3. **Drive it Perplexity-OFF / native-`web_search`-ON** (the fallback path): a `codex exec` with
   `-c web_search="live"` (enables native web search), **no Perplexity registered** (⇒ fallback),
   `--skip-git-repo-check`, `--sandbox workspace-write -c sandbox_workspace_write.network_access=true`
   (so the citation re-fetch can `curl`), and a brief — `skill = enrichment-competitors`,
   `inputs =` a `founder-input.md` you supply + the channel menu path
   (`plugin/reference/Marketing-Channel-Menu-2026.md`), `output =`
   `./<slug>/02-enrichment/competitors-analysis.md`. (With Perplexity registered + attached, the
   same brief exercises the Perplexity path instead.)
4. Verify the output has the required sections (`## Competitor Overview`,
   `## Competitive Channel Matrix`) and **cites real, retrieved URLs (Perplexity or native
   `web_search`)** — sweep every cited URL and confirm **0 NXDOMAIN / 0 hard-404**; on the
   fallback path the worker's return JSON reports `citationsVerified` / `citationsDropped`.

If that works, the shared-skill seam is proven — the remaining work is wiring the DAG + reviewer
loop from `AGENTS.md` into a `PLANS.md` ExecPlan.

> **✅ Validated 2026-06-02 (native `web_search` fallback, Perplexity OFF, codex-cli 0.130).** A
> headless `codex exec` of `enrichment-competitors` on the theona.ai fixture (`-c web_search="live"`,
> no Perplexity, `--sandbox workspace-write -c sandbox_workspace_write.network_access=true`)
> produced both required sections and 6 competitors with a correct tier mix; **30 `web_search`
> calls, 0 Perplexity, 4 `curl` citation re-fetches**; the worker reported `citationsVerified=24,
> citationsDropped=0`; **independent sweep of 26 cited URLs / 15 hosts → 0 NXDOMAIN, 0 hard-404**
> (the few non-200s are 403/WAF/anti-bot on real hosts, correctly kept). See `../docs/STATUS.md`
> Round-6 for the full result, including the first-pass finding (a domain-only check + no shell
> network missed two stale deep-link 404s) that drove the full-URL citation check + the
> network-access dispatch flag.

## Running the full pipeline

The orchestration spec above (`run-growth-tactics.md` → `AGENTS.md`) is implemented by
**`codex/orchestrate.py`** — a stdlib-only Python driver that owns the DAG (Stage 0→4), the
parallel fan-outs (Wave-2 enrichment; the think-tank + growth-factors batch), the reviewer→retry
gate (score ≥ 7, max 3, blocking_issues injected into a fresh worker), the structural checks for
the non-gated stages (`codex/checks.py`), and the Stage-4 `constraints-stale` precheck +
block-level `must_include` enforcement. Workers stay single-shot and stateless; the clean-room
rule is absolute.

**Prerequisites:** Python 3, the `codex` CLI installed + logged in, and the worker stubs
discoverable (`~/.codex/agents/*.toml`, see §3). Then, from any directory:

```bash
# from a URL — Stage 0 researches the site, asking the must-ask founder fields up front:
python3 /path/to/codex/orchestrate.py --url https://yourproduct.com
# hands-off (no Q&A; researched prefill with [NEEDS FOUNDER INPUT] placeholders):
python3 /path/to/codex/orchestrate.py --url https://yourproduct.com --fast-intake
# or from a pre-seeded founder-input.md (skip-if-valid — the A/B / resume path):
python3 /path/to/codex/orchestrate.py --product <slug> --out-dir /path/to/parent
```

It writes the run into `./<slug>/` (slug derived from the URL host unless `--product` is given)
and **stops at `synthesis.md`**. `--max-concurrency 2` (the default) overlaps growth-factors
mining with enrichment + the think-tanks. On a backgrounded / piped run the driver auto-falls
back to `--fast-intake` rather than hang on the founder Q&A.

The final report renders the deliverables to a styled HTML report at `./<slug>/report/index.html`
(via `plugin/scripts/render_html.py`, stdlib-only, best-effort — a render failure never fails the
run) and lists the deliverables before the per-stage timing ledger.

**✅ A/B-validated (theona.ai, 2026-06-04, gpt-5.5, Perplexity OFF).** A full-DAG run matched the
Claude v2.3.0 baseline: **9 tactics · 78% unconventional · 0 phantom vectors · build reviewer
APPROVED 8.0 first-pass · 25-vector clean-room LIGHT DB · 18/18 cited URLs live · ~51 min**. See
`../docs/STATUS.md` Round-7 for the full result (incl. the gpt-5.5-compact min-line-floor
recalibration in `codex/checks.py`).
