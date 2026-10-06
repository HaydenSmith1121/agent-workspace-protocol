$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$installer = Join-Path $scriptDir "skill\agent-workspace-protocol\scripts\install.py"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python 3 is required. Install Python and ensure 'python' is on PATH."
}

& python $installer @args
exit $LASTEXITCODE
