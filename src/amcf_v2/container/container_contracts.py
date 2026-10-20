"""Container validation contracts for AMCF V2 14B."""
from dataclasses import dataclass, field
from typing import List


@dataclass
class ContainerValidationResult:
    archive_path: str
    archive_size: int = 0
    entry_count: int = 0
    manifest_entries: List[str] = field(default_factory=list)
    index_entries: List[str] = field(default_factory=list)
    payload_entries: List[str] = field(default_factory=list)
    payload_included: bool = False
    codec_strategy: str = ""
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    status: str = "unknown"
