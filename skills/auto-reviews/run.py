#!/usr/bin/env python3
"""auto-reviews daily run.

Cron entrypoint. Loads shared config, calls scrape_reviews (live-build TODO),
writes one markdown file per review to the user's Obsidian vault.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path.home() / ".helion-automations" / "config.json"
LOG_PATH = Path.home() / ".auto-reviews.log"


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
    if "vault_path" not in cfg or "auto_reviews" not in cfg:
        print("config incomplete. run: python3 wizard.py", file=sys.stderr)
        sys.exit(1)
    return cfg


def slugify(text, fallback="review"):
    if not text:
        return fallback
    s = re.sub(r"[^\w\s-]", "", text).strip().lower()
    s = re.sub(r"[-\s]+", "-", s)
    return s or fallback


# ============================================================
# TODO LIVE BUILD: Sutton fills this in on stage.
# ============================================================
# Contract: yield one dict per review with keys:
#   id, rating, title, body, reviewer_name, product_title, created_at
#
# Judge.me public endpoint:
#   GET https://judge.me/api/v1/reviews?shop_domain={store_url}&per_page=100
#
# Use urllib.request (stdlib only, no pip installs). Parse JSON.
# Map response fields straight through.
# ============================================================
def scrape_reviews(cfg):
    # TODO LIVE BUILD
    # Example skeleton (uncomment and finish on stage):
    #
    # import urllib.request
    # store = cfg["auto_reviews"]["store_url"]
    # url = f"https://judge.me/api/v1/reviews?shop_domain={store}&per_page=100"
    # with urllib.request.urlopen(url, timeout=20) as resp:
    #     data = json.loads(resp.read().decode("utf-8"))
    # for r in data.get("reviews", []):
    #     yield {
    #         "id": r["id"],
    #         "rating": r["rating"],
    #         "title": r.get("title", ""),
    #         "body": r.get("body", ""),
    #         "reviewer_name": r.get("reviewer", {}).get("name", "Anonymous"),
    #         "product_title": r.get("product_title", ""),
    #         "created_at": r.get("created_at", ""),
    #     }
    raise NotImplementedError("Build live in session")


def write_review_markdown(review, vault_path):
    """Write one review to {vault}/Reviews/{id}-{slug}.md. Skip if file exists."""
    reviews_dir = Path(vault_path) / "Reviews"
    reviews_dir.mkdir(parents=True, exist_ok=True)

    review_id = review.get("id", "unknown")
    title = review.get("title", "")
    slug = slugify(title)
    filename = f"{review_id}-{slug}.md"
    path = reviews_dir / filename

    if path.exists():
        return False

    rating = review.get("rating", "")
    product = review.get("product_title", "")
    customer = review.get("reviewer_name", "")
    date = review.get("created_at", "")
    body = review.get("body", "")
    title_display = title or "Review"

    content = (
        "---\n"
        f"id: {review_id}\n"
        f"rating: {rating}\n"
        f"product: {product}\n"
        f"customer: {customer}\n"
        f"date: {date}\n"
        "source: judgeme\n"
        "---\n"
        "\n"
        f"# {title_display}\n"
        "\n"
        f"{body}\n"
    )
    path.write_text(content)
    return True


def main():
    cfg = load_config()
    vault = cfg["vault_path"]
    log(f"start. vault={vault}")

    try:
        reviews = list(scrape_reviews(cfg))
    except NotImplementedError:
        log("scrape_reviews not implemented yet. build it live on stage.")
        sys.exit(0)
    except Exception as e:
        log(f"scrape failed: {e}")
        sys.exit(1)

    written = 0
    for r in reviews:
        try:
            if write_review_markdown(r, vault):
                written += 1
        except Exception as e:
            log(f"write failed for review {r.get('id')}: {e}")

    log(f"done. {written} new reviews written, {len(reviews) - written} skipped (already present).")


if __name__ == "__main__":
    main()
