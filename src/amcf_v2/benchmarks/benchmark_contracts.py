"""AMCF V2 architecture skeleton. Interfaces only; no media processing."""


from dataclasses import dataclass
from typing import Dict


@dataclass
class BenchmarkCase:
    name: str
    category: str


@dataclass
class BenchmarkResult:
    case: BenchmarkCase
    seconds: float
    metrics: Dict[str, float]
