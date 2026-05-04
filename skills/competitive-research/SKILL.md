---
name: competitive-research
description: Research agent that runs before virtually any build task. Auto-triggers before landing pages, funnels, campaigns, email sequences, product launches, ad copy, and strategy sessions. Manual trigger any time the user says "research X" or "what are competitors doing with X." Runs deep competitive, customer, market, and product research using Perplexity. Outputs a structured brief that feeds directly into the build.
---

# Competitive Research Skill

This runs FIRST. Before strategy. Before funnel maps. Before copy. Before any build.

---

## First-run guard

Before doing anything else, check if `CLAUDE.md` exists in the current working directory and contains `[BRAND COMPLETE]` on the last line.

- If both true → skip this guard, proceed with the skill.
- Otherwise → STOP and tell the user: "Brand brain isn't locked yet. Run `/claude-md-setup` first. Takes about 5 minutes. Come back and run me when you see `[BRAND COMPLETE]` at the bottom of your CLAUDE.md."
- Do not proceed until the marker is present.

---

## Required to run

- `PERPLEXITY_API_KEY` in your shell environment (get one at perplexity.ai/settings/api)
- `curl` available in your terminal (default on Mac/Linux)
- WebFetch tool available in Claude Code (default)

If `PERPLEXITY_API_KEY` is not set, this skill will tell you that on first run and stop. Add it to your shell profile (`~/.zshrc` or `~/.bashrc`) like this:

```
export PERPLEXITY_API_KEY="pplx-your-key-here"
```

Reload your shell (`source ~/.zshrc`) and run the skill again.

**The skill must check `$PERPLEXITY_API_KEY` before its first curl call. If the variable is empty, fail clean with the install instructions above. Do not fail silently.**

---

## Step 1: DETECT AND CALIBRATE

**Auto-trigger on:**
- Landing page build
- Funnel map or campaign build
- Email sequence or flow
- Product launch or LTO
- Ad creative or copy
- Strategy session

**Manual trigger:** Any time the user says "research X," "look into X," or "what are competitors doing with X."

**Depth modes:**
- DEEP: Any build task (landing page, funnel, campaign, email, product, ads)
- BRIEF: Strategy context, quick questions, one-off decisions

State the depth mode before running. Do not start research without confirming what the task is and what depth is needed.

---

## The Moneyball Principle

Every research run has two modes of analysis running simultaneously:

**Inside the box:** Conventional questions. Surface-level data. What is everyone already measuring? This is necessary but not sufficient.

**Outside the box:** The Billy Bean angle. What is the metric nobody is tracking that tells a better story? What correlation exists that is not obvious? What does the audience say in unguarded moments (Reddit threads, comment sections, DMs) that no brand is responding to? What assumption is the entire industry making that might be wrong?

The Moneyball finding is the most valuable output of any research run. It is the insight that separates a good brief from a competitive advantage. Every deep research output must include at least one.

---

## Step 2: RUN THE RESEARCH

### Deep Mode

Spawn parallel sub-agents using the Agent tool. One per track. All four run simultaneously for speed.

**Track 1: Competitor Analysis**
Research prompt to Perplexity:
- Who are the top 3-5 direct competitors for [product/topic]?
- What are their offers, prices, and positioning?
- What does their [landing page / email / ad / funnel] look like?
- What claims do they make? What proof do they show?
- Where are they weak? What do they fail to address?

Outside the box -- also ask:
- What stat or metric are competitors not using that would change their positioning if they did?
- What are customers saying in reviews and forums that competitors are completely ignoring?
- What angle is available that the obvious competitors have never touched?

For competitor landing pages, use WebFetch to pull the actual page and analyze it.

**Track 2: Customer Research**
Research prompt to Perplexity:
- What language does the [audience segment] use to describe their problem?
- What are the top pain points and frustrations? (Search Reddit, Amazon reviews, forums)
- What have they tried that failed?
- What objections do they have when considering [product type]?
- What is the dream outcome they want?

Outside the box -- also ask:
- What do they say when they are NOT trying to impress anyone? (Reddit, private groups, review sections marked "verified purchase")
- What belief do they hold that no [your category] brand is addressing directly?
- What emotional driver is underneath the surface goal they state on the surface?

**Track 3: Market and Trend Research**
Research prompt to Perplexity:
- What is trending right now in [market/niche]?
- What narratives are competitors winning with?
- What cultural moments or timing windows apply?
- What narrative is unowned that aligns with [your brand's positioning from CLAUDE.md `## Identity`]?

Outside the box -- also ask:
- What trend in an adjacent market is about to cross over into your category?
- What is the cultural undercurrent that the mainstream [your category] is ignoring because it is inconvenient or too polarizing?

**Track 4: Product Research** (run only when product-specific)
Research prompt to Perplexity:
- What does the science or evidence say about [ingredient/claim/feature]?
- What real proof exists? What is overstated?
- What makes [product] defensible vs. competitors?
- What proof can [your brand] use legitimately?

Outside the box -- also ask:
- What mechanism or benefit does the evidence support that nobody in your category is talking about?
- What study or data point exists that competitors are not citing because it is too specific or too technical for mainstream marketing, but is actually highly credible?

**Perplexity API call (use Bash):**
```bash
curl -s -X POST 'https://api.perplexity.ai/chat/completions' \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"model":"sonar-pro","messages":[{"role":"user","content":"[research prompt here]"}]}'
```

Use `sonar-pro` for all deep research. It has live web access.

### Brief Mode

Single Perplexity call. One targeted query. Done in under 5 minutes.

---

## Step 3: SYNTHESIZE AND OUTPUT

### Deep Research Output
Save to `research/[topic]-YYYY-MM-DD.md`.

```markdown
# Research: [Topic]
Date: YYYY-MM-DD
Build task: [landing page / funnel / email / campaign / product]

## What Competitors Are Doing
[3-5 specific findings. Name the competitor. Name the tactic. Name the price or claim. Not vague.]

## What [Brand] Can Do Better
[Direct comparison. Specific gaps. Specific alternatives. Not "be more authentic" -- name the exact thing. Pull the brand name from CLAUDE.md `## Identity`.]

## Where Customers Drop Off
[Friction points in competitor funnels and pages. What kills trust. What kills conversions. What's missing.]

## Gaps to Capitalize On
[Unowned positioning. Unmet objections. Claims nobody is making that are true for your brand. Timing windows.]

## The Moneyball Finding
[The one unconventional insight that everyone else missed. The outside-the-box stat, signal, or angle that changes the picture. This is the highest-value output. If there is no non-obvious finding here, the research is not done.]

## Recommended Action
[One clear recommendation. What to do differently in the build based on this research. Often driven by the Moneyball Finding.]
```

### Brief Research Output
Delivered inline. Not saved unless the user asks.

```
Research Note: [Topic]
Key finding: [One sentence]
Implication for [Brand]: [One sentence]
Action: [One sentence]
```

---

## Step 4: HAND OFF

After research is complete, state clearly:

- If a build is next: "Research complete. Handing off to [skill]." Pass findings as context into that skill.
- If strategy is next: Pass findings directly into the strategy skill's diagnostic phase as pre-loaded context.
- If standalone: Deliver output and stop.

The build skill should not start until research is in hand.

---

## Rules
- Depth mode must be stated before starting.
- Deep research uses parallel agents. Do not run the four tracks sequentially -- run them simultaneously.
- Every finding must be specific. Named competitors, named tactics, named prices. No vague generalities.
- The Recommended Action section is the most important part. Everything else feeds it.
- Research docs go in `research/[topic]-YYYY-MM-DD.md`. Never loose in chat.
- This skill runs before strategy, before any funnel map, and before any build. It is the foundation.
