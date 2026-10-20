param(
    [string]$SourceDir = $PSScriptRoot,
    [string]$InstallDir = '',
    [switch]$NoShortcuts
)

$ErrorActionPreference = 'Stop'

function New-Shortcut {
    param(
        [string]$Path,
        [string]$TargetPath,
        [string]$Arguments = '',
        [string]$WorkingDirectory
    )

    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($Path)
    $shortcut.TargetPath = $TargetPath
    $shortcut.Arguments = $Arguments
    $shortcut.WorkingDirectory = $WorkingDirectory
    $shortcut.IconLocation = $TargetPath
    $shortcut.Save()
}

$SourceDir = (Resolve-Path -LiteralPath $SourceDir).Path
if (-not $InstallDir) {
    $localRoot = $env:LOCALAPPDATA
    if (-not $localRoot) { $localRoot = Join-Path $env:USERPROFILE 'AppData\Local' }
    $InstallDir = Join-Path $localRoot 'AMCF'
}
$InstallDir = [System.IO.Path]::GetFullPath($InstallDir)
if ($SourceDir.TrimEnd('\') -ieq $InstallDir.TrimEnd('\')) {
    throw 'SourceDir and InstallDir must be different directories.'
}

$guiExe = Join-Path $InstallDir 'amcf_gui\amcf_gui.exe'
$cliExe = Join-Path $InstallDir 'amcf.exe'
if (-not (Test-Path -LiteralPath (Join-Path $SourceDir 'amcf.exe'))) {
    throw "The source bundle is missing amcf.exe: $SourceDir"
}
if (-not (Test-Path -LiteralPath (Join-Path $SourceDir 'amcf_gui\amcf_gui.exe'))) {
    throw "The source bundle is missing amcf_gui.exe: $SourceDir"
}

New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
Get-ChildItem -LiteralPath $SourceDir -Force | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $InstallDir -Recurse -Force
}

$startMenuDir = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\AMCF'
$desktopShortcut = Join-Path ([Environment]::GetFolderPath('Desktop')) 'AMCF.lnk'
$startShortcut = Join-Path $startMenuDir 'AMCF GUI.lnk'
$cliShortcut = Join-Path $startMenuDir 'AMCF CLI.lnk'

if (-not $NoShortcuts) {
    New-Item -ItemType Directory -Force -Path $startMenuDir | Out-Null
    New-Shortcut -Path $startShortcut -TargetPath (Join-Path $InstallDir 'RUN_AMCF_GUI.cmd') -WorkingDirectory $InstallDir
    New-Shortcut -Path $cliShortcut -TargetPath $cliExe -WorkingDirectory $InstallDir
    New-Shortcut -Path $desktopShortcut -TargetPath (Join-Path $InstallDir 'RUN_AMCF_GUI.cmd') -WorkingDirectory $InstallDir
}

$manifest = [ordered]@{
    product = 'AMCF Windows bundle'
    install_dir = $InstallDir
    installed_utc = [DateTime]::UtcNow.ToString('o')
    gui_exe = $guiExe
    cli_exe = $cliExe
    shortcuts_created = (-not $NoShortcuts)
    hardware_validation_claimed = $false
    physical_level_5_claimed = $false
}
$manifest | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $InstallDir 'install_manifest.json') -Encoding UTF8
Write-Output (ConvertTo-Json ([ordered]@{
    ok = $true
    install_dir = $InstallDir
    gui = $guiExe
    cli = $cliExe
    shortcuts_created = (-not $NoShortcuts)
    unsafe_acceptance_count = 0
}) -Compress)
