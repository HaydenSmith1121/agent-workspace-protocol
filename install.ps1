$ErrorActionPreference = "Stop"

function Get-InstallerPath {
    param([string] $RepositoryRoot)

    Join-Path $RepositoryRoot "skill\agent-workspace-protocol\scripts\install.py"
}

$scriptDir = $PSScriptRoot
if (-not $scriptDir -and $MyInvocation.MyCommand.Path) {
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
}

$installer = if ($scriptDir) {
    Get-InstallerPath $scriptDir
} else {
    $null
}

if (-not $installer -or -not (Test-Path -LiteralPath $installer)) {
    $tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) (
        "agent-workspace-protocol-" + [guid]::NewGuid().ToString("N")
    )
    $archive = Join-Path $tempRoot "source.zip"
    $archiveUri = (
        "https://github.com/HaydenSmith1121/agent-workspace-protocol/" +
        "archive/refs/heads/main.zip"
    )

    New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null
    Write-Host "Downloading agent-workspace-protocol..."
    Invoke-WebRequest -Uri $archiveUri -OutFile $archive -UseBasicParsing
    Expand-Archive -LiteralPath $archive -DestinationPath $tempRoot -Force

    $repository = Get-ChildItem -LiteralPath $tempRoot -Directory |
        Where-Object { $_.Name -like "agent-workspace-protocol-*" } |
        Select-Object -First 1
    if (-not $repository) {
        throw "Downloaded archive did not contain the expected repository."
    }

    $installer = Get-InstallerPath $repository.FullName
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python 3 is required. Install Python and ensure 'python' is on PATH."
}

& python $installer @args
if ($LASTEXITCODE -ne 0) {
    throw "Installer failed with exit code $LASTEXITCODE."
}
