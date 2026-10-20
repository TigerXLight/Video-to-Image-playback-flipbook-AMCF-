"""AMCF V2 architecture skeleton. Interfaces only; no media processing."""


from dataclasses import dataclass


@dataclass
class ArtifactCheckResult:
    check_name: str
    passed: bool
    detail: str
