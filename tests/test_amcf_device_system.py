from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys


PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / "src"))
sys.path.insert(0, str(PACKAGE / "demo"))

from amcf_digital_encoder import encode_source_frames  # noqa: E402
from amcf_carrier_renderer import render_carrier_package
from amcf_device_system import OperationController, discover_devices, recover_reader_package, run_device_software_system
from amcf_physical_carrier import generate_physical_carrier_from_amcf_archive  # noqa: E402
from generate_sample_source_frames import generate_source_frames  # noqa: E402


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class AmcfDeviceSystemTests(unittest.TestCase):
    @staticmethod
    def _make_carrier(root: Path) -> Path:
        source_root = root / "source_frames"
        carrier_root = root / "carrier_package"
        carrier_root.mkdir(parents=True, exist_ok=True)
        archive = carrier_root / "sample_video_source.amcf.zip"
        generate_source_frames(source_root)
        encode_source_frames(source_root / "source_frames_manifest.json", archive)
        result = generate_physical_carrier_from_amcf_archive(archive, carrier_root)
        if not result.get("ok"):
            raise AssertionError(result)
        return carrier_root

    def test_complete_simulated_device_system(self) -> None:
        with tempfile.TemporaryDirectory(prefix="amcf-device-system-") as directory:
            root = Path(directory)
            carrier_root = self._make_carrier(root)
            report = run_device_software_system(carrier_root, root / "run")
            self.assertTrue(report["ok"], report)
            self.assertTrue(report["action_paths"]["pc_to_printer"])
            self.assertTrue(report["action_paths"]["reader_to_pc"])
            self.assertTrue(report["action_paths"]["reader_to_amcf_package"])
            self.assertTrue(report["action_paths"]["reader_to_native_amcf_archive"])
            self.assertTrue(report["action_paths"]["pc_to_player"])
            self.assertTrue(report["native_payload_roundtrip"]["direct_amcf_decoding"])
            self.assertTrue((root / "run" / "carrier_render" / "amcf_carrier_sections.pdf").exists())
            self.assertTrue((root / "run" / "reader_recovery" / "recovered_amcf_physical_package.zip").exists())
            self.assertTrue((root / "run" / "native_payload" / "recovered_native_amcf.zip").exists())
            self.assertEqual(report["unsafe_acceptance_count"], 0)

    def test_render_and_pixel_recovery_reject_missing_registration(self) -> None:
        with tempfile.TemporaryDirectory(prefix="amcf-reader-") as directory:
            root = Path(directory)
            carrier_root = self._make_carrier(root)
            render = render_carrier_package(carrier_root, root / "render")
            self.assertTrue(render["ok"])
            first = root / "render" / "section_0000.png"
            from PIL import Image, ImageDraw
            image = Image.open(first).convert("RGB")
            draw = ImageDraw.Draw(image)
            draw.rectangle((52, 52, 86, 86), fill=(255, 255, 255))
            image.save(first)
            recovery = recover_reader_package(
                carrier_root,
                render["render_manifest_path"],
                root / "render",
                root / "recovery",
            )
            self.assertFalse(recovery["ok"])
            first_result = recovery["sections"][0]
            self.assertFalse(first_result["passed"])
            self.assertEqual(recovery["unsafe_acceptance_count"], 0)

    def test_discovery_always_exposes_simulation_devices(self) -> None:
        result = discover_devices()
        self.assertEqual(len(result["simulated_devices"]), 3)
        self.assertEqual(result["unsafe_acceptance_count"], 0)

    def test_operation_controller_retries_and_cancels(self) -> None:
        controller = OperationController(max_retries=2)
        calls = {"count": 0}

        def flaky() -> dict[str, object]:
            calls["count"] += 1
            return {"ok": calls["count"] >= 2}

        result = controller.run("flaky", flaky)
        self.assertTrue(result["ok"])
        self.assertEqual(result["attempts"], 2)
        controller.cancel()
        cancelled = controller.run("cancelled", lambda: {"ok": True})
        self.assertFalse(cancelled["ok"])
        self.assertEqual(cancelled["status"], "CANCELLED")


if __name__ == "__main__":
    unittest.main()
