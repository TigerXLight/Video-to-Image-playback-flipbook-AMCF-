"""AMCF V2 architecture skeleton. Interfaces only; no media processing."""


from dataclasses import dataclass, field
from typing import List
from .dependency_graph import FrameDependencyGraph


@dataclass
class DecodePlan:
    frame_indexes: List[int] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)


class DecodePlanner:
    def build_plan(self, graph: FrameDependencyGraph, frame_indexes: List[int]) -> DecodePlan:
        return DecodePlan(frame_indexes=frame_indexes, actions=[f"decode_frame:{i}" for i in frame_indexes])
