"""Fail-closed codec stub for AMCF V2 14C."""
from typing import Any, Dict
from .base import PayloadCodec, PayloadDecodeResult


class ZlibResidualPayloadCodec(PayloadCodec):
    codec_id = "zlib_residual"

    def capability_summary(self) -> Dict[str, Any]:
        return {"codec_id": self.codec_id, "can_encode": False, "can_decode": False, "status": "stub_not_used_in_14C"}

    def can_decode(self, payload_metadata: Dict[str, Any]) -> bool:
        return False

    def decode(self, payload_bytes: bytes, payload_metadata: Dict[str, Any]) -> PayloadDecodeResult:
        raise NotImplementedError("zlib_residual is registered as fail-closed stub in 14C.")
