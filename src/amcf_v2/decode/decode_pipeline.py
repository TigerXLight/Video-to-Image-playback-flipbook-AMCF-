"""Read-only WebP decode pipeline skeleton for AMCF 14D."""
import io
import zipfile

try:
    from PIL import Image
except Exception as exc:  # pragma: no cover
    Image = None
    PIL_IMPORT_ERROR = repr(exc)
else:
    PIL_IMPORT_ERROR = None

class DecodePipeline:
    def __init__(self, archive_path, frame_plan):
        self.archive_path = archive_path
        self.frame_plan = list(frame_plan)
    def decode_frame(self, frame_id):
        if Image is None:
            raise RuntimeError(f"Pillow image support is unavailable: {PIL_IMPORT_ERROR}")
        item = next(row for row in self.frame_plan if row["frame_index"] == frame_id)
        with zipfile.ZipFile(self.archive_path, "r") as zf:
            data = zf.read(item["payload_entry"])
        image = Image.open(io.BytesIO(data)).convert("RGB")
        return image, data
