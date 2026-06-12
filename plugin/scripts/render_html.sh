#!/bin/sh
# POSIX mirror of render_html.py — used ONLY when no Python >= 3.8 is on the machine
# (Bash/sh ships with every Claude Code install, incl. Windows git-bash; Python doesn't).
# Splices the SAME templates in assets/ (page.html, index.html, report.css,
# marked.min.js); deliberately dumb: sed-escape the markdown, cat-splice the assets,
# no stats line. Manifest must stay in sync with render_html.py's MANIFEST.
#
# usage: render_html.sh <workspace-dir>

set -u

WS=${1:-}
[ -n "$WS" ] || { echo "usage: render_html.sh <workspace-dir>" >&2; exit 1; }
[ -d "$WS" ] || { echo "report render skipped: workspace not found: $WS" >&2; exit 1; }

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ASSETS="$SCRIPT_DIR/assets"
for f in page.html index.html report.css marked.min.js; do
  [ -f "$ASSETS/$f" ] || { echo "report render skipped: missing asset: $ASSETS/$f" >&2; exit 1; }
done

OUT="$WS/report"
DATE=$(date +%Y-%m-%d)
TT="03-think-tanks/demand-generation"

# "Your Growth Tactics" renders the packaged founder report when Stage 5 produced one,
# else falls back to the raw synthesis (old runs / Codex runs / skipped packaging) —
# the same resolve as render_html.py's _resolve_manifest().
HERO="$TT/growth-tactics.md"
[ -f "$WS/$HERO" ] || HERO="$TT/synthesis.md"

# relpath|Title|group|one-line description  — same rows as render_html.py
MANIFEST="$HERO|Your Growth Tactics|hero|The main event - 7-9 ways to get users, built for your budget, team, and stage.
02-enrichment/competitors-analysis.md|Competitor Research|research|Who you're really up against, and how each rival gets users.
02-enrichment/audience-jtbd.md|Audience Map|research|Your buyer segments, and the job each one hires your product to do.
02-enrichment/acquisition-tactics.md|Acquisition Audit|research|The plays already working in your market, with effort and budget for each.
$TT/competitor-gaps.md|Where Your Size Wins|strategy|Openings your bigger competitors can't or won't fill.
$TT/cross-industry.md|Plays From Other Industries|strategy|Growth moves proven elsewhere, adapted to your market.
$TT/platform-arbitrage.md|Fresh Platform Openings|strategy|New platform features and quiet corners your rivals haven't claimed.
01-diagnostics/founder-input.md|Your Product Brief|papers|What you told us - the product, budget, and goals the research is built on.
$TT/synthesis-explore.md|How These Were Built|papers|Working paper - the mechanism combinations behind your tactics."

# The engineering-notes working paper is a separate page ONLY when the hero is the
# packaged report — otherwise synthesis.md IS the hero and a second page would duplicate it.
if [ -f "$WS/$TT/growth-tactics.md" ]; then
  MANIFEST="$MANIFEST
$TT/synthesis.md|Tactic Engineering Notes|papers|Working paper - the full engineering write-up behind each tactic, scores and traceability included."
fi

escape_html() { # html-escape stdin (kills any literal </pre> / </script> in the markdown)
  sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g'
}

render_page() { # $1=src md, $2=title, $3=out file
  src=$1 title=$2 out=$3
  while IFS= read -r line; do
    case $line in
      __CSS__)    cat "$ASSETS/report.css" ;;
      __MARKED__) cat "$ASSETS/marked.min.js" ;;
      __MD__)     escape_html < "$src" ;;
      *__TITLE__*|*__DATE__*)
        printf '%s\n' "$line" | sed -e "s/__TITLE__/$title/g" -e "s/__DATE__/$DATE/g" ;;
      *) printf '%s\n' "$line" ;;
    esac
  done < "$ASSETS/page.html" > "$out"
}

RENDERED=0
ITEMS=$(mktemp) || exit 1
trap 'rm -f "$ITEMS"' EXIT
last_group=""

printf '%s\n' "$MANIFEST" | while IFS='|' read -r rel title group desc; do
  [ -f "$WS/$rel" ] || continue
  [ -s "$WS/$rel" ] || continue
  mkdir -p "$OUT"
  render_page "$WS/$rel" "$title" "$OUT/$title.html"
  printf '%s|%s|%s\n' "$group" "$title" "$desc" >> "$ITEMS"
  echo "  rendered: $title.html"
done

[ -s "$ITEMS" ] || { echo "nothing to render yet in $WS (no deliverables found)"; exit 0; }

# Build the index card list (same structure as render_html.py: hero card + grids).
CARDS=$(mktemp) || exit 1
trap 'rm -f "$ITEMS" "$CARDS"' EXIT
for group in hero research strategy papers; do
  case $group in
    hero)     label="Start here" ;;
    research) label="Research briefs" ;;
    strategy) label="Strategy reports" ;;
    papers)   label="Working papers" ;;
  esac
  grep "^$group|" "$ITEMS" > /dev/null 2>&1 || continue
  printf '<p class="dm-eyebrow">%s</p>\n' "$label" >> "$CARDS"
  [ "$group" = hero ] || printf '<div class="dm-grid">\n' >> "$CARDS"
  grep "^$group|" "$ITEMS" | while IFS='|' read -r _g title desc; do
    href=$(printf '%s' "$title.html" | sed 's/ /%20/g')
    cls="dm-card"; [ "$group" = hero ] && cls="dm-card dm-card--hero"
    {
      printf '<a class="%s" href="%s">\n' "$cls" "$href"
      printf '  <span class="dm-card__title">%s</span>\n' "$(printf '%s' "$title" | escape_html)"
      printf '  <span class="dm-card__desc">%s</span>\n' "$(printf '%s' "$desc" | escape_html)"
      printf '</a>\n'
    } >> "$CARDS"
  done
  [ "$group" = hero ] || printf '</div>\n' >> "$CARDS"
done

SLUG=$(basename "$WS")
while IFS= read -r line; do
  case $line in
    __CSS__)   cat "$ASSETS/report.css" ;;
    __ITEMS__) cat "$CARDS" ;;
    __STATS__) : ;;  # stats are a python-only nicety; the sh mirror omits them
    *__SLUG__*|*__DATE__*)
      printf '%s\n' "$line" | sed -e "s/__SLUG__/$SLUG/g" -e "s/__DATE__/$DATE/g" ;;
    *) printf '%s\n' "$line" ;;
  esac
done < "$ASSETS/index.html" > "$OUT/index.html"

echo "report ready: $OUT/index.html"
exit 0
