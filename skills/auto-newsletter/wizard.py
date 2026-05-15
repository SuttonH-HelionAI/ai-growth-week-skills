#!/usr/bin/env python3
"""auto-newsletter first-run wizard.

Asks 5 questions, writes config to ~/.helion-automations/config.json.
Parses day list and optional per-day themes.
"""

import json
import os
import re
import sys
from pathlib import Path

CONFIG_DIR = Path.home() / ".helion-automations"
CONFIG_PATH = CONFIG_DIR / "config.json"

DAY_TO_NUM = {
    "sun": 0, "sunday": 0,
    "mon": 1, "monday": 1,
    "tue": 2, "tues": 2, "tuesday": 2,
    "wed": 3, "weds": 3, "wednesday": 3,
    "thu": 4, "thur": 4, "thurs": 4, "thursday": 4,
    "fri": 5, "friday": 5,
    "sat": 6, "saturday": 6,
}

NUM_TO_FULL = {0: "sunday", 1: "monday", 2: "tuesday", 3: "wednesday", 4: "thursday", 5: "friday", 6: "saturday"}


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
        if raw or default == "":
            return raw
        print("required.")


def parse_days(raw, default_nums=(1, 3, 5)):
    """Parse 'Mon,Wed,Fri' into sorted list of cron day numbers."""
    if not raw:
        return sorted(default_nums)
    parts = re.split(r"[,\s]+", raw.lower().strip())
    nums = set()
    for p in parts:
        if not p:
            continue
        if p in DAY_TO_NUM:
            nums.add(DAY_TO_NUM[p])
    if not nums:
        return sorted(default_nums)
    return sorted(nums)


def parse_themes(raw):
    """Parse 'Mon=motivation, Wed=value, Fri=story' into dict keyed by lowercase full day name."""
    out = {}
    if not raw:
        return out
    parts = re.split(r"[,;]", raw)
    for p in parts:
        if "=" not in p:
            continue
        day_part, theme = p.split("=", 1)
        day_key = day_part.strip().lower()
        if day_key in DAY_TO_NUM:
            full_day = NUM_TO_FULL[DAY_TO_NUM[day_key]]
            out[full_day] = theme.strip()
    return out


def parse_time(raw, default="0 8"):
    """Parse '8am' or '6:30am' into 'minute hour' cron format."""
    if not raw:
        return default
    s = raw.lower().strip()
    m = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", s)
    if not m:
        return default
    hour = int(m.group(1))
    minute = int(m.group(2) or 0)
    meridiem = m.group(3)
    if meridiem == "pm" and hour < 12:
        hour += 12
    if meridiem == "am" and hour == 12:
        hour = 0
    return f"{minute} {hour}"


def main():
    print("auto-newsletter setup")
    print("---------------------")
    cfg = load_config()

    if "vault_path" not in cfg:
        vault = ask("Obsidian vault path", default=str(Path.home() / "Documents" / "Vault"))
        cfg["vault_path"] = os.path.expanduser(vault)
    else:
        print(f"using existing vault_path: {cfg['vault_path']}")

    source = ask("Source folder for past newsletters", default="Newsletters")
    output = ask("Output folder for new drafts", default="Newsletter Drafts")
    voice = ask("Voice reference file inside vault", default="Reference/brand-voice.md")
    days_raw = ask("Which days to run (comma list, e.g., Mon,Wed,Fri)", default="Mon,Wed,Fri")
    time_raw = ask("What time", default="8am")
    themes_raw = ask("Optional theme per day (e.g., Mon=motivation, Wed=value, Fri=story). Press enter to skip", default="")

    day_nums = parse_days(days_raw)
    minute_hour = parse_time(time_raw)
    days_csv = ",".join(str(n) for n in day_nums)
    cron_schedule = f"{minute_hour} * * {days_csv}"

    themes = parse_themes(themes_raw)

    cfg["auto_newsletter"] = {
        "source_folder": source,
        "output_folder": output,
        "voice_file": voice,
        "cron_schedule": cron_schedule,
        "themes": themes,
    }

    save_config(cfg)
    print()
    print(f"saved to {CONFIG_PATH}")
    print(f"cron schedule: {cron_schedule}")
    if themes:
        print(f"themes: {themes}")
    print("next: bash install-cron.sh")


if __name__ == "__main__":
    main()
