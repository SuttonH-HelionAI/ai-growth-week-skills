#!/usr/bin/env bash
# AI Growth Week, Day 5 installer (Mac and Linux)
# Drops /start-wiki and /wiki-lint into ./.claude/skills/ from this folder.
# Run inside your kit folder. Public, no auth required.

set -e

REPO="SuttonH-HelionAI/ai-growth-week-skills"
BRANCH="day-five"
SKILLS=("start-wiki" "wiki-lint")

if [ ! -f "CLAUDE.md" ]; then
  echo ""
  echo "  No CLAUDE.md here. Run this in your kit folder."
  echo "  (The folder where Claude is open.)"
  echo ""
  exit 1
fi

mkdir -p .claude/skills

echo ""
echo "  Installing Day 5 wiki tools..."
echo ""

for skill in "${SKILLS[@]}"; do
  url="https://raw.githubusercontent.com/${REPO}/${BRANCH}/skills/${skill}/SKILL.md"
  dest=".claude/skills/${skill}/SKILL.md"
  mkdir -p ".claude/skills/${skill}"
  if curl -fsSL "${url}" -o "${dest}"; then
    echo "    + /${skill}"
  else
    echo "    x /${skill} failed to download"
    exit 1
  fi
done

echo ""
echo "  Done. Two skills installed: /start-wiki and /wiki-lint"
echo ""
echo "  Next step:"
echo "    Type /start-wiki in your Claude window."
echo ""
