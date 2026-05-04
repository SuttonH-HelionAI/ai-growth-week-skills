---
name: brand-guidelines
description: Stops your team from publishing anything off-brand. Auto-triggers on PDPs, ads, emails, social, copy, landing pages, and any customer-facing visual or written output. Reads your brand specifics from CLAUDE.md and the brand-system/ folder if present. Trigger when the user is drafting a PDP, ad, email, social post, landing page, or any branded surface.
---

# /brand-guidelines

Holds the design and writing rules for the brand. Auto-triggers any time someone drafts customer-facing output. Acts as the gate that keeps off-brand work from shipping.

---

## First-run guard

Before doing anything else, check if `CLAUDE.md` exists in the current working directory and contains `[BRAND COMPLETE]` on the last line.

- If both true → skip this guard, proceed with the skill.
- Otherwise → STOP and tell the user: "Brand brain isn't locked yet. Run `/claude-md-setup` first. Takes about 5 minutes. Come back and run me when you see `[BRAND COMPLETE]` at the bottom of your CLAUDE.md."
- Do not proceed until the marker is present.

---

## Step 1: Load the brand brain

Read these files in order:

1. `CLAUDE.md`, pull `## Identity`, `## Lineup`, `## Audience`, `## Tone`, `## Decision Filter` sections.
2. `brand-system/` folder, if present, scan for design tokens, color palettes, typography, logo guidance, component examples. If the folder is missing, tell the user: "No `brand-system/` folder detected. Visual rules will fall back to text. To unlock the full visual system, run `/claude-md-setup` and follow the brand-system step." Continue with text-only rules.

If `## Identity` is missing or empty, stop and tell the user to re-run `/claude-md-setup` to fill it in.

---

## Step 2: Identify the surface

Ask the user (or detect from context) what's being drafted:

- PDP (product detail page)
- Ad (Meta, Google, YouTube, etc.)
- Email (broadcast, flow, transactional)
- Social post (caption, carousel, story, reel script)
- Landing page
- Long-form content (blog, newsletter, script)
- Other customer-facing copy

The rules differ by surface. Confirm which surface before applying.

---

## Step 3: Apply the rules

### Universal rules (apply to every surface)

**Voice:**
- Use the words listed under `## Tone → USE` in CLAUDE.md.
- Strip every word in `## Tone → DON'T`.
- No em-dashes (`—`). Use commas, periods, or line breaks instead.
- No AI tells: "delve," "unleash," "elevate," "leverage," "transformative," "streamline," "dive into," "it's worth noting," "certainly," "absolutely," "navigate the landscape," "in today's world."
- Short sentences over long ones. Punchy over flowing.
- Specific over vague. Numbers over adjectives.

**Audience fit:**
- Every line should make sense to the audience defined in `## Audience`.
- If the line could appear on any brand's marketing, it's too generic. Rewrite it to something only this brand could say.

**Identity fit:**
- Run the draft against `## Identity`. If it contradicts what the brand stands for, kill it.
- Run the draft against `## Decision Filter`. If it fails any of the 5 values, rewrite or kill it.

### Surface-specific rules

**PDP:**
- Hero section: product name, hero benefit, real price, primary CTA.
- Below the fold: 3-5 specific benefits with proof or mechanism for each. No vague claims.
- Ingredient/spec block: full transparency. Real doses, real sourcing, real testing.
- Social proof: real reviews or named experts, never fake testimonials.
- FAQ: address the top 3-5 objections from `## Audience`.

**Ad:**
- Hook in line one. Stop the scroll.
- One core promise. Not three.
- One CTA. Match the awareness level of the audience.
- Visual: must follow the brand-system design tokens if present. If absent, use the brand's tone words to guide the aesthetic.

**Email:**
- Subject line: short, specific, no clickbait, no merge-tag tricks. First-name personalization is fine; complex merge tags break.
- Body: one idea, one CTA. P.S. line is allowed and often the most-read element.
- Voice must match `## Tone` exactly. Read the draft out loud, if it doesn't sound like the brand talking, rewrite.

**Social post:**
- One idea per post. Don't stack three.
- Caption hook in line one. Pay it off in the body. Single CTA.
- Visuals follow brand-system tokens.

**Landing page:**
- One promise above the fold. One CTA.
- Below the fold: proof, mechanism, objection handling, urgency or scarcity if real.
- Single conversion goal. Strip every link or distraction that doesn't serve it.

**Long-form content:**
- Hook in the first sentence. Pay it off by the end.
- Teach something specific. If it's all opinion or all summary, rewrite.
- Closing CTA matches the awareness level of the reader.

---

## Step 4: Output

Produce the draft in the requested surface format. Then add a short audit at the bottom:

```
---
Brand check
- Voice: [pass / [list of words flagged for rewrite]]
- Identity fit: [pass / [conflicts named]]
- Decision Filter: [pass / [filter values violated]]
- Visual rules: [applied from brand-system / text-only fallback]
```

If any check fails, fix it before delivering. Do not ship a draft that fails the brand check.

---

## Rules

- Always read CLAUDE.md before drafting. No exceptions.
- Use the user's tone words verbatim. Do not import outside-brand voice.
- Strip every AI tell on every pass. Catching them is the job.
- If the brand-system folder is present, follow its design tokens. If it's missing, name the gap and continue with text-only.
- Never ship a draft without running the brand check. The check is not optional.
- One CTA per surface. One promise per surface. Subtraction is the work.
