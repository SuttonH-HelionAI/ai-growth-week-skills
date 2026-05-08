# AI Growth Week, Day 5 installer (Windows PowerShell)
# Drops /start-wiki and /wiki-lint into .\.claude\skills\ from this folder.
# Run inside your kit folder. Public, no auth required.

$ErrorActionPreference = 'Stop'

$repo   = 'SuttonH-HelionAI/ai-growth-week-skills'
$branch = 'day-five'
$skills = @('start-wiki', 'seed-wiki', 'wiki-lint')

if (-not (Test-Path 'CLAUDE.md')) {
    Write-Host ''
    Write-Host '  No CLAUDE.md here. Run this in your kit folder.'
    Write-Host '  (The folder where Claude is open.)'
    Write-Host ''
    exit 1
}

New-Item -ItemType Directory -Force -Path '.claude\skills' | Out-Null

Write-Host ''
Write-Host '  Installing Day 5 wiki tools...'
Write-Host ''

foreach ($skill in $skills) {
    $url  = "https://raw.githubusercontent.com/$repo/$branch/skills/$skill/SKILL.md"
    $dir  = ".claude\skills\$skill"
    $dest = "$dir\SKILL.md"
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    try {
        Invoke-WebRequest -UseBasicParsing -Uri $url -OutFile $dest
        Write-Host "    + /$skill"
    } catch {
        Write-Host "    x /$skill failed to download"
        Write-Host "      $_"
        exit 1
    }
}

Write-Host ''
Write-Host '  Done. Three skills installed: /start-wiki, /seed-wiki, /wiki-lint'
Write-Host ''
Write-Host '  Next steps:'
Write-Host '    1. Type /start-wiki to scaffold the wiki and ingest your first source.'
Write-Host '    2. Type /seed-wiki to auto-populate from everything already in your kit.'
Write-Host '    3. Set a Friday calendar reminder to run /wiki-lint every week.'
Write-Host ''
