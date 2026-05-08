---
name: start-wiki
description: Day 5 onboarding skill. Builds a wiki memory inside the kit and walks the founder from "blank" to "wiki alive, first ingest done, first question answered, Friday clean-up scheduled" in about 5 minutes. Asks 2 short questions, creates sources/ and wiki/, writes a tailored wiki schema, ingests the founder's first source live, runs one sample query, and adds a ## Wiki section to the kit's CLAUDE.md so future sessions handle ingest, query, and save conversationally without slash commands. Auto-triggers on phrases like "set up my wiki," "start wiki," "give my AI a memory," "make the AI remember." User-invocable as `/start-wiki`. Idempotent, safe to re-run.
disable-model-invocation: false
---

# /start-wiki

The single command an attendee runs on Day 5. One paste, conversational onboarding, ~5 minutes from cold to compounding.

This skill orchestrates an entire onboarding flow. It is the heavy lifting so the founder does not have to think about folder structure, schema, or commands.

---

## First-run guard

Before doing anything else, check that `CLAUDE.md` exists in the current working directory and contains `[BRAND COMPLETE]` on the last line.

- If both true → continue.
- Otherwise → STOP and tell the user: "Your brand brain is not locked yet. Run `/claude-md-setup` first. Takes about 5 minutes. Come back and run me when you see `[BRAND COMPLETE]` at the bottom of your CLAUDE.md."

Do not proceed until the marker is present.

---

## Step 1: Greet and set expectations

Open with this exact line:

> "Building you a memory that compounds. Two short questions, then I do the rest. About 5 minutes."

Then ask: "Ready?" Wait for confirmation.

---

## Step 2: Idempotency check

Look for an existing `wiki/CLAUDE.md` in the working directory.

- **Found** → say: "Wiki is already set up here. I'll show you what's inside and skip the build." Read `wiki/index.md` if it exists, summarize it in 3 lines, and skip to Step 7 (sample query). The user can drop new sources later.
- **Missing** → continue.

---

## Step 3: Question 1, what do you want it to remember most?

Ask exactly:

> "What do you most want your AI to remember? Pick one to start. You can add more later.
>
> 1. **Customers**, reviews and DMs and support tickets and sales calls
> 2. **Products and ingredients**, research and claims and specs and dosages
> 3. **Competitors**, their pages and ads and pricing and angles
> 4. **Your own writing**, your voice and founder story and past posts
> 5. **Something else**, describe in one line"

Hold the answer. This becomes the seed category for the schema.

---

## Step 4: Question 2, what is your first source?

Ask exactly:

> "Drop your first source on me. Either:
>
> - paste 1-3 paragraphs of content right here in chat (a customer review, a paragraph from a competitor's page, a snippet from a podcast you took notes on)
> - or give me a file path to a doc you already have on your computer
>
> One source is enough. We will use it to seed the wiki."

Wait for the answer. Hold the content.

---

## Step 5: Build the structure

Use the Bash tool to create:

```
wiki/
sources/
sources/[category]/
wiki/[category]/
```

Where `[category]` matches the slug for the user's Step 3 answer:
- Customers → `customers`
- Products and ingredients → `ingredients`
- Competitors → `competitors`
- Your own writing → `voice`
- Something else → derive a one-word slug from their description

Then write three seed files:

### `wiki/CLAUDE.md` (the wiki schema)

```
# Wiki schema

This folder is the AI memory for [Brand Name from kit's CLAUDE.md].

## Layout
- `sources/` holds raw inputs. Read-only for the AI. Originals live here.
- `wiki/` holds AI-built notes. The AI owns this layer.
- `wiki/index.md` catalogs every wiki page by category.
- `wiki/log.md` records every ingest, query, and lint.

## Categories in this wiki
- `[chosen category slug]/` (seeded today)

## Ingest rule
When the user adds a file to `sources/`, or asks to "ingest" or "remember" something:
1. Read the source.
2. Write a short summary page in the matching `wiki/[category]/` folder.
3. Update or create entity pages for any people, products, or competitors named.
4. Update `wiki/index.md` with the new page.
5. Append a one-line entry to `wiki/log.md`: timestamp, source slug, action.

## Query rule
When the user asks a question that could be answered from the wiki:
1. Search `wiki/` for relevant pages.
2. Answer with citations to the source pages.
3. If the answer is reusable, offer to save it back to `wiki/[category]/`.

## Lint rule
When the user asks to "clean up the wiki" or "lint":
1. Scan for contradictions across pages.
2. Flag stale claims (entries older than 90 days that may have changed).
3. List orphaned pages (pages no other page links to).
4. Report missing cross-references.
5. Do not auto-fix. Show the report. The human triages.

## Voice
Read the kit's main `CLAUDE.md` for tone. Write wiki notes in that voice.
```

Substitute `[Brand Name from kit's CLAUDE.md]` with the actual brand name from the first line of the kit's `CLAUDE.md`.

### `wiki/index.md`

```
# Wiki index

Built [today's date in YYYY-MM-DD format].

## Categories
- [category]/ - seeded
```

### `wiki/log.md`

```
# Wiki log

Append-only record of every ingest, query, and lint.

[YYYY-MM-DD HH:MM] init by /start-wiki, category seeded: [category]
```

---

## Step 6: Ingest the first source live

Take the content the user gave in Step 4 and ingest it.

1. If they pasted content: save it to `sources/[category]/first-source.md` with a one-line metadata header: `> source captured [date]`.
2. If they gave a file path: copy the file (or read and re-save it) into `sources/[category]/[original-filename].md`.
3. Write a summary page to `wiki/[category]/first-source-summary.md`. The summary should:
   - Have a one-line title that captures the essence
   - Have a 3-5 bullet "key points" list
   - Link back to the source path
4. Update `wiki/index.md` with the new page.
5. Append to `wiki/log.md`: `[timestamp] ingest by /start-wiki: first-source`.

Show the user the diff. Print:

```
✓ Source saved: sources/[category]/first-source.md
✓ Summary written: wiki/[category]/first-source-summary.md
✓ Index updated, log updated.
```

---

## Step 7: Sample query

Pick a sample query that fits the chosen category:

- **Customers** → "Based on this source, what is the customer's biggest concern?"
- **Products and ingredients** → "Based on this source, what is the most defensible claim?"
- **Competitors** → "Based on this source, what is the competitor's main angle?"
- **Your own writing** → "Based on this source, what 3 phrases sound most like the founder?"
- **Something else** → derive a relevant question

Run the query against the wiki. Answer with citations to the new wiki page. Print the answer on screen.

Then ask:

> "Want me to save that answer back to the wiki? It will be there next time you ask, no re-search needed."

If yes, save to `wiki/[category]/sample-answer.md` and append to `wiki/log.md`.

---

## Step 8: Wire the wiki into the kit's CLAUDE.md

Read the kit's main `CLAUDE.md` (the one at the working directory root, not the one in `wiki/`).

Check for an existing `## Wiki` section.

- **Section exists** → skip this step. Tell the user: "Wiki section already in your CLAUDE.md. Skipping."
- **Section missing** → insert this block immediately before the `[BRAND COMPLETE]` marker:

```
## Wiki

A wiki memory lives at `wiki/` with raw sources at `sources/`.

When the user says "remember this," "save this," "ingest this," or drops a file into `sources/`:
- Read the source.
- Write a summary in the matching `wiki/[category]/` folder.
- Update `wiki/index.md` and `wiki/log.md`.

When the user asks a question that could be answered from the wiki:
- Search `wiki/` for relevant pages.
- Answer with citations to the source pages.
- Offer to save the answer back to the wiki if it is reusable.

When the user says "clean up the wiki" or "lint":
- Run `/wiki-lint`.

The wiki schema is in `wiki/CLAUDE.md`. Read it on first ingest of a new session.
```

This is what makes the daily flow conversational. Future sessions handle ingest, query, and save without slash commands because Claude reads this section every session.

---

## Step 9: Friday clean-up reminder

Print this to the user:

```
✓ Wiki alive.
✓ One source ingested. One question answered.
✓ Kit's CLAUDE.md updated with the wiki rules.

Last thing: a Friday lint keeps the wiki from rotting. Add a 10-minute weekly reminder.

Calendar text to copy:
  Title: Wiki clean-up
  Time: Friday 9:00 AM (your time)
  Repeat: Weekly
  Note: Open Claude in the kit folder. Run /wiki-lint. Triage what it flags. Done in 10 min.
```

Do not auto-add the calendar event. The founder pastes it themselves.

---

## Step 10: Hand off

End with this exact line, customized to the chosen category:

> "Your wiki is alive in `wiki/`. From here on, just talk to me. Drop a [source type from the category] in `sources/` and say 'remember this.' Ask me a question and I will read the wiki first. We are done."

End the skill. Do not editorialize. Do not run another command.

---

## Hard rules

- Two questions, no more. The skill is the teacher; the founder is not filling out a form.
- One ingest live, with a visible diff. The founder must see the wiki get built.
- One sample query with citations. The founder must see the wiki answer.
- The kit's main CLAUDE.md gets the `## Wiki` section appended once. This is what makes the daily flow conversational.
- Idempotent. Re-running the skill on an already-set-up wiki should detect it and skip the build.
- Never write to `sources/` after the first ingest. The founder owns that folder forever after.
- No AI tells. No em dashes. The skill talks like a calm builder, not a marketer.

---

## When to stop

Definition of done:

- `wiki/`, `sources/`, and category subfolders exist.
- `wiki/CLAUDE.md`, `wiki/index.md`, `wiki/log.md` exist.
- One source is in `sources/[category]/`. One summary page is in `wiki/[category]/`.
- The kit's main `CLAUDE.md` has a `## Wiki` section.
- The user saw one sample query answered with citations.
- The Friday reminder text was printed.

When all of the above are true, the wiki is live and the skill exits.
