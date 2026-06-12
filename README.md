# Diffmode Growth Tactics

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-d97757.svg)](https://claude.com/claude-code)
[![OpenAI Codex](https://img.shields.io/badge/OpenAI_Codex-ready-412991.svg)](https://developers.openai.com/codex)

> **Always outcrowded, never outgunned.**

**Install (Claude Code):** two commands, then restart:

```bash
claude plugin marketplace add acogood/diffmode_free
claude plugin install diffmode-growth-tactics@diffmode-free
```

Or [run it on Codex](#run-it-on-codex). Free, no account, no API key.

Diffmode builds a **growth strategy** for startups that can't outspend their competitors. It
researches who your buyers are and how your rivals win them, then hands you unconventional ways
to win them yourself — in about **90 minutes**, free, inside your AI agent.

Built for solo founders, first marketing hires, and small bootstrapped teams — people who can
build the product but find marketing foreign. If you've never mapped an audience or sized up a
competitor before, the run does that *with* you, and leaves the work behind so you can see how
it got there.

Why it's different: each tactic combines two or three proven growth mechanisms from real case
studies — not channels off a checklist.

## Quickstart

It runs on **two runtimes, off the same skill files** — **Claude Code** and **OpenAI Codex**. The
method is identical on both, and each has a one-command run. The Claude Code install is below; for
the Codex command see [run it on Codex](#run-it-on-codex).

### Claude Code

```bash
# add the marketplace (straight from GitHub)
claude plugin marketplace add acogood/diffmode_free
# install the plugin
claude plugin install diffmode-growth-tactics@diffmode-free
```

Restart Claude Code, then from **any folder**:

```
/diffmode-growth-tactics:start your-product.com
```

No account, no API key, no flags. Run it bare and it asks for your product's website (no
site yet? it takes a product name instead); run it again in the same folder and it offers
to continue an unfinished run where it stopped. It writes everything into a
`./<your-product>/` folder in your current
directory. **Perplexity is optional** — with nothing configured, it uses Claude Code's built-in
web search for free.

### Run it in Claude Cowork

Same plugin, same command — installed through the app's menu instead of the CLI:

1. Open the **Claude desktop app**. Click the **Cowork** tab → **Customize** → **Plugins**.
2. Choose **Add from repository** and enter `acogood/diffmode_free` (or the full GitHub URL).
3. Install **diffmode-growth-tactics**, then start a **new session** and run
   `/diffmode-growth-tactics:start your-product.com` as above.

> ⚠️ **Don't ask the agent inside a session to install the plugin.** Cowork sessions run in a
> sandbox, so anything installed there is wiped when the app relaunches — the Customize menu
> is the only install that sticks. If the report doesn't open in your browser at the end of a
> run, open `<your-product>/report/index.html` from the session's files panel.

## What you get

A run builds your growth strategy in three parts — a read on your competition, a map of your
buyers, and unconventional ways to get users. Each part is written to be acted on, even if
you've never built a growth plan before.

**1. A read on your competition.** Who you're really up against, and how each rival *actually*
gets users — the channels they lean on, and the ones they're ignoring. That gap is where you get
in. (A real run mapped **9 competitors** and the acquisition channels behind each.)

**2. A map of your buyers.** Your real segments and the job each one is hiring you to do, plus
the moments that make someone switch. Most founders have never written this down — and it's the
part generic tools skip.

**3. Unconventional ways to get users yourself.** The sharp end of the strategy — the
**Your Growth Tactics** report, with **7–9 specific tactics** built for your budget, stage, and
team. Each tactic is a plain card that spells out:

- **what it is**, in plain language;
- **why your better-funded rivals can't copy it** (your budget, stage, and team size are baked in);
- **how to start this week** — the first steps, with the tools to use; and
- **when to kill it** — the concrete signal that says stop or double down.

The full engineering write-up behind each tactic — mechanism combinations, scores, traceability —
ships alongside as a working paper, for when you want to see how the sausage was made.

They come from an audit of **25–35 plays** already working in your space, then bent into angles
your better-funded competitors haven't thought to copy. Here's the *kind* of tactic a run
produces:

> **The Hiring-Signal Pitch**
> When a company posts a job to hire a person for the exact manual task your product removes,
> that's a buying signal nobody else is watching.
> - *Why it fits a small team:* it's hands-on and doesn't scale — which is exactly why
>   ad-funded competitors won't do it. They can't pay a salesperson to chase one signup at a
>   time; you can, for your first 20 customers.
> - *First three steps:* (1) set LinkedIn/Indeed alerts for the job titles that describe the
>   work you automate; (2) when one is posted, find the hiring manager; (3) send a 60-second
>   screen recording — "saw you're hiring a [role] to do [task]; here's my tool doing it live —
>   try it free this week before you hire."
> - *Week-1 signal:* a reply rate above ~10% means the angle lands; below that, tighten your
>   job-title list.

All three parts are **yours to reuse** — not scratch notes, but briefs in their own right. Hand
the competitor read to a freelancer, drop the buyer map into a deck, or build your content
calendar off the acquisition audit. The run also leaves three short strategy reports behind —
where your size is an advantage, plays worth borrowing from other industries, and fresh openings
on the big platforms. The tactics get spent in a few months. The research keeps working.

And you don't need a markdown viewer to read any of it: the run ends with a **styled report in
your browser** — open `<your-product>/report/index.html` (it offers to open it for you). No
extra installs; the plain-text files stay alongside.

## How it works

```
1. Tell it your product   →  a URL (it researches the site) or a 2-minute Q&A
2. Research your market    →  your competitors and your buyers, and where rivals are weak
3. Mine proven mechanisms  →  growth mechanisms pulled fresh from public case studies
4. Combine into tactics    →  fuse 2–3 mechanisms into tactics that fit your constraints
```

It runs locally, start to finish in about **1–1.5 hours**, and **checks its own work** — a
reviewer re-runs a stage until it clears the quality bar. The full design, including those
quality gates, is in [`docs/architecture.md`](docs/architecture.md).

## Requirements

- **[Claude Code](https://claude.com/claude-code)** (or **OpenAI Codex** — see below). That's
  the only thing you need.
- **Perplexity is optional.** With a Perplexity MCP server configured, the research stages use
  it; without one, they fall back to Claude Code's built-in web search automatically.
- **Cost:** free with the built-in search; about **$2–3 per run** if you point it at Perplexity
  (a few deep-research calls are the only paid part).

## Run it on Codex

On Codex, the same pipeline runs as a small Python driver, Perplexity-optional too (it falls back
to Codex's native web search). You'll need the `codex` CLI installed and logged in, plus Python 3.
Clone this repo first, then from inside it:

```bash
python3 codex/orchestrate.py --url https://your-product.com
```

It writes everything into a `./<your-product>/` folder — same pipeline, same stop point as the
Claude run, though the Codex report keeps the raw `synthesis.md` as its main page (the founder-clean
re-write is Claude-only for now). Add `--fast-intake` to skip the founder Q&A (hands-off; lower quality). Full setup
— making the worker agents discoverable, the optional Perplexity backend, the dispatch flags — is
in [`codex/CODEX.md`](codex/CODEX.md).

## Free vs. the full Diffmode

This free tool builds the **strategy** — the competitor read, the buyer map, and the
unconventional ideas. It stops there, at ideas.

[**Diffmode**](https://diffmode.app) picks up from there: it **ranks the tactics** so you know
what to do first, and turns the top picks into a **week-by-week rollout plan** — drawn from a
much larger, curated database of growth mechanisms than the fresh, per-run research behind this
free tool. Start with a **free audit (no credit card)**. The full plan comes with a **30-day
money-back guarantee**.

→ **[diffmode.app](https://diffmode.app)**

## Under the hood (for contributors)

```
plugin/     the Claude Code plugin — the only thing Claude installs
  skills/   the 13 skill files — the single source of truth
  agents/  commands/  reference/
codex/      Codex driver — runs the same skills through symlinks (no second copy)
docs/       design notes + build history (not shipped to either runtime)
```

The skills live **once**, in `plugin/skills/`; Codex consumes them through relative symlinks, so
there's no second copy and no drift. For the design — the orchestrator, skills, and worker
sub-agents, and why the orchestrator runs in the main thread — see
[`docs/architecture.md`](docs/architecture.md). For build history and measured runtimes, see
[`docs/STATUS.md`](docs/STATUS.md).

License: **[Apache-2.0](LICENSE)**. © 2026 Anton Kogut.
