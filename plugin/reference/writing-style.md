# Writing Style — every user-facing deliverable

How to write the BODY copy of any file the founder reads (`founder-input.md` excepted —
it's a capture form). One central file so the rules live once; skills point here.

## Voice

A confident growth consultant explaining findings to a busy founder over coffee.
**Reading level: grade 6–8** (a non-native speaker at B2 understands every sentence on
first read). **Max ~20 words per sentence** — split a compound idea into two short
sentences. **The coffee test:** if a sentence wouldn't be said out loud across a table,
rewrite it. Specifics beat adjectives: "9 of 10 rivals ignore Reddit" beats "a
significant channel gap."

## Banned jargon (use the plain alternative)

| Banned | Use instead |
|--------|-------------|
| leverage | use |
| optimize | improve / fix |
| arbitrage | pricing gap / opening / early window |
| weaponize | use / turn into |
| exploit (as a verb for tactics) | use / take advantage of |
| structurally (as an adjective) | built-in — or just delete it |
| synergy | (delete the sentence) |
| utilize | use |
| robust | solid / reliable |
| scalable | "doesn't break when you grow" |
| holistic / actionable insights | (delete; just give the action) |
| guerrilla (marketing) | direct / personal outreach |
| PLG (unexplained) | "a free tier that draws people in" |
| growth loop (unexplained) | "a cycle where users bring in more users" — or explain the loop |
| protocol (in tactic names) | a plain description of what you do |

General rule: if a word wouldn't appear in a newspaper article for general readers,
don't use it. **Scope:** this bans jargon in deliverable BODY copy only — internal
skill/file names (`platform-arbitrage.md`, JSON keys, section headings required by a
template) stay as they are.

## Never show internal plumbing

- **Vector IDs** (`lever-003-…`) appear ONLY in `**Source:**` / Traceability lines —
  that's a downstream contract — never in prose ("this uses lever-003" is banned).
- No prompt/skill names, no reviewer/gate/pool vocabulary (`must_include`, "structural
  check", "Pool B"), no "LIGHT DB" / "vector database" in body copy.
- Describe method as depth of analysis, not machinery: "based on mapping all 9
  competitors' channels" — not "the enrichment module found".

## Tactic naming

**The name alone should tell a smart friend what you'd actually do**: what you do + the
twist, in plain words. No invented compound nouns, no codenames, no spy language.

| Bad | Good |
|-----|------|
| The Competitor Ghost Protocol | Personalized Video Audits for Clinics |
| Anti-Enterprise Citation Rebellion | Call Out Enterprise Tools by Name in Your Docs |
| Limited Capacity Drops | "Only 10 Spots This Month" Scarcity Offers |

**Keep the unconventional mechanism — say it plainly.** The edge lives in the
mechanism (the uncomfortable move, the thing big competitors won't copy), not in the
vocabulary. "Call Out Enterprise Tools by Name" keeps the confrontation; "Citation
Rebellion" just hides it behind a label.

## Required per-tactic field (synthesis output)

Every tactic carries, right under its name:

```
**In plain English:** <one ≤20-word sentence — what you actually do>
```

If you can't write that sentence, the tactic isn't clear enough yet — rework it.
