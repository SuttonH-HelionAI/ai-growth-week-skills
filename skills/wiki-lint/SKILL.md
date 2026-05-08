---
name: wiki-lint
description: Day 5 weekly health check for the wiki memory. Scans wiki/ for contradictions, stale claims, orphaned pages, missing cross-references, and gaps in coverage. Reports a triage list. Does not auto-fix. The user decides what to fix, what to archive, and what to queue for next week's ingest. Auto-triggers on phrases like "lint the wiki," "clean up the wiki," "wiki health check," "audit the wiki." User-invocable as `/wiki-lint`. Run weekly, takes about 10 minutes.
disable-model-invocation: false
---

# /wiki-lint

The Friday 10-minute pass that keeps the wiki from rotting. Reads the wiki, surfaces what is broken, hands the founder a clean triage list. The fix is human. The audit is automated.

---

## First-run guard

Before doing anything else, check that:

1. `CLAUDE.md` exists in the working directory and contains `[BRAND COMPLETE]` on the last line.
2. A `wiki/` folder exists and contains `wiki/CLAUDE.md`.

- If either is missing → STOP and tell the user: "No wiki to lint here. Run `/start-wiki` first to build one."
- Otherwise → continue.

---

## Step 1: Greet

Open with this exact line:

> "Wiki health check. Takes about a minute to scan, then I'll hand you a triage list."

---

## Step 2: Scan the wiki

Use the Bash and Read tools to:

1. List every `.md` file in `wiki/` and `sources/`.
2. Read every wiki page (skip `wiki/CLAUDE.md`, `wiki/index.md`, `wiki/log.md`).
3. Hold them in memory for the checks below.

---

## Step 3: Run the five checks

### Check 1: Contradictions

Scan for claims that contradict each other across pages. Examples:

- One page says a customer's biggest pain is X. Another page says it is Y.
- One page lists a competitor's price as $X. Another page lists it as $Y.
- One page says a product helps with sleep. Another page in the same wiki says it helps with focus, with no source distinguishing them.

For each contradiction found, capture:
- The two file paths
- The conflicting claim, in one line each

### Check 2: Stale claims

Read `wiki/log.md` to find page creation dates. Flag any wiki page where:

- The last log entry referencing the page is older than 90 days.
- The page makes a time-sensitive claim ("currently," "this quarter," "the latest," a specific year).

Capture: file path, age in days, the suspect claim.

### Check 3: Orphaned pages

For each wiki page, check if any other wiki page links to it (markdown link or relative path mention).

- Pages with zero inbound links from other wiki pages = orphans. (`wiki/index.md` does not count as an inbound link; only entity-to-entity counts.)
- Capture: file path, last-touched date.

### Check 4: Missing cross-references

For each entity mentioned in a wiki page (a customer name, a competitor name, a product name, a person), check whether the entity has its own page in the wiki.

- If the entity is mentioned 3 or more times across different pages but has no entity page → flag it.
- Capture: entity name, list of pages where it appears.

### Check 5: Coverage gaps

For each category in `wiki/CLAUDE.md`, count how many wiki pages exist in the corresponding `wiki/[category]/` folder.

- Categories with zero wiki pages → coverage gap.
- Categories with only 1-2 pages and 5+ sources sitting un-ingested in `sources/[category]/` → ingest backlog.
- Capture: category name, wiki page count, pending source count.

---

## Step 4: Build the triage report

Print the report on screen using this exact format. If a section has zero items, write "✓ none" and move on.

```
# Wiki lint, [today's date YYYY-MM-DD]

## Contradictions (fix today)
[list, one per line. Empty? "✓ none"]

## Stale claims (review or refresh)
[list, one per line. Empty? "✓ none"]

## Orphaned pages (link in or archive)
[list, one per line. Empty? "✓ none"]

## Missing entity pages (build this week)
[list, one per line. Empty? "✓ none"]

## Coverage gaps and ingest backlog (queue this week)
[list, one per line. Empty? "✓ none"]
```

---

## Step 5: Triage prompt

After the report, ask the user:

> "Want me to fix anything from this list now? I can:
>
> - Resolve a contradiction (you tell me which fact is correct, I update the losing page)
> - Build a missing entity page (I will pull what is known from other pages)
> - Ingest a backlog source (give me the file)
>
> Or pick one to handle yourself. The full report is in `wiki/log.md` for next time."

If the user says "skip," log the report and exit.

If the user picks an action, do that one action only. Do not chain. Do not auto-fix more than what was asked.

---

## Step 6: Log the lint

Append to `wiki/log.md`:

```
[YYYY-MM-DD HH:MM] lint by /wiki-lint: [N] contradictions, [N] stale, [N] orphans, [N] missing entities, [N] coverage gaps. User actioned: [action taken or "none"].
```

Save the full report as `wiki/lint-reports/[YYYY-MM-DD].md` so the founder has a paper trail.

---

## Step 7: Hand off

End with this exact line:

> "Wiki lint logged. See you next Friday."

Do not editorialize. Do not run another skill.

---

## Hard rules

- Audit only. Never auto-fix without the user picking the action.
- The triage list is the deliverable. A clean list is success.
- Always log to `wiki/log.md` and write a dated report to `wiki/lint-reports/`.
- 10-minute pass means the report is shown in under a minute. Long reports get summarized; full detail is in the dated file.
- No AI tells. No em dashes. No motivational language. The lint is a maintenance check, not a pep talk.

---

## When to stop

Definition of done:

- The five checks have run.
- The report is on screen.
- The triage prompt was offered.
- One action was taken (or "skip" was logged).
- `wiki/log.md` and `wiki/lint-reports/[date].md` are updated.

When all of the above are true, the lint is complete.
