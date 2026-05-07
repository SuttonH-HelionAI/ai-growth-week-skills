---
name: launch-campaign
description: Builds a complete campaign from one prompt. Fires six sub-agents in parallel. Each calls a kit skill. Output is one folder with research, strategy, emails, landing page, ads, and social posts. Auto-triggers on phrases like "launch a campaign", "build a campaign", "campaign in a box", "fire the kit", "run the whole flow". User-invocable as `/launch-campaign`. Takes a campaign slug as argument.
argument-hint: [campaign-slug] (e.g. forge-pre-workout)
disable-model-invocation: true
---

# /launch-campaign

One prompt. Six sub-agents. The whole kit fires at once. Output is a complete campaign in a single folder, ready to ship to real systems with the Day 3 deploy commands.

Day 4 hero skill. Built on top of every skill the operator already has.

---

## First-run guard

Before doing anything else, check if `CLAUDE.md` exists in the current working directory and contains `[BRAND COMPLETE]` on the last line.

- If both true → skip this guard, proceed with the skill.
- Otherwise → STOP and tell the user: "Brand brain isn't locked yet. Run `/claude-md-setup` first. Takes about 5 minutes. Come back and run me when you see `[BRAND COMPLETE]` at the bottom of your CLAUDE.md."
- Do not proceed until the marker is present.

---

## What this skill does

Takes one campaign idea and produces six artifacts in parallel:

1. A research brief
2. A strategy memo
3. A 3-email sequence
4. A real landing page (HTML)
5. Three ad hooks plus a visual prompt
6. A platform-tuned social post pack

All six write to `projects/[campaign-slug]/`. Cross-linked. Brand voice consistent across every artifact. Once dispatch finishes, the user can ship the email with `/klaviyo-deploy`, the page with `/site-update`, and any code change with `/github-flow`.

---

## How parallel works (read this once)

Each sub-agent runs in its own context window. None of them see the others' work. They all start at the same time. They all finish independently. This is why six things complete in roughly the time it takes to do one. Andrej Karpathy named the pattern "sub-agent compartmentalization." This skill uses it.

The dispatch is fire-and-forget. The skill reads the brief, fires all six sub-agents in one batch using the Task tool, then waits for all six to return. No back-and-forth with the user during dispatch.

---

## Step 1: Parse argument and load brand voice

If `$ARGUMENTS` is empty, ask the user: "What's the campaign slug? (lowercase, hyphens, like `forge-pre-workout`)"

Use the slug to define the output folder: `projects/$ARGUMENTS/`.

Read `CLAUDE.md` and pull these sections:

- `## Identity` — who the brand is and what it stands for.
- `## Tone` — voice rules, USE list, DON'T list.
- `## Audience` — who's reading, what they want.
- `## Lineup` — products or offers the campaign may reference.
- `## Repo` (if present) — for `/github-flow` follow-up.
- `## Email Lists` (if present) — for `/klaviyo-deploy` follow-up.
- `## Site` (if present) — for `/site-update` follow-up.

If `## Identity`, `## Tone`, `## Audience`, or `## Lineup` is missing, stop and tell the user to re-run `/claude-md-setup` before continuing. The four are the minimum the sub-agents need to produce on-voice work.

---

## Step 2: Get the campaign brief

Ask the user for a one-paragraph brief. Wait for the answer before going to Step 3.

Prompt them with this template:

```
Give me the campaign brief in one paragraph. Cover:
  - The offer (what we're launching or promoting)
  - The goal (first purchase, repeat buyer, win-back, education, etc.)
  - The audience cut (segment of your full audience, if narrower)
  - The hero claim (the one sentence the campaign hangs on)
  - Deadline or window (if any)
```

If the user gives a thin brief (less than three of those covered), ask once for the missing pieces. Do not push for more than one round of follow-up. The sub-agents can work from a thin brief.

Save the brief verbatim to `projects/$ARGUMENTS/brief.md`. Every sub-agent reads from this file.

---

## Step 3: Set up the output folder

Create the folder structure before dispatch. Sub-agents write into pre-existing folders, not folders they create.

```
projects/$ARGUMENTS/
├── brief.md             # the user's brief (already written in Step 2)
├── research.md          # helper 1 writes
├── strategy.md          # helper 2 writes
├── emails/              # helper 3 writes (3 markdown files)
├── landing.html         # helper 4 writes
├── ads.md               # helper 5 writes
├── social/              # helper 6 writes (markdown files per platform)
└── README.md            # this skill writes after all helpers finish
```

Use the Bash tool to create `projects/$ARGUMENTS/`, `projects/$ARGUMENTS/emails/`, and `projects/$ARGUMENTS/social/`.

---

## Step 4: Dispatch six sub-agents in parallel

Fire all six in a SINGLE message with six Task tool calls. Do not fire one and wait. Do not fire them sequentially. Parallel means parallel.

Each sub-agent is a `general-purpose` agent. Each gets the brief, the brand voice context, and one specific job. The exact prompts below — keep them tight.

### Sub-agent 1: Research brief

```
You are sub-agent 1 of 6 in a parallel campaign launch. Your single job is to write a research brief.

Working directory: [current working directory]
Brief file: projects/$ARGUMENTS/brief.md
Output file: projects/$ARGUMENTS/research.md

Steps:
1. Read projects/$ARGUMENTS/brief.md.
2. Read CLAUDE.md sections ## Identity, ## Tone, ## Audience, ## Lineup.
3. If a /competitive-research skill is installed, follow its pattern. Otherwise, write a brief covering:
   - Top 3 competitors in this category (names + one-line positioning each)
   - 5 customer pains pulled from real review-style language
   - 3 angle ideas the brand could own that the competitors don't
4. Save to research.md. Plain markdown. No HTML.

Constraints:
- No AI tells. No em-dashes. No "delve, leverage, transformative, streamline."
- Concrete and specific. No filler.
- Max 600 words.
- Do not write strategy, emails, ads, page copy, or social. That is other sub-agents' work.
```

### Sub-agent 2: Strategy memo

```
You are sub-agent 2 of 6 in a parallel campaign launch. Your single job is to write a strategy memo.

Working directory: [current working directory]
Brief file: projects/$ARGUMENTS/brief.md
Output file: projects/$ARGUMENTS/strategy.md

Steps:
1. Read projects/$ARGUMENTS/brief.md.
2. Read CLAUDE.md sections ## Identity, ## Tone, ## Audience, ## Lineup.
3. If a /strategy skill is installed, follow its pattern. Otherwise, write a memo covering:
   - The hero claim (one sentence the campaign hangs on)
   - The angle (positioning vs alternatives)
   - The channel mix (which channels carry the campaign and why)
   - The CTA (what we want the audience to do, in one verb)
   - The risk (the thing that could fail)
4. Save to strategy.md. Plain markdown.

Constraints:
- No AI tells. No em-dashes.
- One recommendation, not a menu.
- Max 500 words.
- Do not write copy, just direction.
```

### Sub-agent 3: Email sequence

```
You are sub-agent 3 of 6 in a parallel campaign launch. Your single job is to write a 3-email sequence.

Working directory: [current working directory]
Brief file: projects/$ARGUMENTS/brief.md
Output folder: projects/$ARGUMENTS/emails/

Steps:
1. Read projects/$ARGUMENTS/brief.md.
2. Read CLAUDE.md sections ## Identity, ## Tone, ## Audience, ## Lineup.
3. If a /email-sequence-builder skill is installed, follow its file format and rules. Otherwise, write 3 emails as separate files:
   - emails/email-01-[topic].md
   - emails/email-02-[topic].md
   - emails/email-03-[topic].md
4. Each file has: Subject line (under 50 chars, no first name), Preview text (under 80 chars), Send timing (Day 0, Day 2, Day 5), Body (plain text, paragraph breaks, no HTML), P.S. (always present), CTA (one action, one link).

Constraints:
- No AI tells. No em-dashes. No "delve, leverage, transformative, streamline."
- Every email gets a P.S.
- One CTA per email.
- Voice consistent across all three.
- Each email references the one before or builds toward the next.
- Do not write research, strategy, page copy, ads, or social.
```

### Sub-agent 4: Landing page

```
You are sub-agent 4 of 6 in a parallel campaign launch. Your single job is to build a real landing page.

Working directory: [current working directory]
Brief file: projects/$ARGUMENTS/brief.md
Output file: projects/$ARGUMENTS/landing.html

Steps:
1. Read projects/$ARGUMENTS/brief.md.
2. Read CLAUDE.md sections ## Identity, ## Tone, ## Audience, ## Lineup.
3. If a /frontend-design skill is installed, follow its CSS and structure conventions. Otherwise, write a single self-contained landing.html with:
   - Inline CSS (no external dependencies)
   - Hero section (headline = the brief's hero claim, sub-headline, primary CTA)
   - Three benefit blocks
   - One social proof block (placeholder if no real proof yet)
   - Final CTA section
   - Mobile-responsive (use simple CSS grid/flex; no framework)
   - Brand colors and typography matching ## Tone if specified, otherwise clean dark or clean light
4. Save to landing.html. Self-contained file.

Constraints:
- No AI tells in any copy on the page.
- One primary CTA, repeated at top and bottom. Same button text.
- No lorem ipsum. Real copy or specific placeholders.
- Do not write emails, ads, or social.
```

### Sub-agent 5: Ad variant pack

```
You are sub-agent 5 of 6 in a parallel campaign launch. Your single job is to write three ad hooks plus a visual prompt.

Working directory: [current working directory]
Brief file: projects/$ARGUMENTS/brief.md
Output file: projects/$ARGUMENTS/ads.md

Steps:
1. Read projects/$ARGUMENTS/brief.md.
2. Read CLAUDE.md sections ## Identity, ## Tone, ## Audience, ## Lineup.
3. Write three Meta ad variants. Each variant has:
   - Hook (1 sentence, scroll-stopping, brand voice)
   - Body (3-5 short sentences, slippery, ends in CTA)
   - CTA (one action, non-threatening verb)
   - Visual prompt (one paragraph describing the image, ready to paste into kie.ai or similar)
4. Save all three variants to ads.md, separated by `---`.

Constraints:
- No AI tells. No em-dashes.
- Three different angles, not three rewrites of the same thing.
- Each visual prompt is concrete enough to render with a single image model.
- Do not write the page, the emails, or social.
```

### Sub-agent 6: Social post pack

```
You are sub-agent 6 of 6 in a parallel campaign launch. Your single job is to write a social post pack.

Working directory: [current working directory]
Brief file: projects/$ARGUMENTS/brief.md
Output folder: projects/$ARGUMENTS/social/

Steps:
1. Read projects/$ARGUMENTS/brief.md.
2. Read CLAUDE.md sections ## Identity, ## Tone, ## Audience, ## Lineup.
3. If a /content-batch skill is installed, follow its pattern. Otherwise, write five posts, one file each:
   - social/01-instagram.md (carousel, 5-7 slides, Sutton's IG aesthetic)
   - social/02-x.md (single tweet, under 280 chars)
   - social/03-linkedin.md (medium-length post, professional tone, hook + insight + CTA)
   - social/04-threads.md (3-post thread, conversational)
   - social/05-tiktok-script.md (15-30 second script with hook, body, CTA)
4. Each post hooks on the campaign's hero claim from the brief. Same hero claim, five surface treatments.

Constraints:
- No AI tells. No em-dashes.
- Voice consistent with CLAUDE.md ## Tone.
- Each platform's post is shaped to that platform, not a copy-paste.
- Do not write the page, the emails, or the ads.
```

---

## Step 5: Wait, then aggregate

Wait for all six Task calls to return. Then:

1. Verify each expected file exists. If a sub-agent failed to write its file, note it but do not block.
2. Read each artifact. Do a quick voice-consistency check across them. If one obviously drifts (different vocabulary, different tone), note it in the README.
3. Write `projects/$ARGUMENTS/README.md` with the structure below.

---

## Step 6: Write the campaign README

Use this template exactly. Fill it in based on the artifacts that landed.

```markdown
# [Campaign slug, sentence cased]

**Status:** Drafted, ready to review and ship.
**Built:** [date]
**Slug:** [slug]
**Brief:** see brief.md

## What's in this folder

- [ ] [research.md](research.md) — Research brief (competitors, pains, angles)
- [ ] [strategy.md](strategy.md) — Strategy memo (hero claim, angle, channels, CTA)
- [ ] [emails/](emails/) — 3-email sequence
- [ ] [landing.html](landing.html) — Landing page, self-contained HTML
- [ ] [ads.md](ads.md) — 3 Meta ad variants with visual prompts
- [ ] [social/](social/) — Social post pack (IG, X, LinkedIn, Threads, TikTok)

## Hero claim

[one sentence pulled from strategy.md]

## Voice consistency

[one sentence on whether all six artifacts read like the same brand. If one drifted, name which.]

## Ship menu

When the user is ready to ship, run these:

```bash
# Email sequence to live Klaviyo flow
/klaviyo-deploy projects/[slug]/emails/

# Landing page to live site
/site-update projects/[slug]/landing.html

# Any code-side change to a real PR
/github-flow "ship [slug] landing page"
```
```

Replace `[slug]` and the bracketed placeholders with real values before writing.

---

## Step 7: Print the close-out summary

After README.md is written, print this to the user:

```
✓ Campaign drafted: projects/$ARGUMENTS/

Six artifacts:
  - research.md
  - strategy.md
  - emails/ (3 files)
  - landing.html
  - ads.md
  - social/ (5 files)

Ready to ship:
  /klaviyo-deploy projects/$ARGUMENTS/emails/
  /site-update projects/$ARGUMENTS/landing.html
  /github-flow "ship $ARGUMENTS landing page"

Read README.md for the full picture.
```

End the skill. Do not write more. Do not editorialize. The user reviews the artifacts on their own time.

---

## Hard rules

- Six sub-agents. Always six. Do not skip one because the brief feels light.
- Fire all six in parallel in a single message. Sequential dispatch defeats the entire point of the skill.
- Each sub-agent gets exactly one job. Do not let sub-agent prompts drift into "also do X."
- No AI tells in any artifact. The constraints are in each sub-agent prompt.
- The skill does not auto-deploy. It produces drafts. The user runs `/klaviyo-deploy`, `/site-update`, `/github-flow` themselves. This skill is dispatch, not deploy.
- Do not run if `[BRAND COMPLETE]` is missing.
- Do not run if `## Identity`, `## Tone`, `## Audience`, or `## Lineup` is missing from CLAUDE.md.

---

## When to stop

Definition of done:

- All six expected files exist in `projects/$ARGUMENTS/`.
- README.md is written and lists every artifact.
- The close-out summary is printed.
- The user has the three deploy commands in front of them, ready to fire.

When all of the above are true, the campaign is dispatched.
