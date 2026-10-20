# PyInstaller windowed build for the small AMCF workflow UI.
from pathlib import Path

PROJECT = Path.cwd().resolve()
SRC = PROJECT / "src"
PYTHON_HOME = Path(__import__("sys").base_prefix)
TCL_ROOT = PYTHON_HOME / "tcl"
DLL_ROOT = PYTHON_HOME / "DLLs"

a = Analysis(
    [str(SRC / "amcf_gui.py")],
    pathex=[str(SRC)],
    binaries=[
        (str(DLL_ROOT / "_tkinter.pyd"), "."),
        (str(DLL_ROOT / "tcl86t.dll"), "."),
        (str(DLL_ROOT / "tk86t.dll"), "."),
    ],
    datas=[
        (str(TCL_ROOT / "tcl8.6"), "tcl/tcl8.6"),
        (str(TCL_ROOT / "tk8.6"), "tk/tk8.6"),
    ],
    hiddenimports=[
        "amcf_diagnostic_profiles",
        "amcf_diagnostic_state",
        "amcf_component_ffv1_temporal",
        "amcf_component_size_ceiling",
        "amcf_temporal_component_codec",
        "amcf_source_seeded_event_materializer",
        "amcf_physical_adapters",
        "amcf_hardware_adapter_planning",
        "amcf_hardware_provider_runtime",
        "amcf_software_control_protocol",
        "amcf_device_provider_adapters",
        "amcf_device_profiles",
        "amcf_device_interface_conformance",
    "amcf_universal_hardware_simulation",
        "tkinter",
        "_tkinter",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[str(PROJECT / "packaging" / "tkinter_runtime_hook.py")],
    # The GUI launches the explicit setup command for deep inference; those
    # research runtimes are not embedded in the workflow executable.
    excludes=["torch", "torchvision", "sam2", "cotracker", "hydra", "iopath"],
    noarchive=False,
)

pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    [],
    name="amcf_gui",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    exclude_binaries=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="amcf_gui",
)

