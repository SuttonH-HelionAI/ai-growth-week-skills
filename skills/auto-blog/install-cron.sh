#!/usr/bin/env bash
# auto-blog cron installer. Idempotent. Reads schedule from config.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="$HOME/.helion-automations/config.json"
LOG="$HOME/.auto-blog.log"

if [[ ! -f "$CONFIG" ]]; then
  echo "config missing at $CONFIG. run: python3 wizard.py" >&2
  exit 1
fi

SCHEDULE="$(/usr/bin/env python3 -c "import json; print(json.load(open('$CONFIG'))['auto_blog']['cron_schedule'])")"

if [[ -z "$SCHEDULE" ]]; then
  echo "could not read cron_schedule from config" >&2
  exit 1
fi

CRON_LINE="$SCHEDULE cd $SKILL_DIR && /usr/bin/env python3 run.py >> $LOG 2>&1"

EXISTING="$(crontab -l 2>/dev/null || true)"

if echo "$EXISTING" | grep -Fq "cd $SKILL_DIR &&"; then
  echo "auto-blog cron already installed. nothing to do."
  exit 0
fi

{
  echo "$EXISTING"
  echo "$CRON_LINE"
} | sed '/^$/d' | crontab -

echo "installed: $CRON_LINE"
