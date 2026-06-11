#!/usr/bin/env python3
"""Deterministic MVP orchestrator for the Diffmode growth-tactics pipeline under OpenAI Codex.

Ports the proven Claude orchestrator (`plugin/commands/start.md`) + the durable
`codex/AGENTS.md` spec into a stdlib-only Python driver that dispatches each pipeline stage as a
`codex exec` worker (`codex_dispatch.py`) and gates it with deterministic structural checks
(`checks.py`). Control-flow that belongs in code — a reviewer->retry loop, structural gates, a
constraints-stale precheck, block-level must_include, parallel fan-outs — lives here, not in a
model-driven ExecPlan.

The DAG (faithful to AGENTS.md):

    Stage 0   diagnostics-intake          skip-if-exists; else URL -> research-worker (founder Q&A
                                          collected up front; --fast-intake leaves placeholders)
    Stage 1.W1 enrichment competitors     research-worker, REVIEWER-GATED (>=7, max 3)
    Stage 1.5 growth-factors mining       research-worker, launched right after competitors APPROVED,
                                          overlaps Wave 2 + Stage 2, joined at the Stage-3 boundary
    Stage 1.W2 audience || acquisition    analysis || research, structural-check only
    Stage 2   think-tanks x3              platform-arbitrage(research) || competitor-gaps ||
                                          cross-industry (analysis), structural-check only
    Stage 3   lite-constraints            synthesis-worker, structural + vector-id xref
    Stage 4   constraints-stale precheck (BLOCKING) -> synthesis explore (structural + must_include
              A+B) -> synthesis build (REVIEWER-GATED + must_include B) -> synthesis.md.  STOP.

MVP scope cuts (deferred): full --from/--only/--scratch/--remine resume; distinct failure-code
exit codes; model-tiering (one model — Codex has no sonnet). Stage 0 intake is built (URL mode
+ up-front founder Q&A); pure no-URL interactive intake is still out of scope (provide --url or a
pre-seeded founder-input.md).

Usage:
    # from a URL — Stage 0 researches the site, asking the founder the must-ask fields up front:
    python3 <repo>/codex/orchestrate.py --url https://theona.ai
    # hands-off (no Q&A; researched prefill with [NEEDS FOUNDER INPUT] placeholders):
    python3 <repo>/codex/orchestrate.py --url https://theona.ai --fast-intake
    # from a pre-seeded founder-input.md (skip-if-exists, e.g. an A/B re-run):
    cd /tmp/diffmode-codex-e2e && python3 <repo>/codex/orchestrate.py --product theona \\
        --backend native --max-concurrency 2
"""

from __future__ import annotations

import argparse
import shutil
import sys
import time
from pathlib import Path

CODEX_DIR = Path(__file__).resolve().parent
REPO = CODEX_DIR.parent
sys.path.insert(0, str(CODEX_DIR))   # for codex_dispatch
sys.path.insert(0, str(REPO))        # for `import codex.checks`

import codex_dispatch as cd          # noqa: E402
from codex import checks             # noqa: E402

SKILLS_ROOT = str(CODEX_DIR / ".agents" / "skills")
MENU = str(REPO / "plugin" / "reference" / "Marketing-Channel-Menu-2026.md")
STYLE = str(REPO / "plugin" / "reference" / "writing-style.md")
SCRIPTS = REPO / "plugin" / "scripts"   # render_html.py (the HTML report layer)

# Per-stage subprocess timeouts (R4): a hang becomes a `died`->respawn, never an infinite join.
T_RESEARCH = 1800      # enrichment research dims, think-tank research (~25-30 m)
T_ANALYSIS = 1500      # analysis-only dims (~25 m)
T_MINING = 4500        # growth-factors mining — the priciest stage (~75 m)
T_SYNTHESIS = 2700     # explore / build (~45 m)
T_REVIEW = 900         # reviewer (~15 m)


# --------------------------------------------------------------------------------------------
# Stage context
# --------------------------------------------------------------------------------------------
class Ctx:
    """Resolved paths + run knobs shared by every stage."""

    def __init__(self, args):
        out_dir = Path(args.out_dir).resolve()
        self.ws = out_dir / args.slug
        self.ws_parent = str(out_dir)
        self.diag = self.ws / "01-diagnostics"
        self.enr = self.ws / "02-enrichment"
        self.ttd = self.ws / "03-think-tanks" / "demand-generation"
        self.capture_dir = str(self.ws / ".codex-out")
        self.ledger = str(self.ws / ".run-state.json")
        self.model = args.model
        self.max_concurrency = max(1, args.max_concurrency)
        self.url = args.url               # Stage 0: research seed (None on a pre-seeded run)
        self.fast_intake = args.fast_intake  # Stage 0: skip the founder Q&A, accept the prefill

        # canonical artifact paths
        self.founder_input = str(self.diag / "founder-input.md")
        self.comp = str(self.enr / "competitors-analysis.md")
        self.aud = str(self.enr / "audience-jtbd.md")
        self.acq = str(self.enr / "acquisition-tactics.md")
        self.gf = str(self.ttd / "growth-factors.json")
        self.sc = str(self.ttd / "synthesis-constraints.json")
        self.pa = str(self.ttd / "platform-arbitrage.md")
        self.cg = str(self.ttd / "competitor-gaps.md")
        self.ci = str(self.ttd / "cross-industry.md")
        self.explore = str(self.ttd / "synthesis-explore.md")
        self.synth = str(self.ttd / "synthesis.md")

    def disp_kwargs(self) -> dict:
        return {"ws_parent": self.ws_parent, "capture_dir": self.capture_dir,
                "ledger_path": self.ledger, "model": self.model}


# --------------------------------------------------------------------------------------------
# Stage primitives
# --------------------------------------------------------------------------------------------
def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


class StageFailed(Exception):
    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def generate_blocking(ctx: Ctx, stage: str, worker: str, brief: dict, output: str, struct_fn,
                      *, web: bool, timeout: int):
    """Generate one stage: death-respawn (<=2 fresh), then structural check (<=1 fresh respawn).

    Returns (ok, last_dispatch, check_result). Raises StageFailed on a worker `error`.
    """
    d = None
    for death_try in range(3):  # 1 + 2 fresh respawns
        d = cd.dispatch(worker, brief, stage=stage, attempt=death_try + 1,
                        web=web, timeout_s=timeout, **ctx.disp_kwargs())
        if d.classification == "ok":
            break
        if d.classification == "error":
            raise StageFailed("worker-error", f"{stage}: {(d.result_json or {}).get('reason')}")
        log(f"  {stage}: worker {d.classification}; fresh respawn {death_try + 1}/2")
    if d is None or d.classification != "ok":
        raise StageFailed("worker-dispatch-failed", f"{stage}: died after 2 respawns")

    chk = struct_fn(output)
    if chk.ok:
        return True, d, chk
    log(f"  {stage}: structural check failed -> {chk.issues}; one fresh respawn")
    brief2 = dict(brief)
    brief2["blocking_issues"] = list(brief.get("blocking_issues") or []) + chk.issues
    d = cd.dispatch(worker, brief2, stage=stage, attempt=99, web=web, timeout_s=timeout, **ctx.disp_kwargs())
    chk = struct_fn(output)
    return chk.ok, d, chk


def reviewer_gate(ctx: Ctx, dimension: str, spec_path: str, output: str, context_paths: list[str],
                  attempt: int):
    """Dispatch reviewer-worker; return (approved: bool, blocking_issues: list, dispatch)."""
    brief = {
        "dimension": dimension,
        "skills_root": SKILLS_ROOT,
        "spec_path": spec_path,
        "output_path": output,
        "context_paths": context_paths,
    }
    d = cd.dispatch("reviewer-worker", brief, stage=f"{dimension}:review", attempt=attempt,
                    web=False, timeout_s=T_REVIEW, **ctx.disp_kwargs())
    rj = d.result_json or {}
    approved = (d.classification == "reviewed" and d.verdict == "APPROVED" and (d.score or 0) >= 7)
    return approved, rj.get("blocking_issues", []), d


def reviewer_loop(ctx: Ctx, stage: str, worker: str, base_brief: dict, output: str, struct_fn,
                  *, web: bool, timeout: int, dimension: str, spec_path: str,
                  context_paths: list[str], max_iter: int = 3):
    """Generate (+struct) then reviewer-gate; on REJECTED spawn a FRESH worker with blocking_issues."""
    blocking: list[str] = []
    for it in range(1, max_iter + 1):
        brief = dict(base_brief)
        if blocking:
            brief["blocking_issues"] = blocking
        ok, _d, chk = generate_blocking(ctx, f"{stage}#{it}", worker, brief, output, struct_fn,
                                        web=web, timeout=timeout)
        if not ok:
            raise StageFailed("structural-incomplete", f"{stage}: {chk.issues}")
        approved, blocking, _rev = reviewer_gate(ctx, dimension, spec_path, output, context_paths, it)
        if approved:
            log(f"  {stage}: APPROVED on iteration {it}")
            return True
        log(f"  {stage}: REJECTED on iteration {it}: {blocking[:2]}")
    raise StageFailed("reviewer-gate-failed", f"{stage}: REJECTED x{max_iter}; last issues: {blocking}")


# --------------------------------------------------------------------------------------------
# Pre-flight
# --------------------------------------------------------------------------------------------
def welcome(ctx: Ctx) -> None:
    """Plain-text mirror of the Claude orchestrator's Step-0a welcome (print FIRST)."""
    print("=" * 78)
    print("Diffmode — let's build your growth plan")
    print("=" * 78)
    print("""
What happens next:
  1. A few quick questions (~2 minutes) — the things your website can't tell us.
  2. Hands-off research (~60-90 minutes) — your competitors, your buyers, and
     what's already working in your market. You can walk away.
  3. Your growth tactics — 7-9 specific ways to get users, built for your
     budget, team, and stage.

What you'll have at the end:
  - Your Growth Tactics   — the main event: first steps + an early signal each
  - 3 research briefs     — Competitor Research, Audience Map, Acquisition Audit
  - 3 strategy reports    — where your size wins, plays from other industries,
                            fresh platform openings
  - Working papers        — the notes behind the work, yours to keep

Total: usually 1.5-2 hours. You only need to be here for the questions at the
start; the report renders to HTML at the end.""")
    print("=" * 78 + "\n")


def preflight(ctx: Ctx) -> None:
    welcome(ctx)
    log("Pre-flight…")
    if shutil.which("codex") is None:
        raise StageFailed("missing-codex", "the `codex` binary is not on PATH")
    # channel menu + a representative set of skill symlinks must resolve (realpath readable) — fail
    # in ~1s, not 40 min.
    must_resolve = [
        MENU,
        STYLE,
        f"{SKILLS_ROOT}/diagnostics-intake/SKILL.md",
        f"{SKILLS_ROOT}/enrichment-competitors/SKILL.md",
        f"{SKILLS_ROOT}/growth-factors-mining/SKILL.md",
        f"{SKILLS_ROOT}/growth-reviewer/SKILL.md",
        f"{SKILLS_ROOT}/growth-reviewer/references/competitors.md",
        f"{SKILLS_ROOT}/growth-reviewer/references/demand-gen-synthesis.md",
        f"{SKILLS_ROOT}/synthesis-explore/SKILL.md",
        f"{SKILLS_ROOT}/synthesis-build/SKILL.md",
    ]
    for p in must_resolve:
        rp = Path(p)
        if not (rp.exists() and rp.resolve().is_file()):
            raise StageFailed("missing-channel-menu" if p == MENU else "plugin-not-resolved",
                              f"required path does not resolve: {p}")
    for d in (ctx.diag, ctx.enr, ctx.ttd, Path(ctx.capture_dir)):
        d.mkdir(parents=True, exist_ok=True)
    # NB: no founder-input gate here — Stage 0 (stage0_intake) owns intake now
    # (skip-if-valid / produce-from-URL / fail-if-neither).
    log(f"  OK — WS={ctx.ws} · model={ctx.model or 'config default (gpt-5.5)'} · "
        f"concurrency={ctx.max_concurrency} · Perplexity OFF (native web_search)")


# --------------------------------------------------------------------------------------------
# Stage 0 — diagnostics intake (the entry point)
# --------------------------------------------------------------------------------------------
# The must-ask founder fields a website cannot reveal — mirrors the Claude Stage-0
# AskUserQuestion set (start.md §"Stage 0"). (key, prompt) each; the key labels the
# line the diagnostics-intake skill folds into the schema.
INTAKE_QUESTIONS: list[tuple[str, str]] = [
    ("Stage", "Stage (pre-launch / early / traction / growth)"),
    ("Monthly marketing budget", "Monthly marketing budget ($0 / under $500 / $500-2k / $2k+)"),
    ("Biggest growth problem",
     "Biggest growth problem (not enough traffic / traffic doesn't convert / both)"),
    ("Skills you can do",
     "Skills you can do (any of: landing pages, content, ad campaigns, analytics)"),
    ("Current traction",
     "Current traction (visitors/signups/MRR/paying customers — or 'pre-launch')"),
    ("Primary goal + deadline", "Primary goal + deadline (e.g. '20 paying teams in 90 days')"),
    ("Where traffic comes from",
     "Where users/traffic come from today (the demand-gen acquisition signal)"),
]


def collect_answers() -> str:
    """Interactively collect the must-ask founder fields a website can't reveal.

    Mirrors the Claude Stage-0 questions but as plain ``input()`` prompts (a ``codex exec``
    worker is a non-interactive batch call, so the driver asks up front instead of pausing
    mid-run). Returns a formatted answers block the diagnostics-intake skill folds in (founder
    answers win over researched guesses); ``""`` if every field was left blank. Callers must
    have already confirmed a TTY (see :func:`stage0_intake`) — never call this on a piped stdin.
    """
    print("\n" + "=" * 78)
    print("Founder intake — a few quick questions a website can't answer (press Enter to skip any).")
    print("=" * 78)
    lines: list[str] = []
    for key, prompt in INTAKE_QUESTIONS:
        try:
            ans = input(f"  {prompt}\n    > ").strip()
        except EOFError:
            break
        if ans:
            lines.append(f"- {key}: {ans}")
    print("=" * 78 + "\n")
    return "\n".join(lines)


def stage0_intake(ctx: Ctx, url: str | None, fast_intake: bool) -> None:
    """Produce ``WS/01-diagnostics/founder-input.md`` — skip-if-valid, else URL research.

    Mirrors the Claude Stage-0 wiring: a valid founder-input on disk is reused (the A/B / resume
    path); otherwise a ``--url`` is researched headlessly by the diagnostics-intake skill (with
    the founder's must-ask answers folded in unless ``--fast-intake``), gated by
    ``check_founder_input``; with neither, the run fails fast.
    """
    existing = checks.check_founder_input(ctx.founder_input)
    if existing.ok:
        log(f"Stage 0 — founder-input.md present + valid ({existing.info.get('lines')} non-blank "
            f"lines); skipping intake")
        return
    if not url:
        raise StageFailed("intake-incomplete",
                          "no valid founder-input.md and no --url: provide --url <site> or a "
                          "pre-seeded WS/01-diagnostics/founder-input.md")

    # Non-interactive safety: a backgrounded / piped run would hang on input(), so fall back to
    # the hands-off prefill rather than block forever.
    if not fast_intake and not sys.stdin.isatty():
        log("Stage 0 — stdin is not a TTY; falling back to --fast-intake "
            "(researched prefill, [NEEDS FOUNDER INPUT] placeholders left for the founder)")
        fast_intake = True

    answers = "" if fast_intake else collect_answers()

    log(f"Stage 0 — diagnostics-intake from URL "
        f"({'fast (no Q&A)' if fast_intake else 'with founder answers'}): {url}")
    brief = {
        "skill": "diagnostics-intake",
        "skills_root": SKILLS_ROOT,
        "url": url,
        "inputs": [],
        "output": ctx.founder_input,
    }
    if answers:
        brief["answers"] = answers
    if fast_intake:
        brief["fast_intake"] = True

    ok, _d, chk = generate_blocking(
        ctx, "diagnostics:intake", "research-worker", brief,
        ctx.founder_input, lambda p: checks.check_founder_input(p),
        web=True, timeout=T_RESEARCH)
    if not ok:
        raise StageFailed("intake-incomplete", f"diagnostics: {chk.issues}")
    log(f"  founder-input.md OK — {chk.info.get('lines')} non-blank lines")


# --------------------------------------------------------------------------------------------
# The DAG
# --------------------------------------------------------------------------------------------
def run(ctx: Ctx) -> dict:
    preflight(ctx)
    t0 = int(time.time())

    # ---- Stage 0 — diagnostics intake (skip-if-valid; else URL -> research-worker) ----------
    stage0_intake(ctx, ctx.url, ctx.fast_intake)

    # ---- Stage 1 Wave 1 — competitors (reviewer-gated) -------------------------------------
    log("Stage 1 Wave 1 — enrichment:competitors (reviewer-gated)")
    reviewer_loop(
        ctx, "enrichment:competitors", "research-worker",
        {"skill": "enrichment-competitors", "skills_root": SKILLS_ROOT,
         "inputs": [ctx.founder_input, MENU, STYLE], "output": ctx.comp},
        ctx.comp, lambda p: checks.check_markdown_stage("enrichment:competitors", p),
        web=True, timeout=T_RESEARCH,
        dimension="competitors", spec_path=f"{SKILLS_ROOT}/enrichment-competitors/SKILL.md",
        context_paths=[ctx.founder_input],
    )

    # ---- Stage 1.5 — growth-factors mining (overlaps Wave 2 + Stage 2 when concurrency>=2) --
    mining_brief = {"skill": "growth-factors-mining", "skills_root": SKILLS_ROOT,
                    "inputs": [ctx.founder_input, ctx.comp], "output": ctx.gf}
    mining_handle = None
    fanout_concurrency = ctx.max_concurrency
    if ctx.max_concurrency >= 2:
        log("Stage 1.5 — launching growth-factors mining in the background (||)")
        mining_handle = cd.launch("research-worker", mining_brief, stage="growth-factors",
                                  attempt=1, web=True, timeout_s=T_MINING, **ctx.disp_kwargs())
        fanout_concurrency = ctx.max_concurrency - 1  # reserve a slot for mining
    else:
        log("Stage 1.5 — concurrency=1: running growth-factors mining inline (sequential)")
        ensure_growth_factors(ctx, inline_brief=mining_brief)

    # ---- Stage 1 Wave 2 — audience || acquisition-tactics (structural only) -----------------
    log(f"Stage 1 Wave 2 — audience || acquisition-tactics (pool concurrency={fanout_concurrency})")
    wave2 = [
        dict(worker="analysis-worker", output=ctx.aud, struct="enrichment:audience",
             brief={"skill": "enrichment-audience", "skills_root": SKILLS_ROOT,
                    "inputs": [ctx.founder_input, ctx.comp, MENU, STYLE], "output": ctx.aud},
             web=False, timeout=T_ANALYSIS, stage="enrichment:audience"),
        dict(worker="research-worker", output=ctx.acq, struct="enrichment:acquisition-tactics",
             brief={"skill": "enrichment-acquisition-tactics", "skills_root": SKILLS_ROOT,
                    "inputs": [ctx.founder_input, ctx.comp, MENU, STYLE], "output": ctx.acq},
             web=True, timeout=T_RESEARCH, stage="enrichment:acquisition-tactics"),
    ]
    run_fanout(ctx, wave2, fanout_concurrency)

    # ---- Stage 2 — think-tanks x3 (structural only) ----------------------------------------
    log(f"Stage 2 — think-tanks x3 (pool concurrency={fanout_concurrency})")
    tt_inputs = [ctx.founder_input, ctx.comp, ctx.aud, ctx.acq]
    stage2 = [
        # platform-arbitrage first (slowest; only research one) so the analysis branches finish under it
        dict(worker="research-worker", output=ctx.pa, struct="think-tank:platform-arbitrage",
             brief={"skill": "platform-arbitrage", "skills_root": SKILLS_ROOT,
                    "inputs": tt_inputs + [MENU, STYLE], "output": ctx.pa},
             web=True, timeout=T_RESEARCH, stage="think-tank:platform-arbitrage"),
        dict(worker="analysis-worker", output=ctx.cg, struct="think-tank:competitor-gaps",
             brief={"skill": "competitor-gaps", "skills_root": SKILLS_ROOT,
                    "inputs": tt_inputs + [MENU, STYLE], "output": ctx.cg},
             web=False, timeout=T_ANALYSIS, stage="think-tank:competitor-gaps"),
        dict(worker="analysis-worker", output=ctx.ci, struct="think-tank:cross-industry",
             brief={"skill": "cross-industry", "skills_root": SKILLS_ROOT,
                    "inputs": tt_inputs + [STYLE], "output": ctx.ci},
             web=False, timeout=T_ANALYSIS, stage="think-tank:cross-industry"),
    ]
    run_fanout(ctx, stage2, fanout_concurrency)

    # ---- Stage 3 boundary — join + validate the mining branch -------------------------------
    if mining_handle is not None:
        log("Stage 3 boundary — joining growth-factors mining branch")
        join_growth_factors(ctx, mining_handle)
    gfc = checks.check_growth_factors(ctx.gf)
    if not gfc.ok:
        raise StageFailed("growth-factors-invalid", f"{gfc.issues}")
    log(f"  growth-factors OK — {gfc.info.get('vectors')} vectors, {gfc.info.get('category_counts')}")

    # ---- Stage 3 — lite-constraints (structural + xref) ------------------------------------
    log("Stage 3 — lite-constraints")
    def sc_struct(p):
        r = checks.check_constraints(p)
        return r.merge(checks.check_constraints_subset(p, ctx.gf, stage="lite-constraints"))
    ok, _d, chk = generate_blocking(
        ctx, "lite-constraints", "synthesis-worker",
        {"skill": "lite-constraints", "skills_root": SKILLS_ROOT,
         "inputs": [ctx.gf, ctx.founder_input], "output": ctx.sc},
        ctx.sc, sc_struct, web=False, timeout=T_SYNTHESIS)
    if not ok:
        raise StageFailed("constraints-invalid", f"{chk.issues}")

    # ---- Stage 4 — constraints-stale precheck (BLOCKING) -----------------------------------
    log("Stage 4 — constraints-stale precheck")
    stale = checks.check_constraints_subset(ctx.sc, ctx.gf, stage="constraints-stale")
    if not stale.ok:
        raise StageFailed("constraints-stale", f"{stale.issues}")

    # ---- Stage 4 — synthesis explore (structural + must_include A+B) ------------------------
    log("Stage 4 — synthesis explore")
    ok, _d, chk = generate_blocking(
        ctx, "synthesis:explore", "synthesis-worker",
        {"skill": "synthesis-explore", "skills_root": SKILLS_ROOT,
         "inputs": [ctx.founder_input, ctx.gf, ctx.sc, ctx.aud, ctx.ci, ctx.cg, ctx.pa],
         "output": ctx.explore},
        ctx.explore, lambda p: checks.check_synthesis_explore(p, ctx.sc, ctx.gf),
        web=False, timeout=T_SYNTHESIS)
    if not ok:
        raise StageFailed("explore-invalid", f"{chk.issues}")

    # ---- Stage 4 — synthesis build (reviewer-gated + must_include B) ------------------------
    log("Stage 4 — synthesis build (reviewer-gated)")
    reviewer_loop(
        ctx, "synthesis:build", "synthesis-worker",
        {"skill": "synthesis-build", "skills_root": SKILLS_ROOT,
         "inputs": [ctx.explore, ctx.sc, ctx.gf, ctx.founder_input, ctx.aud, ctx.comp,
                    ctx.cg, ctx.pa, ctx.ci, MENU, STYLE],
         "output": ctx.synth},
        ctx.synth, lambda p: checks.check_synthesis_build(p, ctx.sc, ctx.gf),
        web=False, timeout=T_SYNTHESIS,
        dimension="demand-gen-synthesis", spec_path=f"{SKILLS_ROOT}/synthesis-build/SKILL.md",
        context_paths=[ctx.gf, ctx.sc, ctx.founder_input, ctx.aud, ctx.comp, ctx.cg, ctx.ci, ctx.pa],
    )

    total_s = int(time.time()) - t0
    log(f"DONE — total wall-clock {total_s // 60}m{total_s % 60}s")
    return {"total_s": total_s}


# --------------------------------------------------------------------------------------------
# growth-factors helpers (mining is the priciest stage; resume_partial on a dead respawn)
# --------------------------------------------------------------------------------------------
def ensure_growth_factors(ctx: Ctx, *, inline_brief: dict):
    """Inline (sequential) mining with death-respawn + resume_partial; structural-check only."""
    d = None
    for death_try in range(3):
        brief = dict(inline_brief)
        if death_try > 0 and Path(ctx.gf).is_file():
            brief["resume_partial"] = True  # never re-pay for deep-research passes already done
        d = cd.dispatch("research-worker", brief, stage="growth-factors", attempt=death_try + 1,
                        web=True, timeout_s=T_MINING, **ctx.disp_kwargs())
        if d.classification == "ok":
            return
        log(f"  growth-factors: {d.classification}; fresh respawn {death_try + 1}/2 "
            f"({'resume_partial' if Path(ctx.gf).is_file() else 'fresh'})")
    raise StageFailed("growth-factors-invalid", "mining died after 2 respawns")


def join_growth_factors(ctx: Ctx, handle):
    """Finalize the background mining handle; respawn (resume_partial) up to 2x on death."""
    d = cd.finalize(handle)
    log(f"  growth-factors mining returned: {d.classification} ({d.duration_s}s)")
    if d.classification == "ok":
        return
    ensure_growth_factors(ctx, inline_brief={
        "skill": "growth-factors-mining", "skills_root": SKILLS_ROOT,
        "inputs": [ctx.founder_input, ctx.comp], "output": ctx.gf})


# --------------------------------------------------------------------------------------------
# Fan-out resolution (parallel launch, then per-branch structural fix-up)
# --------------------------------------------------------------------------------------------
def run_fanout(ctx: Ctx, specs: list[dict], concurrency: int) -> None:
    """Launch the fan-out in a sliding window, then ensure every branch is ok + structurally complete."""
    launch_specs = [
        dict(worker=s["worker"], brief=s["brief"], stage=s["stage"], attempt=1,
             web=s["web"], timeout_s=s["timeout"], **ctx.disp_kwargs())
        for s in specs
    ]
    results = cd.run_pool(launch_specs, concurrency=concurrency)
    by_stage = {d.stage: d for d in results}
    for s in specs:
        struct_fn = lambda p, st=s["struct"]: checks.check_markdown_stage(st, p)
        d = by_stage.get(s["stage"])
        chk = struct_fn(s["output"])
        if d is not None and d.classification == "ok" and chk.ok:
            log(f"  {s['stage']}: ok + structural pass")
            continue
        # not clean -> blocking redo with death/struct respawn (the spec's incomplete/died handling)
        log(f"  {s['stage']}: needs fix (cls={getattr(d, 'classification', 'none')}, struct={chk.ok}); redoing")
        ok, _d, chk = generate_blocking(ctx, s["stage"], s["worker"], s["brief"], s["output"],
                                        struct_fn, web=s["web"], timeout=s["timeout"])
        if not ok:
            raise StageFailed("dimension-failed", f"{s['stage']}: {chk.issues}")


# --------------------------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------------------------
def report(ctx: Ctx) -> None:
    # 1) HTML report layer — best-effort, never blocks/fails the report (also runs on the
    #    StageFailed path: render_workspace() renders whatever a partial run produced).
    index_path = None
    deliverables = []
    try:
        sys.path.insert(0, str(SCRIPTS))
        import render_html
        deliverables = [(title, ctx.ws / rel) for rel, title, _g, _d in render_html.MANIFEST]
        index_path = render_html.render_workspace(ctx.ws)
    except Exception as e:  # noqa: BLE001 — degrade to md paths, one line, no traceback
        log(f"HTML report skipped: {e}")

    # 2) deliverables first — the founder-facing part of the report
    print("\n" + "=" * 78)
    print(f"Growth Tactics — {ctx.ws.name}                                    (Codex / native web_search)")
    print("=" * 78)
    print("Your deliverables:")
    if not deliverables:  # render_html unavailable — fall back to the canonical md paths
        deliverables = [("Your Growth Tactics", Path(ctx.synth)),
                        ("Competitor Research", Path(ctx.comp)),
                        ("Audience Map", Path(ctx.aud)),
                        ("Acquisition Audit", Path(ctx.acq)),
                        ("Where Your Size Wins", Path(ctx.cg)),
                        ("Plays From Other Industries", Path(ctx.ci)),
                        ("Fresh Platform Openings", Path(ctx.pa))]
    for title, md_path in deliverables:
        html_path = ctx.ws / "report" / f"{title}.html"
        shown = html_path if html_path.is_file() else md_path
        if md_path.is_file():
            print(f"  {title:30} {shown}")
    if index_path:
        print(f"\nOpen it in your browser: {index_path}")

    # 3) the run ledger — Codex is driven by developers, so the timing table stays
    import json
    rows = []
    try:
        for line in Path(ctx.ledger).read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    except OSError:
        pass
    print(f"{'stage':38} {'verdict':12} {'dur':>6}  attempt")
    for r in rows:
        print(f"{r.get('stage', ''):38} {str(r.get('verdict', '')):12} "
              f"{str(r.get('duration_s', '')):>5}s  #{r.get('attempt', '')}")
    print("-" * 78)
    # final acceptance read
    bc = checks.check_synthesis_build(ctx.synth, ctx.sc, ctx.gf)
    gf = checks.check_growth_factors(ctx.gf)
    print(f"synthesis.md      : {'OK' if bc.ok else 'CHECK'}  "
          f"tactics={bc.info.get('tactics')}  vectors_cited={bc.info.get('vectors_cited')}  "
          f"phantom={len(bc.info.get('phantom', []))}  pool-B must_include "
          f"used={len(bc.info.get('used', []))} missing={len(bc.info.get('missing', []))}")
    print(f"growth-factors    : vectors={gf.info.get('vectors')}  categories={gf.info.get('category_counts')}")
    if not bc.ok:
        print(f"  build issues: {bc.issues}")
    print("=" * 78)
    print("\nThis is where the FREE pipeline stops — you have a portfolio of novel demand-gen tactic")
    print("IDEAS, generated by combining mechanisms from a per-run LIGHT growth database. The PAID")
    print("Diffmode adds prioritization, week-by-week implementation guides, and the proprietary")
    print("576-vector database + intelligence layer.")
    print(f"\nsynthesis.md -> {ctx.synth}")


# --------------------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Diffmode growth-tactics Codex MVP orchestrator")
    ap.add_argument("--product", help="workspace slug (./<slug>/)")
    ap.add_argument("--url", help="product URL — feeds Stage 0 intake; slug derived from host "
                                  "if --product absent")
    ap.add_argument("--fast-intake", action="store_true",
                    help="Stage 0: skip the founder Q&A and accept the researched prefill with "
                         "[NEEDS FOUNDER INPUT] placeholders (hands-off; lower quality)")
    ap.add_argument("--out-dir", default=".", help="directory that holds ./<slug>/ (default: cwd)")
    ap.add_argument("--max-concurrency", type=int, default=2)
    ap.add_argument("--backend", default="native", choices=["native"],
                    help="research backend (MVP: native web_search only; Perplexity OFF)")
    ap.add_argument("--model", default=None, help="override model (default: codex config, gpt-5.5)")
    args = ap.parse_args(argv)

    if not args.product and not args.url:
        ap.error("one of --product or --url is required")
    if not args.product:
        host = args.url.split("//")[-1].split("/")[0]
        args.product = host
    args.slug = args.product

    ctx = Ctx(args)
    try:
        run(ctx)
    except StageFailed as e:
        log(f"FAILED [{e.code}] {e.detail}")
        log(f"Resume from disk: re-run after fixing; outputs preserved in {ctx.ws}")
        report(ctx)
        return 2
    report(ctx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
