#!/usr/bin/env bash
# auto-reviews cron installer. Idempotent. Adds the line only if not already present.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG="$HOME/.auto-reviews.log"
CRON_LINE="0 7 * * * cd $SKILL_DIR && /usr/bin/env python3 run.py >> $LOG 2>&1"

EXISTING="$(crontab -l 2>/dev/null || true)"

if echo "$EXISTING" | grep -Fq "cd $SKILL_DIR &&"; then
  echo "auto-reviews cron already installed. nothing to do."
  exit 0
fi

{
  echo "$EXISTING"
  echo "$CRON_LINE"
} | sed '/^$/d' | crontab -

echo "installed: $CRON_LINE"
