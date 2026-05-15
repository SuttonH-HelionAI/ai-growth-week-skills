---
name: auto-newsletter
description: White-labeled newsletter automation. First-run wizard sets up a cron that drafts newsletters on the days you pick. Reads your past newsletters and brand voice, writes a fresh draft into your Obsidian vault. Built for ecom founders.
---

# auto-newsletter

Drafts a fresh newsletter on Monday, Wednesday, and Friday (or whatever days you choose). Reads your last 10 newsletters and your brand voice file, picks an angle, writes 400 to 500 words with a subject line, preview text, and one clear CTA.

## What it does

1. First run: `wizard.py` asks 5 questions, writes config to `~/.helion-automations/config.json`.
2. On each scheduled day at 8am (or your chosen time): cron runs `run.py`.
3. `run.py` reads your last 10 newsletters, picks today's theme if set, calls `claude -p`, writes the draft to `{vault}/{output_folder}/YYYY-MM-DD-slug.md`.

## Setup

```
python3 wizard.py
bash install-cron.sh
```

## Wizard asks

1. Source folder for past newsletters (default: `Newsletters`)
2. Output folder for new drafts (default: `Newsletter Drafts`)
3. Voice reference file inside vault (default: `Reference/brand-voice.md`)
4. Which days to run (default: `Mon,Wed,Fri`)
5. Optional theme per day (e.g., `Mon=motivation, Wed=value, Fri=story`)

## Requires

- `claude` CLI installed and authenticated. Uses `claude -p` non-interactively.
- Python 3.
- Obsidian vault with at least one past newsletter in the source folder works best, empty still functions.

## Files

- `SKILL.md` this file
- `REFERENCE.md` voice rules, prompt template, day mapping
- `wizard.py` first-run setup
- `run.py` what cron triggers, picks today's theme
- `install-cron.sh` idempotent multi-day cron installer

## Voice rules

No em dashes. No AI buzzwords. Direct.
