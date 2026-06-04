#!/usr/bin/env python3
"""The one impure boundary of the Codex orchestrator: dispatching a worker as a ``codex exec``.

Each worker is one ``codex exec`` invocation whose prompt INLINES the worker contract
(``codex/agents/<worker>.toml`` ``developer_instructions``) + a BRIEF block — because
``codex exec`` has no ``--agent`` flag (0.130/0.136), so custom-agent files are not dispatchable
by name. This module owns:

* extracting ``developer_instructions`` from a (possibly future-defective) ``.toml`` via regex,
  not ``tomllib`` — robust to TOML the parser would reject;
* assembling the exact, list-form argv per worker kind (research = web ON; everything else = web
  explicitly ``disabled`` for the clean-room guarantee);
* capturing the worker's final message with ``-o`` and recovering the ``{status,outputPath,…}``
  (or reviewer verdict) JSON via a brace-balanced scan from the END of that file;
* timing every call, appending a run-ledger row, and classifying the outcome
  (``ok`` / ``error`` / ``reviewed`` / ``rate_limited`` / ``died``);
* launch/poll/finalize + a sliding-window pool for the fan-out stages, with 429 backoff.

Nothing here interprets pipeline *content* — that is checks.py (deterministic) and the reviewer
worker (LLM). This module only moves bytes to and from ``codex exec``.
"""

from __future__ import annotations

import json
import random
import re
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

# Resolve the worker contracts next to this file (codex/agents/*.toml).
CODEX_DIR = Path(__file__).resolve().parent
AGENTS_DIR = CODEX_DIR / "agents"

# Worker kinds that get web access (the only one is research-worker).
WEB_WORKERS = {"research-worker"}

# Rate-limit signatures (R1). Detected in combined stdout+stderr+capture.
RATE_LIMIT_RE = re.compile(r"\b429\b|rate.?limit|too many requests|quota", re.IGNORECASE)


# --------------------------------------------------------------------------------------------
# Contract extraction (regex, NOT tomllib — robust to future TOML defects)
# --------------------------------------------------------------------------------------------
_DEV_INSTR_RE = re.compile(
    r'developer_instructions\s*=\s*"""(?P<body>.*?)"""',
    re.DOTALL,
)


def developer_instructions(worker: str) -> str:
    """Return the ``developer_instructions = \"\"\"…\"\"\"`` body from codex/agents/<worker>.toml."""
    toml_path = AGENTS_DIR / f"{worker}.toml"
    text = toml_path.read_text(encoding="utf-8")
    m = _DEV_INSTR_RE.search(text)
    if not m:
        raise ValueError(f"could not extract developer_instructions from {toml_path}")
    return m.group("body").strip()


# --------------------------------------------------------------------------------------------
# Brace-balanced JSON recovery (scan from the END; tolerate a leaked sentence)
# --------------------------------------------------------------------------------------------
def last_json_object(text: str) -> dict | None:
    """Return the LAST top-level ``{...}`` object in ``text`` that parses, else None.

    Scans forward tracking string state + brace depth to record every depth 0->0 span, then
    parses candidates from last to first. This recovers the worker's final summary JSON even if
    a stray sentence leaked before/after it (R2)."""
    spans: list[tuple[int, int]] = []
    depth = 0
    start = -1
    in_str = False
    escape = False
    for i, ch in enumerate(text):
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start >= 0:
                    spans.append((start, i + 1))
    for s, e in reversed(spans):
        try:
            obj = json.loads(text[s:e])
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue
    return None


# alias matching the plan's wording (it scans for the worker's final object)
_first_json_object = last_json_object


# --------------------------------------------------------------------------------------------
# Prompt assembly
# --------------------------------------------------------------------------------------------
def _render_brief(brief: dict) -> str:
    """Render the BRIEF block the worker .toml <task> expects, in a stable, readable order."""
    lines = ["=== BRIEF (from the orchestrator) ==="]
    order = [
        "skill", "skills_root", "dimension", "spec_path",
        "inputs", "context_paths", "output", "output_path",
        "blocking_issues", "retry_mode", "resume_partial", "remine", "notes",
    ]
    seen = set()
    for key in order + [k for k in brief if k not in order]:
        if key in seen or key not in brief:
            continue
        seen.add(key)
        val = brief[key]
        if val is None or val == [] or val == "":
            continue
        if isinstance(val, list):
            lines.append(f"{key}:")
            for item in val:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {val}")
    return "\n".join(lines)


def build_prompt(worker: str, brief: dict) -> str:
    """Inline-contract prompt = the worker's developer_instructions + the rendered BRIEF."""
    instr = developer_instructions(worker)
    skills_root = brief.get("skills_root")
    skill_hint = ""
    if brief.get("skill") and skills_root:
        skill_hint = (
            f"\n\nRead the skill from the ABSOLUTE path "
            f"`{skills_root}/{brief['skill']}/SKILL.md` (the .agents/skills symlink farm). "
            f"All other paths in the brief are absolute too."
        )
    if brief.get("dimension") and skills_root:
        skill_hint = (
            f"\n\nLoad the reviewer skill from `{skills_root}/growth-reviewer/SKILL.md` and the "
            f"dimension rubric from `{skills_root}/growth-reviewer/references/{brief['dimension']}.md`."
        )
    return f"{instr}{skill_hint}\n\n{_render_brief(brief)}\n"


# --------------------------------------------------------------------------------------------
# argv assembly (list form — never a shell string)
# --------------------------------------------------------------------------------------------
def build_argv(
    worker: str,
    *,
    ws_parent: str | Path,
    capture_path: str | Path,
    model: str | None = None,
    web: bool | None = None,
) -> list[str]:
    """Exact ``codex exec`` argv for a worker. ``web`` defaults to (worker in WEB_WORKERS)."""
    if web is None:
        web = worker in WEB_WORKERS
    argv = [
        "codex", "exec",
        "-C", str(ws_parent),
        "--skip-git-repo-check",
        "--sandbox", "workspace-write",
    ]
    if web:
        argv += [
            "-c", 'web_search="live"',
            "-c", "sandbox_workspace_write.network_access=true",
        ]
    else:
        # Clean-room guarantee (R8): native web_search defaults to `cached` (web!), so disable it
        # EXPLICITLY — "no mcp_servers" alone is insufficient on Codex.
        argv += ["-c", 'web_search="disabled"']
    if model:
        argv += ["-m", model]
    argv += ["-o", str(capture_path), "-"]  # `-` => read the prompt from stdin
    return argv


# --------------------------------------------------------------------------------------------
# Ledger
# --------------------------------------------------------------------------------------------
def append_ledger(ledger_path: str | Path, row: dict) -> None:
    """Append one JSON-lines row to the workspace-local run ledger (best-effort)."""
    try:
        with open(ledger_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except OSError:
        pass


# --------------------------------------------------------------------------------------------
# Handle + finalize
# --------------------------------------------------------------------------------------------
@dataclass
class Dispatch:
    """A launched (or completed) worker invocation."""

    worker: str
    stage: str
    attempt: int
    argv: list[str]
    prompt: str
    capture_path: Path
    stderr_path: Path
    ledger_path: Path
    timeout_s: int
    started_at: int
    proc: subprocess.Popen | None = None
    # filled by finalize():
    rc: int | None = None
    duration_s: int | None = None
    classification: str | None = None
    result_json: dict | None = None
    verdict: str | None = None
    score: float | None = None
    info: dict = field(default_factory=dict)

    def is_done(self) -> bool:
        return self.proc is not None and self.proc.poll() is not None


def launch(
    worker: str,
    brief: dict,
    *,
    stage: str,
    attempt: int,
    ws_parent: str | Path,
    capture_dir: str | Path,
    ledger_path: str | Path,
    model: str | None = None,
    web: bool | None = None,
    timeout_s: int = 1500,
) -> Dispatch:
    """Start a worker as a background ``codex exec`` (does NOT wait). Use :func:`finalize` to reap."""
    capture_dir = Path(capture_dir)
    capture_dir.mkdir(parents=True, exist_ok=True)
    capture_path = capture_dir / f"{stage.replace(':', '_')}.{attempt}.json"
    stderr_path = capture_dir / f"{stage.replace(':', '_')}.{attempt}.stderr.log"
    # A fresh capture file each attempt (stale content would poison the JSON scan).
    if capture_path.exists():
        capture_path.unlink()

    prompt = build_prompt(worker, brief)
    argv = build_argv(worker, ws_parent=ws_parent, capture_path=capture_path, model=model, web=web)
    started_at = int(time.time())

    stderr_f = open(stderr_path, "w", encoding="utf-8")
    proc = subprocess.Popen(
        argv,
        stdin=subprocess.PIPE,
        stdout=stderr_f,   # codex exec event log goes here (we only consume the -o capture)
        stderr=subprocess.STDOUT,
        text=True,
    )
    # Hand the prompt over stdin, then close it so the worker can start.
    assert proc.stdin is not None
    try:
        proc.stdin.write(prompt)
        proc.stdin.close()
    except BrokenPipeError:
        pass

    return Dispatch(
        worker=worker, stage=stage, attempt=attempt, argv=argv, prompt=prompt,
        capture_path=capture_path, stderr_path=stderr_path, ledger_path=Path(ledger_path),
        timeout_s=timeout_s, started_at=started_at, proc=proc,
    )


def finalize(d: Dispatch) -> Dispatch:
    """Reap a launched Dispatch: wait (with timeout), parse the capture, classify, ledger."""
    assert d.proc is not None
    try:
        d.rc = d.proc.wait(timeout=max(1, d.timeout_s - (int(time.time()) - d.started_at)))
    except subprocess.TimeoutExpired:
        d.proc.kill()
        d.proc.wait()
        d.rc = -9
    d.duration_s = int(time.time()) - d.started_at

    capture_text = ""
    if d.capture_path.exists():
        capture_text = d.capture_path.read_text(encoding="utf-8", errors="replace")
    stderr_text = ""
    if d.stderr_path.exists():
        stderr_text = d.stderr_path.read_text(encoding="utf-8", errors="replace")[-4000:]

    combined = capture_text + "\n" + stderr_text
    d.result_json = last_json_object(capture_text)

    # Classify.
    if d.rc == -9:
        d.classification = "died"  # timeout
    elif RATE_LIMIT_RE.search(combined) and d.result_json is None:
        d.classification = "rate_limited"
    elif d.result_json is None:
        d.classification = "died"  # no recoverable JSON / hard failure
    elif "verdict" in d.result_json:
        d.classification = "reviewed"
        d.verdict = d.result_json.get("verdict")
        score = d.result_json.get("score")
        d.score = float(score) if isinstance(score, (int, float)) else None
    elif d.result_json.get("status") == "ok":
        d.classification = "ok"
    elif d.result_json.get("status") == "error":
        d.classification = "error"
    else:
        d.classification = "died"

    append_ledger(d.ledger_path, {
        "stage": d.stage,
        "attempt": d.attempt,
        "worker": d.worker,
        "verdict": d.verdict or d.classification,
        "score": d.score,
        "started_at": d.started_at,
        "duration_s": d.duration_s,
        "rc": d.rc,
        "classification": d.classification,
        "output": (d.result_json or {}).get("outputPath"),
        "summary": (d.result_json or {}).get("summary") or (d.result_json or {}).get("reason"),
    })
    return d


# --------------------------------------------------------------------------------------------
# Blocking dispatch (with 429 backoff) — the common path
# --------------------------------------------------------------------------------------------
def dispatch(
    worker: str,
    brief: dict,
    *,
    stage: str,
    attempt: int = 1,
    ws_parent: str | Path,
    capture_dir: str | Path,
    ledger_path: str | Path,
    model: str | None = None,
    web: bool | None = None,
    timeout_s: int = 1500,
    rate_limit_retries: int = 4,
) -> Dispatch:
    """Launch + wait + finalize one worker. On ``rate_limited``, backoff+jitter and respawn."""
    backoff = 20.0
    for rl in range(rate_limit_retries + 1):
        d = finalize(launch(
            worker, brief, stage=stage, attempt=attempt, ws_parent=ws_parent,
            capture_dir=capture_dir, ledger_path=ledger_path, model=model, web=web, timeout_s=timeout_s,
        ))
        if d.classification != "rate_limited" or rl == rate_limit_retries:
            return d
        sleep_s = backoff + random.uniform(0, backoff / 2)
        print(f"    [{stage}] rate-limited; backoff {sleep_s:.0f}s then respawn ({rl + 1}/{rate_limit_retries})")
        time.sleep(sleep_s)
        backoff *= 2
    return d  # unreachable, keeps type-checkers happy


# --------------------------------------------------------------------------------------------
# Sliding-window pool for fan-outs (think-tanks, Wave-2 enrichment)
# --------------------------------------------------------------------------------------------
def run_pool(specs: Sequence[dict], *, concurrency: int, poll_s: float = 5.0) -> list[Dispatch]:
    """Run a list of dispatch specs with a sliding window of ``concurrency``.

    Each spec is a kwargs dict for :func:`launch` plus a ``brief`` and ``worker``. Results are
    returned in the SAME ORDER as ``specs``. Rate-limited members are respawned once with backoff.
    """
    concurrency = max(1, concurrency)
    results: list[Dispatch | None] = [None] * len(specs)
    pending = list(range(len(specs)))
    running: dict[int, Dispatch] = {}
    rl_count: dict[int, int] = {}   # rate-limit respawns per member (capped)
    rl_cap = 2

    def _launch(idx: int) -> Dispatch:
        spec = dict(specs[idx])
        worker = spec.pop("worker")
        brief = spec.pop("brief")
        return launch(worker, brief, **spec)

    while pending or running:
        while pending and len(running) < concurrency:
            idx = pending.pop(0)
            running[idx] = _launch(idx)
            print(f"    launched [{running[idx].stage}] ({len(running)} running)")
        done_now = [idx for idx, d in running.items() if d.is_done()]
        for idx in done_now:
            d = finalize(running.pop(idx))
            if d.classification == "rate_limited" and rl_count.get(idx, 0) < rl_cap:
                # backoff + jitter, then respawn (capped — persistent 429 falls through to the
                # post-pool blocking fix-up, which has full exponential backoff)
                rl_count[idx] = rl_count.get(idx, 0) + 1
                time.sleep(20 * rl_count[idx] + random.uniform(0, 10))
                running[idx] = _launch(idx)
                print(f"    re-launched [{d.stage}] after rate-limit ({rl_count[idx]}/{rl_cap})")
            else:
                results[idx] = d
                print(f"    finished  [{d.stage}] -> {d.classification} ({d.duration_s}s)")
        if running and not done_now:
            time.sleep(poll_s)

    return [r for r in results if r is not None]


# --------------------------------------------------------------------------------------------
# CLI smoke (python3 codex_dispatch.py self-check) — argv + prompt assembly only, no Codex call
# --------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    print("== developer_instructions extraction ==")
    for w in ("research-worker", "analysis-worker", "synthesis-worker", "reviewer-worker"):
        body = developer_instructions(w)
        print(f"  {w}: {len(body)} chars, starts: {body[:60]!r}")

    print("\n== argv (research = web ON) ==")
    print("  " + " ".join(build_argv("research-worker", ws_parent="/tmp/ws", capture_path="/tmp/ws/x.json")))
    print("== argv (analysis = web disabled) ==")
    print("  " + " ".join(build_argv("analysis-worker", ws_parent="/tmp/ws", capture_path="/tmp/ws/x.json")))

    print("\n== last_json_object recovery (leaked sentence) ==")
    sample = 'Here is my answer.\n{"status": "ok", "outputPath": "/x.md", "summary": "7 competitors"}\nDone!'
    print("  ", last_json_object(sample))
    sample2 = 'noise {"a":1} more noise {"verdict":"APPROVED","score":8} trailing'
    print("  ", last_json_object(sample2))
    assert last_json_object(sample)["status"] == "ok"
    assert last_json_object(sample2)["verdict"] == "APPROVED"

    print("\n== prompt assembly (reviewer) ==")
    p = build_prompt("reviewer-worker", {
        "dimension": "competitors", "skills_root": "/abs/.agents/skills",
        "spec_path": "/abs/skills/enrichment-competitors/SKILL.md",
        "output_path": "/ws/competitors-analysis.md", "context_paths": ["/ws/founder-input.md"],
    })
    print("  prompt length:", len(p), "| contains rubric path:", "references/competitors.md" in p)
    print("\nOK")
    sys.exit(0)
