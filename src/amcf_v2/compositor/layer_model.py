"""AMCF V2 architecture skeleton. Interfaces only; no media processing."""


from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class FrameLayer:
    layer_id: str
    frame_index: int
    order: int = 0
    alpha: float = 1.0


@dataclass
class ComponentLayer:
    component_id: str
    bbox: Optional[Tuple[int, int, int, int]] = None
    semantic_label: Optional[str] = None
