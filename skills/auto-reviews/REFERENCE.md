# auto-reviews REFERENCE

## Why this exists

Reviews are the highest-converting asset most ecom founders own and the most underused. They sit locked inside Judge.me, Yotpo, Loox, etc. This skill drags them into your knowledge vault where you can search, quote, and reuse them.

## Config schema

Lives at `~/.helion-automations/config.json`, shared by all three skills.

```json
{
  "vault_path": "/Users/founder/Documents/MyVault",
  "auto_reviews": {
    "review_app": "judgeme",
    "store_url": "store.myshopify.com",
    "api_key": null
  }
}
```

If `vault_path` already exists in config, the wizard skips that question.

## The live-build target

`run.py` has one function flagged `# TODO LIVE BUILD`. That function is `scrape_reviews(cfg)`.

Contract:
- Takes the loaded config dict.
- Yields one dict per review with these keys: `id`, `rating`, `title`, `body`, `reviewer_name`, `product_title`, `created_at`.
- Raises clearly if the API call fails.

### Judge.me hint

Public endpoint shape:

```
GET https://judge.me/api/v1/reviews?shop_domain={store_url}&per_page=100
```

Returns JSON with a `reviews` array. Each item has `id`, `rating`, `title`, `body`, `reviewer_name`, `product_title`, `created_at`. Map them straight through.

For private review access you would need an API token. For demo, public endpoint is enough.

## Output format

Each review becomes a file at `{vault}/Reviews/{review_id}.md`:

```markdown
---
id: 12345
rating: 5
product: Resilience Whey Protein
customer: John D.
date: 2026-05-12
source: judgeme
---

# Best whey I have used

I switched from another brand and the difference is real...
```

## De-duplication

`write_review_markdown` skips writes when the target file already exists. So the cron can run daily and only new reviews land.

## Voice rules

- No em dashes or en dashes.
- No AI buzzwords (delve, leverage, unleash, transformative, etc).
- Direct, short.
- No emojis in user-facing console output unless the user added them first.

## Future expansion

- Tag low-rating reviews differently so you can find product issues fast.
- Pipe high-rating reviews into a swipe file for ad copy.
- Hook into auto-newsletter so Friday's story email can pull a real customer quote.
