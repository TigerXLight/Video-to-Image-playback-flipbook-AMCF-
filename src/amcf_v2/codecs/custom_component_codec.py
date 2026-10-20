"""AMCF V2 architecture skeleton. Interfaces only; no media processing."""


from typing import Any, Dict
from .base import PayloadCodec, PayloadDecodeResult


class CustomComponentPayloadCodec(PayloadCodec):
    codec_id = "custom_component_v2"

    def capability_summary(self) -> Dict[str, Any]:
        return {"codec_id": self.codec_id, "can_encode": False, "can_decode": False, "status": "14A_stub", "notes": "Future component-aware V2 codec placeholder."}

    def decode(self, payload: bytes, metadata: Dict[str, Any]) -> PayloadDecodeResult:
        raise NotImplementedError("custom_component_v2 decode is a future milestone; 14A is interface-only.")
