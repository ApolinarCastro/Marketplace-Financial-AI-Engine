<#
.SYNOPSIS
    Install .githooks as the active git hooks path for this repository.
    Idempotent: safe to run multiple times.
.NOTES
    Run from repository root:  .\.githooks\install-hooks.ps1
    To verify:  git config --get core.hooksPath
    To uninstall:  git config --unset core.hooksPath
#>
$ErrorActionPreference = 'Stop'
$repoRoot = git rev-parse --show-toplevel
if (-not $repoRoot) {
    Write-Error "Not in a git repository"
    exit 1
}
$current = git config --get core.hooksPath
$expected = '.githooks'
if ($current -eq $expected) {
    Write-Host "hooksPath already set to '$expected' (idempotent)"
    exit 0
}
git config core.hooksPath $expected
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to set core.hooksPath"
    exit 1
}
Write-Host "hooksPath set to '$expected'"
Write-Host ""
Write-Host "To verify:  git config --get core.hooksPath"
Write-Host "To uninstall:  git config --unset core.hooksPath"
exit 0
