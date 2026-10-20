from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.amcf_physical_medium_simulation import write_report


def main() -> int:
    output_dir = Path("output") / "amcf_physical_medium_simulation"
    report = write_report(output_dir)
    print(f"final_passed: {report['final_passed']}")
    print(f"unsafe_acceptance_count: {report['unsafe_acceptance_count']}")
    print(f"output: {output_dir}")
    return 0 if report["final_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
