"""Bounded seek controller for AMCF 14D dry-run."""
class SeekController:
    def __init__(self, frame_ids):
        self.frame_ids = list(frame_ids)
        self.frame_set = set(self.frame_ids)
        self.position = None
    def validate_frame_id(self, frame_id):
        return frame_id in self.frame_set
    def seek(self, frame_id):
        if not self.validate_frame_id(frame_id):
            raise ValueError(f"Invalid frame id: {frame_id}")
        self.position = frame_id
        return frame_id
    def seek_first(self):
        return self.seek(self.frame_ids[0])
    def seek_middle(self):
        return self.seek(self.frame_ids[len(self.frame_ids)//2])
    def seek_last(self):
        return self.seek(self.frame_ids[-1])
