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
        "amcf_physical_adapters",
        "amcf_hardware_adapter_planning",
        "amcf_hardware_provider_runtime",
        "amcf_software_control_protocol",
        "amcf_device_provider_adapters",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # Deep SAM2/CoTracker runtimes are installed into .amcf-runtime by the
    # explicit setup command; they are intentionally not embedded in the
    # core CLI executable.
    excludes=["torch", "torchvision", "sam2", "cotracker", "hydra", "iopath"],
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
