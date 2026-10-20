from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

from amcf_cross_corridor_roundtrip import run_cross_corridor_roundtrip
from amcf_player_pc_runtime import write_player_pc_runtime_demo
from amcf_print_layout import write_print_layout_demo
from amcf_reader_recovery import write_reader_recovery_demo
from amcf_shared_package_model import CLAIM_BOUNDARY_FLAGS


ADAPTER_CONTRACT_VERSION = "amcf-physical-software-adapter-contract-v1"
RUN_NAME = "AMCF_PHYSICAL_SOFTWARE_ADAPTER_ROUNDTRIP_V1"

CORRIDOR_SHARED = "shared_core"
CORRIDOR_PRINTER = "pc_to_printer"
CORRIDOR_READER = "reader_to_pc"
CORRIDOR_PLAYER = "pc_to_player"


@dataclass(frozen=True)
class AdapterStatusEvent:
    sequence: int
    adapter_id: str
    corridor: str
    state: str
    code: str
    accepted: bool
    severity: str
    message: str
    display_allowed: bool
    transition_allowed: bool
    retry_allowed: bool
    rescan_allowed: bool
    fail_closed: bool
    unsafe_acceptance: bool = False


@dataclass(frozen=True)
class AdapterResult:
    adapter_id: str
    corridor: str
    passed: bool
    report_ref: str
    output_dir: str
    hardware_connected: bool
    unsafe_acceptance_count: int


def _report_passed(result: dict[str, Any]) -> bool:
    report = result.get("report", result)
    return bool(report.get("final_passed", result.get("final_passed", False)))


def _report_unsafe_count(result: dict[str, Any]) -> int:
    report = result.get("report", result)
    return int(report.get("unsafe_acceptance_count", result.get("unsafe_acceptance_count", 0)) or 0)


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_summary(path: Path, report: dict[str, Any]) -> None:
    feedback = report["feedback"]
    lines = [
        "# AMCF Physical Software Adapter Roundtrip",
        "",
        "This run validates the shared software contract across the PC-to-printer/carrier, reader-to-PC, and PC-to-player corridors.",
        "It uses the maintained deterministic fixtures and does not claim real hardware validation.",
        "",
        f"- contract_version: {report['contract_version']}",
        f"- final_passed: {'yes' if report['final_passed'] else 'no'}",
        f"- status: {feedback['status']}",
        f"- display_allowed: {'yes' if feedback['display_allowed'] else 'no'}",
        f"- transition_allowed: {'yes' if feedback['transition_allowed'] else 'no'}",
        f"- unsafe_acceptance_count: {report['unsafe_acceptance_count']}",
        "- hardware connected: no",
        "- real printer/scanner/player/USB/firmware validation claimed: no",
        "- physical Level 5 claimed: no",
        "",
        "## Corridors",
        "",
    ]
    for item in report["adapter_results"]:
        lines.append(
            f"- {item['adapter_id']} ({item['corridor']}): "
            f"{'PASS' if item['passed'] else 'FAIL-CLOSED'}; report={item['report_ref']}"
        )
    lines.extend(
        [
            "",
            "## Next boundary",
            "",
            feedback["message"],
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def run_physical_software_adapter_roundtrip(
    repo_root: str | Path,
    output_dir: str | Path,
) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    events: list[AdapterStatusEvent] = []
    results: list[AdapterResult] = []
    sequence = 0

    def add_event(
        adapter_id: str,
        corridor: str,
        state: str,
        code: str,
        accepted: bool,
        severity: str,
        message: str,
        display_allowed: bool,
        transition_allowed: bool,
        retry_allowed: bool,
        rescan_allowed: bool,
        fail_closed: bool,
        unsafe_acceptance: bool = False,
    ) -> None:
        nonlocal sequence
        events.append(
            AdapterStatusEvent(
                sequence=sequence,
                adapter_id=adapter_id,
                corridor=corridor,
                state=state,
                code=code,
                accepted=accepted,
                severity=severity,
                message=message,
                display_allowed=display_allowed,
                transition_allowed=transition_allowed,
                retry_allowed=retry_allowed,
                rescan_allowed=rescan_allowed,
                fail_closed=fail_closed,
                unsafe_acceptance=unsafe_acceptance,
            )
        )
        sequence += 1

    add_event(
        "adapter-contract",
        CORRIDOR_SHARED,
        "contract_ready",
        "SOFTWARE_ADAPTER_CONTRACT_READY",
        True,
        "info",
        "Shared status, feedback, and fail-closed rules are active.",
        False,
        False,
        False,
        False,
        False,
    )

    def execute(
        adapter_id: str,
        corridor: str,
        target: Path,
        report_name: str,
        runner: Callable[[str | Path, str | Path], dict[str, Any]],
    ) -> None:
        report_ref = str(target / report_name)
        add_event(
            adapter_id,
            corridor,
            "adapter_ready",
            "ADAPTER_FIXTURE_READY",
            True,
            "info",
            "Deterministic software fixture is ready.",
            False,
            False,
            False,
            False,
            False,
        )
        try:
            result = runner(root, target)
            passed = _report_passed(result)
            unsafe = _report_unsafe_count(result)
            if passed and unsafe == 0:
                add_event(
                    adapter_id,
                    corridor,
                    "accepted",
                    "ADAPTER_ACCEPTED_SOFTWARE_ONLY",
                    True,
                    "info",
                    "Software corridor passed; no physical transition is authorized by this run.",
                    False,
                    False,
                    False,
                    False,
                    False,
                )
            else:
                add_event(
                    adapter_id,
                    corridor,
                    "rejected",
                    "ADAPTER_REJECTED_FAIL_CLOSED",
                    False,
                    "error",
                    "Corridor failed validation or reported unsafe acceptance; hold the state.",
                    False,
                    False,
                    True,
                    corridor == CORRIDOR_READER,
                    True,
                    unsafe_acceptance=unsafe > 0,
                )
            results.append(
                AdapterResult(
                    adapter_id=adapter_id,
                    corridor=corridor,
                    passed=passed and unsafe == 0,
                    report_ref=report_ref,
                    output_dir=str(target),
                    hardware_connected=False,
                    unsafe_acceptance_count=unsafe,
                )
            )
        except Exception as exc:  # noqa: BLE001 - convert adapter faults into deterministic feedback.
            add_event(
                adapter_id,
                corridor,
                "fault",
                "ADAPTER_EXCEPTION_FAIL_CLOSED",
                False,
                "error",
                f"Adapter fixture raised {type(exc).__name__}: {exc}",
                False,
                False,
                True,
                corridor == CORRIDOR_READER,
                True,
            )
            results.append(
                AdapterResult(
                    adapter_id=adapter_id,
                    corridor=corridor,
                    passed=False,
                    report_ref=report_ref,
                    output_dir=str(target),
                    hardware_connected=False,
                    unsafe_acceptance_count=1,
                )
            )

    execute(
        "printer-carrier-adapter",
        CORRIDOR_PRINTER,
        out / CORRIDOR_PRINTER,
        "print_layout_report.json",
        write_print_layout_demo,
    )
    execute(
        "reader-recovery-adapter",
        CORRIDOR_READER,
        out / CORRIDOR_READER,
        "reader_recovery_report.json",
        write_reader_recovery_demo,
    )
    execute(
        "player-control-adapter",
        CORRIDOR_PLAYER,
        out / CORRIDOR_PLAYER,
        "player_pc_session_report.json",
        write_player_pc_runtime_demo,
    )

    try:
        shared_result = run_cross_corridor_roundtrip(root)
        shared_report = shared_result["roundtrip_report"]
        shared_passed = bool(shared_report.get("final_passed")) and int(shared_report.get("unsafe_acceptance_count", 0)) == 0
        shared_unsafe = int(shared_report.get("unsafe_acceptance_count", 0))
        shared_report_ref = str(out / "shared_core" / "cross_corridor_roundtrip_report.json")
        _write_json(out / "shared_core" / "cross_corridor_roundtrip_report.json", shared_report)
        _write_json(
            out / "shared_core" / "roundtrip_component_reports.json",
            {key: value for key, value in shared_result.items() if key != "roundtrip_report"},
        )
        add_event(
            "shared-corridor-validator",
            CORRIDOR_SHARED,
            "accepted" if shared_passed else "rejected",
            "SHARED_CORRIDOR_ACCEPTED" if shared_passed else "SHARED_CORRIDOR_REJECTED_FAIL_CLOSED",
            shared_passed,
            "info" if shared_passed else "error",
            "Shared manifest and cross-corridor validator completed.",
            False,
            False,
            not shared_passed,
            False,
            not shared_passed,
            unsafe_acceptance=shared_unsafe > 0,
        )
        results.append(
            AdapterResult(
                adapter_id="shared-corridor-validator",
                corridor=CORRIDOR_SHARED,
                passed=shared_passed,
                report_ref=shared_report_ref,
                output_dir=str(out / "shared_core"),
                hardware_connected=False,
                unsafe_acceptance_count=shared_unsafe,
            )
        )
    except Exception as exc:  # noqa: BLE001 - shared failures are also fail-closed.
        shared_report_ref = str(out / "shared_core" / "cross_corridor_roundtrip_report.json")
        add_event(
            "shared-corridor-validator",
            CORRIDOR_SHARED,
            "fault",
            "SHARED_CORRIDOR_EXCEPTION_FAIL_CLOSED",
            False,
            "error",
            f"Shared validator raised {type(exc).__name__}: {exc}",
            False,
            False,
            True,
            False,
            True,
        )
        results.append(
            AdapterResult(
                adapter_id="shared-corridor-validator",
                corridor=CORRIDOR_SHARED,
                passed=False,
                report_ref=shared_report_ref,
                output_dir=str(out / "shared_core"),
                hardware_connected=False,
                unsafe_acceptance_count=1,
            )
        )

    unsafe_acceptance_count = sum(item.unsafe_acceptance_count for item in results) + sum(
        1 for event in events if event.unsafe_acceptance
    )
    final_passed = all(item.passed for item in results) and unsafe_acceptance_count == 0
    feedback = {
        "status": "accepted_software_only" if final_passed else "rejected_fail_closed",
        "display_allowed": False,
        "transition_allowed": False,
        "retry_allowed": not final_passed,
        "rescan_allowed": not final_passed,
        "recommended_action": (
            "continue_to_hardware_adapter_planning"
            if final_passed
            else "inspect_adapter_status_events_before_any_transition"
        ),
        "message": (
            "The software contracts are ready for hardware-adapter planning. A real device must still pass a device-specific contract before any physical transition is authorized."
            if final_passed
            else "At least one software corridor failed. Keep the system fail-closed and inspect the ordered status events before retrying."
        ),
    }
    claim_flags = dict(CLAIM_BOUNDARY_FLAGS)
    report = {
        "run_name": RUN_NAME,
        "contract_version": ADAPTER_CONTRACT_VERSION,
        "repo_root": str(root),
        "output_dir": str(out),
        "final_passed": final_passed,
        "adapter_results": [asdict(item) for item in results],
        "status_events": [asdict(event) for event in events],
        "feedback": feedback,
        "claim_boundary_flags": claim_flags,
        "unsafe_acceptance_count": unsafe_acceptance_count,
        "hardware_connected": False,
        "real_driver_or_protocol_used": False,
        "physical_level_5_claimed": False,
        "manufactured_player_claimed": False,
        "source_video_required": False,
    }
    _write_json(out / "physical_software_adapter_report.json", report)
    _write_json(out / "adapter_status_events.json", report["status_events"])
    _write_json(out / "adapter_feedback.json", feedback)
    _write_summary(out / "PHYSICAL_SOFTWARE_ADAPTER_ROUNDTRIP_SUMMARY.md", report)
    return {"report": report, "output_dir": str(out)}
