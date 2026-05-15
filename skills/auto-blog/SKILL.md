---
name: auto-blog
description: White-labeled blog post automation. First-run wizard sets up a cron that drafts new blog posts every Monday from your past posts plus research. Output lands in your Obsidian vault as a draft. Built for ecom founders.
---

# auto-blog

Drafts a fresh blog post every Monday morning. Reads your last 10 posts, learns your voice from a reference file, picks an angle you have not covered, and writes a 600 to 800 word draft into your vault.

## What it does

1. First run: `wizard.py` asks 4 questions, writes config to `~/.helion-automations/config.json`.
2. Each Monday at 8am (or whatever schedule you set): cron runs `run.py`.
3. `run.py` reads your last 10 posts plus your voice file, calls `claude -p` non-interactively, writes the draft to `{vault}/{output_folder}/YYYY-MM-DD-slug.md`.
4. You review and publish.

## Setup

```
python3 wizard.py
bash install-cron.sh
```

## Wizard asks

1. Source folder for past blog posts (default: `Blog Posts`)
2. Output folder for new drafts (default: `Blog Drafts`)
3. Voice reference file inside vault (default: `Reference/brand-voice.md`)
4. Day and time to run (default: Monday 8am)

## Requires

- `claude` CLI installed and authenticated. `run.py` shells out to `claude -p`.
- Python 3 (mac default works).
- An Obsidian vault with at least one past post in the source folder. Empty source folder still works, it just gives the model less to learn from.

## Files

- `SKILL.md` this file
- `REFERENCE.md` voice rules, prompt template, troubleshooting
- `wizard.py` first-run setup
- `run.py` what the cron triggers
- `install-cron.sh` idempotent cron installer

## Voice rules

No em dashes. No AI buzzwords. Direct.
