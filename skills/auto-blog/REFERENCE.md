# auto-blog REFERENCE

## How the prompt is built

`run.py` assembles a single prompt and pipes it to `claude -p`:

```
You are drafting a new blog post for an ecommerce brand.

Here are my last 10 blog posts so you can see what I have covered and how I write:
<<<
{concatenated posts>>>
<<<

Here is my brand voice reference:
<<<
{voice file content}
<<<

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
```

## Cron schedule

Default: `0 8 * * 1` (Monday 8am local).

Wizard accepts natural input ("Monday 8am", "Tuesday 6:30am", etc) and converts to cron format. Falls back to the default if it cannot parse.

## File output

Drafts land at `{vault}/{output_folder}/YYYY-MM-DD-slug.md`. Slug is derived from the first `# Heading` line in the draft. If parsing fails the file is named `YYYY-MM-DD-draft.md`.

## Troubleshooting

- "claude: command not found" — install the Claude Code CLI and run `claude login`.
- "source folder empty" — the script still runs but the prompt has no examples, so the draft will be generic. Drop one or two past posts in.
- "permission denied" — `chmod +x wizard.py run.py install-cron.sh`.
- "log file growing" — rotate or truncate `~/.auto-blog.log` whenever you want. No automation depends on it.

## Voice rules

- No em dashes or en dashes.
- No AI buzzwords.
- Direct, short.

## Why claude -p

Non-interactive mode. Returns one shot of output to stdout. Perfect for cron. No API keys, no SDK install. Uses the user's existing Claude Code auth.
