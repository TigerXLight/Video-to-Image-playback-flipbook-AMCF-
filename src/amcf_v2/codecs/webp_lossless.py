"""WebP-lossless payload decode adapter for AMCF V2 14C."""
import hashlib
import io
from typing import Any, Dict
from .base import PayloadCodec, PayloadDecodeResult

try:
    from PIL import Image, features
except Exception as exc:  # pragma: no cover
    Image = None
    features = None
    PIL_IMPORT_ERROR = repr(exc)
else:
    PIL_IMPORT_ERROR = None


class WebPLosslessPayloadCodec(PayloadCodec):
    codec_id = "webp_lossless_frames"

    def _webp_available(self) -> bool:
        return Image is not None and features is not None and bool(features.check("webp"))

    def capability_summary(self) -> Dict[str, Any]:
        available = self._webp_available()
        return {"codec_id": self.codec_id, "can_encode": False, "can_decode": available, "pil_webp_available": available, "status": "ready" if available else "unavailable", "error": PIL_IMPORT_ERROR}

    def can_decode(self, payload_metadata: Dict[str, Any]) -> bool:
        if not self._webp_available():
            return False
        strategy = str(payload_metadata.get("codec_strategy", "")).lower()
        extension = str(payload_metadata.get("extension", "")).lower()
        return strategy == self.codec_id or strategy == "webp_lossless_frames" or extension == ".webp"

    def decode(self, payload_bytes: bytes, payload_metadata: Dict[str, Any]) -> PayloadDecodeResult:
        if not self._webp_available():
            raise RuntimeError("PIL WebP support is unavailable")
        with Image.open(io.BytesIO(payload_bytes)) as img:
            rgb = img.convert("RGB")
            raw = rgb.tobytes()
            width, height = rgb.size
            return PayloadDecodeResult(
                frame_index=payload_metadata.get("frame_index"),
                payload_kind="webp_lossless_frame",
                decoded=rgb.copy(),
                width=width,
                height=height,
                channels=3,
                mode="RGB",
                raw_sha256=hashlib.sha256(raw).hexdigest(),
                checksum_ok=None,
                metadata=dict(payload_metadata),
            )
