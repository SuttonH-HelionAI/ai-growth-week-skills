---
name: seed-wiki
description: Auto-populate the wiki from everything already in the kit. Run this once after /start-wiki. Five sub-agents fire in parallel, ingest CLAUDE.md plus context/, decisions/, projects/, and references/ into wiki/voice/, wiki/founder/, wiki/business/, wiki/team/, wiki/priorities/, wiki/decisions/, wiki/projects/, and wiki/references/. Builds entity pages and cross-references. Runs four sample queries to prove the wiki is alive. White-label, robust to missing files, idempotent. Auto-triggers on phrases like "seed the wiki," "fill the wiki," "auto-populate the wiki," "ingest everything I have." User-invocable as `/seed-wiki`.
---

# /seed-wiki

The wiki gets a real brain in 10 minutes. Five sub-agents fire in parallel against everything already on disk in the kit. By the end, the wiki has 20-50 pages, entity cross-references, and four sample queries already answered.

Run this once after `/start-wiki`. It is the "make my wiki immediately useful" skill.

---

## First-run guard

Before doing anything else, check:

1. `CLAUDE.md` exists in the working directory and contains `[BRAND COMPLETE]` on the last line.
2. `wiki/` folder exists and contains `wiki/CLAUDE.md` (the schema written by `/start-wiki`).

If either is missing → STOP and tell the user: "Run `/start-wiki` first. It scaffolds the wiki I need to seed. Two minutes, then come back."

Do not proceed.

---

## Step 1: Inventory the kit

Use Bash, Glob, and Read to find every kit file that can become a wiki source. Check for:

- `CLAUDE.md` (always present at this point)
- `context/me.md`, `context/work.md`, `context/team.md`, `context/current-priorities.md`, `context/goals.md`
- `decisions/log.md`
- `projects/*/README.md`
- `references/sops/*.md`, `references/examples/*.md`
- Any other root-level `*.md` that names a brand or business doc (skip `README.md`, `CLAUDE.local.md`)

Build an inventory tree and print it on screen:

```
Inventory of your kit:
  CLAUDE.md                            [N] sections
  context/                             [N] files
    me.md, work.md, team.md, current-priorities.md, goals.md
  decisions/log.md                     [N] entries
  projects/                            [N] active
    project-a, project-b
  references/sops/                     [N] files
```

Skip categories with zero files. Show only what is actually present.

Then say:

> "I will dispatch five sub-agents in parallel to ingest these into your wiki. About 10 minutes, no further input from you. Continue?"

Wait for confirmation. If "skip projects" or similar narrowing, filter the dispatch list. If "go," proceed.

---

## Step 2: Build the category map and pre-create folders

Map kit sources to wiki categories:

| Kit source                              | Wiki category        |
|-----------------------------------------|----------------------|
| `CLAUDE.md` sections                    | `wiki/voice/`        |
| `context/me.md`                         | `wiki/founder/`      |
| `context/work.md`                       | `wiki/business/`     |
| `context/team.md`                       | `wiki/team/`         |
| `context/current-priorities.md`, `goals.md` | `wiki/priorities/` |
| `decisions/log.md`                      | `wiki/decisions/`    |
| `projects/*/README.md`                  | `wiki/projects/`     |
| `references/sops/*`, `references/examples/*` | `wiki/references/` |

Pre-create `wiki/[category]/` folders for every category that has at least one source. Sub-agents write into pre-existing folders.

---

## Step 3: Dispatch five sub-agents in parallel

Fire all five in a SINGLE message with five Task tool calls. Each `general-purpose` agent gets one category and one job. Sequential dispatch defeats the speed.

### Sub-agent 1: voice (CLAUDE.md → wiki/voice/)

```
You are sub-agent 1 of 5, the voice agent. Your single job is to extract the brand brain from CLAUDE.md into wiki/voice/.

Read CLAUDE.md. Identify every section heading (## Identity, ## Lineup, ## Audience, ## Tone, ## Decision Filter, etc.).

For each section that exists, write a wiki page at wiki/voice/[section-slug].md with:
- A 2-line distilled summary at the top
- The verbatim section content
- A "## Key claims" bullet list (3-5 distilled points)
- A "## Entities mentioned" list (any names of people, products, brands, competitors)
- Footer: "Source: CLAUDE.md, captured [today's date]"

Then write wiki/voice/index.md listing all pages with one-line summaries.

Append one line to wiki/log.md: "[YYYY-MM-DD HH:MM] seed-wiki/voice: [N] pages from CLAUDE.md".

Do NOT touch any folder outside wiki/voice/. Do NOT modify CLAUDE.md.
```

### Sub-agent 2: context (context/*.md → wiki/founder/, wiki/business/, wiki/team/, wiki/priorities/)

```
You are sub-agent 2 of 5, the context agent. Your single job is to ingest context/*.md into wiki/founder/, wiki/business/, wiki/team/, and wiki/priorities/.

Read every file in context/ that exists. Map each:
- context/me.md → wiki/founder/[founder-slug].md (slug from the founder's name, lowercase, hyphens)
- context/work.md → wiki/business/[business-slug].md (one page, or split per business if multiple businesses are described in the same file)
- context/team.md → wiki/team/index.md (overview) + wiki/team/[person-slug].md for each named person
- context/current-priorities.md → wiki/priorities/current.md
- context/goals.md → wiki/priorities/goals.md

For every wiki page:
- 2-line summary at top
- Verbatim content from the source
- "## Key facts" bullet list
- "## Entities mentioned" list (people, products, businesses, competitors)
- Footer: "Source: context/[file].md, captured [today's date]"

Write wiki/founder/index.md, wiki/business/index.md, wiki/team/index.md, wiki/priorities/index.md as section TOCs.

Append one line per category to wiki/log.md.

Skip any source file that does not exist. Do not error. Do NOT touch any folder outside the four assigned. Do NOT modify originals.
```

### Sub-agent 3: decisions (decisions/log.md → wiki/decisions/)

```
You are sub-agent 3 of 5, the decisions agent. Your single job is to parse decisions/log.md into per-decision pages in wiki/decisions/.

Read decisions/log.md. The file uses one of these patterns:
- "[YYYY-MM-DD] DECISION: ... | REASONING: ... | CONTEXT: ..."
- One paragraph per entry separated by blank lines or "---"
- Or another append-only style

For each entry:
- Slug it as [YYYY-MM-DD]-[short-name]
- Write wiki/decisions/[slug].md with:
  - 2-line distilled summary
  - The full verbatim entry
  - "## Why this matters" 1-2 line interpretation in the kit's voice (read CLAUDE.md ## Tone for guidance)
  - "## Entities mentioned" list
  - Footer: "Source: decisions/log.md, captured [today's date]"

Write wiki/decisions/index.md sorted by date, newest first, one-line summary per decision.

Append one line to wiki/log.md.

If decisions/log.md is empty or missing, exit gracefully and log "no decisions to ingest" to wiki/log.md. Do NOT touch other folders.
```

### Sub-agent 4: projects (projects/*/README.md → wiki/projects/)

```
You are sub-agent 4 of 5, the projects agent. Your single job is to ingest each projects/*/README.md into wiki/projects/.

For each subfolder of projects/ that has a README.md:
- Slug from the folder name
- Write wiki/projects/[slug].md with:
  - 2-line summary
  - Verbatim README content (or distilled if the README is over 500 lines, keep the most signal-dense parts)
  - "## Status" line: active | paused | done (parse from README, default to active)
  - "## Key dates" list if any are mentioned
  - "## Entities mentioned" list
  - "## Source" link back to projects/[slug]/

Write wiki/projects/index.md sorted by status (active first), with one-line summaries.

Append one line to wiki/log.md.

If projects/ is empty or has no README files, exit gracefully and log "no projects to ingest". Do NOT touch other folders.
```

### Sub-agent 5: references (references/ → wiki/references/)

```
You are sub-agent 5 of 5, the references agent. Your single job is to ingest references/sops/*.md and references/examples/*.md into wiki/references/.

For each file:
- Write wiki/references/[slug].md with:
  - 2-line summary
  - Verbatim content
  - "## What this is for" 1-line line: which project, workflow, or skill this reference supports
  - "## Entities mentioned" list
  - Footer: "Source: references/[subdir]/[file], captured [today's date]"

Write wiki/references/index.md grouped by sops vs examples.

Append one line to wiki/log.md.

If references/ is empty or missing, exit gracefully and log accordingly. Do NOT touch other folders.
```

---

## Step 4: Wait for all five sub-agents to return, then run the entity merge

Once all five have returned:

1. Glob `wiki/**/*.md` (excluding `wiki/CLAUDE.md`, `wiki/index.md`, `wiki/log.md`, `wiki/entities/*`).
2. For each page, parse the `## Entities mentioned` section.
3. Build a unique entity list across all pages. Classify each:
   - Person (founder, team, named individual)
   - Product (named product or SKU)
   - Business (Ascend, Helion, Purpose, etc.)
   - Competitor (named competing brand)
   - Concept (recurring idea, framework, or theme)
4. Create `wiki/entities/[entity-slug].md` for each unique entity with:
   - Type and one-line definition (synthesize from how the entity is described across pages)
   - "## Mentioned in" bullet list with relative links to every wiki page that names it
   - Footer: "First indexed [today's date]"
5. Add a one-line "Entities" section to each source page with markdown links back to `wiki/entities/[slug].md`.

Append `wiki/log.md`: "[date] seed-wiki/entities: [N] entities indexed across [M] pages".

---

## Step 5: Update wiki/index.md

Rewrite `wiki/index.md` as a master TOC. Format:

```markdown
# Wiki Index

Built [today's date]. [N] pages, [M] entities.

## Categories
- [voice/]([N]), brand brain
- [founder/]([N]), who runs this
- [business/]([N]), what we make and sell
- [team/]([N]), who's on the team
- [priorities/]([N]), current focus
- [decisions/]([N]), strategic decisions
- [projects/]([N]), active workstreams
- [references/]([N]), SOPs and examples
- [entities/]([N]), people, products, businesses, competitors, concepts

## Recent activity
[last 10 lines from wiki/log.md, newest first]
```

Replace any existing content in `wiki/index.md`.

---

## Step 6: Run four sample queries

Don't exit silently. Pick four queries based on what was actually seeded:

- **Q1** (always): "What do I stand for?", searches voice/decision-filter, voice/identity.
- **Q2** (if business/ exists): "What businesses do I run, and what's the priority right now?", searches business/, priorities/current.
- **Q3** (if decisions/ exists): "What was my most recent strategic decision and why?", searches decisions/ (newest first).
- **Q4** (always, the stretch): "What's a connection across my work that I might not have noticed yet?", synthesizes across at least 3 pages, looks for non-obvious cross-references.

For each query:
- Read the relevant wiki pages
- Synthesize a 3-5 sentence answer in the kit's voice (read CLAUDE.md ## Tone)
- Cite the source pages with relative markdown links

Print all four with this exact format:

```
========================================
Sample queries on your seeded wiki
========================================

Q1: What do I stand for?
A: [3-5 sentence answer]
   Sources: [wiki/voice/identity.md], [wiki/voice/decision-filter.md]

Q2: What businesses do I run and what's the priority?
A: ...
   Sources: ...

Q3: Most recent strategic decision and why?
A: ...
   Sources: ...

Q4 (stretch): A connection across my work I might not have noticed.
A: ...
   Sources: ...

========================================
```

This is the proof step. The user sees the wiki working.

---

## Step 7: Hand off

End with this exact line, with the real numbers:

> "Wiki seeded. [N] pages, [M] entities, four sample queries answered. Try asking your own question. Just type it in plain English."

Append the final entry to `wiki/log.md`: "[date] seed-wiki: complete. [N] pages, [M] entities."

End the skill. Do not editorialize. Do not run another command.

---

## Hard rules

- Five sub-agents, ALL fired in ONE message. Parallel means parallel.
- Each sub-agent writes ONLY its assigned `wiki/[category]/` folder. No cross-folder writes.
- Entity merge runs ONLY after all five sub-agents have returned.
- Robust to missing files. If `context/me.md` doesn't exist, the context agent skips and logs "skipped." No errors.
- Idempotent. If `wiki/voice/index.md` already exists from a prior run, ask: "Wiki has prior seed data. Refresh, append, or skip? (refresh wipes wiki/[category]/ folders before re-ingesting; append adds new pages alongside existing; skip exits.)" Default to skip on no answer.
- The kit voice rules apply to every wiki page written. Read CLAUDE.md `## Tone` first and pass that voice to every sub-agent.
- No AI tells. No em dashes. No "delve, leverage, transformative, streamline" anywhere.
- The user sees the four sample queries answered before the skill exits. This is non-negotiable.
- Do NOT modify any source file in `context/`, `decisions/`, `projects/`, `references/`, or `CLAUDE.md`. The wiki is a derivative; sources stay clean.

---

## When to stop

Definition of done:

- Inventory shown, user confirmed.
- Five sub-agents fired in parallel and all returned.
- Entity merge completed; `wiki/entities/` populated.
- `wiki/index.md` rewritten.
- Four sample queries printed with citations.
- `wiki/log.md` has the final completion entry.

When all of the above are true, the wiki is seeded and the skill exits.
