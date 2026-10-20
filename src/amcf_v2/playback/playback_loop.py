"""Playback-loop dry-run contracts for AMCF 14D."""
class PlaybackClock:
    def __init__(self, source_fps=30.0):
        self.source_fps = float(source_fps)
        self.frame_duration_seconds = 1.0 / self.source_fps
    def timestamp_for(self, frame_number):
        return frame_number * self.frame_duration_seconds

class PlaybackLoop:
    def __init__(self, frame_ids, clock=None):
        self.frame_ids = list(frame_ids)
        self.clock = clock or PlaybackClock()
        self.paused = False
    def pause(self):
        self.paused = True
    def resume(self):
        self.paused = False
