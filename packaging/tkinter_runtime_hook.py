"""Point a frozen Tkinter process at the Tcl/Tk data bundled beside it."""

from __future__ import annotations

import os
import sys
from pathlib import Path


_base = Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
os.environ.setdefault("TCL_LIBRARY", str(_base / "tcl" / "tcl8.6"))
os.environ.setdefault("TK_LIBRARY", str(_base / "tk" / "tk8.6"))
