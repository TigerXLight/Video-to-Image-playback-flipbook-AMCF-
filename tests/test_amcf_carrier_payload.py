from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from amcf_carrier_payload import run_native_payload_roundtrip


class AmcfCarrierPayloadTests(unittest.TestCase):
    def test_native_archive_roundtrip_is_exact_and_directly_decodable(self) -> None:
        archive = PROJECT_ROOT / "demo" / "output" / "amcf_to_physical_carrier" / "sample_video_source.amcf.zip"
        with tempfile.TemporaryDirectory(prefix="amcf-carrier-payload-") as directory:
            result = run_native_payload_roundtrip(archive, Path(directory), page_bytes=30_000, write_pdf=False)
            self.assertTrue(result["ok"], result)
            self.assertTrue(result["recovery"]["exact_archive_recovered"])
            self.assertTrue(result["direct_amcf_decoding"])
            self.assertTrue(result["corruption_rejected"])
            self.assertFalse(result["source_video_embedded"])
            self.assertFalse(result["source_video_required_for_decode"])
            self.assertEqual(result["unsafe_acceptance_count"], 0)
            self.assertGreaterEqual(result["build"]["page_count"], 2)


if __name__ == "__main__":
    unittest.main()
