"""Payload codec interfaces for AMCF V2 14C."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class PayloadDecodeResult:
    frame_index: Optional[int]
    payload_kind: str
    decoded: Any = None
    width: Optional[int] = None
    height: Optional[int] = None
    channels: Optional[int] = None
    mode: Optional[str] = None
    raw_sha256: Optional[str] = None
    checksum_ok: Optional[bool] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PayloadEncodeResult:
    payload_kind: str
    encoded: bytes
    checksum: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class PayloadCodec(ABC):
    codec_id = "abstract"

    def capability_summary(self) -> Dict[str, Any]:
        return {"codec_id": self.codec_id, "can_encode": False, "can_decode": False, "status": "abstract"}

    @abstractmethod
    def can_decode(self, payload_metadata: Dict[str, Any]) -> bool:
        raise NotImplementedError

    def can_encode(self, payload_metadata: Dict[str, Any]) -> bool:
        return False

    @abstractmethod
    def decode(self, payload_bytes: bytes, payload_metadata: Dict[str, Any]) -> PayloadDecodeResult:
        raise NotImplementedError

    def encode(self, frame: Any, metadata: Dict[str, Any]) -> PayloadEncodeResult:
        raise NotImplementedError("Encoding is not implemented in 14C.")
