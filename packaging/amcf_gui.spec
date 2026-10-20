# PyInstaller windowed build for the small AMCF workflow UI.
from pathlib import Path

PROJECT = Path.cwd().resolve()
SRC = PROJECT / "src"

a = Analysis(
    [str(SRC / "amcf_gui.py")],
    pathex=[str(SRC)],
    binaries=[],
    datas=[],
    hiddenimports=[
        "amcf_diagnostic_profiles",
        "amcf_diagnostic_state",
        "amcf_component_ffv1_temporal",
        "amcf_component_size_ceiling",
        "amcf_temporal_component_codec",
        "amcf_source_seeded_event_materializer",
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
    name="amcf_gui",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)

