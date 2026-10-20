"""Bounded in-memory frame cache for AMCF 14D dry-run."""
from collections import OrderedDict

class FrameCache:
    def __init__(self, max_items=None):
        self.max_items = max_items
        self._frames = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.puts = 0
    def get(self, frame_id):
        if frame_id in self._frames:
            self.hits += 1
            self._frames.move_to_end(frame_id)
            return self._frames[frame_id]
        self.misses += 1
        return None
    def put(self, frame_id, frame):
        self.puts += 1
        self._frames[frame_id] = frame
        self._frames.move_to_end(frame_id)
        if self.max_items is not None:
            while len(self._frames) > self.max_items:
                self._frames.popitem(last=False)
    def has(self, frame_id):
        return frame_id in self._frames
    def clear(self):
        self._frames.clear()
        self.hits = 0
        self.misses = 0
        self.puts = 0
    def stats(self):
        return {"items": len(self._frames), "hits": self.hits, "misses": self.misses, "puts": self.puts}
