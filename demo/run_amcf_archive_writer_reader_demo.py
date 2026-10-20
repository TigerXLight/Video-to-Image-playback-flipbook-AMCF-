from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from amcf_archive_writer_reader import (  # noqa: E402
    build_archive,
    build_demo_report,
    extract_summary,
    fail_closed_validate,
    list_components,
    list_files,
    list_frames,
    list_semantic_objects,
    read_member_json,
    verify_checksums,
)


DEFAULT_OUTPUT = REPO_ROOT / "output" / "amcf_archive_writer_reader_demo"


def print_json(data: object) -> int:
    print(json.dumps(data, indent=2, sort_keys=True))
    if isinstance(data, dict) and data.get("ok") is False:
        return 2
    if isinstance(data, dict) and data.get("final_passed") is False:
        return 2
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AMCF archive writer/reader parity demo")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("demo", help="Create valid and invalid demo archives and reports.")
    p.add_argument("--output", default=str(DEFAULT_OUTPUT))

    p = sub.add_parser("create-minimal-valid")
    p.add_argument("output")

    p = sub.add_parser("create-component-demo")
    p.add_argument("output")

    p = sub.add_parser("create-semantic-parked-reference")
    p.add_argument("output")
    p.add_argument("--source-reference", default="")

    p = sub.add_parser("create-invalid-demo")
    p.add_argument("output")
    p.add_argument("--invalid-case", required=True, choices=["fake_level5", "missing_payload", "fake_user_approval"])

    p = sub.add_parser("inspect")
    p.add_argument("archive")

    p = sub.add_parser("list-files")
    p.add_argument("archive")

    p = sub.add_parser("read-manifest")
    p.add_argument("archive")

    p = sub.add_parser("read-sidecar")
    p.add_argument("archive")

    p = sub.add_parser("read-claim-boundaries")
    p.add_argument("archive")

    p = sub.add_parser("list-frames")
    p.add_argument("archive")

    p = sub.add_parser("list-components")
    p.add_argument("archive")

    p = sub.add_parser("list-semantic-objects")
    p.add_argument("archive")

    p = sub.add_parser("verify-checksums")
    p.add_argument("archive")

    p = sub.add_parser("extract-summary")
    p.add_argument("archive")

    p = sub.add_parser("fail-closed-validate")
    p.add_argument("archive")

    args = parser.parse_args(argv)
    command = args.command or "demo"

    if command == "demo":
        return print_json(build_demo_report(getattr(args, "output", str(DEFAULT_OUTPUT))))
    if command == "create-minimal-valid":
        archive = build_archive(args.output, "minimal_valid", "minimal_valid")
        return print_json({"ok": True, "archive": str(archive), "command": command})
    if command == "create-component-demo":
        archive = build_archive(args.output, "component_demo", "component_demo")
        return print_json({"ok": True, "archive": str(archive), "command": command})
    if command == "create-semantic-parked-reference":
        archive = build_archive(
            args.output,
            "semantic_parked_reference",
            "semantic_parked_reference",
            source_reference=args.source_reference,
        )
        return print_json({"ok": True, "archive": str(archive), "command": command})
    if command == "create-invalid-demo":
        archive = build_archive(
            args.output,
            f"invalid_{args.invalid_case}",
            "invalid_demo",
            invalid_case=args.invalid_case,
        )
        return print_json({"ok": True, "archive": str(archive), "command": command})
    if command == "inspect":
        return print_json(extract_summary(args.archive))
    if command == "list-files":
        return print_json({"ok": True, "files": list_files(args.archive)})
    if command == "read-manifest":
        return print_json(read_member_json(args.archive, "manifest.json"))
    if command == "read-sidecar":
        return print_json(read_member_json(args.archive, "sidecars/semantic_sidecar.json"))
    if command == "read-claim-boundaries":
        return print_json(read_member_json(args.archive, "claim_boundaries.json"))
    if command == "list-frames":
        return print_json({"ok": True, "frames": list_frames(args.archive)})
    if command == "list-components":
        return print_json({"ok": True, "components": list_components(args.archive)})
    if command == "list-semantic-objects":
        return print_json({"ok": True, "objects": list_semantic_objects(args.archive)})
    if command == "verify-checksums":
        return print_json(verify_checksums(args.archive))
    if command == "extract-summary":
        return print_json(extract_summary(args.archive))
    if command == "fail-closed-validate":
        return print_json(fail_closed_validate(args.archive))
    parser.error(f"unsupported command: {command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
