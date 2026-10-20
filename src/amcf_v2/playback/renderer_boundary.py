"""AMCF V2 architecture skeleton. Interfaces only; no media processing."""


class RendererBoundary:
    def submit_frame(self, frame):
        raise NotImplementedError("Renderer/UI boundary is not implemented in 14A.")
