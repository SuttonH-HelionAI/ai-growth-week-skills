---
name: brand-voice
description: Strips AI tells out of every line of copy. Auto-triggers on emails, ads, captions, copy, and any draft that needs to sound like the brand instead of like ChatGPT. Reads ## Tone from CLAUDE.md and rewrites until the draft matches. Trigger when the user pastes a draft, asks to clean up copy, or any time output sounds generic.
---

# /brand-voice

Forces every line of copy through the brand's `## Tone` rules. Strips AI tells. Tightens voice until the draft sounds like the brand talking, not a generic chatbot.

---

## First-run guard

Before doing anything else, check if `CLAUDE.md` exists in the current working directory and contains `[BRAND COMPLETE]` on the last line.

- If both true → skip this guard, proceed with the skill.
- Otherwise → STOP and tell the user: "Brand brain isn't locked yet. Run `/claude-md-setup` first. Takes about 5 minutes. Come back and run me when you see `[BRAND COMPLETE]` at the bottom of your CLAUDE.md."
- Do not proceed until the marker is present.

---

## Step 1: Load the tone rules

Read `CLAUDE.md`. Pull the `## Tone` section. Extract:

- **USE list**, words and patterns the brand actively uses.
- **DON'T list**, words and patterns the brand avoids.

If `## Tone` is missing or empty, stop and tell the user to re-run `/claude-md-setup` and fill in the Tone section before continuing.

---

## Step 2: Take the draft

The user will either paste a draft or ask you to write one. Either way, the output is judged against the same rules.

If the user pastes a draft, run it through the strip-and-rewrite pass below.
If the user asks for a fresh draft, write it with the rules already applied.

---

## Step 3: Strip the AI tells

Every draft gets scanned for these. Replace or remove every hit.

**Banned words and phrases (universal AI tells):**
- "delve" / "delving"
- "unleash"
- "elevate"
- "leverage" (as a verb)
- "transformative"
- "streamline"
- "dive into" / "deep dive"
- "it's worth noting"
- "certainly"
- "absolutely"
- "navigate the landscape"
- "in today's world"
- "in the realm of"
- "unlock"
- "harness"
- "robust" (as filler)
- "comprehensive" (as filler)
- "embark on"
- "tapestry"
- "ever-evolving"
- "cutting-edge" (as filler)

**Banned punctuation:**
- Em-dashes (`—`). Replace with commas, periods, or line breaks.
- En-dashes (`–`). Same.
- Excess exclamation points. One in a draft is plenty. Zero is usually better.

**Banned patterns:**
- Hedging openers: "It's important to note that..." "One could argue..." "Many people believe..."
- Trailing summaries: "In conclusion..." "To summarize..." "All in all..."
- Throat-clearing: "Great question." "Sure thing." "Of course."
- Generic affirmation closers: "Hope this helps!" "Let me know if you have questions!"
- Three-adjective stacks: "innovative, dynamic, transformative." Pick one or zero.
- Vague abstractions where a specific noun would land: "various solutions," "key insights," "valuable resources."

---

## Step 4: Apply the brand's USE list

After stripping, rewrite using the words and patterns under `## Tone → USE`.

If the USE list says "direct, technical, calm", the draft must read direct, technical, and calm. Not "polished" or "approachable" or any neighbor word.

If the USE list includes specific phrases or signature lines, work them in where they fit. Don't force them.

---

## Step 5: Apply the brand's DON'T list

Even if a word is not on the universal AI-tell list, if it's on the brand's `## Tone → DON'T` list, strip it.

This is where each brand differs. Honor what the user wrote. Don't second-guess their `DON'T` list.

---

## Step 6: Tightness pass

Read the draft out loud (or simulate doing so). Cut every word that doesn't pull weight.

- Long sentences → split.
- Three adjectives → one.
- Filler words ("really," "very," "actually," "just," "quite") → cut.
- Passive voice → active.
- Abstract noun → concrete noun.

The test: if the line could appear on any brand's marketing, rewrite it until only this brand could have written it.

---

## Step 7: Output

Return the cleaned draft. Then add a short audit at the bottom:

```
---
Voice check
- AI tells stripped: [list of words removed, or "none"]
- Em-dashes stripped: [count]
- USE-list words present: [list]
- DON'T-list words flagged: [list, or "none"]
- Tightness: [list of cuts made, or "draft was tight"]
```

If any DON'T-list word still appears in the final draft, fix it before delivering. Do not ship a draft that fails its own brand's tone rules.

---

## Rules

- Always read `## Tone` from CLAUDE.md before rewriting.
- Strip every AI tell on the universal list. No exceptions.
- Strip every word on the brand's DON'T list. No exceptions.
- No em-dashes. Ever.
- One idea per sentence. One CTA per draft.
- The output should read like the brand wrote it, not like an assistant approximated it.
- Don't add new content the user didn't ask for. Tighten what's there.
