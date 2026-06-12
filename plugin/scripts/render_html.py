#!/usr/bin/env python3
"""Render a Diffmode growth-tactics workspace into a styled HTML report.

Stdlib-only. Takes the user-valuable markdown deliverables from a run workspace and
writes a self-contained HTML report to ``<workspace>/report/`` — an ``index.html`` plus
one page per deliverable, with human-friendly file names ("Your Growth Tactics.html").
The hero page renders ``growth-tactics.md`` (the packaged founder report) when present,
falling back to ``synthesis.md`` for runs that never packaged one — see
``_resolve_manifest``.
Markdown is NOT parsed in Python: each page embeds the escaped source in a hidden
``<pre>`` and renders it client-side with the vendored marked.js (``assets/marked.min.js``);
with JavaScript off the raw markdown un-hides and reads fine as-is.

Usage:
    python3 render_html.py <workspace-dir> [--open]

Behavior:
    - renders whatever deliverables exist, silently skips the rest (a partial run still
      gets a report); exits 0 on partial.
    - ``--open`` opens index.html in the default browser (os.startfile / open / xdg-open),
      best-effort — an open failure never fails the render.
    - index stats (tactic / competitor / mechanism counts) are best-effort: on any parse
      failure the number is omitted, never guessed.

Importable: ``render_workspace(ws, open_browser=False)`` returns the index.html Path, or
None when nothing could be rendered (used by codex/orchestrate.py's report step).

Templates + stylesheet + marked.js live in ``assets/`` next to this script; the POSIX
mirror ``render_html.sh`` splices the SAME templates for machines with no Python.
"""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import urllib.parse
from datetime import date
from pathlib import Path

ASSETS = Path(__file__).resolve().parent / "assets"

# The user-valuable deliverables, in display order: (workspace-relative source,
# human-friendly page name, index group, one-line plain-English value).
# Internal artifacts (growth-factors.json, synthesis-constraints.json, .run-state.json)
# are deliberately NOT rendered. Kept in sync with render_html.sh's MANIFEST.
TT = "03-think-tanks/demand-generation"
MANIFEST: list[tuple[str, str, str, str]] = [
    (f"{TT}/growth-tactics.md", "Your Growth Tactics", "hero",
     "The main event — 7-9 ways to get users, built for your budget, team, and stage."),
    ("02-enrichment/competitors-analysis.md", "Competitor Research", "research",
     "Who you're really up against, and how each rival gets users."),
    ("02-enrichment/audience-jtbd.md", "Audience Map", "research",
     "Your buyer segments, and the job each one hires your product to do."),
    ("02-enrichment/acquisition-tactics.md", "Acquisition Audit", "research",
     "The plays already working in your market, with effort and budget for each."),
    (f"{TT}/competitor-gaps.md", "Where Your Size Wins", "strategy",
     "Openings your bigger competitors can't or won't fill."),
    (f"{TT}/cross-industry.md", "Plays From Other Industries", "strategy",
     "Growth moves proven elsewhere, adapted to your market."),
    (f"{TT}/platform-arbitrage.md", "Fresh Platform Openings", "strategy",
     "New platform features and quiet corners your rivals haven't claimed."),
    ("01-diagnostics/founder-input.md", "Your Product Brief", "papers",
     "What you told us — the product, budget, and goals the research is built on."),
    (f"{TT}/synthesis-explore.md", "How These Were Built", "papers",
     "Working paper — the mechanism combinations behind your tactics."),
    (f"{TT}/synthesis.md", "Tactic Engineering Notes", "papers",
     "Working paper — the full engineering write-up behind each tactic, scores and "
     "traceability included."),
]


def _resolve_manifest(ws: Path) -> list[tuple[str, str, str, str]]:
    """Per-workspace manifest. The hero renders ``growth-tactics.md`` (the packaged
    founder report) when present. When it's absent (an old run, a Codex run, or a
    skipped packaging stage) the hero falls back to ``synthesis.md`` and the
    "Tactic Engineering Notes" entry is dropped — synthesis.md IS the hero then, so a
    separate working-paper page would be a duplicate."""
    if (ws / TT / "growth-tactics.md").is_file():
        return MANIFEST
    rows: list[tuple[str, str, str, str]] = []
    for rel, title, group, desc in MANIFEST:
        if rel == f"{TT}/growth-tactics.md":
            rows.append((f"{TT}/synthesis.md", title, group, desc))
        elif title == "Tactic Engineering Notes":
            continue
        else:
            rows.append((rel, title, group, desc))
    return rows

GROUPS = [
    ("hero", "Start here"),
    ("research", "Research briefs"),
    ("strategy", "Strategy reports"),
    ("papers", "Working papers"),
]


def _load_asset(name: str) -> str:
    p = ASSETS / name
    if not p.is_file():
        raise RuntimeError(f"missing asset: {p}")
    return p.read_text(encoding="utf-8")


def _read_md(path: Path) -> str | None:
    """Read a markdown source tolerantly (CRLF workspaces, stray bytes)."""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _render_page(template: str, css: str, marked_js: str, title: str, md: str) -> str:
    page = template.replace("__CSS__", css).replace("__MARKED__", marked_js)
    page = page.replace("__TITLE__", html.escape(title))
    page = page.replace("__DATE__", date.today().isoformat())
    # html.escape kills any literal </pre> / </script> inside the markdown.
    return page.replace("__MD__", html.escape(md))


# ----------------------------------------------------------------------------------------
# Best-effort index stats — omit silently on any failure; never print a wrong number.
# ----------------------------------------------------------------------------------------
def _stats_line(ws: Path) -> str:
    parts: list[str] = []
    try:  # tactic count — the heading form of checks.py's Tactic\s+#\d+ block regex
        text = _read_md(ws / TT / "synthesis.md") or ""
        n = len(re.findall(r"^#{1,6}\s*Tactic\s+#\d+", text, re.M))
        if n:
            parts.append(f"<strong>{n} growth tactics</strong>")
    except Exception:
        pass
    try:  # competitor count — the report header line
        text = _read_md(ws / "02-enrichment/competitors-analysis.md") or ""
        m = re.search(r"Competitors Analyzed:\*{0,2}\s*(\d+)", text)
        if m:
            parts.append(f"{m.group(1)} competitors mapped")
    except Exception:
        pass
    try:  # mined growth mechanisms — LIGHT DB metadata
        gf = json.loads((ws / TT / "growth-factors.json").read_text(encoding="utf-8"))
        n = gf.get("metadata", {}).get("total_vectors")
        if isinstance(n, int) and n > 0:
            parts.append(f"{n} growth mechanisms mined from public case studies")
    except Exception:
        pass
    if not parts:
        return ""
    return '<p class="dm-stats">' + " &middot; ".join(parts) + "</p>"


def _card(title: str, desc: str, hero: bool = False) -> str:
    href = urllib.parse.quote(f"{title}.html")
    cls = "dm-card dm-card--hero" if hero else "dm-card"
    return (
        f'<a class="{cls}" href="{href}">\n'
        f'  <span class="dm-card__title">{html.escape(title)}</span>\n'
        f'  <span class="dm-card__desc">{html.escape(desc)}</span>\n'
        f"</a>"
    )


def _render_index(template: str, css: str, ws: Path,
                  rendered: list[tuple[str, str, str]]) -> str:
    items: list[str] = []
    for group, label in GROUPS:
        cards = [(t, d) for t, g, d in rendered if g == group]
        if not cards:
            continue
        items.append(f'<p class="dm-eyebrow">{html.escape(label)}</p>')
        if group == "hero":
            items.extend(_card(t, d, hero=True) for t, d in cards)
        else:
            items.append('<div class="dm-grid">')
            items.extend(_card(t, d) for t, d in cards)
            items.append("</div>")
    page = template.replace("__CSS__", css)
    page = page.replace("__SLUG__", html.escape(ws.name))
    page = page.replace("__DATE__", date.today().isoformat())
    page = page.replace("__STATS__", _stats_line(ws))
    return page.replace("__ITEMS__", "\n".join(items))


def open_in_browser(path: Path) -> bool:
    """Open a file in the OS default browser. Best-effort — never raises."""
    try:
        if sys.platform.startswith("win"):
            import os
            os.startfile(str(path))  # type: ignore[attr-defined]
            return True
        cmd = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.Popen([cmd, str(path)], stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def render_workspace(ws: str | Path, open_browser: bool = False) -> Path | None:
    """Render every present deliverable + index.html into ws/report/.

    Returns the index.html Path, or None when no deliverable was found. Raises
    RuntimeError only when the bundled assets are missing/broken (callers treat the
    whole render as best-effort).
    """
    ws = Path(ws).resolve()
    if not ws.is_dir():
        raise RuntimeError(f"workspace not found: {ws}")
    page_tpl = _load_asset("page.html")
    index_tpl = _load_asset("index.html")
    css = _load_asset("report.css")
    marked_js = _load_asset("marked.min.js")

    out_dir = ws / "report"
    rendered: list[tuple[str, str, str]] = []  # (title, group, desc)
    for rel, title, group, desc in _resolve_manifest(ws):
        md = _read_md(ws / rel)
        if md is None or not md.strip():
            continue
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / f"{title}.html"
        out.write_text(_render_page(page_tpl, css, marked_js, title, md),
                       encoding="utf-8")
        rendered.append((title, group, desc))

    if not rendered:
        return None
    index = out_dir / "index.html"
    index.write_text(_render_index(index_tpl, css, ws, rendered), encoding="utf-8")
    if open_browser:
        open_in_browser(index)
    return index


def main(argv: list[str]) -> int:
    args = [a for a in argv if a != "--open"]
    if len(args) != 1:
        print("usage: render_html.py <workspace-dir> [--open]", file=sys.stderr)
        return 1
    try:
        index = render_workspace(args[0], open_browser="--open" in argv)
    except RuntimeError as e:
        print(f"report render skipped: {e}", file=sys.stderr)
        return 1
    if index is None:
        print(f"nothing to render yet in {args[0]} (no deliverables found)")
        return 0
    print(f"report ready: {index}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
