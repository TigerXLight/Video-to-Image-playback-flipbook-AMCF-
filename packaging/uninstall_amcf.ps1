param(
    [string]$InstallDir = ''
)

$ErrorActionPreference = 'Stop'
if (-not $InstallDir) {
    $localRoot = $env:LOCALAPPDATA
    if (-not $localRoot) { $localRoot = Join-Path $env:USERPROFILE 'AppData\Local' }
    $InstallDir = Join-Path $localRoot 'AMCF'
}
$InstallDir = [System.IO.Path]::GetFullPath($InstallDir)
$startMenuDir = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\AMCF'
$desktopShortcut = Join-Path ([Environment]::GetFolderPath('Desktop')) 'AMCF.lnk'

Remove-Item -LiteralPath (Join-Path $startMenuDir 'AMCF GUI.lnk'), (Join-Path $startMenuDir 'AMCF CLI.lnk'), $desktopShortcut -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $startMenuDir -Recurse -Force -ErrorAction SilentlyContinue
if (Test-Path -LiteralPath $InstallDir) {
    Remove-Item -LiteralPath $InstallDir -Recurse -Force
}
Write-Output (ConvertTo-Json ([ordered]@{
    ok = $true
    removed_install_dir = $InstallDir
    unsafe_acceptance_count = 0
}) -Compress)
