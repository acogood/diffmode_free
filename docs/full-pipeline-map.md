# Full demand-gen architecture (beyond the enrichment pilot)

The orchestrator + skills + workers pattern (`architecture.md`) extends to the rest of
the demand-gen pipeline. This doc specifies the mapping for think-tanks,
prioritization, and implementation — **specified, not built in v1.** Two added
complications recur: **vector-DB context** and **deterministic pre/post scripts**.

## The recurring complication: scripts are NOT skills

Skills are passive prose. Deterministic Python scripts (constraint generation, vector
validation, SSR analysis, librarian context-file generation) must be run by the
**orchestrator via Bash as explicit steps**, exactly where `workflow-config.yaml`
declares `pre_execution_script` / `post_execution_script`. They never go inside a
skill. The orchestrator shells out, checks exit code, then proceeds. (Per CLAUDE.md:
scripts in `tactics_DB/scripts/` resolve resources via
`Path(__file__).resolve().parent.parent` — the orchestrator must invoke them with the
CWD / `--workspace` they expect.)

## Think-tanks (`prompts/think-tanks/demand-generation/`)

**Shape:** 3 parallel opportunity explorers → multi-step synthesis with a blocking
reviewer loop.

```
[parallel fan-out, 1 message, 3 Agent calls] gated on all enrichment approved:
  • competitor-gaps      (reads founder-input, competitors-analysis, channel-menu)
  • cross-industry       (reads founder-input, acquisition-tactics, audience-jtbd)
  • platform-arbitrage   (reads founder-input, audience-jtbd, channel-menu)
        │
        ▼ (sequential synthesis chain)
  synthesis-step1 (combinations)  ── reads intelligence-layer + convergence clusters
  synthesis-step2 (mechanisms)    ── reads vector_cache/demand_generation  ◄ VECTOR DB
        │  [orchestrator Bash step: generate_synthesis_constraints.py --workspace <slug>]   ◄ PRE-SCRIPT
  synthesis-pass1 (white space)   ── reads synthesis-constraints.json
  synthesis-pass2 (founder fit)   ── reviewer loop (demand-gen-synthesis, ≥7, max 3)
        │  [orchestrator Bash step: validate_synthesis_vectors.py --workspace <slug>]        ◄ POST-SCRIPT
```

**Complication (a) — vector-DB context.** `synthesis-step2` and downstream need the
demand-gen vector taxonomy (`tactics_DB/exploit-vectors-database.json` via the
`vector_cache`) + intelligence-layer artifacts loaded into the synthesis skills/
workers. These are large; load them into the *worker* context (not the orchestrator),
keeping with the lean-orchestrator state contract.

**Complication (b) — deterministic pre/post scripts.** `generate_synthesis_constraints.py`
(pre, before pass1) and `validate_synthesis_vectors.py` (post, after pass2) are
orchestrator Bash steps with `required: true` / exit-code gating — never folded into a
skill.

**Mapping:** 3 explorer skills + 4 synthesis skills + 1 synthesis-reviewer skill;
workers fan out the 3 explorers in parallel, then run the synthesis chain sequentially
with the 2 Bash script steps interleaved and the pass2 reviewer-retry loop.

> Note: CRO think-tanks (persona generation → 3× SSR cycles) also live in
> `workflow-config.yaml` and would map the same way, but each SSR batch requires the
> `run_ssr_analysis.py` post-script (`environment: venv:ai-cmo-cli/.venv`, gemini-flash
> SSR-only per the model-routing policy). Out of demand-gen scope; flagged for a CRO
> companion project.

## Prioritization (`prompts/prioritization/strategic-prioritization.md`)

**Shape:** single scoring step + reviewer; optional librarian post-script.

```
prioritization (reads founder-input, audience-jtbd, synthesis.md [+ CRO reports])
   ├─ reviewer (demand-gen-prioritization-reviewer)
   └─ [orchestrator Bash step: librarian.py --workspace <slug>]   ◄ POST-SCRIPT (per-tactic context files)
```

**Mapping:** 1 prioritization skill + 1 reviewer worker + 1 `librarian.py` Bash step.
The 6-dimension scoring formula (Resource 20 / Skill 15 / Purity 20 / Impact 20 /
Speed 15 / Unconventional 10; hard filter Purity ≤2 → ELIMINATE) lives in the skill.
**Can be skipped at runtime** (user's note) but is specified for completeness.

## Implementation (`prompts/implementation/demand-generation/`)

**Closest existing analog to this whole project** — already a generic-template +
context-injection design, driven by `execution-manifest.json` (`dynamic_execution` in
the config). The manifest becomes the **orchestrator's work queue**, exactly like
pSEO's per-cell list.

```
librarian.py already produced context-XX-<tactic>.md per tactic.
[per-tactic worker fan-out — like pSEO's per-cell fan-out]:
  for each tactic in execution-manifest.json:
     research-generic   → research-XX-<tactic>.md   (web research)
     sr-research-quality → review-research-XX
     plan-generic       → plan-XX-<tactic>.md        (NO internet — analysis only)
     sr-plan-quality + implementation-review (comprehensive)
  then ONCE across all tactics:
     tactic-sanity-review (fresh-eyes gate; reads founder-input + competitors + all plan-*.md)
```

**Mapping:** a per-tactic worker (research → plan, mirroring pSEO's per-cell worker) +
sanity-reviewer gate driving the **replacement / reserve loop** (a failed tactic is
swapped for a reserve from the prioritized list — analogous to pSEO Stage 7 self-heal
but at the tactic level). The `plan-generic` step must run on a worker with **no web
tools** (the prompt forbids internet — plan uses only the research file), the same
no-MCP discipline the audience dimension uses in the pilot.

## Summary table

| Module | Skills | Workers | Bash script steps | Reviewer loops |
|--------|--------|---------|-------------------|----------------|
| enrichment (built) | 5 + 1 reviewer | research / analysis / reviewer | none | 5 (per dimension) |
| think-tanks | 3 explorer + 4 synthesis + 1 reviewer | research + synthesis (no-web) | `generate_synthesis_constraints.py` (pre), `validate_synthesis_vectors.py` (post) | 1 (pass2) |
| prioritization | 1 + 1 reviewer | scoring + reviewer | `librarian.py` (post, optional) | 1 |
| implementation | 1 research + 1 plan(no-web) + sanity | per-tactic fan-out + sanity | (librarian already ran) | per-tactic + sanity replacement loop |

The enrichment pilot proves the spine (fan-out + reviewer-retry + lean state); the
remaining modules add only **vector-DB context loading** and **orchestrator Bash
script steps** on top of the identical pattern.
