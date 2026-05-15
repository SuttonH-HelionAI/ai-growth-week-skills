# auto-newsletter REFERENCE

## How the prompt is built

`run.py` checks today's day-of-week, looks up the theme from config (if any), then assembles:

```
You are drafting a newsletter for an ecommerce brand.

Here are my last 10 newsletters:
<<<
{concatenated newsletters}
>>>

Brand voice reference:
<<<
{voice file content}
>>>

Today's theme: {theme or "no specific theme, pick what fits"}

Now write a complete newsletter, 400 to 500 words, in this brand voice.

Output format:
Subject: <one line>
Preview: <one line, max 90 chars>

<body>

End with ONE clear CTA. Direct, specific.

Voice rules:
- No em dashes or en dashes. Use commas or periods.
- No AI buzzwords (delve, leverage, unleash, transformative, etc).
- Short punchy sentences.
- Match the voice of the past newsletters.
```

## Day mapping

| Wizard input | Cron day-of-week |
|--------------|------------------|
| Sun, Sunday  | 0 |
| Mon, Monday  | 1 |
| Tue, Tuesday | 2 |
| Wed, Wednesday | 3 |
| Thu, Thursday | 4 |
| Fri, Friday  | 5 |
| Sat, Saturday | 6 |

## Multi-day cron

If user picks all days at the same time (default 8am), one cron line covers it:
`0 8 * * 1,3,5 ...`

`install-cron.sh` builds the line that way. Time is the same across all days.

## Theme lookup

In config:
```json
"themes": {"monday": "motivation", "wednesday": "value", "friday": "story"}
```

`run.py` matches today's day name (lowercase) against keys. If no match, the prompt says "no specific theme."

## File output

`{vault}/{output_folder}/YYYY-MM-DD-slug.md`. Slug derived from `Subject:` line. Falls back to `YYYY-MM-DD-newsletter.md`.

## Voice rules

- No em dashes or en dashes.
- No AI buzzwords.
- Direct, short.
