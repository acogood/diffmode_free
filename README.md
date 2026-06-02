# Diffmode Growth Tactics

> **Always outcrowded, never outgunned.**

A free, open growth-ideation tool for teams that can't outspend their competitors — solo
founders, first marketing hires, small bootstrapped teams. Point it at your product and it
hands back **7–9 specific, unconventional tactics built for *your* constraints** — your budget,
your stage, your team size — not a generic channel checklist.

What makes it different: it doesn't just list the channels you already know. It takes proven
growth *mechanisms* from real case studies and **combines two or three at a time** into tactics
your better-funded competitors haven't thought to copy — because they didn't exist in any single
playbook before.

## Quickstart (Claude Code)

```bash
# add the marketplace (straight from GitHub)
claude plugin marketplace add acogood/diffmode_free
# install the plugin
claude plugin install diffmode-growth-tactics@diffmode-free
```

Restart Claude Code, then from **any folder**:

```
/diffmode-growth-tactics:run-growth-tactics --url https://your-product.com
```

No account, no API key. It writes everything into a `./<your-product>/` folder in your current
directory. **Perplexity is optional** — with nothing configured, it uses Claude Code's built-in
web search for free.

## What you get

One file lands in that folder — **`synthesis.md`** — with **7–9 tactics**. Each one spells out:

- **what it is**, in plain language;
- **why it fits a team like yours** (your budget, stage, and team size are baked in);
- the **first three steps** to run it; and
- the **week-1 signal** that tells you whether it's working.

Here's the *kind* of tactic a run produces:

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

The run also leaves the **full research** behind in the same folder — who your real competitors
are, who your audience is and what they're trying to get done, and where rivals are weak — so
you can check the thinking behind every tactic.

## How it works

```
1. Tell it your product   →  a URL (it researches the site) or a 2-minute Q&A
2. Research your market    →  competitors, audience, where rivals are weak
3. Mine proven mechanisms  →  growth mechanisms pulled fresh from public case studies
4. Combine into tactics    →  fuse 2–3 mechanisms into tactics that fit your constraints
```

It runs locally on your machine, start to finish in about **1–1.5 hours**. It also **checks its
own work** — a reviewer re-runs a stage until it clears the quality bar. The full design,
including how those quality gates work, is in [`docs/architecture.md`](docs/architecture.md).

## Requirements

- **[Claude Code](https://claude.com/claude-code)** (or **OpenAI Codex** — see below). That's
  the only thing you need.
- **Perplexity is optional.** With a Perplexity MCP server configured, the research stages use
  it; without one, they fall back to Claude Code's built-in web search automatically.
- **Cost:** free with the built-in search; about **$2–3 per run** if you point it at Perplexity
  (a few deep-research calls are the only paid part).

## Run it on Codex

The skills are runtime-neutral — Codex reads the same skill files Claude does, and both runtimes
are Perplexity-optional (Codex falls back to its own native web search). The single-skill path is
proven and documented today; the single-command full pipeline is in progress. See
[`codex/CODEX.md`](codex/CODEX.md) to run a skill on Codex now.

## Free vs. the full Diffmode

This free tool gives you the **ideas** — a portfolio of tactics built for your constraints.

[**Diffmode**](https://diffmode.app) picks up from there: it **ranks the tactics** so you know
what to do first, and turns the top picks into a **week-by-week rollout plan** — drawn from a
much larger, curated database of growth mechanisms than the fresh, per-run research behind this
free tool. Start with a **free audit (no credit card)**; the full plan comes with a **30-day
money-back guarantee**.

→ **[diffmode.app](https://diffmode.app)**

## Under the hood (for contributors)

```
plugin/     the Claude Code plugin — the only thing Claude installs
  skills/   the 12 skill files — the single source of truth
  agents/  commands/  reference/
codex/      Codex scaffold — reads the same skills through symlinks (no second copy)
docs/       design notes + build history (not shipped to either runtime)
```

The skills live **once**, in `plugin/skills/`; Codex consumes them through relative symlinks, so
there's no second copy and no drift. For the design — the orchestrator, skills, and worker
sub-agents, and why the orchestrator runs in the main thread — see
[`docs/architecture.md`](docs/architecture.md). For build history and measured runtimes, see
[`docs/STATUS.md`](docs/STATUS.md).

License: **[Apache-2.0](LICENSE)**. © 2026 Anton Kogut.
