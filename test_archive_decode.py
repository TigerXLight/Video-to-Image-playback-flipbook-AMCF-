from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python test_archive_decode.py PATH_TO_AMCF_ZIP")
        return 2
    archive = Path(sys.argv[1])
    with zipfile.ZipFile(archive, "r") as zf:
        names = set(zf.namelist())
        manifest = json.loads(zf.read("manifest.json"))
        required = {"manifest.json", manifest["base"]["path"], manifest["audio"]["path"]}
        missing = required - names
        if missing:
            raise AssertionError(f"missing archive members: {sorted(missing)}")
        events = manifest["events"]
        if not events:
            raise AssertionError("archive has no component events")
        absent = [ev["path"] for ev in events if ev["path"] not in names]
        if absent:
            raise AssertionError(f"missing event payloads: {absent[:5]}")
        if manifest["source"]["width"] != 3840 or manifest["source"]["height"] != 1920:
            raise AssertionError("archive is not native source resolution")
    print(f"OK archive structure: {archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
