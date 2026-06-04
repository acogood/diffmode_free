#!/usr/bin/env python3
"""Pure, deterministic structural checks for the Diffmode growth-tactics Codex orchestrator.

NO Codex calls, NO network — just file reads + parsing. This is the highest-value unit-test
surface and the spine of the orchestrator's quality gates (it decides whether a worker output
is "complete" before a reviewer is ever paid). Every function here is referenced from
`orchestrate.py`; the ``__main__`` block is a self-test harness (`python3 checks.py`).

Design notes
------------
* Markdown completeness is checked against each skill's **OUTPUT TEMPLATE** (the contract),
  NOT the SKILL.md's own doc headers, and NOT a particular run's quirks. Anchors are matched as
  *case-insensitive substrings of a heading line* so they tolerate skill drift such as
  ``## Section 5: Research Limitations`` (an older platform-arbitrage run) vs the current
  ``## Research Limitations`` — both contain "research limitations".
* Headings inside fenced code blocks (```` ``` ````/``` ~~~ ```) are ignored, so an output that
  quotes a template or shell snippet does not trip the heading scan.
* The completeness anchor for each markdown stage is its **last written content section** — the
  section before the worker-only ``## Calibration`` / ``## Validation`` / ``## Before you
  return`` instruction blocks, which most workers do not write into the output file. A worker
  that died mid-write will not have reached the anchor, which is exactly what we want to catch.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

# A growth-factor / vector id, e.g. ``lever-004-organic-fan-formalization``. The six category
# prefixes match the keys in ``growth-factors.json`` -> ``metadata.category_counts``.
VECTOR_ID_RE = re.compile(r"(?:struct|lever|resource|psych|pos|conv)-\d+-[a-z0-9-]+")
VECTOR_ID_ANCHORED_RE = re.compile(r"^(?:struct|lever|resource|psych|pos|conv)-\d+-[a-z0-9-]+$")

# Required keys on every vector in growth-factors.json (per run-growth-tactics.md Stage 3).
GROWTH_FACTOR_REQUIRED_KEYS = (
    "vector_id",
    "category",
    "mechanism",
    "transferability",
    "saturation_risk",
    "examples",
    "source_url",
)

# Block delimiters for the block-level ``must_include`` co-occurrence test.
COMBINATION_BLOCK_RE = re.compile(r"^Combination\s+#\d+")  # synthesis-explore.md
TACTIC_BLOCK_RE = re.compile(r"^Tactic\s+#\d+")            # synthesis.md (excludes "### #N:" anti-portfolio)


# --------------------------------------------------------------------------------------------
# Result type
# --------------------------------------------------------------------------------------------
@dataclass
class CheckResult:
    """The verdict of one structural check. ``ok`` gates the DAG; ``issues`` feed a retry brief."""

    ok: bool
    stage: str
    issues: list[str] = field(default_factory=list)
    info: dict = field(default_factory=dict)

    def __bool__(self) -> bool:  # so ``if result:`` reads naturally
        return self.ok

    def merge(self, other: "CheckResult") -> "CheckResult":
        """Fold another result in (AND the ``ok``, concatenate issues, merge info)."""
        return CheckResult(
            ok=self.ok and other.ok,
            stage=self.stage,
            issues=self.issues + other.issues,
            info={**self.info, **other.info},
        )

    def as_dict(self) -> dict:
        return {"ok": self.ok, "stage": self.stage, "issues": self.issues, "info": self.info}


# --------------------------------------------------------------------------------------------
# Low-level helpers
# --------------------------------------------------------------------------------------------
def read_text(path: str | Path) -> str | None:
    """Read a UTF-8 file, returning None if it is missing (the caller turns None into an issue)."""
    p = Path(path)
    if not p.is_file():
        return None
    return p.read_text(encoding="utf-8", errors="replace")


def headings(text: str) -> list[tuple[int, str, int]]:
    """Return ``(level, heading_text, lineno)`` for every ATX heading OUTSIDE fenced code.

    ``lineno`` is 1-based. ``heading_text`` is stripped of the leading ``#``s and surrounding
    whitespace (so ``## Research Limitations`` -> ``"Research Limitations"``).
    """
    out: list[tuple[int, str, int]] = []
    in_fence = False
    fence_tok = ""
    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            tok = stripped[:3]
            if not in_fence:
                in_fence, fence_tok = True, tok
            elif stripped.startswith(fence_tok):
                in_fence, fence_tok = False, ""
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*\S)\s*$", line)
        if m:
            out.append((len(m.group(1)), m.group(2).strip(), i))
    return out


def heading_line(hs: Sequence[tuple[int, str, int]], anchor: str) -> int | None:
    """First line number of a heading whose text contains ``anchor`` (case-insensitive), else None."""
    a = anchor.lower()
    for _, text, ln in hs:
        if a in text.lower():
            return ln
    return None


def has_heading(hs: Sequence[tuple[int, str, int]], anchor: str) -> bool:
    return heading_line(hs, anchor) is not None


def heading_order_ok(hs: Sequence[tuple[int, str, int]], first: str, second: str) -> bool:
    """True iff a heading containing ``first`` exists and precedes one containing ``second``."""
    l1 = heading_line(hs, first)
    l2 = heading_line(hs, second)
    return l1 is not None and l2 is not None and l1 < l2


def nonblank_line_count(text: str) -> int:
    return sum(1 for ln in text.splitlines() if ln.strip())


def split_blocks(text: str, header_text_re: re.Pattern) -> list[tuple[str, str]]:
    """Split markdown into ``(header_text, block_body)`` for each heading matching ``header_text_re``.

    A block runs from its header line until the next heading of the SAME-or-shallower level
    (so a ``### Tactic #2`` or any ``## …`` ends a ``### Tactic #1`` block, but a ``#### …``
    sub-heading stays inside it). Fence-aware via :func:`headings`.
    """
    hs = headings(text)
    lines = text.splitlines()
    blocks: list[tuple[str, str]] = []
    for idx, (level, htext, ln) in enumerate(hs):
        if not header_text_re.search(htext):
            continue
        end = len(lines)  # default: to EOF
        for level2, _h2, ln2 in hs[idx + 1:]:
            if level2 <= level:
                end = ln2 - 1
                break
        body = "\n".join(lines[ln - 1:end])
        blocks.append((htext, body))
    return blocks


def vector_ids_in(text: str) -> set[str]:
    """All vector ids appearing in a chunk of text (with or without backticks)."""
    return set(VECTOR_ID_RE.findall(text))


# --------------------------------------------------------------------------------------------
# Generic markdown completeness check
# --------------------------------------------------------------------------------------------
def check_markdown(
    path: str | Path,
    stage: str,
    *,
    anchors: Iterable[str] = (),
    order_pairs: Iterable[tuple[str, str]] = (),
    forbid_headings: Iterable[str] = (),
    min_lines: int = 0,
) -> CheckResult:
    """Completeness check for a markdown stage output.

    * ``anchors`` — each must be present as a heading (catches truncation / mid-write death).
    * ``order_pairs`` — ``(a, b)`` heading ordering walls (e.g. blind-draw precedes combinations).
    * ``forbid_headings`` — headings that must NOT appear (e.g. a build-only section in explore).
    * ``min_lines`` — non-blank line floor (a second, cheap truncation signal).
    """
    text = read_text(path)
    if text is None:
        return CheckResult(False, stage, [f"output missing: {path}"])
    if not text.strip():
        return CheckResult(False, stage, [f"output empty: {path}"])

    issues: list[str] = []
    hs = headings(text)
    nb = nonblank_line_count(text)

    for a in anchors:
        if not has_heading(hs, a):
            issues.append(f"missing required section heading containing '{a}' (truncated/incomplete?)")
    for a, b in order_pairs:
        if not heading_order_ok(hs, a, b):
            issues.append(f"section ordering broken: '{a}' must appear before '{b}'")
    for a in forbid_headings:
        if has_heading(hs, a):
            issues.append(f"forbidden section present: heading containing '{a}' (leak from another stage)")
    if nb < min_lines:
        issues.append(f"too short: {nb} non-blank lines < floor {min_lines} (truncated?)")

    return CheckResult(not issues, stage, issues, info={"nonblank_lines": nb, "headings": len(hs)})


# --------------------------------------------------------------------------------------------
# Per-stage markdown anchors (derived from each skill's OUTPUT TEMPLATE; see module docstring)
# --------------------------------------------------------------------------------------------
# Non-blank line floors are a SECONDARY backstop only — they catch a pathologically near-empty
# fragment. The LAST-section anchor (+ ordering walls) is the PRIMARY non-truncation signal: a
# file whose final required section is present cannot have died mid-write. Codex/gpt-5.5 writes
# markedly more compactly than the Claude/theona-lite3 fixtures (a complete audience analysis with
# all 4 segments + evaluations came in at 39 non-blank lines), so floors are set low enough never
# to false-positive on a complete-but-terse output while still flagging a near-empty stub.
MARKDOWN_STAGES: dict[str, dict] = {
    # enrichment-competitors: ends at "## Research Limitations" (then worker-only "## Calibration")
    "enrichment:competitors": {
        "anchors": ["Competitive Channel Matrix", "Research Limitations"],
        "min_lines": 35,
    },
    # enrichment-audience: ends at "## Segment Evaluation Summary" (then "## Calibration")
    "enrichment:audience": {
        "anchors": ["Customer Segments", "Segment Evaluation Summary"],
        "min_lines": 20,
    },
    # enrichment-acquisition-tactics: last content section is "## Research Sources"
    # (note: "Research Limitations" appears near the TOP here, so it is NOT the completeness anchor)
    "enrichment:acquisition-tactics": {
        "anchors": ["Tactics Summary Dashboard", "Research Sources"],
        "min_lines": 45,
    },
    # platform-arbitrage (research-worker): ends at "## Research Limitations"
    # (older runs numbered it "## Section 5: Research Limitations" -> substring match handles both)
    "think-tank:platform-arbitrage": {
        "anchors": ["Platform Audit Results", "Research Limitations"],
        "min_lines": 35,
    },
    # competitor-gaps (analysis): "## Executive Summary" is written LAST (after the 3 tiers)
    "think-tank:competitor-gaps": {
        "anchors": ["Tier 1", "Tier 3", "Executive Summary"],
        "min_lines": 30,
    },
    # cross-industry (analysis mode): "## Research Sources" is research-mode-only, so the last
    # guaranteed section is "## Controversial / Aggressive Tactics Worth Noting"
    "think-tank:cross-industry": {
        "anchors": ["Cross-Industry Case Studies", "Transferable Patterns", "Controversial"],
        "min_lines": 35,
    },
}


def check_markdown_stage(stage: str, path: str | Path) -> CheckResult:
    """Run the registered completeness check for a known markdown stage name."""
    if stage not in MARKDOWN_STAGES:
        raise KeyError(f"no markdown check registered for stage '{stage}'")
    cfg = MARKDOWN_STAGES[stage]
    return check_markdown(
        path,
        stage,
        anchors=cfg.get("anchors", ()),
        order_pairs=cfg.get("order_pairs", ()),
        forbid_headings=cfg.get("forbid_headings", ()),
        min_lines=cfg.get("min_lines", 0),
    )


# --------------------------------------------------------------------------------------------
# growth-factors.json (LIGHT DB) — schema + clean-room structural check
# --------------------------------------------------------------------------------------------
def load_json(path: str | Path) -> tuple[dict | list | None, str | None]:
    text = read_text(path)
    if text is None:
        return None, f"file missing: {path}"
    try:
        return json.loads(text), None
    except json.JSONDecodeError as e:
        return None, f"invalid JSON ({e})"


def growth_factor_ids(gf: dict) -> set[str]:
    return {
        v["vector_id"]
        for v in gf.get("vectors", [])
        if isinstance(v, dict) and isinstance(v.get("vector_id"), str)
    }


def check_growth_factors(path: str | Path, *, min_vectors: int = 15, max_vectors: int = 40) -> CheckResult:
    """Structural + schema check for the per-run LIGHT vector DB.

    The orchestrator's structural gate is 15-40 (run-growth-tactics.md Stage 3); the *acceptance*
    target is the tighter 20-40 — the count is returned in ``info`` so the A/B report can apply
    the tighter bar separately.
    """
    stage = "growth-factors"
    obj, err = load_json(path)
    if err:
        return CheckResult(False, stage, [err])
    if not isinstance(obj, dict):
        return CheckResult(False, stage, ["growth-factors.json is not a JSON object"])

    issues: list[str] = []
    meta = obj.get("metadata", {}) if isinstance(obj.get("metadata"), dict) else {}
    vectors = obj.get("vectors")
    if not isinstance(vectors, list) or not vectors:
        return CheckResult(False, stage, ["'vectors' missing or empty"])

    n = len(vectors)
    total = meta.get("total_vectors")
    if total != n:
        issues.append(f"metadata.total_vectors ({total}) != len(vectors) ({n})")
    if not (min_vectors <= n <= max_vectors):
        issues.append(f"vector count {n} outside {min_vectors}-{max_vectors}")

    # category_counts sums to total and no prefix exceeds ~60%
    cc = meta.get("category_counts")
    if not isinstance(cc, dict) or not cc:
        issues.append("metadata.category_counts missing")
    else:
        s = sum(v for v in cc.values() if isinstance(v, (int, float)))
        if s != n:
            issues.append(f"category_counts sum ({s}) != vector count ({n})")
        for prefix, count in cc.items():
            if isinstance(count, (int, float)) and n and count / n > 0.6 + 1e-9:
                issues.append(f"category '{prefix}' is {count}/{n} = {count / n:.0%} of vectors (>60%)")

    # per-vector schema + clean-room (real http(s) source_url)
    bad_ids: list[str] = []
    missing_keys = 0
    bad_urls = 0
    empty_examples = 0
    for v in vectors:
        if not isinstance(v, dict):
            issues.append("a vector entry is not an object")
            continue
        vid = v.get("vector_id", "")
        if not (isinstance(vid, str) and VECTOR_ID_ANCHORED_RE.match(vid)):
            bad_ids.append(str(vid))
        for k in GROWTH_FACTOR_REQUIRED_KEYS:
            if k not in v:
                missing_keys += 1
        url = v.get("source_url")
        if not (isinstance(url, str) and re.match(r"^https?://", url)):
            bad_urls += 1
        ex = v.get("examples")
        if not (isinstance(ex, list) and ex):
            empty_examples += 1

    if bad_ids:
        issues.append(f"{len(bad_ids)} vector_id(s) not matching {{prefix}}-NNN-slug, e.g. {bad_ids[:3]}")
    if missing_keys:
        issues.append(f"{missing_keys} missing required key(s) across vectors {GROWTH_FACTOR_REQUIRED_KEYS}")
    if bad_urls:
        issues.append(f"{bad_urls} vector(s) without a real http(s) source_url (clean-room/citation gap)")
    if empty_examples:
        issues.append(f"{empty_examples} vector(s) with empty 'examples'")

    return CheckResult(
        not issues,
        stage,
        issues,
        info={"vectors": n, "category_counts": cc if isinstance(cc, dict) else {}},
    )


# --------------------------------------------------------------------------------------------
# synthesis-constraints.json — schema check + vector-id cross-reference
# --------------------------------------------------------------------------------------------
def constraints_referenced_ids(constraints: dict) -> set[str]:
    """Every vector id referenced anywhere in synthesis-constraints.json.

    These are the ids the Stage-3 cross-reference and the Stage-4 ``constraints-stale`` precheck
    confirm against the CURRENT growth-factors.json.
    """
    ids: set[str] = set()
    for item in constraints.get("diverse_white_space", []) or []:
        ids.update(item.get("vectors", []) or [])
    for item in constraints.get("mandatory_combinations", []) or []:
        ids.update(item.get("vectors", []) or [])
    for item in constraints.get("prohibited_combinations", []) or []:
        ids.update(item.get("vectors_if_present", []) or [])
    for item in constraints.get("unconventional_anchors", []) or []:
        if isinstance(item.get("vector"), str):
            ids.add(item["vector"])
        ids.update(item.get("good_partners", []) or [])
        ids.update(item.get("avoid_partners", []) or [])
    return {i for i in ids if isinstance(i, str) and i}


def must_include_pairs(constraints: dict, pools: Sequence[str]) -> list[tuple[str, str]]:
    """The ``must_include`` vector pairs from the named ``mandatory_combinations`` pools.

    explore enforces pools A+B (``A_white_space``, ``B_synergy``); build enforces Pool B only.
    Only 2-id pairs are returned (the co-occurrence test is defined on pairs).
    """
    pairs: list[tuple[str, str]] = []
    for item in constraints.get("mandatory_combinations", []) or []:
        if item.get("pool") in pools:
            vs = [v for v in (item.get("vectors") or []) if isinstance(v, str)]
            if len(vs) >= 2:
                pairs.append((vs[0], vs[1]))
    return pairs


def check_constraints(path: str | Path) -> CheckResult:
    """Schema check for synthesis-constraints.json (does NOT need growth-factors.json)."""
    stage = "lite-constraints"
    obj, err = load_json(path)
    if err:
        return CheckResult(False, stage, [err])
    if not isinstance(obj, dict):
        return CheckResult(False, stage, ["synthesis-constraints.json is not a JSON object"])

    issues: list[str] = []

    dws = obj.get("diverse_white_space")
    if not isinstance(dws, list) or len(dws) < 5:
        issues.append(f"diverse_white_space has <5 pairs ({len(dws) if isinstance(dws, list) else 'missing'})")

    pools = {item.get("pool") for item in obj.get("mandatory_combinations", []) or []}
    for required in ("A_white_space", "B_synergy", "C_founder_fit"):
        if required not in pools:
            issues.append(f"mandatory_combinations missing pool '{required}'")

    prohibited = obj.get("prohibited_combinations")
    if not isinstance(prohibited, list) or len(prohibited) < 5:
        issues.append(
            f"prohibited_combinations has <5 generic patterns "
            f"({len(prohibited) if isinstance(prohibited, list) else 'missing'})"
        )

    cdr = obj.get("category_diversity_requirements", {})
    if not isinstance(cdr, dict) or cdr.get("max_single_category_pct") != 60:
        issues.append("category_diversity_requirements.max_single_category_pct != 60")

    if "anti_patterns" not in obj:
        issues.append("anti_patterns missing (clean-room replacement for the proprietary anti-vectors DB)")

    return CheckResult(
        not issues,
        stage,
        issues,
        info={
            "white_space_pairs": len(dws) if isinstance(dws, list) else 0,
            "must_include_AB": len(must_include_pairs(obj, ("A_white_space", "B_synergy"))),
        },
    )


def check_constraints_subset(constraints_path: str | Path, gf_path: str | Path, *, stage: str = "constraints-xref") -> CheckResult:
    """Confirm every vector id referenced by the constraints exists in the CURRENT growth-factors.

    Used twice: the Stage-3 cross-reference (constraints just built) and the Stage-4
    ``constraints-stale`` precheck (catches ``--remine`` without rebuilding constraints).
    """
    constraints, e1 = load_json(constraints_path)
    gf, e2 = load_json(gf_path)
    if e1:
        return CheckResult(False, stage, [f"constraints: {e1}"])
    if e2:
        return CheckResult(False, stage, [f"growth-factors: {e2}"])
    if not isinstance(constraints, dict) or not isinstance(gf, dict):
        return CheckResult(False, stage, ["constraints or growth-factors not a JSON object"])

    referenced = constraints_referenced_ids(constraints)
    available = growth_factor_ids(gf)
    missing = sorted(referenced - available)
    if missing:
        return CheckResult(
            False,
            stage,
            [
                f"{len(missing)} vector id(s) referenced in constraints absent from current "
                f"growth-factors.json: {missing[:5]}{'…' if len(missing) > 5 else ''}"
            ],
            info={"referenced": len(referenced), "missing": missing},
        )
    return CheckResult(True, stage, info={"referenced": len(referenced)})


# --------------------------------------------------------------------------------------------
# Block-level must_include co-occurrence (the Bug-C hardening)
# --------------------------------------------------------------------------------------------
def check_must_include_blocks(
    md_path: str | Path,
    constraints_path: str | Path,
    gf_path: str | Path,
    *,
    block_re: re.Pattern,
    pools: Sequence[str],
    stage: str,
) -> CheckResult:
    """Enforce that each ``must_include`` pair is *validly used* or *validly substituted*.

    Validly used  = BOTH of the pair's ids appear inside a SINGLE block (``### Combination #N``
                    in explore, ``### Tactic #N`` in build) — not merely somewhere in the file.
    Validly subst = a line mentioning "substitut…" that names >=1 id of the pair AND names a
                    replacement id that EXISTS in growth-factors.json (validity, not just the
                    word "substituted").
    """
    text = read_text(md_path)
    if text is None:
        return CheckResult(False, stage, [f"output missing: {md_path}"])
    constraints, e1 = load_json(constraints_path)
    gf, e2 = load_json(gf_path)
    if e1 or e2:
        return CheckResult(False, stage, [e1 or "", e2 or ""])

    pairs = must_include_pairs(constraints, pools)
    if not pairs:
        return CheckResult(True, stage, info={"pairs": 0, "note": "no must_include pairs in those pools"})

    gf_ids = growth_factor_ids(gf)
    blocks = split_blocks(text, block_re)
    block_idsets = [vector_ids_in(body) for _h, body in blocks]

    # Substitution notes: any line mentioning "substitut" + the vector ids named on that line.
    subst_lines: list[set[str]] = []
    for line in text.splitlines():
        if "substitut" in line.lower():
            subst_lines.append(vector_ids_in(line))

    used: list[str] = []
    substituted: list[str] = []
    missing: list[str] = []

    for a, b in pairs:
        pair_label = f"{a}+{b}"
        if any(a in s and b in s for s in block_idsets):
            used.append(pair_label)
            continue
        validly_subst = False
        for ids_on_line in subst_lines:
            names_pair = (a in ids_on_line) or (b in ids_on_line)
            replacement = ids_on_line & gf_ids - {a, b}
            if names_pair and replacement:
                validly_subst = True
                break
        if validly_subst:
            substituted.append(pair_label)
        else:
            missing.append(pair_label)

    issues = []
    if missing:
        issues.append(
            f"{len(missing)} must_include pair(s) neither co-located in one block nor validly "
            f"substituted: {missing}"
        )
    return CheckResult(
        not issues,
        stage,
        issues,
        info={"pairs": len(pairs), "used": used, "substituted": substituted, "missing": missing, "blocks": len(blocks)},
    )


# --------------------------------------------------------------------------------------------
# synthesis-explore.md and synthesis.md (build) composite checks
# --------------------------------------------------------------------------------------------
def check_synthesis_explore(path: str | Path, constraints_path: str | Path, gf_path: str | Path) -> CheckResult:
    """Completeness + section-order wall + Pool A+B block-level must_include for explore."""
    stage = "synthesis:explore"
    md = check_markdown(
        path,
        stage,
        anchors=["Blind Draw", "Vector Combinations", "Validated Mechanisms", "Action Deduplication Result"],
        order_pairs=[("Blind Draw", "Vector Combinations"), ("Vector Combinations", "Validated Mechanisms")],
        forbid_headings=["Generated Tactics"],  # build-only — its presence = tactic-name leak
        min_lines=60,
    )
    mi = check_must_include_blocks(
        path, constraints_path, gf_path,
        block_re=COMBINATION_BLOCK_RE, pools=("A_white_space", "B_synergy"), stage=stage,
    )
    # vector ids used must exist in growth-factors.json
    xref = _check_used_ids_subset(path, gf_path, stage)
    return md.merge(mi).merge(xref)


def check_synthesis_build(path: str | Path, constraints_path: str | Path, gf_path: str | Path) -> CheckResult:
    """Completeness + 7-9 tactic count + Pool B block-level must_include for synthesis.md."""
    stage = "synthesis:build"
    md = check_markdown(
        path,
        stage,
        anchors=["Pass 1 Disposition", "Generated Tactics", "Traceability Summary", "Post-Synthesis Self-Review"],
        min_lines=70,
    )
    text = read_text(path) or ""
    n_tactics = len(split_blocks(text, TACTIC_BLOCK_RE))
    if not (7 <= n_tactics <= 9):
        md = md.merge(CheckResult(False, stage, [f"tactic count {n_tactics} outside 7-9"]))
    md.info["tactics"] = n_tactics

    mi = check_must_include_blocks(
        path, constraints_path, gf_path,
        block_re=TACTIC_BLOCK_RE, pools=("B_synergy",), stage=stage,
    )
    xref = _check_used_ids_subset(path, gf_path, stage)
    return md.merge(mi).merge(xref)


def _check_used_ids_subset(md_path: str | Path, gf_path: str | Path, stage: str) -> CheckResult:
    """Every vector id cited in a synthesis output must exist in growth-factors.json (no phantoms)."""
    text = read_text(md_path)
    gf, err = load_json(gf_path)
    if text is None:
        return CheckResult(False, stage, [f"output missing: {md_path}"])
    if err:
        return CheckResult(False, stage, [f"growth-factors: {err}"])
    used = vector_ids_in(text)
    gf_ids = growth_factor_ids(gf)
    phantom = sorted(used - gf_ids)
    if phantom:
        return CheckResult(
            False, stage,
            [f"{len(phantom)} phantom vector id(s) not in growth-factors.json: {phantom[:5]}"],
            info={"phantom": phantom},
        )
    return CheckResult(True, stage, info={"vectors_cited": len(used)})


# --------------------------------------------------------------------------------------------
# founder-input.md presence (Stage 0 skip-if-exists support)
# --------------------------------------------------------------------------------------------
def check_founder_input(path: str | Path) -> CheckResult:
    stage = "diagnostics"
    text = read_text(path)
    if text is None or not text.strip():
        return CheckResult(False, stage, [f"founder-input.md missing/empty: {path}"])
    hs = headings(text)
    issues = []
    for anchor in ("1. Product", "4. Challenge Separation", "5. Resources", "7. Module Routing"):
        if not has_heading(hs, anchor):
            issues.append(f"founder-input.md missing section '{anchor}'")
    return CheckResult(not issues, stage, issues, info={"lines": nonblank_line_count(text)})


# --------------------------------------------------------------------------------------------
# Self-test (python3 checks.py) — runs against real fixtures + synthetic negatives
# --------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import os
    import sys
    import tempfile

    FIX = os.environ.get(
        "DIFFMODE_FIXTURE_WS",
        "/Users/antonk/dev/aicmo/ai-cmo/ai-cmo-workspace",
    )
    lite3 = Path(FIX) / "theona-lite3"
    ttd = lite3 / "03-think-tanks" / "demand-generation"
    enr = lite3 / "02-enrichment"
    gf = ttd / "growth-factors.json"
    sc = ttd / "synthesis-constraints.json"
    competitors_smoke = Path("/tmp/diffmode-codex-smoke/theona.ai/02-enrichment/competitors-analysis.md")

    passed = 0
    failed = 0

    def report(name: str, result: CheckResult, expect_ok: bool):
        global passed, failed
        ok = bool(result) == expect_ok
        passed += ok
        failed += not ok
        mark = "PASS" if ok else "FAIL"
        exp = "ok" if expect_ok else "fail"
        print(f"  [{mark}] {name}  (expected {exp}, got {'ok' if result else 'fail'})")
        if not ok or os.environ.get("VERBOSE"):
            for iss in result.issues:
                print(f"          - {iss}")
        if os.environ.get("VERBOSE"):
            print(f"          info={result.info}")

    def skip(name: str, why: str):
        print(f"  [SKIP] {name}  ({why})")

    print("== growth-factors.json ==")
    if gf.is_file():
        report("real growth-factors.json passes", check_growth_factors(gf), True)
    else:
        skip("real growth-factors.json", f"fixture absent: {gf}")

    print("== synthesis-constraints.json ==")
    if sc.is_file():
        report("real synthesis-constraints.json passes", check_constraints(sc), True)
    else:
        skip("real synthesis-constraints.json", f"fixture absent: {sc}")

    print("== constraints subset / xref ==")
    if sc.is_file() and gf.is_file():
        report("matched pair: all referenced ids exist", check_constraints_subset(sc, gf), True)
    else:
        skip("constraints subset", "fixtures absent")

    print("== markdown completeness (real fixtures) ==")
    md_cases = [
        ("enrichment:competitors", competitors_smoke),
        ("enrichment:audience", enr / "audience-jtbd.md"),
        ("enrichment:acquisition-tactics", enr / "acquisition-tactics.md"),
        ("think-tank:platform-arbitrage", ttd / "platform-arbitrage.md"),
        ("think-tank:competitor-gaps", ttd / "competitor-gaps.md"),
        ("think-tank:cross-industry", ttd / "cross-industry.md"),
    ]
    for stage, p in md_cases:
        if p.is_file():
            report(f"{stage} ({p.name})", check_markdown_stage(stage, p), True)
        else:
            skip(stage, f"fixture absent: {p}")

    print("== synthesis build (real synthesis.md, Pool-B must_include) ==")
    real_synth = ttd / "synthesis.md"
    if real_synth.is_file() and sc.is_file() and gf.is_file():
        report("real synthesis.md build check", check_synthesis_build(real_synth, sc, gf), True)
    else:
        skip("synthesis build", "fixtures absent")

    print("== NEGATIVE tests (must FAIL) ==")
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        # truncated markdown (only first heading)
        trunc = td / "trunc.md"
        trunc.write_text("# Competitive Analysis Report\n\n## Competitor Overview\nfoo\n", encoding="utf-8")
        report("truncated competitors fails", check_markdown_stage("enrichment:competitors", trunc), False)

        # growth-factors with phantom-id reference in constraints
        if gf.is_file():
            gf_obj, _ = load_json(gf)
            stale_sc = td / "stale_constraints.json"
            stale_sc.write_text(json.dumps({
                "diverse_white_space": [{"vectors": ["struct-999-does-not-exist", "lever-001-x"]}],
                "mandatory_combinations": [], "prohibited_combinations": [], "unconventional_anchors": [],
            }), encoding="utf-8")
            report("stale constraints (phantom id) fails", check_constraints_subset(stale_sc, gf), False)

        # bad growth-factors: 3 vectors (under floor), bad url, bad id
        bad_gf = td / "bad_gf.json"
        bad_gf.write_text(json.dumps({
            "metadata": {"total_vectors": 3, "category_counts": {"struct-": 3}},
            "vectors": [
                {"vector_id": "struct-001-ok", "category": "x", "mechanism": "m", "transferability": "High",
                 "saturation_risk": "Emerging", "examples": ["e"], "source_url": "https://example.com"},
                {"vector_id": "BADID", "category": "x", "mechanism": "m", "transferability": "High",
                 "saturation_risk": "Emerging", "examples": ["e"], "source_url": "not-a-url"},
                {"vector_id": "struct-003-ok", "category": "x", "mechanism": "m", "transferability": "High",
                 "saturation_risk": "Emerging", "examples": [], "source_url": "https://example.com"},
            ],
        }), encoding="utf-8")
        report("bad growth-factors fails (count/id/url/examples)", check_growth_factors(bad_gf), False)

        # synthetic VALID explore fixture (proves the positive explore path)
        valid_explore = td / "synthesis-explore.md"
        if sc.is_file():
            sc_obj, _ = load_json(sc)
            ab = must_include_pairs(sc_obj, ("A_white_space", "B_synergy"))
            combo_blocks = "\n".join(
                f"### Combination #{i+1}\n- **Vectors:** `{a}` + `{b}`\n- detail line\n"
                for i, (a, b) in enumerate(ab)
            )
            valid_explore.write_text(
                "# Synthesis Explore — Blind Combinations & Emergent Mechanisms\n\n"
                "## Founder Context Summary\n- ctx\n\n"
                "## Blind Draw (IDs only)\n- Pool A\n\n"
                "## Vector Combinations (15-20)\n" + combo_blocks + "\n"
                "## Validated Mechanisms\n### Mechanism #1\n- m\n\n"
                "## Action Deduplication Result\n| x | y |\n"
                + ("\nfiller line" * 100) + "\n",
                encoding="utf-8",
            )
            report("synthetic valid explore passes", check_synthesis_explore(valid_explore, sc, gf), True)

            # broken explore: blind-draw AFTER combinations (wall violated)
            broken_explore = td / "broken-explore.md"
            broken_explore.write_text(
                "# Synthesis Explore\n\n## Vector Combinations\n### Combination #1\n- **Vectors:** `x` + `y`\n\n"
                "## Blind Draw (IDs only)\n- late\n\n## Validated Mechanisms\n- m\n"
                "## Action Deduplication Result\n- d\n" + ("\nfiller" * 100),
                encoding="utf-8",
            )
            report("broken explore (order wall) fails", check_synthesis_explore(broken_explore, sc, gf), False)

    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
