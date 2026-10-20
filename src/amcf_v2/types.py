"""AMCF V2 architecture skeleton. Interfaces only; no media processing."""


from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class ArchiveFingerprint:
    archive_id: str
    path: str
    size_bytes: int
    sha256: Optional[str] = None


@dataclass(frozen=True)
class FrameSpec:
    frame_index: int
    width: int
    height: int
    pixel_format: str = "rgb24"


@dataclass
class PayloadReference:
    codec_id: str
    entry_path: str
    checksum: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationIssue:
    code: str
    message: str
    severity: str = "error"
