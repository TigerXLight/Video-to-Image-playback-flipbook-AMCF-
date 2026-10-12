from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ComponentUpdatePolicy:
    min_interval_frames: int = 1
    changed_pixel_threshold: int = 1
    changed_ratio_threshold: float = 0.0


@dataclass(frozen=True)
class ComponentUpdateDecision:
    frame_index: int
    should_update: bool
    reason: str
    changed_pixels: int
    changed_ratio: float
    frames_since_last_update: int | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "frame_index": self.frame_index,
            "should_update": self.should_update,
            "reason": self.reason,
            "changed_pixels": self.changed_pixels,
            "changed_ratio": self.changed_ratio,
            "frames_since_last_update": self.frames_since_last_update,
        }


def decide_component_update(
    *,
    frame_index: int,
    last_update_frame: int | None,
    changed_pixels: int,
    total_pixels: int,
    policy: ComponentUpdatePolicy | None = None,
    force_first: bool = False,
) -> ComponentUpdateDecision:
    policy = policy or ComponentUpdatePolicy()
    if total_pixels <= 0:
        raise ValueError("total_pixels must be positive")
    changed_ratio = changed_pixels / total_pixels
    frames_since = None if last_update_frame is None else frame_index - last_update_frame
    if force_first and last_update_frame is None:
        return ComponentUpdateDecision(frame_index, True, "initial_component_state", changed_pixels, changed_ratio, frames_since)
    interval_ok = last_update_frame is None or frames_since is not None and frames_since >= policy.min_interval_frames
    pixel_ok = changed_pixels >= policy.changed_pixel_threshold
    ratio_ok = changed_ratio >= policy.changed_ratio_threshold
    should_update = interval_ok and pixel_ok and ratio_ok
    if should_update:
        reason = "changed_region"
    elif not interval_ok:
        reason = "min_interval_not_met"
    elif not pixel_ok:
        reason = "changed_pixel_threshold_not_met"
    else:
        reason = "changed_ratio_threshold_not_met"
    return ComponentUpdateDecision(frame_index, should_update, reason, changed_pixels, changed_ratio, frames_since)


def build_update_schedule(
    changed_pixel_counts: list[int],
    *,
    total_pixels: int,
    policy: ComponentUpdatePolicy | None = None,
) -> list[dict[str, Any]]:
    last_update: int | None = None
    schedule: list[dict[str, Any]] = []
    for frame_index, changed_pixels in enumerate(changed_pixel_counts):
        decision = decide_component_update(
            frame_index=frame_index,
            last_update_frame=last_update,
            changed_pixels=changed_pixels,
            total_pixels=total_pixels,
            policy=policy,
            force_first=frame_index == 0,
        )
        if decision.should_update:
            last_update = frame_index
        schedule.append(decision.to_dict())
    return schedule
