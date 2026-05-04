---
name: claude-md-setup
description: Master lock-in orchestrator. Run this FIRST after dropping the AI Growth Week skill kit into a project. Checks for a brand-system/ folder, runs the 5-section CLAUDE.md interview (Identity, Lineup, Audience, Tone, Decision Filter), writes the file, and appends [BRAND COMPLETE] as the last line. Idempotent, safe to re-run. Trigger when the user says "set up CLAUDE.md", "lock in my brand", "/claude-md-setup", or runs another skill that fails its first-run guard.
---

# /claude-md-setup

The single command an attendee runs after dropping the kit in. Walks them from "fresh project folder" to "CLAUDE.md locked, brand brain wired in" in about 5 minutes.

This skill does NOT include a first-run guard. It IS the first run.

---

## Step 1: Greet

Open with this exact line:

> "Locking you in for Day 2. Takes about 5 minutes."

Then ask: "Ready?" Wait for confirmation before continuing.

---

## Step 2: Brand-system check

Look for a `brand-system/` folder in the current working directory.

- **Found** → "Brand design system detected. Good." Continue to Step 3.
- **Missing** → ask:

  > "Did you build a brand design system in claude.ai/design today?"

  Three options:

  - **"yes, I have the zip"** → "Drop it in this folder, unzip it, and rename the folder to `brand-system/`. Tell me when done." Wait. Recheck for the folder.
  - **"not yet"** → "Open claude.ai/design now. Build the system (5 min). Export ZIP. Drop it in this folder, unzip, rename the folder `brand-system/`. Tell me when done." Wait. Recheck for the folder.
  - **"skip for now"** → "Some Day-2 references will fall back to text. You can add it later. Continuing." Continue to Step 3.

---

## Step 3: CLAUDE.md state check

Read `CLAUDE.md` from the current working directory.

- **File missing** → run the full 5-section interview (Step 4). Skip the keep/augment/rebuild prompt.
- **File exists, last line is `[BRAND COMPLETE]`** → say: "Already locked. Skipping the interview." Skip to Step 6.
- **File exists, no `[BRAND COMPLETE]` marker** → ask:

  > "Found a CLAUDE.md but it's not marked complete. Three options:
  > (a) keep as-is and just add the flag
  > (b) augment, I'll fill in any sections that are missing
  > (c) rebuild from scratch
  > Pick one."

  - **(a) keep as-is** → just append `[BRAND COMPLETE]` on a new last line. Skip to Step 6.
  - **(b) augment** → read the file, identify which of the 5 sections (Identity, Lineup, Audience, Tone, Decision Filter) are missing or empty, run the interview ONLY for those sections. Merge into the existing file.
  - **(c) rebuild from scratch** → archive the existing file as `CLAUDE.md.backup-YYYY-MM-DD` (use today's date), then run the full interview.

---

## Step 4: The 5-section interview

Ask one question at a time. Show one example with each question. Wait for the answer before moving to the next.

Use the user's words. Do not paraphrase or "improve" them. The goal is to capture how they actually talk about their brand.

### Section 1, Identity

> "Who are you, what do you do, what do you stand for? 3-5 lines is enough.
>
> Example: 'We design home-office furniture for remote operators who treat their workspace like a cockpit. We stand against the cheap, disposable, plastic-everywhere norm in the category. Every piece is built to last 20 years and serviceable, not landfill bait.'"

### Section 2, Lineup

> "List every product. For each one, give me: the name, the hero benefit (one line), and the real price.
>
> Example:
> - Operator Chair: 12-hour ergonomic chair, $1,290
> - Ridge Desk: solid walnut sit-stand, $1,890
> - Field Lamp: warm task light, no blue spill, $240"

### Section 3, Audience

> "Two paragraphs. Who do you sell to? What hurts them right now? What do they want?
>
> Example: 'Remote operators 30-50 who spend 6+ hours a day at a desk. Founders, engineers, designers, writers. They've already cycled through three cheap chairs and a folding table, and their back is paying for it. They want one piece they buy once and never think about again, from a brand that knows what real desk work feels like.'"

### Section 4, Tone

> "Words you USE. Words you DON'T. The voice that strips AI tells from every output.
>
> Example:
> USE: direct, calm, technical when needed, never hyped, never preachy
> DON'T: 'unleash,' 'elevate,' 'transformative,' em-dashes, exclamation points, motivational-poster phrases"

### Section 5, Decision Filter

> "5 non-negotiable values. Every recommendation /strategy makes runs through these before it outputs. These are yours, not mine.
>
> Examples (yours will be different):
> - Does this serve the customer's actual outcome, not just our revenue?
> - Does this strengthen our category positioning?
> - Does this preserve our quality standard?
> - Would I be proud of this in 10 years?
> - Does this honor what we stand for?"

If they don't have 5, push them to fill in the blanks. The Decision Filter is what `/strategy` reads from in Step 4. If it's empty, `/strategy` will refuse to run.

---

## Step 5: Write the file

Write `CLAUDE.md` in the current working directory using this template, populated with the answers from the interview:

```
# [Brand Name]

## Identity
[Their answer to section 1]

## Lineup
[Their answer to section 2, bullet list, one product per line]

## Audience
[Their answer to section 3]

## Tone
[Their answer to section 4, split into USE: and DON'T: lines]

## Decision Filter
1. [Value 1]
2. [Value 2]
3. [Value 3]
4. [Value 4]
5. [Value 5]

[BRAND COMPLETE]
```

**Hard rules:**
- Cap the entire file at 200 lines. If a section runs long, trim it before writing, quality over quantity.
- `[BRAND COMPLETE]` must be the LAST line of the file with no trailing whitespace or blank lines after it.
- Use the user's words verbatim. Do not "polish" their voice.

---

## Step 6: Suggested test

Tell the user:

> "Now run `/brand-guidelines` and ask it to draft a fake PDP for one of your products. Confirm the skill auto-triggers, reads your CLAUDE.md, and outputs in your voice."

Do NOT auto-run `/brand-guidelines`. Hand off and exit.

---

## Step 7: Confirm

End with this exact line:

> "Locked in for Day 2."

---

## Rules

- One question at a time. Never dump a full questionnaire.
- Show one example per question. Make the example concrete, not abstract.
- Use the user's words. Do not paraphrase or sanitize.
- 200-line cap on the final file. Hard rule.
- `[BRAND COMPLETE]` is always the last line. No exceptions.
- This skill is idempotent. Re-running it on a complete file should detect the marker and skip gracefully.
- Do not edit any other files in the project. CLAUDE.md only.
