"""AMCF V2 architecture skeleton. Interfaces only; no media processing."""


from dataclasses import dataclass, field
from typing import Dict


@dataclass
class ComponentModel:
    component_id: str
    metadata: Dict[str, str] = field(default_factory=dict)
