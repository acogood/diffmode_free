# Architecture: orchestrator + skills + workers

The pattern, the four hard constraints, the state contract, and the portability seam.
Applies to the enrichment pilot (`enrichment-pilot.md`) and the full pipeline
(`full-pipeline-map.md`) alike.

## Three roles

| Role | Lives in | Active/passive | Owns |
|------|----------|----------------|------|
| **Orchestrator** | `commands/run-enrichment.md` (→ `.claude/commands/`) | active, **main thread** | the DAG, parallel dispatch, the reviewer-retry loop, stage-boundary existence checks |
| **Skills** | `skills/<name>/SKILL.md` (→ `.claude/skills/`) | **passive** | reusable domain logic (≈90% of each existing prompt); each also invocable standalone |
| **Worker sub-agents** | `agents/<name>.md` (→ `.claude/agents/`) | active, isolated context | load the named skill, read named inputs, write the named output, return `{status, outputPath, summary}` |

The workers are deliberately **thin and generic** — the intelligence is in the skills,
the control flow is in the orchestrator. A worker is just "load skill X, read files
Y, write file Z, report."

> **Packaged as a plugin.** The canonical install is the `diffmode-growth-tactics` Claude
> Code plugin: `.claude-plugin/plugin.json` makes Claude Code auto-discover `skills/`,
> `agents/`, and `commands/` at the plugin root. The `(→ .claude/…)` annotations below
> describe the *legacy* symlink layout (`install.sh`, now local-dev only). Under the plugin,
> skills and agents are **namespaced** `diffmode-growth-tactics:<name>`, and a worker "loads
> skill X" via the **Skill tool** (preloaded through its `skills:` frontmatter; the research
> worker invokes the dispatched dimension at runtime) — **not** by reading
> `.claude/skills/<name>/SKILL.md`. A sub-agent must not Read a sibling skill's file by
> hardcoded path; the reviewer worker reaches its bundled rubric via
> `${CLAUDE_PLUGIN_ROOT}/skills/growth-reviewer/references/`.

## The four hard constraints (these shape everything)

1. **The orchestrator runs in the main thread — never as a sub-agent.** Sub-agents are
   one level deep (`../../pipeline-skills/research/claude-code-skills-2026.md`); a sub-agent orchestrator
   could not spawn the research/reviewer workers. So the orchestrator is a slash
   command read and executed by the primary agent.
2. **Skills are passive.** The fan-out, the waiting, and the retry loop are performed
   by the orchestrator's Agent-tool calls — *not* "by the skill." Skills supply the
   *logic*; the orchestrator supplies the *control flow*.
3. **State passes through the filesystem** — the existing `ai-cmo-workspace/{product}/…`
   convention. Workers return only a small JSON summary + the output path, so the
   orchestrator's context stays lean even across a 5-output stage.
4. **The reviewer→retry quality gate is a main-thread loop.** On a failing review, the
   orchestrator **spawns a FRESH worker** with the reviewer's blocking issues injected into
   the brief. Workers are **stateless and not addressable after they return** — there is no
   "re-dispatch the same worker," and the orchestrator never `SendMessage`s a completed
   worker. Capped at 3 iterations — the repo's existing threshold-7 / max-3 norm
   (`workflow-config.yaml` `output_validation_config`).

## Control flow (one dimension)

```
orchestrator (main thread)
  │
  ├─ dispatch worker(skill=<dimension>, inputs=[…], output=<path>)   ──► writes <path>
  │     worker returns {status, outputPath, summary}
  │     three outcomes:
  │       ok                          → continue
  │       error{reason}               → surface reason, stop this branch
  │       died mid-run (no JSON)       → spawn a FRESH worker, up to 2×;
  │                                       still dead → fail clean (worker-dispatch-failed),
  │                                       print the --from/--only resume hint, NO main-thread fallback
  │
  ├─ existence check: <path> exists AND non-empty?  else spawn a fresh worker / abort
  │
  └─ reviewer loop (iter = 1..3):
        dispatch reviewer(rubric=<dimension>, spec=<path>, output=<path>)
        reviewer returns {score, pass/fail, blocking_issues[]}
        if score ≥ 7 and pass → done
        else if iter < 3 → spawn a FRESH worker with blocking_issues injected
                           (workers are stateless / not addressable after return —
                            never SendMessage a completed worker)
        else → mark dimension failed, surface to user, stop the dependent branch
```

This is structurally identical to `generate-pseo-cells.md`'s Stage 5 (generate) →
Stage 6/8 (validate/review) → Stage 7 (capped self-heal). We are not inventing a
pattern; we are reusing the proven one.

## State contract (worker return shape)

Every worker returns a small JSON object (printed as its final message), never the
file contents:

```json
{ "status": "ok",    "outputPath": "ai-cmo-workspace/<slug>/02-enrichment/<file>.md", "summary": "<1-2 lines: what was produced, counts>" }
{ "status": "error", "reason": "<what blocked it>" }
```

The reviewer returns:

```json
{ "score": 8, "verdict": "APPROVED", "format_compliance": "PASS", "blocking_issues": [], "confidence": "HIGH" }
{ "score": 5, "verdict": "REJECTED", "format_compliance": "PASS", "blocking_issues": ["…", "…"], "confidence": "HIGH" }
```

The orchestrator reads only these summaries to drive the DAG — it does not re-read the
big markdown outputs into its own context except when it must inject a path.

## Model-agnostic research seam

Skills describe a **capability** ("use the web-research backend; Perplexity when present,
else the built-in WebSearch fallback"), never a vendor. The concrete tool is chosen by the
**worker's `tools:` list**:

- Claude Code: `mcp__perplexity__perplexity_research` / `_search` **plus `WebSearch`** on the
  `research-worker` — it **prefers Perplexity when present and falls back to the built-in
  `WebSearch`** otherwise, with a Step-6 citation-integrity re-fetch on the fallback path that
  drops any non-resolving (NXDOMAIN / hard-404) cited URL (shipped in plugin **v2.4.0**).
- Codex: the custom agent declares the Perplexity MCP in `mcp_servers` (attached only if
  registered) and otherwise **falls back to the native `web_search` tool** (enabled per-dispatch
  with `-c web_search="live"`), with the **same citation-integrity re-fetch** on the fallback
  path. So Diffmode is now **Perplexity-optional on BOTH runtimes** (Claude → built-in
  `WebSearch`; Codex → native `web_search`), shipped 2026-06-02.

The **audience** dimension is the exception (ENR-001 forbids new web searches). It is
served by a dedicated **no-MCP worker** (`enrichment-analysis-worker`, `tools: [Read,
Write, Glob, Grep]`) so the no-search rule is **structurally enforced** — not merely
requested in prose.

## Deterministic checks replace Python `verify_outputs`

The CLI's Python `verify_outputs` (existence + non-empty + section presence) becomes
the orchestrator's **stage-boundary completeness check** — a Bash `test -s <path>` plus a
last-required-section grep (and a min-line floor for large stages). No Python needed. In the
free `diffmode-growth-tactics` pipeline the proprietary Python scripts the paid pipeline
shelled out to are **replaced by clean-room skills** (`lite-constraints` for the constraints
generator; in-context validation for the vector checks) — no proprietary script ships in the
plugin (`full-pipeline-map.md`).

## Portability seam (one-line summary)

**Share the skills (`SKILL.md`), re-author the orchestrator per runtime.** The skills
are the portable asset; the DAG/fan-out/retry control flow is runtime-specific
(`../../pipeline-skills/research/sources.md` → "the portability headline").
