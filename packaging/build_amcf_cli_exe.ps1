param(
    [string]$Python = "python",
    [string]$OutputDir = ""
)

$ErrorActionPreference = "Stop"
$MainRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\")).Path
if (-not $OutputDir) {
    $OutputDir = Join-Path $MainRoot "output\amcf_cli_exe"
}
$OutputDir = [System.IO.Path]::GetFullPath($OutputDir)
$WorkDir = Join-Path $OutputDir "build"
$Spec = Join-Path $PSScriptRoot "amcf_cli.spec"

& $Python -m PyInstaller --version *> $null
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller is not installed for the selected Python. Install the optional EXE tool first: python -m pip install pyinstaller"
}

New-Item -ItemType Directory -Force $OutputDir | Out-Null
Remove-Item -LiteralPath $WorkDir -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath (Join-Path $OutputDir "amcf.exe") -Force -ErrorAction SilentlyContinue

Push-Location $MainRoot
try {
    & $Python -m PyInstaller --clean --noconfirm `
        --distpath $OutputDir `
        --workpath $WorkDir `
        $Spec
    if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed" }
} finally {
    Pop-Location
}

$Exe = Join-Path $OutputDir "amcf.exe"
if (-not (Test-Path -LiteralPath $Exe)) {
    throw "PyInstaller completed without producing $Exe"
}

& $Exe status
if ($LASTEXITCODE -ne 0) { throw "Built amcf.exe failed the status smoke test" }
& $Exe --help *> $null
if ($LASTEXITCODE -ne 0) { throw "Built amcf.exe failed the help smoke test" }

Write-Output (ConvertTo-Json @{
    ok = $true
    exe = $Exe
    hardware_validation_claimed = $false
    physical_level_5_claimed = $false
    manufactured_player_claimed = $false
    unsafe_acceptance_count = 0
} -Compress)
