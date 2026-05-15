---
name: auto-reviews
description: White-labeled review automation. First-run wizard sets up a daily cron that pulls new customer reviews from your store and drops them into your Obsidian vault as searchable markdown. Built for ecom founders.
---

# auto-reviews

Pulls customer reviews from your review app every morning, writes each one as a markdown file to `{vault}/Reviews/`, ready for search, swipe files, ad copy, and social proof.

## What it does

1. First run: `wizard.py` asks 3 questions, writes config to `~/.helion-automations/config.json`.
2. Daily at 7am: cron runs `run.py`, hits your review app API, writes new reviews to your vault.
3. Each review gets YAML frontmatter (rating, product, customer, date, source) so Obsidian and grep both work.

## Setup

```
python3 wizard.py
bash install-cron.sh
```

That is it. The wizard handles everything else.

## STATUS: scaffold

The plumbing is built. The scrape function is intentionally left as a TODO so you can build it live on stage.

Look for `# TODO LIVE BUILD` in `run.py`. That is the one function you fill in. Hit Judge.me's public endpoint, parse JSON, yield review dicts. Everything downstream of that, the file writer, the cron, the logging, is already done.

## Files

- `SKILL.md` this file
- `REFERENCE.md` voice rules, API notes, prompt patterns
- `wizard.py` first-run setup
- `run.py` what the cron triggers (contains the live-build TODO)
- `install-cron.sh` idempotent cron installer

## Voice rules

No em dashes. No AI buzzwords. Direct.
