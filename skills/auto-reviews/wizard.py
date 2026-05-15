#!/usr/bin/env python3
"""auto-reviews first-run wizard.

Asks 3 questions, writes config to ~/.helion-automations/config.json.
If vault_path already exists in config, skips that question.
"""

import json
import os
import sys
from pathlib import Path

CONFIG_DIR = Path.home() / ".helion-automations"
CONFIG_PATH = CONFIG_DIR / "config.json"

VALID_APPS = ["judgeme", "yotpo", "loox", "other"]


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


def ask(prompt, default=None, choices=None):
    suffix = ""
    if choices:
        suffix = f" [{'/'.join(choices)}]"
    if default is not None:
        suffix += f" (default: {default})"
    while True:
        raw = input(f"{prompt}{suffix}: ").strip()
        if not raw and default is not None:
            return default
        if not raw:
            print("required.")
            continue
        if choices and raw not in choices:
            print(f"pick one of: {', '.join(choices)}")
            continue
        return raw


def main():
    print("auto-reviews setup")
    print("------------------")
    cfg = load_config()

    if "vault_path" not in cfg:
        vault = ask("Obsidian vault path", default=str(Path.home() / "Documents" / "Vault"))
        cfg["vault_path"] = os.path.expanduser(vault)
    else:
        print(f"using existing vault_path: {cfg['vault_path']}")

    app = ask("Which review app", choices=VALID_APPS, default="judgeme")
    store = ask("Store domain (e.g., mystore.myshopify.com)")

    cfg["auto_reviews"] = {
        "review_app": app,
        "store_url": store,
        "api_key": cfg.get("auto_reviews", {}).get("api_key"),
    }

    save_config(cfg)
    print()
    print(f"saved to {CONFIG_PATH}")
    print("next: bash install-cron.sh")


if __name__ == "__main__":
    main()
