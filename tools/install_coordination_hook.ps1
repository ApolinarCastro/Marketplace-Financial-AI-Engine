$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$hookSource = Join-Path $repoRoot '.githooks'
$expected = Join-Path $hookSource 'pre-commit'

if (-not (Test-Path $expected)) {
    throw 'Missing versioned hook at .githooks/pre-commit'
}

$current = git config --local --get core.hooksPath 2>$null
if ($current -eq '.githooks') {
    Write-Host 'core.hooksPath already configured to .githooks'
    exit 0
}

git config --local core.hooksPath .githooks
Write-Host 'Configured core.hooksPath=.githooks'
Write-Host 'Hook installation is explicit and idempotent.'
