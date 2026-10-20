"""Payload codec registry for AMCF V2 14C."""
from typing import Dict, Iterable, Optional
from .base import PayloadCodec


class PayloadCodecRegistry:
    def __init__(self):
        self._codecs: Dict[str, PayloadCodec] = {}

    def register(self, codec: PayloadCodec) -> None:
        self._codecs[codec.codec_id] = codec

    def get(self, codec_id: str) -> Optional[PayloadCodec]:
        return self._codecs.get(codec_id)

    def list_codecs(self) -> Iterable[str]:
        return tuple(sorted(self._codecs))

    def choose_decoder(self, payload_metadata):
        for codec in self._codecs.values():
            if codec.can_decode(payload_metadata):
                return codec
        raise LookupError(f"no decoder registered for payload metadata: {payload_metadata}")

    def capability_report(self):
        return [self._codecs[k].capability_summary() for k in sorted(self._codecs)]
