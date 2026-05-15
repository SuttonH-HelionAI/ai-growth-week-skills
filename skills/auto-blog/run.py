#!/usr/bin/env python3
"""auto-blog weekly run.

Reads last 10 blog posts + voice file, builds prompt, calls `claude -p`,
writes draft to vault output folder.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path.home() / ".helion-automations" / "config.json"
LOG_PATH = Path.home() / ".auto-blog.log"

# Ensure subprocess can find `claude` when launched from cron (cron's PATH is minimal).
for _p in ("/opt/homebrew/bin", "/usr/local/bin", str(Path.home() / ".local/bin")):
    if _p not in os.environ.get("PATH", ""):
        os.environ["PATH"] = _p + ":" + os.environ.get("PATH", "")


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
    if "vault_path" not in cfg or "auto_blog" not in cfg:
        print("config incomplete. run: python3 wizard.py", file=sys.stderr)
        sys.exit(1)
    return cfg


def read_recent_posts(folder, limit=10):
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


def slugify(text, fallback="draft"):
    if not text:
        return fallback
    s = re.sub(r"[^\w\s-]", "", text).strip().lower()
    s = re.sub(r"[-\s]+", "-", s)
    return s[:60] or fallback


def build_prompt(posts, voice):
    posts_block = "\n\n--- POST BREAK ---\n\n".join(posts) if posts else "(no prior posts available)"
    voice_block = voice if voice else "(no voice file provided, infer from posts above)"
    return f"""You are drafting a new blog post for an ecommerce brand.

Here are my last 10 blog posts so you can see what I have covered and how I write:
<<<
{posts_block}
>>>

Here is my brand voice reference:
<<<
{voice_block}
>>>

Now do this:
1. Pick a fresh angle I have NOT covered in the last 10 posts.
2. Use your existing knowledge to research it briefly.
3. Write a complete blog post, 600 to 800 words, in this brand voice.

Output ONLY the markdown. Start with `# Title` on the first line. Then the body.
No preamble, no explanation, no closing remarks. Just the post.

Voice rules:
- No em dashes or en dashes. Use commas or periods.
- No AI buzzwords (delve, leverage, unleash, transformative, etc).
- Short punchy sentences. Direct.
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


def extract_title(markdown):
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def main():
    cfg = load_config()
    vault = Path(cfg["vault_path"])
    blog = cfg["auto_blog"]
    source = vault / blog["source_folder"]
    output = vault / blog["output_folder"]
    voice = vault / blog["voice_file"]

    log(f"start. source={source} output={output}")

    posts = read_recent_posts(source)
    log(f"read {len(posts)} past posts")

    voice_text = read_voice(voice)
    if voice_text:
        log(f"voice file loaded ({len(voice_text)} chars)")
    else:
        log("voice file missing or empty, model will infer from posts")

    prompt = build_prompt(posts, voice_text)
    log(f"prompt assembled ({len(prompt)} chars). calling claude -p")

    # Allow dry run via env var for testing
    if os.environ.get("AUTO_BLOG_DRY_RUN") == "1":
        log("DRY RUN: skipping claude call. exiting.")
        return

    draft = call_claude(prompt)
    if not draft:
        log("claude returned empty output. nothing written.")
        sys.exit(1)

    title = extract_title(draft)
    slug = slugify(title)
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date}-{slug}.md"

    output.mkdir(parents=True, exist_ok=True)
    out_path = output / filename
    out_path.write_text(draft + "\n")
    log(f"wrote draft to {out_path}")


if __name__ == "__main__":
    main()
