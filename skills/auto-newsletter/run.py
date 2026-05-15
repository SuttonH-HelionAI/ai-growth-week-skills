#!/usr/bin/env python3
"""auto-newsletter run.

Reads last 10 newsletters + voice file, picks today's theme, builds prompt,
calls `claude -p`, writes draft to vault output folder.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path.home() / ".helion-automations" / "config.json"
LOG_PATH = Path.home() / ".auto-newsletter.log"

WEEKDAY_NAME = {0: "monday", 1: "tuesday", 2: "wednesday", 3: "thursday", 4: "friday", 5: "saturday", 6: "sunday"}


def log(msg):
    line = f"[{datetime.now().isoformat(timespec='seconds')}] {msg}"
    print(line)
    try:
        with open(LOG_PATH, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def load_config():
    if not CONFIG_PATH.exists():
        print("config missing. run: python3 wizard.py", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    if "vault_path" not in cfg or "auto_newsletter" not in cfg:
        print("config incomplete. run: python3 wizard.py", file=sys.stderr)
        sys.exit(1)
    return cfg


def read_recent_files(folder, limit=10):
    if not folder.exists():
        return []
    files = sorted(
        [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() == ".md"],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    out = []
    for f in files[:limit]:
        try:
            out.append(f.read_text())
        except Exception as e:
            log(f"could not read {f}: {e}")
    return out


def read_voice(path):
    if not path.exists():
        return ""
    try:
        return path.read_text()
    except Exception as e:
        log(f"could not read voice file {path}: {e}")
        return ""


def slugify(text, fallback="newsletter"):
    if not text:
        return fallback
    s = re.sub(r"[^\w\s-]", "", text).strip().lower()
    s = re.sub(r"[-\s]+", "-", s)
    return s[:60] or fallback


def todays_theme(themes):
    """themes is a dict keyed by lowercase full day name."""
    if not themes:
        return None
    today = WEEKDAY_NAME[datetime.now().weekday()]
    return themes.get(today)


def build_prompt(newsletters, voice, theme):
    nl_block = "\n\n--- NEWSLETTER BREAK ---\n\n".join(newsletters) if newsletters else "(no prior newsletters available)"
    voice_block = voice if voice else "(no voice file provided, infer from newsletters above)"
    theme_line = theme if theme else "no specific theme, pick what fits"
    return f"""You are drafting a newsletter for an ecommerce brand.

Here are my last 10 newsletters:
<<<
{nl_block}
>>>

Brand voice reference:
<<<
{voice_block}
>>>

Today's theme: {theme_line}

Now write a complete newsletter, 400 to 500 words, in this brand voice.

Output format (exactly this structure):
Subject: <one line>
Preview: <one line, max 90 chars>

<body>

End with ONE clear CTA. Direct, specific.

Voice rules:
- No em dashes or en dashes. Use commas or periods.
- No AI buzzwords (delve, leverage, unleash, transformative, etc).
- Short punchy sentences.
- Match the voice of the past newsletters.

Output ONLY the newsletter. No preamble, no closing remarks.
"""


def call_claude(prompt):
    try:
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=300,
        )
    except FileNotFoundError:
        log("claude CLI not found. install Claude Code and run `claude login`.")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        log("claude call timed out after 5 minutes.")
        sys.exit(1)

    if result.returncode != 0:
        log(f"claude returned non-zero. stderr: {result.stderr.strip()}")
        sys.exit(1)
    return result.stdout.strip()


def extract_subject(markdown):
    for line in markdown.splitlines():
        if line.lower().startswith("subject:"):
            return line.split(":", 1)[1].strip()
    return ""


def main():
    cfg = load_config()
    vault = Path(cfg["vault_path"])
    nl = cfg["auto_newsletter"]
    source = vault / nl["source_folder"]
    output = vault / nl["output_folder"]
    voice = vault / nl["voice_file"]
    themes = nl.get("themes", {})

    theme = todays_theme(themes)
    log(f"start. source={source} output={output} theme={theme}")

    newsletters = read_recent_files(source)
    log(f"read {len(newsletters)} past newsletters")

    voice_text = read_voice(voice)
    if voice_text:
        log(f"voice file loaded ({len(voice_text)} chars)")
    else:
        log("voice file missing or empty")

    prompt = build_prompt(newsletters, voice_text, theme)
    log(f"prompt assembled ({len(prompt)} chars). calling claude -p")

    if os.environ.get("AUTO_NEWSLETTER_DRY_RUN") == "1":
        log("DRY RUN: skipping claude call. exiting.")
        return

    draft = call_claude(prompt)
    if not draft:
        log("claude returned empty output. nothing written.")
        sys.exit(1)

    subject = extract_subject(draft)
    slug = slugify(subject)
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date}-{slug}.md"

    output.mkdir(parents=True, exist_ok=True)
    out_path = output / filename
    out_path.write_text(draft + "\n")
    log(f"wrote draft to {out_path}")


if __name__ == "__main__":
    main()
