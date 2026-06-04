# STATUS — diffmode-growth-tactics plugin

*Living "where things stand + what's left" view — this file is the dated build log (the Round
notes below) and tracks current state. For onboarding + install see [`README.md`](./README.md);
for the design (orchestrator + skills + workers) see [`architecture.md`](./architecture.md).*

Last updated: **2026-06-04**

> **Round-7 — Full Codex orchestrator built + Stage 0 URL intake + A/B-validated (2026-06-04).** The
> Codex runtime is no longer a scaffold. A stdlib-only Python driver — **`codex/orchestrate.py`**
> (the DAG) + **`codex/checks.py`** (deterministic structural gates) + **`codex/codex_dispatch.py`**
> (the single `codex exec` boundary) — runs the **full DAG, Stage 0 → 4**, exactly as
> `run-growth-tactics.md` → `AGENTS.md` specify: reviewer→retry on the two gated stages
> (`competitors`, synthesis `build`), structural checks on the rest, the Stage-1.5 growth-factors
> hoist with background overlap, the Stage-4 `constraints-stale` precheck, and block-level
> `must_include` enforcement. This round also closed the last MVP scope cut — **Stage 0 URL
> intake**: `--url` now researches the site headlessly through the `diagnostics-intake` skill,
> asking the founder the must-ask fields **up front** (each worker is a non-interactive `codex exec`
> batch call, so the driver asks before the run rather than pausing mid-run); `--fast-intake` — and
> any non-TTY / backgrounded run, by an `isatty` fallback — skips the Q&A and accepts the researched
> prefill with `[NEEDS FOUNDER INPUT]` placeholders.
>
> **✅ Full-DAG A/B-validated (theona.ai, gpt-5.5, Perplexity OFF, 2026-06-04).** Matched the Claude
> v2.3.0 baseline: **9 tactics · 78% unconventional · 0 phantom vectors · build reviewer APPROVED
> 8.0 first-pass · 25-vector clean-room LIGHT DB · 18/18 cited URLs live · ~51 min**. Calibration
> note: gpt-5.5 writes markedly more compactly than the Claude/theona-lite3 fixtures (a complete
> 4-segment audience analysis came in at ~39 non-blank lines), so the per-stage **min-line floors in
> `codex/checks.py` were recalibrated downward** — low enough never to false-positive on a
> complete-but-terse output, with the LAST-required-section anchor staying the primary
> non-truncation signal.
>
> **No `plugin.json` bump, no tag** — `codex/` does not ship to Claude users (marketplace
> `source: ./plugin`) and `plugin/` is byte-unchanged; consistent with the Round-6 codex-parity
> commit. Changed: `codex/orchestrate.py` (Stage 0), `codex/checks.py`, `codex/codex_dispatch.py`,
> `.gitignore`, `codex/AGENTS.md`, `codex/CODEX.md`, `README.md`, `docs/STATUS.md`. The dispatch
> flags + `.toml` schema notes are verified against **codex-cli 0.136** (Round-6's worker smoke was
> 0.130).

> **Round-6 — Codex parity: Perplexity-optional on the Codex runtime too (2026-06-02).** Brought the
> Codex `research-worker` to the same Perplexity-optional posture the Claude plugin reached in
> Round-5 / v2.4.0: it now **prefers the Perplexity MCP when registered and otherwise falls back to
> Codex's native `web_search` tool**, gated by the same universal **citation-source rule** + a
> **citation-integrity re-fetch** (re-fetch every cited URL on the fallback path, drop/re-ground
> NXDOMAIN/404, report `citationsVerified`/`citationsDropped`). **No `plugin.json` bump, no new
> tag** — `codex/` does not ship to Claude users (marketplace `source: ./plugin`) and `plugin/` is
> byte-unchanged; this completes the v2.4.0 "Codex follow-up."
>
> **Grounding facts (verified against codex-cli 0.130 + `codex --help`):** native web search is
> per-invocation via the top-level `web_search` config key — `disabled` / `cached` (default) /
> `live`; on `codex exec` it is enabled with **`-c web_search="live"`** (the bare `--search` flag is
> interactive-only: `codex exec --search` errors; `codex --search exec …` works). Because the
> default `cached` still serves web-cache results, the no-web workers (analysis / synthesis /
> reviewer) are dispatched with an explicit **`web_search="disabled"` baseline** — "no `mcp_servers`"
> alone is insufficient. Custom agents live at **`~/.codex/agents/*.toml`** and are **silently
> ignored if malformed**; the scaffold's `mcp_servers = ["perplexity"]` (an array) is rejected
> (`invalid type: sequence, expected a map` — the field is a *map* keyed by server name with a
> transport), so the worker now declares **no** `mcp_servers` and **inherits a globally-registered
> Perplexity MCP** instead, with native `web_search` as the keyless default.
>
> **✅ Live smoke validated (theona.ai competitors stage, native `web_search`, Perplexity OFF).** A
> headless `codex exec` (`-c web_search="live"`, no Perplexity, `--sandbox workspace-write` +
> `sandbox_workspace_write.network_access=true`) ran `enrichment-competitors` end-to-end:
> **30 `web_search` calls · 0 Perplexity · 4 `curl` citation re-fetches**; output had both required
> sections (`## Competitor Overview`, `## Competitive Channel Matrix`) + 6 competitors with a correct
> tier mix (4 market_leader + 2 indie_direct); worker reported **`citationsVerified=24,
> citationsDropped=0`**; **independent sweep of 26 cited URLs / 15 hosts → 0 NXDOMAIN, 0 hard-404**
> (the 5 non-200s are 403/WAF/anti-bot on real hosts — g2, make.com, producthunt, linkedin-999 —
> correctly kept). The agent file loaded with **no warning** (schema-valid). *Honesty note:* a first
> pass **without** shell network exposed that a domain-only re-fetch misses deep-path 404s (2 stale
> deep links slipped through on real domains, `citationsDropped=0`); the fix was to tighten
> `citation_integrity_check` to verify **full URLs** and to grant the research dispatch shell network
> for the `curl` re-fetch — the re-run was clean. Changed: `codex/agents/*.toml`, `codex/CODEX.md`,
> `codex/AGENTS.md`, `docs/architecture.md`, `README.md`. Skills byte-identical; 12 symlinks intact.
> Smoke installs `~/.codex/agents/research-worker.toml` (additive, reversible) and removes it after.

> **Round-5 — Perplexity-optional / WebSearch fallback (2026-06-02, plugin v2.4.0).** Made the
> Perplexity MCP **optional**: the `research-worker` now **prefers Perplexity when present and
> falls back to the built-in `WebSearch`** (zero setup, no API key) across all 5 research stages,
> removing the single biggest adoption barrier — a new user can run the full pipeline with **no
> MCP at all**. The one degradation the measure-first experiment found (the WebSearch path
> fabricated **1** source domain — `digitalailiens.com`, NXDOMAIN — where Perplexity fabricated
> 0, and the no-web reviewer structurally can't catch a hallucinated URL) is **gated by a
> citation-integrity mitigation** in `agents/research-worker.md`: (a) a universal
> **citation-source rule** ("cite only URLs you actually retrieved this run; never reconstruct,
> recall, or invent a domain"), and (b) a new **Step-6 citation-integrity re-fetch** that
> `WebFetch`-verifies every distinct cited domain on the fallback path and **drops/re-grounds any
> NXDOMAIN / hard-404** before returning (reporting `citationsVerified` / `citationsDropped`); the
> Perplexity path **skips** the re-fetch (its URLs are already grounded → no added latency). Both
> orchestrators print a one-line **WebSearch-fallback-mode banner** when no Perplexity MCP is
> detected (no hard gate — there never was one). The 5 research skills, both READMEs, `CLAUDE.md`,
> `architecture.md`, and `eval-methodology.md` §4c were softened/updated to backend-neutral;
> `plugin.json` 2.3.0 → **2.4.0**. **Codex side was unchanged in this round** — its
> `research-worker` still required Perplexity; **mirrored in Round-6 below** (Codex parity).
>
> **✅ Targeted re-validation PASSED (theona.ai competitors stage, 2026-06-02; `--plugin-dir` on
> the edited tree, no reinstall):**
> - **(a) Citation gate, Perplexity-OFF** (`--strict-mcp-config '{"mcpServers":{}}'`): ran fully
>   on the fallback — **75 WebSearch + 28 WebFetch, 0 Perplexity**; the worker ran Step 6 and
>   reported **`citationsVerified=8, citationsDropped=0`** (correctly treating a G2 403/WAF block
>   as real, not a fabrication); independent sweep **81/81 cited hosts resolve (0 NXDOMAIN)** +
>   **62/62 clickable URLs reachable (0 hard-404)** — the old `digitalailiens.com` fabrication is
>   **gone**; reviewer **APPROVED score 8**.
> - **(b) Regression smoke, Perplexity-ON** (perplexity-only MCP): the worker still prefers
>   Perplexity exclusively — **21 `perplexity_*` calls, 0 WebSearch**, no citation re-fetch
>   (correct); reviewer **APPROVED score 9**.
> - **(c)** `claude plugin validate` → green.

> **Round-4 speed + simplicity pass (2026-06-01, plugin v2.3.0).** Faster + cheaper + simpler,
> quality held: (1) **synthesis 5→3 calls** — fused step1+step2 → `synthesis-explore` (sonnet,
> structural-check-only) and pass1+pass2 → `synthesis-build` (opus, reviewer-gated); the hard
> phase walls (blind-draw ordering, Stripped-Core-Action / Reframing tests, verb-group dedup,
> Preserve-the-Unconventional-Core, purity + deception vetoes, the exact final output template)
> carry over verbatim. (2) **Reviewers 7→2** — only enrichment `competitors` and the final
> `synthesis-build` stay gated; audience + acquisition-tactics + the 3 think-tanks are
> structural-check-only. (3) **Reliable think-tank parallelism** — one message, exactly three
> Agent calls, `platform-arbitrage` launched first; removes the ~18-min serialization. (4)
> **Stage-1.5 retry-in-place** (`resume_partial`) — a socket-death respawn resumes mining
> instead of re-running the deep-research passes (≈8 duplicate Perplexity calls saved). (5)
> **Perplexity caps** — search-first, ≤~1-2 deep `perplexity_research` calls/stage. (6)
> **Channel-Menu-2026** bundled (replaces 2025). Counts: skills 14→12, reviewer **gates** 7→2
> (the 7 rubric files are retained, just unused for the dropped stages).
>
> **✅ Re-test PASSED (theona.ai, 2026-06-02) — SHIPPED.** All ship bars held; the moat-risky
> synthesis collapse *improved* quality. **8 tactics · 88% unconventional** (vs v2.2.0 67%, bar
> ≥60%) · **100% white-space retention** (4/4 Phase-1 carried) · **0 phantom vectors** (18 unique
> IDs, all traceable) · **verb groups 9, ≤2/group** · **0 purity / 0 deception failures** ·
> **`synthesis-build` reviewer APPROVED score 9, first pass.** Wins measured: **wall-clock 85 min**
> (vs ~112 min) even *with* one `explore` socket-death respawn (auto-recovered, att2 OK); **think-tanks
> 0s `started_at` spread** (true parallel); **5 deep `perplexity_research` calls** (down from 6) +
> search-first rebalance, growth-factors mining 10 min (vs ~38 min), no respawn duplication. No
> revert triggered — commit kept.

> **Round-3 speed pass (2026-06-01, plugin v2.2.0).** Cut the 2.5–3h run without changing
> output quality: (1) **per-stage timing** instrumented in the run-ledger (`started_at` +
> `duration_s`) and printed in the final report; (2) **`growth-factors-mining` hoisted to a
> Stage 1.5** that starts right after the competitors gate and overlaps enrichment + the
> think-tanks (~40 min off the critical path — it strictly needs only `founder-input.md`);
> (3) **`purchase-objections` dropped** — a verified dead-leaf enrichment dim nothing
> downstream consumed (same pattern as `demographics`), removing a whole reviewer-gated stage
> (~25 min); (4) **synthesis chain model-tiered** — the mechanical steps (lite-constraints,
> step1, step2) run on sonnet via per-dispatch override, pass1/pass2 stay on opus. Counts:
> enrichment 4→3 dims, skills 15→14, reviewer rubrics 8→7.

> **Round-2 remediation (2026-05-29).** Independent-review fixes landed: `Edit` tool added to
> the writing workers (operable format-only retry); the demand-gen-synthesis rubric rewritten
> clean-room-native and aligned to pass2's actual output; `design/` relocated out of the
> shipped plugin to `../docs/pipeline-skills-design/` + residual IP scrubbed; gate hardening
> (`constraints-stale` precheck, block-level `must_include`, truncation completeness check);
> an orchestrator run-ledger; and the moat framing reconciled.

## TL;DR (plain language)

We grew the enrichment pilot into the **full free Diffmode growth-ideation pipeline**,
packaged as one installable Claude Code plugin: `diffmode-growth-tactics`. It takes a founder
from a **2-minute intake** (research a URL, or answer ~8 questions) all the way to a final
`synthesis.md` of **7-9 novel demand-gen tactic IDEAS** — and **stops at synthesis**.

The free moat substitute is the key new idea: because a public plugin ships every file to the
user's disk, it can't bundle the proprietary **576-vector database** or the Python script
that reads it. So each run **builds a clean-room LIGHT vector DB fresh** from public case
studies (`growth-factors-mining` → `growth-factors.json`) and a skill replaces the Python
constraints generator (`lite-constraints`). The 4-step synthesis was ported and IP-scrubbed to
read that LIGHT DB. Paid Diffmode keeps prioritization, implementation guides, and the real DB.

**This work is written, validated (all 12 skills pass `quick_validate.py`), and the v2.3.0
theona.ai re-test PASSED every ship bar (2026-06-02) — SHIPPED at v2.3.0 (see the Round-4 note).**

## Status at a glance

| Component | State |
|-----------|-------|
| 2 manifests (`plugin.json` v2.4.0 + repo-root `marketplace.json`) | ✅ done |
| `diagnostics-intake` skill (URL prefill / minimal Q&A) | ✅ done |
| 3 enrichment dimension skills | ✅ done (carried from v1; demographics removed 2026-05-28, purchase-objections removed 2026-06-01) |
| 3 think-tank research skills (competitor-gaps, cross-industry, platform-arbitrage) | ✅ done |
| `growth-factors-mining` (per-run clean-room LIGHT DB) | ✅ done — ⚠ moat-critical |
| `lite-constraints` (no-Python synthesis-constraints) | ✅ done |
| 2 synthesis skills (`synthesis-explore` → `synthesis-build`) | ✅ done — fused from 4 (v2.3.0), IP-scrubbed |
| `growth-reviewer` (parameterized, 7 rubrics) | ✅ done |
| 4 worker sub-agents (research / analysis / synthesis / reviewer) | ✅ done |
| Orchestrator (`run-growth-tactics.md`) + standalone `run-enrichment.md` | ✅ done |
| All 12 skills pass `quick_validate.py` | ✅ done |
| Clean-room verified (nothing reads `tactics_DB/`) | ✅ done (grep + skill prohibitions) |
| End-to-end live run | ✅ v2.3.0 theona.ai re-test PASSED (2026-06-02): 8 tactics, 88% unconv, 100% white-space, 0 phantom, build reviewer 9, 85 min, think-tanks 0s-parallel |
| Git commit on `main` | ✅ v2.4.0 — Perplexity-optional (2026-06-02) |
| Per-run cost/latency measured | ✅ v2.3.0 theona (2026-06-02): ~85 min wall-clock (~75–80 clean); ~5 deep + ~51 search Perplexity calls ≈ $2–3 |
| Light-DB vs proprietary-DB moat comparison | ⬜ not started |
| Reviewer-model calibration (Gemini→Sonnet) | ⬜ open (carried) |
| Codex / OpenClaw ports | ✅ Codex full-DAG orchestrator built + A/B-validated (Round-7, `codex/orchestrate.py` + `checks.py` + `codex_dispatch.py`, codex-cli 0.136); OpenClaw port still deferred |

Legend: ✅ done · 🟡 built not verified · ⬜ not started.

## Measured cost & runtime (per-stage)

Point-in-time, measured end-to-end on **theona.ai** (v2.3.0, `--fast-intake`, 2026-06-02).
Aggregate: **~75–85 min** wall-clock (~75–80 clean; one synthesis socket-death respawn added
~8 min) and **~5 deep `perplexity_research` + ~51 `perplexity_search` ≈ $2–3** — or free on the
built-in WebSearch fallback. Overlapping stages share a start time:

| Stage | ~Time | Notes |
|-------|-------|-------|
| diagnostics intake | 8 min | URL research + prefill |
| enrichment: competitors (gate) | 15 min | the one reviewer-gated enrichment dim |
| enrichment: audience ‖ acquisition-tactics | 4 / 17 min | concurrent (Wave 2) |
| growth-factors mining | 10 min | concurrent — hidden under the critical path |
| think-tanks ×3 | 12 min | parallel, not 3× |
| lite-constraints | 4 min | |
| synthesis: explore → build | 12 + 7 min | +~8 min if a synthesis socket death respawns |

Treat as rough — one product, one run. `growth-factors.json` is cached (re-mined only on
`--remine`), so a `--from synthesis` re-run is minutes, not the full hour.

## What's in the package

**2 orchestrator commands** ([`commands/`](./commands/)):
- `run-growth-tactics.md` — the main entry; runs the full DAG in the main thread (intake →
  enrichment → think-tanks ‖ LIGHT-DB mining → lite-constraints → 4-step synthesis → STOP).
- `run-enrichment.md` — standalone enrichment-only entry, under the new namespace.

**12 skills** ([`skills/`](./skills/)) — passive instruction docs:

| Stage | Skills | Produces |
|-------|--------|----------|
| Diagnostics | `diagnostics-intake` | `01-diagnostics/founder-input.md` |
| Enrichment | `enrichment-{competitors,audience,acquisition-tactics}` | `02-enrichment/*.md` |
| Think-tank | `competitor-gaps`, `cross-industry`, `platform-arbitrage` | `03-think-tanks/demand-generation/<name>.md` |
| LIGHT DB | `growth-factors-mining` | `…/growth-factors.json` (20-40 clean-room vectors) |
| Constraints | `lite-constraints` | `…/synthesis-constraints.json` |
| Synthesis | `synthesis-explore` (blind combinations → emergent mechanisms) → `synthesis-build` (white-space → founder-fit → merge) | `…/synthesis.md` (7-9 tactics, STOP) |
| Review | `growth-reviewer` (+ 7 rubrics in `references/`) | JSON verdict |

**4 worker sub-agents** ([`agents/`](./agents/)) — thin runners:
- `research-worker` — web research (Perplexity + WebFetch): diagnostics URL mode, the
  enrichment research dims (competitors, acquisition-tactics), platform-arbitrage,
  growth-factors mining.
- `analysis-worker` — **no research MCP**: audience, competitor-gaps, cross-industry.
- `synthesis-worker` — **no MCP, clean-room; default opus** but model-tiered per dispatch
  (lite-constraints + `explore` → sonnet, `build` → opus): lite-constraints + the 2
  synthesis stages.
- `reviewer` — read-only; runs `growth-reviewer` and returns the verdict.

**2 manifests:** `plugin/.claude-plugin/plugin.json` (`name: diffmode-growth-tactics`) and
the repo-root `.claude-plugin/marketplace.json` (marketplace `diffmode-free`, `source: ./plugin`).

## How it gates

Filesystem state is the contract between stages. Each generating stage runs: dispatch worker
→ existence/structural check → (where it has a rubric) reviewer loop, score **≥ 7**, **max 3**
retries with blocking issues injected. **Reviewer-gated (v2.3.0): only** enrichment
`competitors` and the final `synthesis-build`. **Structural check only:** enrichment `audience`
+ `acquisition-tactics`, the 3 think-tanks, `growth-factors.json` (JSON + schema + counts +
clean-room; mined at Stage 1.5, collected at the Stage-3 boundary), `synthesis-constraints.json`
(schema + every ID exists in the LIGHT DB), and synthesis `explore` (required sections +
blind-draw ordering + verb-group validity). Wave 1 (competitors) and the LIGHT DB are blocking
gates for everything downstream.

## Key decisions

- **Plugin `diffmode-growth-tactics`, marketplace `diffmode-free`.** Command surface
  `/diffmode-growth-tactics:run-growth-tactics`; skills/workers namespaced
  `diffmode-growth-tactics:*`.
- **The moat is DB breadth + paid downstream — not the method.** The synthesis method is what
  this plugin demonstrates (free); the moat is the proprietary 576-vector DB (breadth) +
  intelligence layer + the paid prioritization + implementation stages. Free runs the method
  on a weaker per-run LIGHT DB and stops at synthesis.
- **Per-run clean-room LIGHT DB.** `growth-factors-mining` never reads `tactics_DB/`; it mines
  public case studies fresh each run (mechanism-over-tactic), caches `growth-factors.json`, and
  re-mines only on `--remine`. `lite-constraints` reasons in-context to emit the same
  `synthesis-constraints.json` shape the proprietary Python generator produced (white-space
  pairs, synergy / founder-fit pools, prohibited conventional patterns, category diversity,
  anti_patterns) — dropping the proprietary intelligence layer's internal pair-scoring
  (scaffolding, not a consumed field).
- **Synthesis: 4 IP-scrubbed steps, fused to 2 stages (v2.3.0).** `synthesis-explore` (Phase 1
  blind vector-first combinations → Phase 2 emergent mechanism derivation) → `synthesis-build`
  (Phase 1 white-space exploration → Phases 2-3 founder-fit merge → final). Proprietary vector
  IDs/examples were genericized to category-level patterns + the `{prefix}-NNN-slug` format;
  vector definitions come from `growth-factors.json`. The proprietary anti-vector-tracking read
  was dropped (uses the lite `anti_patterns`); no proprietary vector-validation post-step. The
  blind-draw → mechanism wall inside `explore` is the novelty engine and is independent of the
  removed intelligence layer.
- **Generalized workers (3→4).** Stage-neutral `research`/`analysis`/`synthesis`/`reviewer`;
  synthesis-worker is opus + no-MCP for reasoning-heavy clean-room synthesis.
- **One parameterized reviewer, 7 rubric files (2 used in v2.3.0).** 3 enrichment (SR-ENR) +
  3 think-tank + the demand-gen-synthesis rubric, bundled in `growth-reviewer/references/`,
  reached via `${CLAUDE_PLUGIN_ROOT}`. v2.3.0 dispatches only the `competitors` +
  `demand-gen-synthesis` rubrics; the other five are retained but unused (no churn). The
  synthesis rubric carries a clean-room note: score against the per-run LIGHT DB, and synthesis
  is the final stage (no Week-1 depth required).
- **Reviewer threshold ≥ 7, max 3 retries** — faithful to the pipeline's enrichment config.

## Open items / next steps

1. **Live end-to-end run** — `/diffmode-growth-tactics:run-growth-tactics --url <site>
   --scratch` on a known workspace (e.g. `theona.ai`); confirm `synthesis.md` has 7-9 tactics,
   ≥50% unconventional, each traceable to a `growth-factors.json` vector.
2. ✅ **Per-run cost/latency measured** (v2.3.0 theona, 2026-06-02): **~85 min** wall-clock
   (~75–80 clean; one synthesis socket-death respawn added ~8 min) and **~5 deep
   `perplexity_research` + ~51 `perplexity_search` ≈ $2–3** (deep-research-dominated;
   `growth-factors-mining` ran ~10 min concurrent, off the critical path). Caching + `--remine`
   behaved (the explore respawn did NOT re-mine growth-factors). See **Measured cost & runtime**
   above for the per-stage table.
3. **Moat comparison** — diff a light-DB synthesis vs a proprietary-DB run for the same
   workspace; confirm the free output is *useful but visibly weaker*.
4. **Reviewer-model calibration** — Gemini→Sonnet, same as the enrichment pilot; confirm
   Sonnet's scores land in range during the smoke-test.
5. **Commit on a branch** — everything under `pipeline-skills/` + repo-root `.claude-plugin/`
   is untracked on `main`.
6. **OpenClaw port** — still deferred. (The Codex full-DAG orchestrator is **built + A/B-validated**
   as of Round-7 — `codex/orchestrate.py`; OpenClaw is the remaining runtime port.)
7. **Cross-repo bundling** (optional) — bundle the channel menu + spec prompts so the plugin
   can run outside the ai-cmo tree.

## Where to read more

| Doc | What it covers |
|-----|----------------|
| [`README.md`](./README.md) | Onboarding: what it is, quickstart + install, what you get, how it works |
| [`../docs/pipeline-skills-design/architecture.md`](../docs/pipeline-skills-design/architecture.md) | Orchestration model, one-level-deep constraint, state contract (internal; not shipped in the plugin) |
| [`../docs/pipeline-skills-design/full-pipeline-map.md`](../docs/pipeline-skills-design/full-pipeline-map.md) | Original mapping of think-tank / prioritization / implementation stages (internal; not shipped) |
| [`../docs/MODULES.md`](../docs/MODULES.md) | The pipeline-skills module entry in the repo module map |
| [`../docs/CHANGELOG.md`](../docs/CHANGELOG.md) | The entry for this expansion |

> The design notes (now in `../docs/pipeline-skills-design/`, **not shipped in the plugin**)
> were written for the original enrichment pilot; **README.md + STATUS.md are the current
> source of truth** for the expanded `diffmode-growth-tactics` pipeline.
