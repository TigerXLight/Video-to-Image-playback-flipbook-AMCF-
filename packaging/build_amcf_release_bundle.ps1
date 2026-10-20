param(
    [string]$Python = "python",
    [string]$OutputDir = ""
)

$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\")).Path
if (-not $OutputDir) { $OutputDir = Join-Path $Root "output\amcf_windows_bundle" }
$OutputDir = [System.IO.Path]::GetFullPath($OutputDir)
$CliDir = Join-Path $OutputDir "cli"
$GuiDir = Join-Path $OutputDir "gui"
$BundleDir = Join-Path $OutputDir "AMCF_Windows_Bundle"
$ZipPath = Join-Path $OutputDir "AMCF_Windows_Bundle.zip"

New-Item -ItemType Directory -Force $OutputDir | Out-Null
Remove-Item -LiteralPath $CliDir,$GuiDir,$BundleDir,$ZipPath -Recurse -Force -ErrorAction SilentlyContinue

& $PSScriptRoot\build_amcf_cli_exe.ps1 -Python $Python -OutputDir $CliDir
if ($LASTEXITCODE -ne 0) { throw "CLI EXE build failed" }

Push-Location $Root
try {
    & $Python -m PyInstaller --clean --noconfirm --distpath $GuiDir --workpath (Join-Path $GuiDir "build") (Join-Path $PSScriptRoot "amcf_gui.spec")
    if ($LASTEXITCODE -ne 0) { throw "GUI EXE build failed" }
} finally { Pop-Location }

 $GuiAppDir = Join-Path $GuiDir "amcf_gui"
if (-not (Test-Path (Join-Path $GuiAppDir "amcf_gui.exe"))) { throw "GUI EXE was not produced" }
New-Item -ItemType Directory -Force $BundleDir | Out-Null
Copy-Item (Join-Path $CliDir "amcf.exe") (Join-Path $BundleDir "amcf.exe")
Copy-Item $GuiAppDir (Join-Path $BundleDir "amcf_gui") -Recurse -Force
Copy-Item (Join-Path $PSScriptRoot "RUN_AMCF_GUI.cmd") (Join-Path $BundleDir "RUN_AMCF_GUI.cmd")
Copy-Item (Join-Path $PSScriptRoot "README_WINDOWS.md") (Join-Path $BundleDir "README_WINDOWS.md")
Copy-Item (Join-Path $Root "QUICKSTART.md") (Join-Path $BundleDir "QUICKSTART.md")
$FixtureSource = Join-Path $Root "tests\fixtures\amcf_software_io"
$FixtureTarget = Join-Path $BundleDir "tests\fixtures\amcf_software_io"
New-Item -ItemType Directory -Force $FixtureTarget | Out-Null
Copy-Item (Join-Path $FixtureSource "*") $FixtureTarget -Force
if (Test-Path (Join-Path $Root "amcf_dependency_manifest.json")) {
    Copy-Item (Join-Path $Root "amcf_dependency_manifest.json") (Join-Path $BundleDir "amcf_dependency_manifest.json")
}
Compress-Archive -Path (Join-Path $BundleDir "*") -DestinationPath $ZipPath -CompressionLevel Optimal

Write-Output (ConvertTo-Json @{ ok = $true; cli = (Join-Path $BundleDir "amcf.exe"); gui = (Join-Path $BundleDir "amcf_gui\amcf_gui.exe"); gui_launcher = (Join-Path $BundleDir "RUN_AMCF_GUI.cmd"); zip = $ZipPath; unsafe_acceptance_count = 0 } -Compress)

