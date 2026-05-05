---
name: email-sequence-builder
description: Drafts complete email sequences in the brand's voice. Covers welcome flows, launch sequences, re-engagement, abandoned cart, and post-purchase. Auto-triggers on phrases like "draft an email sequence", "welcome flow", "launch emails", "re-engagement", "post-purchase emails", "abandoned cart". User-invocable as `/email-sequence-builder`. Accepts an argument for sequence type.
---

# /email-sequence-builder

Builds a full email sequence from a short brief. Pulls the brand's voice straight from CLAUDE.md, asks three questions, then writes one email at a time with a feedback gate between each.

---

## First-run guard

Before doing anything else, check if `CLAUDE.md` exists in the current working directory and contains `[BRAND COMPLETE]` on the last line.

- If both true → skip this guard, proceed with the skill.
- Otherwise → STOP and tell the user: "Brand brain isn't locked yet. Run `/claude-md-setup` first. Takes about 5 minutes. Come back and run me when you see `[BRAND COMPLETE]` at the bottom of your CLAUDE.md."
- Do not proceed until the marker is present.

---

## What this skill does

Drafts a complete email sequence in the brand's voice the first time, no rewrite cycles needed. Reads identity, tone, audience, and product lineup from CLAUDE.md so every email sounds like the brand instead of a generic template. Outputs each email as its own markdown file inside an `emails/` folder.

---

## Step 1: Load brand voice

Read `CLAUDE.md` and pull these sections:

- `## Identity` — who the brand is and what it stands for.
- `## Tone` — voice rules, USE list, DON'T list.
- `## Audience` — who's reading.
- `## Lineup` — products or offers the sequence may reference.

If a `brand-voice` skill is also installed in this project, defer all voice and AI-tell rules to it. This skill writes the sequence. `brand-voice` enforces the line-level rules.

If any of those sections are missing, stop and tell the user to re-run `/claude-md-setup` before continuing.

---

## Step 2: Ask for the brief

Ask these three questions, one at a time. Wait for the answer before asking the next.

1. **Sequence type?** Welcome, launch, re-engagement, abandoned cart, post-purchase, or other.
2. **Product or offer?** Which product or promotion the sequence is built around, and what the goal is (first purchase, repeat purchase, win-back, education).
3. **Cadence?** How many emails and what day spacing. Example: 3 emails over 7 days, or 5 emails over 14 days.

Do not start writing until all three answers are in.

---

## Step 3: Output structure

Create an `emails/` folder in the current working directory if it does not exist. Each email is its own markdown file:

```
emails/
  email-01-[topic].md
  email-02-[topic].md
  email-03-[topic].md
```

Each file contains:

- **Subject line** — under 50 characters, no AI tells.
- **Preview text** — under 80 characters.
- **Send timing** — Day 0, Day 2, Day 5, etc.
- **Body** — plain text with paragraph breaks. No HTML.
- **P.S. line** — always present. Second most-read element after the subject.
- **CTA** — one clear action. One link. One button.

---

## Step 4: Write the emails

Write one email at a time. Follow this loop:

1. Draft email 01 fully, in the file format above, using the brand's voice from Step 1.
2. Show it to the user and ask: "Does this land, or do you want another pass before I move to email 02?"
3. Apply any feedback.
4. Move to email 02. Repeat.

Do not batch all drafts at once. Feedback after each email tightens the voice across the rest of the sequence and prevents redoing the same work five times.

---

## Hard rules

- No AI tells. No em-dashes, en-dashes, or "delve", "elevate", "unleash", "transformative", "leverage", "streamline", "dive into", "robust", "comprehensive", "harness". No corporate hedging like "it's worth noting" or "absolutely".
- Subject lines do not use the recipient's first name unless the brand's `## Tone` explicitly calls for casual personalization. Default is no name in the subject.
- Every email gets a P.S. No exceptions.
- One CTA per email. No "or you could also..." stacking. No secondary asks.
- Body length matches the brand's cadence. If the brand writes short and punchy, every email is short and punchy. If it writes long-form storytelling, every email is long-form storytelling. Consistent across the sequence.
- Keep the through-line. Each email should reference the one before it or build toward the next, not read like five disconnected blasts.

---

## When to stop

Definition of done:

- Every email in the cadence is written and saved as its own file in `emails/`.
- Voice is consistent across the sequence.
- Every email has a P.S.
- Every email has exactly one CTA.
- No AI tells in any draft.
- The user has signed off on each email before moving to the next.

When all of the above are true, the sequence ships.
