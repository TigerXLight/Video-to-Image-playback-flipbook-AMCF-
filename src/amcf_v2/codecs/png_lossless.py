"""Fail-closed codec stub for AMCF V2 14C."""
from typing import Any, Dict
from .base import PayloadCodec, PayloadDecodeResult


class PNGLosslessPayloadCodec(PayloadCodec):
    codec_id = "png_lossless_frame"

    def capability_summary(self) -> Dict[str, Any]:
        return {"codec_id": self.codec_id, "can_encode": False, "can_decode": False, "status": "stub_not_used_in_14C"}

    def can_decode(self, payload_metadata: Dict[str, Any]) -> bool:
        return False

    def decode(self, payload_bytes: bytes, payload_metadata: Dict[str, Any]) -> PayloadDecodeResult:
        raise NotImplementedError("png_lossless_frame is registered as fail-closed stub in 14C.")
