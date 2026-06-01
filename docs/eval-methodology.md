# Eval methodology for the packaged enrichment module

How we measure enrichment quality *as developers* — distinct from the runtime
quality gate the skill ships *for users*. Sits beside `architecture.md` (roles, state
contract) and `enrichment-pilot.md` (DAG, distillation map). **This is a methodology
doc only — no harness, script, or committed fixtures this pass.** What gets built later
is sketched in §8 and flagged in §10.

## 0. The question this resolves

When a module ships as a Claude Code skill, it already carries a **runtime
Scrutiny-&-Review (S&R) gate** — the `growth-reviewer` worker that scores every
dimension and blocks the pipeline below threshold. So what is an *eval* for, if the
skill already grades itself at runtime?

Answer: they are **not substitutes**. They run at different times, for different
beneficiaries, and only one of them ever sees the next user's actual input. But they
**share one judge** — the `growth-reviewer` rubric. One rubric, two harnesses.

---

## 1. Two quality systems, two beneficiaries

| | **Runtime S&R gate** | **Eval** |
|---|---|---|
| **Lives in** | inside the shipped skill (`pipeline-skills/agents/growth-reviewer.md` + `pipeline-skills/commands/run-enrichment.md` loop) | in our repo, never shipped |
| **Runs when** | every time a *user* runs the pipeline | when *we* edit a prompt / skill / model choice |
| **Runs over** | the user's never-seen-before product context | a frozen set of fixture workspaces |
| **Judge model** | the user's host model (or whatever the reviewer agent is pinned to) | a **pinned** judge, distinct from the host under test (see §6) |
| **What it judges** | *this one run* — does this output clear the bar? | *the change* — did this edit raise or lower quality across cases? |
| **On fail** | re-dispatch the worker with blocking issues injected, max 3 iterations, then mark the dimension FAILED | block the version bump; investigate the regression |
| **Beneficiary** | the **end user** (defends their run) | the **developer** (decides what to ship) |
| **Retry?** | yes — capped self-heal loop | no — a measurement run scores once, no healing |

The flow they sit in:

```
  [ we edit a prompt / skill / model ]
            │
            ▼
        EVAL  ──fail──►  don't ship; fix the regression
            │ pass
            ▼
        ship the version bump
            │
            ▼
  [ user runs /run-enrichment on THEIR product ]
            │
            ▼
   RUNTIME S&R GATE  ──fail──►  re-dispatch worker (≤3×), else FAILED
            │ pass
            ▼
        user gets their enrichment outputs
```

**The shared judge.** Both systems call the same rubric: the per-dimension files in
`pipeline-skills/skills/growth-reviewer/references/{competitors,audience,acquisition-tactics,demographics,purchase-objections}.md`,
applied by the `growth-reviewer` worker, which returns:

```json
{
  "dimension": "competitors",
  "score": 8,
  "verdict": "APPROVED",
  "format_compliance": "PASS",
  "blocking_issues": [],
  "confidence": "MEDIUM",
  "summary": "1-2 sentences",
  "ssr_readiness": null
}
```

(`ssr_readiness` is non-null only for `demographics`: `READY | NEEDS_IMPROVEMENT |
NOT_READY`.) The runtime gate reads this verdict to decide *retry vs. proceed*; the
eval reads the same verdict to decide *ship vs. don't*. We do **not** maintain a second
rubric — if the bar moves, it moves in one place and both systems inherit it.

---

## 2. Why you keep both (you can't collapse one into the other)

The temptation: "if the eval proves the prompt is good across 21 fixtures, why keep
paying for a runtime gate on every user run?"

Because **21 fixtures prove "works across these representative cases" — never "works
for the next user's specific niche."** The fixtures are 21 products we already saw. The
next user is a corporate-EdTech reseller in Kazakhstan, or a hyper-local expat news
service in three languages — a context that may share *zero* surface features with any
fixture. The eval cannot have scored an input that does not exist yet.

So the runtime gate is the **only** check that ever runs on unseen input. The eval
raises our confidence that a *change* didn't break the representative cases; the runtime
gate is what catches the long tail the fixtures can't represent. Removing it would mean
shipping every user's run ungated on the strength of cases that, by construction, don't
include them.

They answer different questions:

- **Eval:** "Did my edit make the *prompt* better or worse?" (about the artifact)
- **Runtime gate:** "Is *this output*, for *this user*, good enough to hand over?"
  (about the instance)

---

## 3. What a "harness" is, in our terms

A harness is the **runner / scaffolding** around the thing under test — pytest is the
canonical analogy: pytest is not your code and not your assertions; it's the runner that
*feeds inputs in, captures outputs, applies assertions, and reports*. Map that onto our
parts:

| pytest concept | enrichment equivalent |
|---|---|
| function under test | the dimension **prompt / skill** (`enrichment-competitors`, …) |
| the runtime executing it | the **host model** (whatever runs the worker) |
| test input / fixture | a fixture **workspace** (`founder-input.md` + frozen upstream context) |
| `assert` | the **`growth-reviewer` rubric** → `{score, verdict, …}` |
| pytest itself (the runner) | the **harness** — feeds fixtures in, collects verdicts, reports |

We already own a **production harness** — in fact two implementations of it, which use
*different* reviewers and thresholds (this is the §7 split, not a single shared gate):

- the legacy `manual_test_automation/run_workflow.py` (Python; invokes the
  **markdown-format** S&R reviewers at `prompts/reviewers/enrichment/*.md`, parsed via
  `parse_sr_output()`, threshold ≥ 8), and
- the skill-side `pipeline-skills/commands/run-enrichment.md` orchestrator (dispatches
  the **JSON-returning** `growth-reviewer` agent from §1, threshold ≥ 7).
- Both run the pipeline **once per user/workspace**, **with** the retry loop, to produce
  *real deliverables*. They play the same role — gated production, not measurement.

What we *don't* own yet is a **measurement harness**:

- Runs the dimension **in batch over many fixtures**, **without** retry/self-heal (you
  want the raw first-pass quality, not the healed quality), and just **collects scores**
  to compare versions.
- A passing measurement run does not produce a deliverable — it produces a *number*.

The distinction matters because retry hides regressions: a prompt that needs 3 passes to
clear threshold and a prompt that clears it on pass 1 both look "APPROVED" to the
production harness. The measurement harness must score **pass-1 output, no healing**, or
it measures the loop, not the prompt.

**The measurement harness never ships** — it is developer-only repo infrastructure. The
*runtime* gate that does ship (the `growth-reviewer` worker + the orchestrator's
retry loop in `run-enrichment.md`) is what defends the user's run (§1); `run_workflow.py`
is legacy and ships with neither the skill nor the eval.

---

## 4. The four eval axes for enrichment

Cover all four. For each: *what it measures · what one "case" is · what varies · the
baseline · when you'd run it.*

### 4a. Version regression — the headline axis

- **Measures:** did a new prompt/skill version raise or lower quality versus the
  previous version, across the fixture set?
- **One case:** one fixture workspace, scored on `version N` and on `version N-1`.
- **What varies:** the prompt/skill version. Host model and judge held constant.
- **Baseline:** the previous version's scores on the same fixtures.
- **When:** every time you edit a dimension prompt or its `SKILL.md`. This is the
  everyday iteration guard — the equivalent of "run the tests before merging."

### 4b. Host-model floor

- **Measures:** does the dimension still clear threshold on the **weakest host a user
  might plausibly run** (e.g. a Sonnet/Haiku-class or non-Claude GPT-class model),
  rather than only on the strongest?
- **One case:** one fixture, generated on the floor host, scored by the pinned judge.
- **What varies:** the host model (generation side). Prompt version and judge held
  constant.
- **Baseline:** the same fixtures on the reference/strong host; and the pass/fail line.
- **When:** before declaring a minimum supported host, or when changing the default
  model. Reframes the unanswerable "which model is best?" into the answerable **"does
  the skill survive the floor?"** — if yes, model choice above the floor is the user's.

### 4c. MCP-degradation delta

- **Measures:** the quality gap between running the research worker **with Perplexity**
  vs. with a **generic WebSearch fallback**. This is the number that justifies (or
  retires) "require Perplexity."
- **One case:** one fixture, generated twice — once with `mcp__perplexity__*`, once with
  the fallback — scored by the pinned judge; the case's result is the *delta*.
- **What varies:** the research backend. Prompt, host, judge held constant.
- **Baseline:** the Perplexity-backed score; the delta against fallback is the finding.
- **When:** before changing the research-backend requirement, or when a new fallback
  appears.
- **⚠ Scope:** applies to the **4 research dimensions only** — `competitors`,
  `acquisition-tactics`, `demographics`, `purchase-objections`. It does **NOT** apply to
  **`audience`**: the audience worker (`enrichment-analysis-worker`) ships with **no
  research MCP by design** (ENR-001 forbids new web search; the no-MCP worker enforces it
  structurally). There is no backend to degrade, so this axis is undefined for audience.

### 4d. Self-grading trust

- **Measures:** is the *shipped self-grading gate* trustworthy? Generate on model A, then
  review with model A (self-grade) vs. an **independent** judge; measure agreement.
- **One case:** one fixture, scored by the self-grader and by the independent judge; the
  case's result is the agreement / disagreement (e.g. score delta, verdict match).
- **What varies:** the judge (self vs. independent). Generation held constant.
- **Baseline:** the independent judge's verdict, treated as the more credible signal.
- **When:** whenever you rely on a model grading its own output — which is exactly what
  the runtime gate does when host and reviewer are the same model. High disagreement
  here means the runtime gate is grading leniently and you should pin the reviewer to a
  *different* model than the host (the motivation for §6).

---

## 5. Fixture strategy

### The pool

`ai-cmo-workspace/` holds **30** workspaces with an `02-enrichment/` directory; **27**
carry all five core outputs (`competitors-analysis.md`, `audience-jtbd.md`,
`acquisition-tactics.md`, `demographics.md`, `purchase-objections.md`). After removing
same-product re-run variants (model, pipeline, or method: `diffmode` vs.
`diffmode-3.5flash-test`; `aprena-academy` vs. `_2/_3/_4`; `visibility-pro` vs. `_2/_3`)
and internal/test workspaces (`perplexity_test`, `ai-cmo-self`, `ai-cmo-agency`), **21**
represent *distinct products* — the usable fixture set. (`kolays_user_1_cli` and
`endercomio_manual` are method re-runs of products already present; the count keeps them
for coverage — treat them as non-independent and the set is 19.)

**Name the edge cases — keep them in the set on purpose:**

- `expat-news-lang` — only 3 enrichment files (no `demographics.md`,
  `purchase-objections.md`). A partial workspace: tests behavior when the DAG didn't
  complete. Also a hyper-niche multilingual product — a stress case for "does the next
  user's niche resemble any fixture?" (§2).
- `stepik.org` — only 2 files (`competitors-analysis.md` + a Russian-named market
  analysis), no `audience-jtbd.md`. Tests a non-English, large-market context and an
  off-template filename.

### Picking a representative subset

You don't run all 21 on every iteration. Pick a subset that spans the axes that move
quality: **B2B vs. B2C**, **English vs. non-English market**, **broad vs. ultra-niche
audience** (the SSR-data-availability axis from `demographics`), and **complete vs.
partial** workspaces. A 5–7 fixture subset that hits each corner gives a fast everyday
regression signal; reserve the full 21 for pre-release sweeps.

### The input / golden contract

- **Seed (input):** `01-diagnostics/founder-input.md` is the one true input for the whole
  chain. An eval case starts from this file and (frozen) upstream context.
- **Golden (reference):** the existing `02-enrichment/*.md` outputs are the *reference
  point* a regeneration is compared against — see the provenance caveat below.

### Subtlety 1 — DAG dependency in the inputs

Enrichment is a DAG (`enrichment-pilot.md`): `audience` needs `competitors-analysis.md`;
`demographics` and `purchase-objections` need `audience-jtbd.md`. For a **clean
per-dimension eval**, do **not** regenerate the whole chain to score one dimension —
that would entangle the dimension's quality with its upstream's. Instead **freeze the
upstream context from the golden workspace** and feed it in as fixed input. You are then
measuring *that dimension's prompt* given known-good upstream, not the compounded chain.

### Subtlety 2 — golden provenance

The existing goldens were generated by the legacy Python pipeline (`run_workflow.py`),
predominantly via **Gemini**. They are a **reference point, not ground truth.** When an
eval regenerates a dimension with a *different* model (e.g. the host-model-floor axis),
expect legitimate divergence from the golden that is not a regression. This is why the
eval's verdict comes from the **rubric score**, not from a diff against the golden text.
The golden is for eyeballing and for spotting *structural* drift (missing sections), not
for string equality.

---

## 6. Judge-model decision

The eval judge should be **pinned to one fixed model** — chosen once, recorded, changed
deliberately — and **distinct from the host model under test.**

- **Pinned** → reproducibility. If the judge drifts between runs, a score change can't be
  attributed to the prompt change you're testing. A pinned judge makes version-over-version
  comparison (§4a) meaningful.
- **Distinct from the host** → it's the only thing that makes the **self-grading-trust
  axis (§4d) measurable at all.** If judge == host you are measuring self-agreement, which
  is exactly the quantity §4d is trying to audit, not control for.

This is the single biggest difference from the runtime gate, where host and reviewer may
coincide (the user runs everything on one model). The eval *deliberately* separates them.

---

## 7. Threshold reconciliation (flagged finding — not fixed this pass)

There are **two different pass/fail lines** in the repo today:

| Source | Threshold | Evidence |
|---|---|---|
| Skill orchestrator (shipped) | **score ≥ 7** = APPROVED | `commands/run-enrichment.md` (pre-flight, reviewer loop, acceptance check) and `enrichment-pilot.md` ("score ≥ 7, max 3 iterations") |
| Legacy Python harness | **score ≥ 8** = pass | `run_workflow.py:134` → `MIN_PASSING_SCORE = 8` |

**Principle:** the eval's pass/fail line must equal **whichever threshold the *shipped
runtime gate* uses** — otherwise the eval green-lights versions the user's gate would
reject, or vice versa. Today the shipped gate is `run-enrichment.md`, which uses **≥ 7**.
So an eval built now should use **≥ 7**.

But the two numbers should not stay split. **Decision to settle (out of scope this
pass):** reconcile `MIN_PASSING_SCORE` and the orchestrator threshold to one value, in
one place, and have both harnesses read it. Recorded here; not changed.

---

## 8. Recommended harness approach (deferred build)

**Recommendation: a thin homegrown script.** Reasons:

- **Reuse the judge we already have.** The `growth-reviewer` rubric +
  `growth-reviewer` worker already produce a structured verdict. A measurement
  harness just dispatches the reviewer over fixtures and collects the JSON — it parses
  `json.loads(verdict)` directly (the reviewer emits structured JSON, §1). The repo
  already contains score-extraction precedent in `parse_sr_output()`
  (`run_workflow.py:163`), written for the *legacy markdown* S&R format; the JSON reviewer
  is strictly easier to consume than that.
- **No new dependencies.** Consistent with the repo ethos — "this is NOT traditional
  software," stdlib-only Python scripts (CLAUDE.md; `tactics_DB/` scripts use the standard
  library only). A batch-score-and-diff loop is ~stdlib `json` + a results table.

**What a framework (promptfoo / Inspect) would add** — and why it's not worth the
dependency *yet*:

| Framework gives you | Worth it now? |
|---|---|
| dashboards / HTML reports | No — a markdown results table suffices for 21 fixtures |
| model-matrix runner (host × judge grid) | Maybe later — useful once §4b/§4c are run routinely |
| response caching / cost tracking | Nice-to-have, not blocking at this fixture count |
| assertion DSL | Redundant — our "assertion" is the reviewer rubric, already authored |

**Adoption trigger (record, don't act):** revisit a framework when the fixture set or the
host×judge matrix grows past what a single results table can hold, or when caching cost
becomes the bottleneck. Until then the thin script wins on simplicity.

**This harness is NOT built this pass.** This section specifies the recommendation only.

---

## 9. How it plugs into the release flow

The eval is **the gate before bumping a skill version** — the same way a test suite
gates a library release:

```
edit dimension prompt / SKILL.md
   └─► run measurement harness over the fixture subset (§5), pinned judge (§6)
         └─► all fixtures clear the shipped threshold (§7)  ─── no ──► fix; do not bump
               └─── yes ──► bump the skill version, update CHANGELOG, ship
                              └─► users run /run-enrichment; runtime gate defends each run (§1)
```

A version bump that lowers a fixture below threshold is treated as a release blocker, not
a "ship and watch." Pre-release, run the full 21; for everyday edits, the 5–7 subset.

---

## 10. Open / deferred

- **Threshold reconciliation (§7)** — settle on one value for `MIN_PASSING_SCORE` and the
  orchestrator threshold; have both harnesses read one source. *Doc flags only.*
- **Commit a frozen fixture set?** — decide whether to snapshot a chosen subset (seed +
  frozen upstream context + golden) into the repo as a stable eval corpus, or keep
  pointing at live `ai-cmo-workspace/` (which drifts as workspaces are re-run). A frozen
  corpus is reproducible; a live one is current. *Not decided.*
- **Framework adoption trigger (§8)** — the conditions under which promptfoo/Inspect earn
  their dependency. *Recorded, not met.*
- **Other modules** — eval methodology for demand-gen, think tanks, CRO is **out of scope
  this pass.** Enrichment is the pilot because it is script-free and vector-DB-free
  (`enrichment-pilot.md`); the others add Python-script and vector-DB steps that change
  the harness shape.

---

### Out of scope (file separately)

- Building any harness, script, or committing fixtures.
- The ≥7-vs-≥8 threshold fix itself (this doc only flags it).
- Eval methodology for other modules (demand-gen, think tanks, CRO).
