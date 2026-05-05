---
name: frontend-design
description: Builds high-craft HTML/CSS pages that match the brand. Auto-triggers on phrases like "build a landing page," "design a PDP," "make a hero section," "frontend page," "web page," "design a page." User-invocable as `/frontend-design`. Accepts an argument: page type (landing, PDP, hero, about) or a reference URL/image. Use before writing any frontend code. Covers reference matching, local server setup, screenshot loop, brand asset usage, and anti-generic guardrails.
---

# /frontend-design

Builds web pages that look like a designer made them, not an LLM. Reads the brand brain, matches a reference, runs a screenshot loop, and refuses generic AI defaults. Use before writing any frontend code.

---

## First-run guard

Before doing anything else, check if `CLAUDE.md` exists in the current working directory and contains `[BRAND COMPLETE]` on the last line.

- If both true → skip this guard, proceed with the skill.
- Otherwise → STOP and tell the user: "Brand brain isn't locked yet. Run `/claude-md-setup` first. Takes about 5 minutes. Come back and run me when you see `[BRAND COMPLETE]` at the bottom of your CLAUDE.md."
- Do not proceed until the marker is present.

---

## What this skill does

Builds high-craft HTML and CSS pages that match the brand identity defined in `CLAUDE.md` and `brand-system/`. Replaces generic AI design output with intentional, branded craft. Treats every page as a design problem first, code problem second.

---

## Step 1: Load brand context

Read these in order:

1. `CLAUDE.md`, pull `## Identity`, `## Tone`, `## Audience`, and any color/typography sections.
2. `brand-system/` folder if present. Pull color palette, typography stack, logo assets, spacing tokens, component examples, and any do/don't visual rules.
3. If `brand-system/` is missing, tell the user: "No `brand-system/` folder detected. I'll fall back to text rules from CLAUDE.md. To unlock the full visual system, run `/claude-md-setup` and add the brand-system step." Continue.

If `## Identity` is missing or empty, stop and tell the user to re-run `/claude-md-setup`.

---

## Step 2: Reference image workflow

Ask the user one question: "Do you have a reference image, URL, or page you want this to look like?"

- If yes → load it. Match composition, hierarchy, spacing, typography scale. Match it, don't invent around it.
- If no → propose 2-3 directional examples from real brands that fit the user's identity and tone. Ask the user to pick one. Then proceed.
- If they describe it in words → restate the description back as a layout outline (hero, sections, footer) and confirm before building.

The reference is the target. Every iteration is judged against it.

---

## Step 3: Local dev server

Spin up a local server so the page can be viewed in browser during the build. Pick the simplest option for the project:

- Static HTML/CSS → `python3 -m http.server 8000` from the project root.
- Has a `package.json` → `npx serve` or the project's existing dev command.
- Already on Next.js / Vite / Astro → use the existing dev server.

Tell the user the URL (e.g. `http://localhost:8000`). Keep the server running across the build. Iterate live.

---

## Step 4: Build the page

- Semantic HTML. Real tags (`header`, `main`, `section`, `article`, `footer`). No `div` soup.
- Brand colors only. Pull hex/HSL values from CLAUDE.md or `brand-system/`. No invented colors.
- Brand fonts only. Pull from CLAUDE.md typography section or `brand-system/`. No invented fonts.
- Real assets. Use the brand logo, real product images, real photography. No stock placeholders. No emoji unless the brand uses them.
- Mobile-first responsive. Build the small breakpoint first, then scale up.
- Real copy. Write it in the brand's voice. No lorem ipsum. No filler.
- One conversion goal per page. Strip every link or section that doesn't serve it.

---

## Step 5: Screenshot loop

After every meaningful change, screenshot the page in browser at desktop and mobile widths. Compare to the reference. Note what's off (spacing, weight, hierarchy, color, alignment). Fix. Screenshot again. Repeat.

The screenshot is the source of truth, not the code. A page that looks right is right. A page that reads clean in code but looks generic in the browser is wrong.

Loop until the screenshot matches the reference and the brand.

---

## Anti-generic guardrails (hard rules)

- No purple gradients unless the brand explicitly uses them.
- No glassmorphism dump unless the brand calls for it.
- No stock fluency in copy: "transformative," "elevate," "unleash," "leverage," "streamline," "delve," "in today's world."
- No invented fonts. Use only fonts declared in CLAUDE.md or `brand-system/`.
- No invented brand colors. Pull from CLAUDE.md or `brand-system/`.
- No emoji unless the brand explicitly uses them.
- No lorem ipsum. Real copy that matches the brand voice.
- No stock placeholder images. Use real assets or stop and ask.
- No three-column-card pattern unless the reference has it. The default AI layout is the tell.
- Mobile breakpoint is non-negotiable. If it breaks under 400px wide, it's not done.
- One CTA per surface. Subtraction is the work.

---

## When to stop

- The screenshot matches the reference at desktop and mobile.
- HTML is semantic and clean. No leftover scaffolding, no commented-out blocks.
- Copy passes the brand check (run `/brand-guidelines` against the final draft).
- Mobile responsive verified at 375px, 768px, and 1280px.
- No AI tells in copy or visual defaults.

If any of those fail, keep iterating. Don't ship a page that fails the brand check.
