"""AMCF V2 architecture skeleton. Interfaces only; no media processing."""


from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class FrameDependencyGraph:
    dependencies: Dict[int, List[str]] = field(default_factory=dict)

    def dependencies_for(self, frame_index: int) -> List[str]:
        return list(self.dependencies.get(frame_index, []))
