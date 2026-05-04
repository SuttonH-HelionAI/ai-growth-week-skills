# Install Guide

Step-by-step for non-devs. Five steps. About 10 minutes.

---

## 1. Install Claude Code

Follow Anthropic's official install: [docs.anthropic.com/claude-code](https://docs.anthropic.com/en/docs/claude-code/overview)

You'll need a Claude Pro or Max subscription. Once installed, you should be able to type `claude` in your terminal and it opens.

---

## 2. Make a project folder

Open your terminal and run:

```
mkdir my-brand
cd my-brand
```

This is where your brand's AI workspace lives. Everything else happens inside this folder.

---

## 3. Drop the skills in

**Option A, clone with git:**

```
git clone https://github.com/SuttonH-HelionAI/ai-growth-week-skills.git
mkdir -p .claude/skills
cp -r ai-growth-week-skills/skills/* .claude/skills/
rm -rf ai-growth-week-skills
```

**Option B, download the ZIP:**

1. Go to [github.com/SuttonH-HelionAI/ai-growth-week-skills](https://github.com/SuttonH-HelionAI/ai-growth-week-skills)
2. Click the green "Code" button → "Download ZIP"
3. Unzip the file
4. Copy everything inside the `skills/` folder into your project's `.claude/skills/` folder. (If `.claude/skills/` doesn't exist yet, create it.)

When you're done, your folder should look like this:

```
my-brand/
└── .claude/
    └── skills/
        ├── claude-md-setup/
        ├── brand-guidelines/
        ├── brand-voice/
        ├── competitive-research/
        └── strategy/
```

---

## 4. Open Claude Code

From inside your project folder:

```
claude
```

---

## 5. Run `/claude-md-setup`

This is the first skill you should run. It writes your `CLAUDE.md` (your brand brain) and unlocks every other skill in the kit.

```
/claude-md-setup
```

Answer the 5-section interview. About 5 minutes. When you see `[BRAND COMPLETE]` on the last line of your `CLAUDE.md`, you're locked in.

---

## 6. Run any other skill

After `/claude-md-setup` is done, you can run any skill in the kit:

```
/brand-guidelines
/brand-voice
/competitive-research
/strategy
```

Some skills need extra setup (for example, `/competitive-research` needs a Perplexity API key). Each skill tells you exactly what it needs on first run.

---

## Stuck?

Book at [helionhq.com/book](https://helionhq.com/book).
