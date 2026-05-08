# AI Growth Week Skills

Battle-tested Claude Code skills you can drop into any project. Built live during AI Growth Week.

The kit is white-labeled, every skill reads your brand from your `CLAUDE.md`, so the same skill works for any business once you've locked in your brand brain.

---

## Install in 60 seconds

```
git clone https://github.com/SuttonH-HelionAI/ai-growth-week-skills.git
cp -r ai-growth-week-skills/skills/* ~/your-project/.claude/skills/
cd ~/your-project && claude
```

Or download the ZIP: [github.com/SuttonH-HelionAI/ai-growth-week-skills](https://github.com/SuttonH-HelionAI/ai-growth-week-skills) → green "Code" button → "Download ZIP." Unzip, then copy the contents of the `skills/` folder into your project's `.claude/skills/` folder.

---

## First step: run `/claude-md-setup`

It walks you through a 5-section interview and writes your `CLAUDE.md`. After that, every other skill just works.

```
/claude-md-setup
```

The skill will:
1. Check for a `brand-system/` folder (from claude.ai/design). If missing, walk you through it.
2. Run a 5-section interview (Identity, Lineup, Audience, Tone, Decision Filter).
3. Write your `CLAUDE.md` and append `[BRAND COMPLETE]` as the last line.
4. Tell you to test `/brand-guidelines` on a fake PDP.

Once `[BRAND COMPLETE]` is on the last line of your `CLAUDE.md`, every other skill in this kit unlocks.

---

## Day-by-day schedule

**Day 1 (today):**
- `/claude-md-setup`, locks your brand brain
- `/brand-guidelines`, stops your team from publishing anything off-brand
- `/brand-voice`, strips AI tells out of every line of copy
- `/competitive-research`, Perplexity-driven competitor teardown
- `/strategy`, diagnose, apply mental models, get one recommendation

**Day 2:** `/pdp-generator`, `/email-sequence`, `/landing-page` (added morning of Day 2)

**Day 3-4:** added each morning. To pull the new skills, just `git pull` or re-download the ZIP.

**Day 5:**
- `/start-wiki`, builds a wiki memory inside your kit. Two questions, then it does the rest. Your AI stops forgetting.
- `/wiki-lint`, weekly health check for the wiki. Run it every Friday for 10 minutes.

After `/start-wiki` runs, you do not need to type slash commands for daily wiki use. Just talk to Claude. *"Remember this." "What do customers complain about?" "Save that answer."* The skill wires the wiki into your `CLAUDE.md` so future sessions handle ingest, query, and save conversationally.

---

## Need help?

Book at [helionhq.com/book](https://helionhq.com/book).
