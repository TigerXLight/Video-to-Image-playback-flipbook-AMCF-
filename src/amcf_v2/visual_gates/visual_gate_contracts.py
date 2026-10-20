"""AMCF V2 architecture skeleton. Interfaces only; no media processing."""


from dataclasses import dataclass
from typing import Dict


@dataclass
class VisualGateCase:
    name: str
    requires_human_review: bool = True


@dataclass
class VisualGateResult:
    case: VisualGateCase
    passed: bool
    notes: str
    metrics: Dict[str, float]
