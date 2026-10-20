"""Pass-through compositor for complete decoded frames in AMCF 14D."""
class PassThroughCompositor:
    def compose_frame(self, frame, expected_size=None):
        if frame is None:
            raise ValueError("Cannot compose a missing frame")
        if expected_size is not None and getattr(frame, "size", None) != tuple(expected_size):
            raise ValueError(f"Frame size mismatch: {getattr(frame, 'size', None)} != {expected_size}")
        return frame
