# PyInstaller one-file console build for the maintained AMCF CLI.
# Optional research packages are intentionally not bundled by this baseline.

from pathlib import Path


# The build wrapper deliberately runs PyInstaller from Main, making this
# independent of PyInstaller's spec-variable path semantics.
PROJECT = Path.cwd().resolve()
SRC = PROJECT / "src"


a = Analysis(
    [str(SRC / "amcf_cli.py")],
    pathex=[str(SRC)],
    binaries=[],
    datas=[],
    hiddenimports=[
        "amcf_diagnostic_profiles",
        "amcf_diagnostic_state",
        "amcf_component_ffv1_temporal",
        "amcf_component_size_ceiling",
        "amcf_temporal_component_codec",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="amcf",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
)
