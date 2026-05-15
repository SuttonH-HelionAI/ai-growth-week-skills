#!/usr/bin/env python3
"""auto-blog first-run wizard.

Asks 4 questions, writes config to ~/.helion-automations/config.json.
Parses natural day/time input into a cron expression.
"""

import json
import os
import re
import sys
from pathlib import Path

CONFIG_DIR = Path.home() / ".helion-automations"
CONFIG_PATH = CONFIG_DIR / "config.json"

DAY_MAP = {
    "sun": 0, "sunday": 0,
    "mon": 1, "monday": 1,
    "tue": 2, "tues": 2, "tuesday": 2,
    "wed": 3, "weds": 3, "wednesday": 3,
    "thu": 4, "thur": 4, "thurs": 4, "thursday": 4,
    "fri": 5, "friday": 5,
    "sat": 6, "saturday": 6,
}


def load_config():
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH) as f:
                return json.load(f)
        except Exception as e:
            print(f"warning: could not parse existing config ({e}). starting fresh.", file=sys.stderr)
    return {}


def save_config(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)


def ask(prompt, default=None):
    suffix = f" (default: {default})" if default is not None else ""
    while True:
        raw = input(f"{prompt}{suffix}: ").strip()
        if not raw and default is not None:
            return default
        if not raw:
            print("required.")
            continue
        return raw


def parse_schedule(raw, default="0 8 * * 1"):
    """Parse 'Monday 8am' or 'Tue 6:30am' style input into cron format."""
    if not raw:
        return default
    s = raw.lower().strip()

    # Day
    day_num = None
    for key, val in DAY_MAP.items():
        if re.search(rf"\b{key}\b", s):
            day_num = val
            break
    if day_num is None:
        day_num = 1  # Monday default

    # Time
    hour = 8
    minute = 0
    m = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", s)
    if m:
        hour = int(m.group(1))
        minute = int(m.group(2) or 0)
        meridiem = m.group(3)
        if meridiem == "pm" and hour < 12:
            hour += 12
        if meridiem == "am" and hour == 12:
            hour = 0

    return f"{minute} {hour} * * {day_num}"


def main():
    print("auto-blog setup")
    print("---------------")
    cfg = load_config()

    if "vault_path" not in cfg:
        vault = ask("Obsidian vault path", default=str(Path.home() / "Documents" / "Vault"))
        cfg["vault_path"] = os.path.expanduser(vault)
    else:
        print(f"using existing vault_path: {cfg['vault_path']}")

    source = ask("Source folder for past blog posts (inside vault)", default="Blog Posts")
    output = ask("Output folder for new drafts (inside vault)", default="Blog Drafts")
    voice = ask("Voice reference file inside vault", default="Reference/brand-voice.md")
    schedule_raw = ask("Day and time to run (e.g., Monday 8am)", default="Monday 8am")
    cron_schedule = parse_schedule(schedule_raw)

    cfg["auto_blog"] = {
        "source_folder": source,
        "output_folder": output,
        "voice_file": voice,
        "cron_schedule": cron_schedule,
    }

    save_config(cfg)
    print()
    print(f"saved to {CONFIG_PATH}")
    print(f"cron schedule: {cron_schedule}")
    print("next: bash install-cron.sh")


if __name__ == "__main__":
    main()
