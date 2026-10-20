from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(PACKAGE / "src"))

from amcf_software_control_protocol import (  # noqa: E402
    COMMAND_HELLO,
    COMMAND_PLAYER_LOAD_MANIFEST,
    COMMAND_PLAYER_SWITCH,
    PROTOCOL_VERSION,
    ProtocolEnvelope,
    SoftwareControlSession,
    run_software_control_session,
)
from amcf_software_io_fixtures import load_fixture_bundle  # noqa: E402


class AmcfSoftwareControlProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="amcf_software_control_"))
        self.bundle = load_fixture_bundle(PACKAGE)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_complete_session_is_directly_auditable(self) -> None:
        result = run_software_control_session(PACKAGE, self.tmp / "run")
        report = result["report"]
        self.assertTrue(report["final_passed"])
        self.assertEqual(report["command_count"], 19)
        self.assertEqual(report["accepted_command_count"], 19)
        self.assertEqual(report["unsafe_acceptance_count"], 0)
        self.assertFalse(report["hardware_connected"])
        self.assertFalse(report["direct_hardware_transition_authorized"])

    def test_unverified_visible_switch_is_fail_closed(self) -> None:
        session = SoftwareControlSession(self.bundle)
        self.assertTrue(
            session.send(
                COMMAND_HELLO,
                "shared_core",
                {"protocol_version": PROTOCOL_VERSION, "required_capabilities": []},
            ).accepted
        )
        self.assertTrue(session.send(COMMAND_PLAYER_LOAD_MANIFEST, "pc_to_player").accepted)
        response = session.send(
            COMMAND_PLAYER_SWITCH,
            "pc_to_player",
            {"section_id": self.bundle["package"]["manifest"]["physical_sections"][0]["section_id"]},
        )
        self.assertFalse(response.accepted)
        self.assertTrue(response.fail_closed)
        self.assertFalse(response.unsafe_acceptance)

    def test_sequence_gap_is_rejected_and_closes_session(self) -> None:
        session = SoftwareControlSession(self.bundle)
        self.assertTrue(
            session.send(
                COMMAND_HELLO,
                "shared_core",
                {"protocol_version": PROTOCOL_VERSION, "required_capabilities": []},
            ).accepted
        )
        response = session.dispatch(
            ProtocolEnvelope(
                session_id=session.session_id,
                sequence=4,
                command_id="gap-probe",
                corridor="pc_to_player",
                command="PLAYER_STOP",
            )
        )
        self.assertFalse(response.accepted)
        self.assertTrue(response.fail_closed)
        self.assertEqual(response.code, "SEQUENCE_REJECTED_FAIL_CLOSED")
        self.assertFalse(response.unsafe_acceptance)


if __name__ == "__main__":
    unittest.main(verbosity=2)
