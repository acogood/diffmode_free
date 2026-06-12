---
description: Build your growth plan — researches your market and builds 7–9 unconventional tactics (~1.5h, free). Type /diffmode-growth-tactics:start your-site.com
---

# Start — build your growth plan

Main-thread orchestrator for the **Diffmode free growth-ideation pipeline** — from a fast
founder intake all the way to a final `synthesis.md` of **7-9 novel demand-gen tactic
IDEAS**, and it **STOPS there**. (A best-effort packaging stage then re-writes `synthesis.md`
as the founder-facing `growth-tactics.md` — same tactics, plain language, no new content.)
Prioritization, implementation guides, and the proprietary 576-vector database are the paid
product; this command never attempts them.

It runs the workflow as skills + worker sub-agents. It owns the DAG, the parallel fan-out,
the reviewer-retry quality gate, and the stage-boundary checks, and supersedes
`run-enrichment.md` (which remains a standalone entry for running enrichment alone — an
advanced/testing tool, not advertised to founders).

> **This command runs in the main thread.** It dispatches worker sub-agents via the
> Agent/Task tool, and it is the only place that may talk to the human (via AskUserQuestion,
> for intake). It must NOT itself be run as a sub-agent — sub-agents are one level deep and
> could not then spawn the workers. (See the repo's `docs/architecture.md` — internal design
> notes, not shipped in the plugin.)

> **Naming under the plugin.** Ships in the `diffmode-growth-tactics` plugin; invoked as
> `/diffmode-growth-tactics:start`. Use these exact plugin-namespaced ids in
> Agent-tool dispatches:
> - skills: `diffmode-growth-tactics:diagnostics-intake`,
>   `diffmode-growth-tactics:enrichment-<dimension>`,
>   `diffmode-growth-tactics:competitor-gaps` · `:cross-industry` · `:platform-arbitrage`,
>   `diffmode-growth-tactics:growth-factors-mining`, `diffmode-growth-tactics:lite-constraints`,
>   `diffmode-growth-tactics:synthesis-explore` · `:synthesis-build`,
>   `diffmode-growth-tactics:founder-report`
> - workers: `diffmode-growth-tactics:research-worker`,
>   `diffmode-growth-tactics:analysis-worker`, `diffmode-growth-tactics:synthesis-worker`,
>   `diffmode-growth-tactics:reviewer`
> The plugin is **self-contained**: it reads its bundled channel menu from
> `${CLAUDE_PLUGIN_ROOT}/reference/` and writes all run outputs to a `./<slug>/` workspace in
> the user's current directory. No host repo is required.

## Step 0a — Welcome (print BEFORE any tool call)

The very FIRST thing this command does — before pre-flight, before any Bash/Read/Agent
call — is print this welcome so the founder knows what's about to happen, how long it
takes, and what they get back. Print it verbatim. **Markdown only** — headers, bold,
lists, `---` rules; NO ASCII art, NO ANSI codes (rendering is terminal-dependent;
markdown renders reliably).

> # Diffmode — let's build your growth plan
>
> Here's what happens next:
>
> 1. **A few quick questions** (~2 minutes) — the things your website can't tell us.
> 2. **Hands-off research** (~60–90 minutes) — we study your competitors, your buyers,
>    and what's already working in your market. You can walk away.
> 3. **Your growth tactics** — 7–9 specific ways to get users, built for your budget,
>    team, and stage.
>
> **What you'll have at the end:**
>
> - **Your Growth Tactics** — the main event: each tactic with first steps and an
>   early signal to watch.
> - **3 research briefs** — Competitor Research, an Audience Map, and an Acquisition
>   Audit. Reusable on their own.
> - **3 strategy reports** — where your size wins, plays from other industries, and
>   fresh platform openings.
> - **Working papers** — the notes behind the work, yours to keep.
>
> **Total: usually 1–1.5 hours.** You only need to be here for the questions at the
> start; results open in your browser at the end.

(Fill in nothing; the block is static, and it always prints in full — auto-resume
detection needs tool calls, so it happens after (Pre-flight step 1). When the founder
picks **Continue** there, follow the choice with one short line: what's already done +
the time estimate for the remaining stages.)

## User-facing voice (applies to EVERYTHING you print during the run)

The founder is a marketer or a busy founder, not a developer. The routines below define
what to DO; this section defines what to SAY. When they differ about what to print,
this section wins.

- **Stage start = ONE plain line with an ETA.** Stage done = ONE line with a human
  metric. Suggested lines (vary naturally, keep the shape):

  | Stage | Start line | Done line |
  |-------|-----------|-----------|
  | diagnostics | "Looking at your site and getting set up (~3 min)…" | "✓ Got your product brief" |
  | enrichment competitors | "🔍 Researching your competitors (~15–20 min)…" | "✓ Competitor research done — 9 competitors mapped" |
  | enrichment wave 2 | "🔍 Mapping your buyers + auditing what works in your market (~15–20 min)…" | "✓ Buyer map + acquisition audit done" |
  | growth-factors | "⛏️ Mining growth mechanisms from public case studies (runs in the background, ~40 min)…" | "✓ 27 growth mechanisms mined" |
  | think-tanks | "🔭 Working three strategy angles in parallel (~15–25 min)…" | "✓ 3 strategy reports done" |
  | lite-constraints | "Setting up the tactic builder (~3 min)…" | (fold into the next start line) |
  | synthesis | "🧪 Building your tactics (~25–35 min)…" | "✓ 8 tactics built — passed the quality check" |
  | founder-report | "📦 Packaging your report (~3 min)…" | "✓ Your Growth Tactics ready to read" |

- **NEVER narrate to the founder:** structural-check internals, run-ledger writes or
  any JSON, reviewer scores/verdicts/rubric mechanics, vector counts-as-plumbing
  (`must_include`, pools, anchors, IDs), retry/respawn logistics, worker lifecycle, or
  model tiering. All of that detail still goes into `WS/.run-state.json` exactly as the
  routines specify — the ledger is unchanged; only the narration is quiet.
- **On a gate retry print exactly one line:** "Quality check asked for one fix —
  re-running, a few extra minutes." (Same shape for a structural re-dispatch.)
- **Pre-flight is silent unless something fails.** At most one line: "✓ Setup checks
  passed". The WebSearch-fallback notice (pre-flight step 5) stays — it's one line and
  the founder should know research runs on the built-in search.
- Stage *failures* are the exception: report them plainly with the resume command, as
  the failure-modes table specifies.

## Arguments

`$ARGUMENTS` is free-form — founders never need a flag:

- **A URL or domain** (`theona.ai`, `https://theona.ai` — anything that looks like a
  host, scheme optional) → **URL mode**: research the website to prefill diagnostics.
  The workspace slug is derived from the host (`theona.ai`).
- **Bare word(s), no domain shape** (e.g. `my-product`) → a workspace/product name:
  names the workspace at `./<name>/` and runs the **no-website Q&A intake** (product
  one-liner, business model, audience are asked in Stage 0).
- **Empty** → ask, AFTER the welcome block (and only when the auto-resume scan in
  Pre-flight step 1 didn't already resolve a workspace), via `AskUserQuestion`:
  *"What's your product's website?"* — options **[type it via "Other"]** /
  **[I don't have a site yet]**. The second option asks for the product name instead
  and proceeds in no-website Q&A mode.
- `--fast` — the only flag. In URL mode, skip the founder Q&A and accept the researched
  prefill with `[NEEDS FOUNDER INPUT]` placeholders left in (useful for demos; quality
  is lower). **Auto-enabled on non-interactive runs** (headless `-p` mode — never hang
  on a question nobody can answer).

**Legacy tolerance** (older docs / muscle memory — never an error dump): `--url X` and
`--product X` are understood as their positional equivalents; `--fast-intake` means
`--fast`. If `--from`, `--only`, `--remine`, or `--scratch` appear, print ONE polite
line — *"this version resumes automatically — just run the command again"* — and
otherwise ignore them (auto-resume replaces `--from`/`--only`; **Start fresh** replaces
`--remine`; scratch-dir dry-runs are no longer a launch option).

**Stage names** (internal — used in the run-ledger and failure rows; the founder never
types them): `diagnostics`, `enrichment`, `think-tanks`, `growth-factors`,
`lite-constraints`, `synthesis` (or finer synthesis steps `explore`, `build`),
`founder-report`.

## Pre-flight

1. **Auto-resume scan (FIRST — before resolving a new workspace or asking the website
   question).** Scan the current directory for existing workspaces: any `*/.run-state.json`.
   A workspace is an **unfinished run** when its ledger exists but the final `synthesis`
   stage has no APPROVED row, **or** synthesis has an APPROVED row but `growth-tactics.md`
   is missing — stopped during packaging (a recorded `founder-report-skipped` row counts as
   done; the skip was deliberate). When the ledger and the on-disk outputs disagree, trust
   the on-disk outputs — the existing rule. Then:
   - the typed URL/name resolves to a workspace with an unfinished run, **or** the command
     was run bare and exactly ONE unfinished run exists → `AskUserQuestion`: *"Found an
     unfinished run for `<slug>` (stopped at: <human stage name>). Continue where it left
     off, or start fresh?"* **[Continue / Start fresh]**. Use the plain stage descriptions
     from the *User-facing voice* table for `<human stage name>` (e.g. "researching your
     competitors"), never internal codes.
   - bare command + MULTIPLE unfinished runs → one `AskUserQuestion` listing each
     `<slug> (stopped at: …)` as a Continue option, plus a **"Start a new run"** option.
   - no unfinished run (or the founder picked "Start a new run") → fresh launch; continue
     with step 2.

   **Continue** → derive the resume point from the ledger + the on-disk stage outputs:
   read the ledger FIRST, then confirm each "done" stage's output actually passes its
   completeness check (a stage whose output is missing, truncated, or stale — e.g. the
   Stage-4 `constraints-stale` mismatch — does NOT count as done). Re-enter the DAG at the
   first stage that isn't done. The per-stage routine, completeness checks, and ledger
   rules below are unchanged; the cached `growth-factors.json` is reused as always.

   **Start fresh** → a full re-run of every stage **including re-mining**: discard the
   cached `growth-factors.json` and set `remine: true` on the mining brief (fresh means
   fresh). Only Start fresh re-mines; Continue and within-run retries keep reusing the
   cache.
2. **Resolve the workspace** — `WS = ./<slug>` under the user's **current working directory**
   (slug from the positional argument — a bare name, or derived from the URL/domain host,
   e.g. `theona.ai` — or from the website-question answer). Create
   `WS/01-diagnostics`, `WS/02-enrichment`, `WS/03-think-tanks/demand-generation` as needed.
   **No host repo is required** — the plugin
   is self-contained and writes the run into the cwd.
3. **Confirm the channel menu** — `${CLAUDE_PLUGIN_ROOT}/reference/Marketing-Channel-Menu-2026.md`
   exists (it is bundled in the plugin; `${CLAUDE_PLUGIN_ROOT}` expands to the plugin's
   install directory at runtime). All stages that need the channel taxonomy read it from
   there.
4. **Confirm the plugin is active** — its skills/agents (`diffmode-growth-tactics:*`) exist
   whenever the plugin is enabled. If a dispatch reports an unknown agent/skill, the plugin
   isn't enabled — run `/plugin` → enable `diffmode-growth-tactics` (or
   `claude plugin install diffmode-growth-tactics@diffmode-free`).
5. **Detect the research backend (capability note — no hard gate).** Check whether a
   Perplexity MCP server is available (the `mcp__perplexity__*` tools resolve). If it is, the
   research stages use it. **If no Perplexity MCP is detected, print one line —** *"WebSearch
   fallback mode — no Perplexity MCP detected; research quality slightly lower, citations
   auto-verified."* **— and proceed.** There is no hard gate: the `research-worker` falls back
   to the built-in `WebSearch` (see its Step 3 + its Step-6 citation-integrity check), so the
   pipeline runs either way. Only the genuine absence of *both* backends is a research failure.
6. **Reviewer gate** — score **≥ 7**, **max 3** iterations, applied at the **two gated stages
   only**: enrichment **`competitors`** (the Wave-1 blocker) and the **final synthesis
   deliverable** (`synthesis.md`). Every other generating stage gets a **structural check
   only** — see *The per-stage routine*. (v2.3.0 cut the gates from 7 → 2: the dropped gates
   added latency, tokens, and retry risk without moving the outcome in the field.)

## The DAG

```
Stage 0    diagnostics-intake        → WS/01-diagnostics/founder-input.md
Stage 1    enrichment (2 waves)      → WS/02-enrichment/*.md
              Wave 1 (reviewer gate):           competitors
              Wave 2 (‖, structural check only): audience ‖ acquisition-tactics
Stage 1.5  growth-factors mining     → …/growth-factors.json  (LIGHT DB)
              ↑ starts right after Wave-1 competitors is APPROVED and runs
                CONCURRENTLY through the rest of enrichment + Stage 2; structural
                check only (no reviewer gate); collected/validated at the Stage-3 boundary.
Stage 2    think-tank ×3             (parallel, after enrichment; structural check only — no reviewer gate)
              competitor-gaps · cross-industry · platform-arbitrage
Stage 3    lite-constraints          → WS/03-think-tanks/demand-generation/synthesis-constraints.json
              precondition: growth-factors.json present + valid
Stage 4    synthesis  explore → build   → synthesis.md   (the last gated stage — STOP generating here)
Stage 5    founder-report (best-effort)  → growth-tactics.md   (packages synthesis.md for the founder; never blocks)
```

Filesystem state is the contract between stages (same pattern as the enrichment pilot).
**`growth-factors-mining` is deliberately hoisted to Stage 1.5** — it strictly needs only
`founder-input.md` (its enrichment inputs are optional search seeds), so overlapping it with
enrichment + the think-tanks takes its ~40-min runtime off the critical path.

## The per-stage routine (generate → check → reviewer loop)

For each generating stage `S` with worker `W`, output `O`, and (where it has one) rubric
dimension `D` + spec `Spec`:

1. **Dispatch the worker** — Agent tool, `subagent_type = W`, with a self-contained brief:
   ```
   skill:   diffmode-growth-tactics:<skill>
   inputs:  [ …paths… ]
   output:  <O>
   blocking_issues: <none on first pass; reviewer items verbatim on a retry>
   ```
   The worker loads the skill, reads inputs, (researches/reasons), writes `O`, returns
   `{status, outputPath, summary}`. **Capture wall-clock:** before dispatching, run `date +%s`
   (you have Bash) and remember it as the stage's `started_at`; after the attempt resolves,
   run `date +%s` again and compute `duration_s = end − start`. **After every attempt** (this
   one and each retry below), append a row to the run-ledger (`WS/.run-state.json`):
   `{stage, attempt, verdict, score, started_at, duration_s}` — see *Run-ledger* near the end
   of this file. (Timing is additive instrumentation: never block a stage on it.)

   > **Worker lifecycle (read this — it prevents two bugs).** Workers are **stateless and
   > NOT addressable after they return.** Every retry (for ANY reason — gap, reviewer
   > rejection, or a dispatch failure) **spawns a FRESH worker** with the same brief plus any
   > injected `blocking_issues`. **Never `SendMessage` a worker that has already returned** —
   > there is no "re-dispatch the same worker." (The single-shot pattern: "retry that single
   > agent ONCE" via a fresh spawn.) This keeps the architecture reproducible: no main-thread
   > content fallback.

   **Three dispatch outcomes** (handle each):
   - **`ok`** → go to step 2.
   - **`error`** (worker returned `{status:"error", reason}`) → surface `reason` and stop
     this branch (the input it named must be fixed).
   - **dispatch failed / worker died mid-run** (API/socket error, no JSON returned at all) →
     **re-spawn a FRESH worker** with the identical brief, up to **2×** (transient socket
     deaths usually clear on a fresh spawn). If it still dies after 2 fresh spawns, mark `S`
     FAILED with code **`worker-dispatch-failed`** and tell the founder: *"run
     `/diffmode-growth-tactics:start` again — it picks up from this point"* (the auto-resume
     pre-flight resumes cheaply from what's already on disk). Do NOT
     do the worker's content work in the main thread.
2. **Stage-boundary completeness check** (replaces Python `verify_outputs`): confirm `O`
   exists and is non-empty (`test -s`), AND — critically — that it is **not truncated**.
   `test -s` + a first-header grep both pass on a file that died mid-write, so for markdown
   stages require the stage's **LAST** required section to be present (a worker that crashed
   mid-write won't have reached it), plus a sane **min-line floor** for the large stages.
   For JSON stages: parses + has the required keys + expected counts. Per-stage anchors:

   | Stage | Last-required-section anchor | Min-line floor |
   |-------|------------------------------|----------------|
   | explore (`synthesis-explore.md`) | `## Validated Mechanisms` (the completeness anchor; `## Blind Draw (IDs only)` must precede `## Vector Combinations`; ends with `## Action Deduplication Result`) | ~120 |
   | build (`synthesis.md`) | `## Post-Synthesis Self-Review` | ~150 |
   | enrichment / think-tank `.md` | the skill's final section | per skill |

   If the worker returned `ok` but `O` is missing / empty / **lacks its last-required section
   or falls under the floor** (i.e. truncated — a mid-write death), treat it like a dead
   worker: **spawn a fresh worker** once noting the gap (a full regenerate, since a truncated
   file has no sections to `Edit` onto).
3. **Reviewer loop** (only for stages with a rubric — see table): dispatch
   `diffmode-growth-tactics:reviewer` with `{dimension: D, spec_path: Spec, output_path: O,
   context_paths: […upstream…]}`; read the JSON verdict. If `APPROVED` (score ≥7, format
   PASS) → done. If `REJECTED` and `iter < 3` → **spawn a FRESH worker** `W` with the same
   brief plus `blocking_issues` injected verbatim; re-check; `iter++`. If `REJECTED` at
   `iter = 3` → mark `S` FAILED, record blocking_issues, stop dependents.

   > **Smaller-retry rule (format-only fixes on a large existing file).** When the rejection
   > is **format-only** (missing sections, missing checklist) and `O` already exists and is
   > large, the re-dispatch brief MUST set `retry_mode: format-only` and instruct the fresh
   > worker: **"use the `Edit` tool to ADD the missing sections in place; do NOT
   > Read-then-Write the whole file."** The three writing workers now carry the `Edit` tool,
   > so this is a real, small in-place patch — not a full regenerate. (A full rewrite of a
   > ~900-line file is what repeatedly hit socket deaths in the field; a targeted `Edit` is
   > far smaller and safer.) Fail-clean is unchanged: a worker that dies twice is still
   > `worker-dispatch-failed` with a resume hint — **the orchestrator never does the worker's
   > content work in the main thread, including never patching `O` itself.**

Stages **without** a reviewer gate — growth-factors, lite-constraints, the synthesis
intermediate step(s), enrichment `audience` + `acquisition-tactics`, and all 3 think-tanks —
get a **structural check only** (step 2); see each stage below. Only **two** stages are
reviewer-gated: enrichment **`competitors`** (the Wave-1 blocker) and the **final synthesis
deliverable** (`synthesis.md`).

## Stage 0 — Diagnostics intake (the entry point)

Goal: produce `WS/01-diagnostics/founder-input.md`. If it already exists and an
auto-resume **Continue** put the resume point past `diagnostics`, skip. **Human
interaction happens HERE, in the main thread.**

**Collect the must-ask fields** (the things a website can't reveal) via `AskUserQuestion`.
Recommended batching (≤4 questions/call; founders pick "Other" to free-type):

- *Call 1 (structured):* **Stage** [pre-launch / early / traction / growth]; **Monthly
  marketing budget** [$0 / under $500 / $500-2k / $2k+]; **Biggest growth problem** [Not
  enough traffic (demand gen) / Traffic doesn't convert (CRO) / Both]; **Skills you can do**
  (multiSelect) [landing pages / content / ad campaigns / analytics].
- *Call 2 (free-form, founders use "Other"):* **Current traction** (visitors/signups/MRR/
  paying customers — or "pre-launch"); **Primary goal + deadline**; **Where users/traffic
  come from today** (the Q8 acquisition signal); and — **only in no-website Q&A mode** —
  **product one-liner + business model/pricing + target-audience hypothesis**.

(Skip Call 2 / accept placeholders if `--fast`.)

Then dispatch **`research-worker`** with skill `diffmode-growth-tactics:diagnostics-intake`:
- URL mode: pass the site URL + the collected `answers`. The worker scrapes homepage/
  pricing/about + a research-backend pass (Perplexity if present, else WebSearch) to fill
  researchable fields, folds in `answers`, marks
  any remaining gaps, writes `founder-input.md`.
- No-website Q&A mode: pass the `answers` (incl. product/model/audience). The worker formats them
  into the schema (light research allowed to enrich product description + competitive
  alternatives), writes `founder-input.md`.

**Check:** `founder-input.md` exists, non-empty, has the 7 `## N.` sections (grep
`## 1. Product`, `## 4. Challenge Separation`, `## 5. Resources`, `## 7. Module Routing`).
If a `## Confirmation Gaps` block lists must-ask fields and not `--fast`, ask the
founder those specific gaps (one more `AskUserQuestion`) and patch the file in the main
thread. No reviewer rubric for diagnostics (it's capture, not analysis).

## Stage 1 — Enrichment (2 waves)

Run the enrichment DAG exactly as `run-enrichment.md` specifies (that file is the detailed
reference and the standalone entry). Compactly:

```
Wave 1 (blocking reviewer gate):  competitors
Wave 2 (parallel, structural check only):  audience  ‖  acquisition-tactics   (depend on competitors)
```

Per-dimension wiring (worker · inputs · gate):

| Dim | Worker | Inputs | Gate |
|-----|--------|--------|------|
| competitors | research-worker | founder-input; channel menu | **reviewer-gated** — spec `${CLAUDE_PLUGIN_ROOT}/skills/enrichment-competitors/SKILL.md`, rubric dim `competitors` |
| audience | **analysis-worker** (no MCP) | founder-input; competitors-analysis; channel menu | structural check only (no reviewer) |
| acquisition-tactics | research-worker | founder-input; competitors-analysis; channel menu | structural check only (no reviewer) |

Skills: `diffmode-growth-tactics:enrichment-<dim>`. Outputs in `OUT = WS/02-enrichment/`:
`competitors-analysis.md`, `audience-jtbd.md`, `acquisition-tactics.md`. **Only `competitors`
is reviewer-gated** (the Wave-1 blocker); `audience` + `acquisition-tactics` get a structural
completeness check only — confirm required sections present per `run-enrichment.md` step 2,
re-dispatch once on a gap (their outputs proved reliable enough in the field that a reviewer
gate added latency + retry risk without changing the result). **Wave 1 is a blocking gate** —
if `competitors` FAILS, abort (the rest of enrichment, Stage 1.5 mining, the think-tanks, and
all synthesis depend on `competitors-analysis.md`). (`acquisition-tactics` is a leaf within
enrichment, but its output feeds the think-tanks, so let it complete.)

> **Kick off Stage 1.5 the moment `competitors` is APPROVED** — see the next section. The
> mining branch runs concurrently with Wave 2 and Stage 2; do not wait for the rest of
> enrichment before starting it.

## Stage 1.5 — Start growth-factors mining (overlaps enrichment + Stage 2)

The slowest single stage (~40 min) is `growth-factors-mining`. Its enrichment inputs are
**optional search seeds** — per its own skill it strictly needs only `founder-input.md` — so
hoist it out of the Stage-2 fan-out and **start it the moment Wave-1 `competitors` is
APPROVED**, then let it run concurrently through Wave 2, Stage 2, and the think-tank reviewer
loops. It is **structural-check-only** (no reviewer gate), so it does not block anything until
the Stage-3 boundary, where it is collected and validated.

**Dispatch** (a single Agent call, fired right after the competitors gate; do NOT await it
before moving on to Wave 2 / Stage 2):

| Stage | Worker | Skill | Inputs | Output |
|-------|--------|-------|--------|--------|
| growth-factors | **research-worker** | `:growth-factors-mining` | founder-input (required); competitors-analysis (seed, ready after Wave 1); acquisition-tactics (optional seed — pass it if Wave 2 has produced it, otherwise omit) | `WS/03-think-tanks/demand-generation/growth-factors.json` |

- On a **Start-fresh** relaunch (pre-flight step 1), set `remine: true` in the brief — the
  worker discards the cached `growth-factors.json` and re-researches. Otherwise the skill's
  **cache rule is unchanged**: if `growth-factors.json` already exists and the brief does
  NOT set `remine`, the worker reuses it.
- **Socket-death respawn = retry-in-place, NOT re-mine (cost fix).** This stage's deep-research
  passes are the priciest in the pipeline, and a mid-mine socket death used to make the fresh
  respawn re-run them all from scratch (≈8 duplicated research-backend calls, Perplexity if
  present else WebSearch — the single biggest
  avoidable cost in the field). So whenever you re-spawn a **dead** growth-factors worker (per
  the worker-lifecycle rule / the Stage-3-boundary `died` path) **and a partial
  `growth-factors.json` already exists at the output path**, set **`resume_partial: true`** in
  the respawn brief. The fresh worker then reads the partial file, KEEPS the vectors already
  distilled, and mines only the remainder to reach the target count — it does NOT re-run the
  deep-research passes already paid for. **Never combine `resume_partial` with `remine: true`**:
  `remine` means "discard the cache and re-research from scratch" (the opposite intent), so a
  respawn under `remine: true` re-mines fresh and ignores any partial file.
- Record the long-running branch in the run-ledger as `growth-factors` (one row when dispatched,
  one when it resolves, with `started_at`/`duration_s`).
- The `acquisition-tactics.md` seed is "optional but recommended" — if mining is dispatched
  before Wave 2 finishes it simply won't have that seed yet, which the skill explicitly allows.

**Collection happens at the Stage-3 boundary** (see Stage 3) — the orchestrator runs the
growth-factors structural + clean-room check there, NOT here. This stage just launches the
branch and keeps a handle on it.

## Stage 2 — Think-tank research (parallel, structural check only)

After enrichment outputs exist, **dispatch all three think-tanks in a SINGLE message
containing exactly three Agent tool calls** so they run concurrently (alongside the
still-running Stage-1.5 mining branch). **Order them platform-arbitrage → competitor-gaps →
cross-industry within that one message:** `platform-arbitrage` is the slowest branch and the
only one that needs a research backend (Perplexity if present, else WebSearch; it runs on
`research-worker`), so launching it first lets the
two no-MCP analysis branches finish under its cover. **Do NOT split them across messages** —
separate messages serialize the batch (the field bug that cost ~18 min); "single message,
exactly three Agent calls" is load-bearing, and with the per-branch reviewer loops removed
(below) the batch now resolves on its **slowest branch**, not the sum.

| Stage | Worker | Skill | Inputs | Output |
|-------|--------|-------|--------|--------|
| platform-arbitrage | **research-worker** | `:platform-arbitrage` | founder-input; competitors-analysis; **audience-jtbd**; acquisition-tactics; channel menu | `…/platform-arbitrage.md` |
| competitor-gaps | analysis-worker | `:competitor-gaps` | founder-input; competitors-analysis; audience-jtbd; acquisition-tactics; channel menu | `…/competitor-gaps.md` |
| cross-industry | analysis-worker | `:cross-industry` | founder-input; competitors-analysis; audience-jtbd; acquisition-tactics | `…/cross-industry.md` |

(`…` = `WS/03-think-tanks/demand-generation/`.) **Input fix:** `platform-arbitrage` now
declares **`audience-jtbd`** — its `SKILL.md` lists it as a required input ("use to judge
audience fit for each platform/feature"), and the old orchestrator row omitted it.

**No reviewer gate (v2.3.0).** The 3 think-tanks are **structural-check-only** — there is no
reviewer dispatch for them anymore. They are exploration outputs that the synthesis chain
reads as context; a reviewer gate added latency + retry risk without changing the synthesis
result in the field.

**Concurrent-partial resolution (the 3-way fan-out).** The three are dispatched in one message
and return independently, so handle them as a batch: **after the batch returns, run each
branch's structural completeness check** (step 2 — confirm the skill's required sections are
present per its `SKILL.md`: `platform-arbitrage` carries its feature-recency findings with
cited sources, `competitor-gaps` its Tier-1/2/3 gaps, `cross-industry` its case studies +
transferable patterns) and classify + record each in the run-ledger:

- **`ok`** (structural check passes) → resolved.
- **`incomplete`** (worker returned ok but the output is missing a required section or
  truncated) → **regenerate ONCE** with a fresh worker noting the specific gap → resolves to
  ok or `failed`.
- **`died`** (dispatch failed / no JSON) → re-spawn a FRESH worker up to 2× per the worker
  lifecycle rule → resolves to ok or `worker-dispatch-failed`.
- **`failed`** (still incomplete after the single regenerate, or still dead after 2 respawns)
  → record FAILED.

**Gate Stage 3 on all three think-tanks RESOLVED + `ok`**: a failed think-tank **blocks
synthesis** (the synthesis chain reads all three think-tank reports). If any think-tank ends
`failed`, stop before Stage 3, surface its gap, and tell the founder to run
`/diffmode-growth-tactics:start` again — it picks up from this point (only what's missing
re-runs). The Stage-1.5 `growth-factors` branch is gated separately,
at the Stage-3 boundary below.

## Stage 3 — Lite constraints

**Stage-3 boundary precondition — collect + validate the Stage-1.5 mining branch (BLOCKING).**
Before dispatching `lite-constraints`, the `growth-factors` branch launched in Stage 1.5 must
have RESOLVED and passed its check. Classify it like any concurrent branch (record in the
run-ledger): `ok` if it passes the check below; `died` → re-spawn a FRESH worker up to 2×
(carry **`resume_partial: true`** when a partial `growth-factors.json` is on disk and this
is NOT a Start-fresh re-mine, so the respawn resumes mining the remainder instead of re-paying for
the deep-research passes — see Stage 1.5); `failed` → still bad after 2 respawns. A failed
`growth-factors.json` **blocks everything**
(synthesis needs the LIGHT DB → the constraints), so on `failed`, stop here, surface
`blocking_issues`, and tell the founder to run `/diffmode-growth-tactics:start` again — it
picks up from this point (Continue retries mining from what's on disk; **Start fresh**
re-mines from scratch).

**growth-factors.json check** (no rubric → **structural + clean-room check only**): it parses
as JSON; `metadata.total_vectors` matches `vectors.length` and is **15-40**; `category_counts`
sums to total and no prefix > ~60%; every vector has `vector_id` (matching `{prefix}-NNN-slug`),
`category`, `mechanism`, `transferability`, `saturation_risk`, `examples`, and a real
`source_url`. **Clean-room spot-check:** confirm the worker did not read `tactics_DB/` (its
summary should say so; the schema requires real source URLs). If the check fails and the
worker returned ok, re-dispatch once with the specific gap; max 2 attempts.

**Then dispatch lite-constraints.** Worker **`synthesis-worker`** with a **per-dispatch model
override** (see Stage 4's *Model tiering* note):

| Step | Worker | Model | Skill | Inputs | Output |
|------|--------|-------|-------|--------|--------|
| lite-constraints | synthesis-worker | **sonnet** | `:lite-constraints` | growth-factors.json; founder-input.md | `WS/03-think-tanks/demand-generation/synthesis-constraints.json` |

`lite-constraints` is a deterministic JSON build from the LIGHT DB, so dispatch it with
`model: sonnet` (the Agent/Task tool's `model` param overrides the worker's `opus` default).

**Structural check only** (no rubric): parses as JSON; has `diverse_white_space` (≥5 pairs),
`mandatory_combinations` (pools A/B/C present), `prohibited_combinations` (the 5 generic
conventional patterns), `anti_patterns`, and `category_diversity_requirements`
(`max_single_category_pct: 60`). **Every vector ID referenced must exist in
`growth-factors.json`** (cheap cross-check of a sample of ids). Re-dispatch once on failure.

## Stage 4 — Synthesis chain (explore → build)

**ID-consistency precheck (BLOCKING — run BEFORE explore).** `synthesis-constraints.json` is
built against a specific `growth-factors.json`. If the LIGHT DB was re-mined (a Start-fresh
relaunch) without rebuilding constraints — e.g. a resume that re-entered the DAG past Stage 3
— the on-disk constraints reference vector IDs that no longer exist, and synthesis would
emit broken traceability silently. So before dispatching explore: collect every vector ID
referenced anywhere in `synthesis-constraints.json` (`diverse_white_space`,
`mandatory_combinations`, `prohibited_combinations.vectors_if_present`,
`unconventional_anchors`) and confirm **each one exists in the CURRENT `growth-factors.json`**.
On ANY mismatch, do NOT proceed to explore with stale constraints: record
**`constraints-stale`** in the ledger and **re-run Stage 3 (`lite-constraints`) first** to
rebuild `synthesis-constraints.json` against the current LIGHT DB — within this run when
possible (it is a cheap sonnet stage); if the run is stopping anyway, tell the founder to
run `/diffmode-growth-tactics:start` again — the auto-resume treats stale constraints as
not-done and re-enters at lite-constraints.

Both on **`synthesis-worker`** (no MCP, clean-room), sequentially — but **model-tiered**
(see the *Model tiering* note below the table):

| Step | Model | Skill | Inputs | Output | Gate |
|------|-------|-------|--------|--------|------|
| explore | **sonnet** | `:synthesis-explore` | founder-input; growth-factors.json; synthesis-constraints.json; audience-jtbd; the 3 think-tank reports | `…/synthesis-explore.md` | structural |
| build | **opus** | `:synthesis-build` | synthesis-explore.md; synthesis-constraints.json; growth-factors.json; founder-input; audience-jtbd; competitors-analysis; competitor-gaps; cross-industry; platform-arbitrage; channel menu | `…/synthesis.md` | **reviewer-gated** |

> **Model tiering (cost/latency tuning, no quality change expected).** The mechanical
> blind-draw + mechanism-derivation stage — `explore` (its Phase 1 draws blind vector
> combinations + runs the strip test; its Phase 2 writes the 3-step mechanism prototypes +
> conventional-detection gate), plus `lite-constraints` (Stage 3) — runs on **sonnet**; the
> creative/novelty engine + final reviewer-gated deliverable — `build` (its Phase 1 ideates
> white-space tactics, Phases 2-3 do founder-fit adaptation + merge) — stays on **opus**. Pass
> the tier with a **per-dispatch `model` override** on the Agent/Task call (e.g. `model: sonnet`
> for explore) — that param takes precedence over `synthesis-worker`'s `opus` frontmatter
> default, so no extra worker file is needed. **`explore` is the riskier downgrade** (its
> Phase-2 mechanism-novelty work was the highest-risk part of the old chain): if a run's
> strip-test pass-rate or unconventional ratio visibly drops, revert just `explore` to `opus`
> (one-line change), or re-split `explore` back into the two former synthesis skills it fused
> (recover them from git history / `docs/STATUS.md` — the documented partial-revert path).
> *(Fallback if a runtime ever ignores the per-dispatch override: add a 5th worker
> `agents/synthesis-fast-worker.md` — `model: sonnet`, same tools + clean-room rule — and route
> lite-constraints/explore to it instead.)*

**Structural check for `explore`:** file exists, non-empty, not truncated, with a min-line
floor (~120). Verify the skill's required sections **in order** — `## Blind Draw (IDs only)`
must **physically precede** `## Vector Combinations` (the Phase-1 blind-draw wall held), and
`## Validated Mechanisms` (the completeness anchor — NOT `## Generated Tactics`, which is a
build-only section and would always be absent here) must be present, followed by
`## Action Deduplication Result`. Quick novelty smell-test: referenced vector IDs exist in
`growth-factors.json` and NO tactic names leak in. If explore's own validation marks it
INVALID (e.g. verb groups < 7, or the blind-draw wall is out of order), spawn a fresh worker
once with the gap.

**`must_include` enforcement gate — Bug-C fix (hardened).** Skill self-checks alone were
shown to be skippable, so the orchestrator enforces this deterministically. Parse
`synthesis-constraints.json` for the `must_include` pairs (`mandatory_combinations` pools
A + B). A raw whole-file grep only proves *line-presence*, which is too weak — the two IDs
could appear in unrelated combinations. So enforce **block-level co-occurrence**:

- **After `explore` writes its output:** split the file into `### Combination #N` blocks (parse
  per-block, not whole-file). For EACH `must_include` pair, a pair is **validly used** only
  if **both** of its vector IDs appear **within a single `### Combination #N` block**. A pair
  is **validly substituted** only if there is an explicit substitution note that (i) names
  that pair AND (ii) **names a replacement vector that EXISTS in `growth-factors.json`**
  (validity, not mere presence of the word "substituted"). If any pair is neither validly
  used nor validly substituted, spawn a fresh explore worker **ONCE** with the specific pairs
  in `blocking_issues` (e.g. "Pool-B pair `lever-NNN`+`struct-NNN` is not co-located in any
  one combination and has no valid substitution — co-locate both IDs in one combination, or
  substitute with a replacement vector that exists in growth-factors.json").
- **After `build` writes the final `synthesis.md` (closing check WITH remediation):** apply the
  same block-level test per *tactic* — for each Pool-B `must_include` pair, both IDs must
  appear within a single tactic's `**Source:** … Vectors` line/block, OR a valid substitution
  note (naming an existing replacement vector) must be present. If any Pool-B pair is neither
  validly used nor validly substituted, **re-dispatch build ONCE** with `blocking_issues`
  listing exactly the missing pairs (this is a real remediation, not just a re-grep). If a
  pair is still uncovered after that single build retry, record it as a known gap in the
  run-ledger and the final report — do not silently pass.

**`build` reviewer gate:** dispatch `diffmode-growth-tactics:reviewer` with
`{dimension: "demand-gen-synthesis", spec_path:
"${CLAUDE_PLUGIN_ROOT}/skills/synthesis-build/SKILL.md", output_path: "…/synthesis.md",
context_paths: [growth-factors.json, synthesis-constraints.json, founder-input.md,
audience-jtbd.md, competitors-analysis.md, competitor-gaps.md, cross-industry.md,
platform-arbitrage.md]}`.
Score ≥7 / max 3 retries, blocking_issues injected verbatim on re-dispatch. The reviewer
applies the demand-gen-synthesis rubric WITH the clean-room adjustments noted in the
growth-reviewer skill (score against the per-run LIGHT DB; do not require Week-1 depth;
synthesis is the final stage).

## Stage 5 — Package the founder report (best-effort — NEVER blocks the run)

`synthesis.md` is written to pass the reviewer — disposition tables, traceability lines,
scores — and downstream checks parse that structure, so it stays exactly as built. The page
the founder opens first is **derived** from it after the build gate: a packaging stage
re-writes the tactics as plain cards, and the renderer (Output step 1) uses that page as
"Your Growth Tactics", keeping `synthesis.md` available as a working paper.

Run this only after the Stage-4 build gate is APPROVED. Dispatch **`synthesis-worker`** with
a per-dispatch **`model: sonnet`** override (packaging is re-writing, not reasoning):

| Stage | Worker | Model | Skill | Inputs | Output |
|-------|--------|-------|-------|--------|--------|
| founder-report | synthesis-worker | **sonnet** | `:founder-report` | `…/synthesis.md`; `${CLAUDE_PLUGIN_ROOT}/reference/writing-style.md` | `…/growth-tactics.md` |

(`…` = `WS/03-think-tanks/demand-generation/`.)

**Structural check (deterministic — no reviewer gate):**

- exists, non-empty, min-line floor ~80;
- the LAST section is `## Where these came from`;
- the `### N.` card count equals `synthesis.md`'s `### Tactic #N` count;
- the banned-pattern grep returns nothing:

  ```bash
  grep -nE '(struct|lever|resource|psych|pos|conv)-[0-9]|Pass [12]|must_include|Pool [AB]|[Ww]hite[ -][Ss]pace|growth-factors\.json|\bPASS\b|\bFAIL\b|/10\b|/50\b|[Aa]nti-[Pp]attern' "<WS>/03-think-tanks/demand-generation/growth-tactics.md"
  ```

On a failed check, re-dispatch ONCE with the specific gaps in `blocking_issues` (the usual
fresh-worker rule). If it still fails — or the worker dies twice — record informational
**`founder-report-skipped`** in the ledger, **delete the failed `growth-tactics.md`** (the
renderer's fallback keys on the file being absent — never leave a broken page behind), and
continue to the Output step: the report falls back to `synthesis.md` as the main page (the
pre-v2.7 behavior). This stage never fails the run and never counts against its success.

## Output / report — and STOP

The run ends with **deliverables, not logs.** Do these in order:

### 1. Render the HTML report (best-effort — NEVER blocks or fails the run)

The deliverables are markdown files; the founder's machine may have no markdown viewer,
so render them to styled HTML and open in the browser. Find a real Python ≥3.8 first
(probing with `-c` defeats the Windows Store stub, which would otherwise pop the Store):

```bash
PY=""
for P in python3 python "py -3"; do
  $P -c "import sys; assert sys.version_info >= (3,8)" >/dev/null 2>&1 && { PY="$P"; break; }
done
```

- **Python found** → `$PY "${CLAUDE_PLUGIN_ROOT}/scripts/render_html.py" "<WS>"`
- **No Python** → `bash "${CLAUDE_PLUGIN_ROOT}/scripts/render_html.sh" "<WS>"`
- **Both fail** → record `report-render-skipped` (informational), use the `.md` paths in
  step 2 instead of HTML links, and add one line: *"Couldn't build the browser report —
  your files are plain text, listed below. To render later:
  `python3 <plugin>/scripts/render_html.py <WS>`."*

The renderer writes `WS/report/index.html` plus one page per deliverable
(human-friendly names like `Your Growth Tactics.html`). It renders whatever exists and
skips the rest, so a partial/failed run still gets a report of what it produced. The
"Your Growth Tactics" page renders from `growth-tactics.md` (Stage 5); when that file is
absent (an old run, a Codex run, or a skipped packaging stage) it falls back to
`synthesis.md` and the "Tactic Engineering Notes" working-paper page is skipped — the
renderer handles this itself, no orchestrator work needed.

### 2. Final message — LEAD with the deliverables

The first line is the result, not a log. **Print this full message BEFORE the
open-question of step 3** — the itemized list must appear even when that question is
skipped or auto-answered; never fold it into the post-answer reply. Template (fill real
numbers from the outputs; drop any line whose file doesn't exist; use `.md` paths if
step 1 rendered nothing):

> ## Your growth strategy is ready
>
> **8 growth tactics** built for your budget, team, and stage — plus the research they
> stand on (9 competitors mapped · 4 buyer segments · 31 acquisition plays audited).
>
> **Start here → Your Growth Tactics** — what to run and the first steps for each
> (`<WS>/report/Your Growth Tactics.html`)
>
> **Research briefs** — reusable on their own (hand one to a freelancer, drop one in a deck):
> - **Competitor Research** — who you're up against and how each rival gets users
> - **Audience Map** — your buyer segments and what each one hires you for
> - **Acquisition Audit** — the plays already working in your market
>
> **Strategy reports:**
> - **Where Your Size Wins** — openings big competitors can't or won't fill
> - **Plays From Other Industries** — proven moves adapted to your market
> - **Fresh Platform Openings** — new platform features rivals haven't claimed
>
> **Working papers:** Your Product Brief · How These Were Built · Tactic Engineering Notes
>
> Done in ~1h25m — say "show the run ledger" for per-stage timings.

### 3. Offer to open it

`AskUserQuestion` (main thread): *"Open your report in the browser?"* [Yes / No]. On
Yes, open `<WS>/report/index.html` with the OS command — macOS `open`, Linux
`xdg-open`, Windows/git-bash `explorer.exe "$(cygpath -w "<WS>/report/index.html")"`.
A failed open is one apologetic line with the path — never an error dump. If the open
command fails or the session is sandboxed with no host browser to reach (e.g. Claude
Cowork), print the `<WS>/report/index.html` path and say to open it from the app's
files panel. Skip the question entirely if nothing was rendered, or if the run is
non-interactive (headless `-p` mode — just print the path instead).

### 4. The run ledger — demoted (print ONLY on failure or on request)

Do NOT print the per-stage timing table by default. Print it only when (a) a stage
FAILED, or (b) the founder asks (e.g. "show the run ledger"). When asked, read the
real `duration_s` rows from `WS/.run-state.json`:

```
Growth Tactics — <slug>                                                          duration
  diagnostics          OK                                  …/founder-input.md           42s
  enrichment           competitors APPROVED · audience+acq OK (structural)   WS/02-enrichment/*.md   14m
  growth-factors       OK  (31 vectors, 6 categories)      …/growth-factors.json  [‖ 34m, clean-room, no re-mine]
  think-tanks          3/3 OK (structural, parallel)       …/{competitor-gaps,cross-industry,platform-arbitrage}.md  ~11m
  lite-constraints     OK                                  …/synthesis-constraints.json  3m
  synthesis            APPROVED (score 8, 1 pass)          …/synthesis.md  (8 tactics, 5 unconv.)  15m
  ── total wall-clock ──────────────────────────────────────────────────────────  ~1h25m
```

(The `‖` marks growth-factors as concurrent — its time hides under the critical path.)

### 5. Free stops here

Then tell the founder explicitly:

> This is where the **free** run stops. You have 7–9 unconventional ways to get users,
> built fresh for your product. **[Diffmode](https://diffmode.app)** picks up from here:
> it ranks these tactics so you know what to run first, and turns the top picks into a
> week-by-week plan — drawn from a much deeper research base than this free run uses.
> Start with a **free audit** at **[diffmode.app](https://diffmode.app)**.

For any FAILED stage, list its final `blocking_issues`.

## Failure modes

| Code | Where | Meaning | Recovery |
|------|-------|---------|----------|
| `missing-channel-menu` | pre-flight | bundled channel menu absent from `${CLAUDE_PLUGIN_ROOT}/reference/` | reinstall the plugin |
| `plugin-not-enabled` | any dispatch | a `diffmode-growth-tactics:…` id doesn't resolve | enable the plugin |
| `worker-dispatch-failed` | any stage | worker died mid-run (API/socket error, no JSON) after 2 fresh re-spawns | stage FAILED; run `/diffmode-growth-tactics:start` again — it picks up from this point. No main-thread fallback |
| `intake-incomplete` | Stage 0 | founder-input has unresolved must-ask gaps | ask the founder the Confirmation Gaps |
| `competitors-gate-failed` | Wave 1 | competitors REJECTED ×3 | inspect blocking_issues; downstream can't run |
| `dimension-failed` | enrichment (Wave 2) | `audience`/`acquisition-tactics` structurally incomplete after a single re-dispatch (no reviewer loop in v2.3.0) | list the gap; dependents skipped |
| `growth-factors-invalid` | Stage 1.5 / Stage-3 boundary | JSON/schema/clean-room check failed ×2 | inspect; synthesis can't run without the LIGHT DB — run `/diffmode-growth-tactics:start` again (Start fresh re-mines) |
| `constraints-invalid` | Stage 3 | synthesis-constraints schema/id check failed | re-dispatch lite-constraints |
| `constraints-stale` | Stage 4 precheck | `synthesis-constraints.json` references vector IDs absent from the CURRENT `growth-factors.json` (a re-mine without a constraints rebuild) | re-run `lite-constraints` against the current LIGHT DB (in-run; or run `/diffmode-growth-tactics:start` again — auto-resume re-enters there) |
| `synthesis-failed` | Stage 4 | `build` REJECTED ×3 | list blocking_issues |
| `clean-room-violation` | Stage 1.5/3/4 | a worker read `tactics_DB/` | re-dispatch; the LIGHT-DB stages must never touch the proprietary DB |
| `founder-report-skipped` | Stage 5 | packaging structural check failed after one re-dispatch (or the worker died twice) — informational, the run itself is fine | nothing required — the report falls back to `synthesis.md` as the main page; run `/diffmode-growth-tactics:start` again to retry packaging |
| `report-render-skipped` | Output step 1 | no usable Python AND the sh fallback failed — HTML report not built (informational; the run itself is fine) | print the `.md` deliverable list + the manual render command (`python3 <plugin>/scripts/render_html.py <WS>`) |

## Idempotency

Overwrite-on-rerun for stage outputs, EXCEPT `growth-factors.json`, which is **cached and
reused** on auto-resume **Continue** and on within-run retries (the deliberate cost
mitigation for per-run mining — it is the slowest/priciest stage). A **Start-fresh**
relaunch is the one thing that discards that cache and re-mines: fresh means fresh.

**Start fresh invalidates `synthesis-constraints.json`.** The constraints file is derived from
a specific LIGHT DB, so re-mining makes the cached constraints stale (its vector IDs may no
longer exist). Whenever a Start-fresh re-mine runs, the orchestrator **must also force
`lite-constraints` to re-run** (rebuild `synthesis-constraints.json` against the fresh
`growth-factors.json`) before any synthesis step. The Stage-4 `constraints-stale` precheck is
the backstop that catches a resume which skipped this.

**Run-ledger.** The orchestrator maintains a workspace-local `WS/.run-state.json` (see
*Run-ledger* below) recording each stage attempt's verdict. The auto-resume pre-flight
(step 1) reads it first to know which stages are done / failed / mid-retry. It is per-run
workspace state (git-ignored), and is **best-effort** recovery aid, not a hard guarantee.

## Run-ledger (durability across a multi-hour run)

A full run can take ~2.5h and span context compaction. To survive that and make
auto-resume reliable, maintain a small, human-readable, **workspace-local**
ledger at `WS/.run-state.json` and **append to it after every stage attempt**:

```json
{ "stage": "enrichment:competitors", "attempt": 1, "verdict": "APPROVED", "score": 8, "started_at": 1717200000, "duration_s": 1080, "output": "WS/02-enrichment/competitors-analysis.md" }
{ "stage": "growth-factors", "attempt": 1, "verdict": "OK", "started_at": 1717200200, "duration_s": 2280, "output": "WS/03-think-tanks/demand-generation/growth-factors.json" }
{ "stage": "synthesis:build", "attempt": 2, "verdict": "REJECTED", "score": 6, "started_at": 1717206000, "duration_s": 900, "blocking": ["…"] }
```

(JSON-lines, or an equivalent `WS/RUN-LOG.md` table — append-only, one row per attempt.)

- **Write a row after EVERY attempt** of every gated/structural stage: the verdict
  (`APPROVED` / `REJECTED` / `OK` / `FAILED` / `died→respawn`), the score where there is one,
  the **`started_at`** (epoch seconds from `date +%s` before dispatch) and **`duration_s`**
  (epoch seconds after the attempt resolves, minus `started_at`), and the output path. The
  per-stage `duration_s` is what the final report's timing column and the *Output/report*
  total wall-clock are read from — the first instrumented run replaces the rough minute
  estimates in this file with real numbers. (The `growth-factors` branch runs concurrently, so
  its `duration_s` overlaps enrichment + Stage 2 rather than adding to the critical path.)
- **On an auto-resume Continue** (pre-flight step 1), read the ledger FIRST to learn which
  stages are done, which failed, and which were mid-retry — then resume from the right point
  instead of re-deriving state from scratch.
- This is **best-effort durability.** The orchestrator is an LLM following prose, so the
  ledger is a recovery *aid*, not a transactional guarantee — if it and the filesystem
  disagree, trust the on-disk stage outputs (the contract between stages) and reconcile.
- The ledger is **per-run workspace state** — it is git-ignored (see repo `.gitignore`).

## Acceptance check (user runs after the orchestrator finishes)

1. `synthesis.md` exists with **7-9 tactics**, ≥50% unconventional, every tactic traceable
   to a vector combination from `growth-factors.json`.
2. `growth-tactics.md` exists (the packaged founder report): same card count as
   `synthesis.md`'s tactic count, ends with `## Where these came from`, and the Stage-5
   banned-pattern grep over it is empty (no vector IDs, pass labels, pools, or scores). If
   the ledger recorded `founder-report-skipped` instead, the report's main page fell back
   to `synthesis.md` — acceptable, note it.
3. `growth-factors.json` is a clean-room LIGHT DB (20-40 vectors, correct schema, real
   source URLs, nothing traceable to `tactics_DB/`).
4. Spot-check that tactics are **non-generic** (the novelty test the whole pipeline exists
   for) — strip the tactic name + adjectives; a traditional marketer should NOT say "obviously
   do that" for the majority.
5. Enrichment `competitors` reached APPROVED (score ≥7); `audience` + `acquisition-tactics`
   and all 3 think-tank outputs passed their structural completeness check (required sections
   present). Note anything that needed a re-dispatch.
6. `WS/.run-state.json` carries a `duration_s` for every stage attempt, and the run report
   printed the per-stage timing column — confirm `growth-factors` overlapped enrichment +
   Stage 2 (its row started right after the competitors gate) rather than serializing after them.
7. (Optional moat check) Compare a light-DB synthesis run against a proprietary-DB run for
   the same workspace — the free output should be **useful but visibly weaker**.
