"""Manifest discovery and loading for AMCF V2 14B."""
from typing import Any, Dict, List, Optional


class ManifestLoader:
    def __init__(self, reader):
        self.reader = reader

    def discover_manifest_entries(self) -> List[str]:
        return [n for n in self.reader.list_entries() if n.endswith(".json") and ("manifest/" in n or "manifest" in n)]

    def _first(self, tokens: List[str]) -> Optional[str]:
        for name in self.discover_manifest_entries():
            low = name.lower()
            if all(tok in low for tok in tokens):
                return name
        return None

    def load_native_manifest(self) -> Dict[str, Any]:
        path = self._first(["native", "manifest"])
        if not path:
            raise KeyError("native manifest entry not found")
        data = self.reader.read_json(path)
        data["_entry_path"] = path
        return data

    def load_residual_stream_manifest(self) -> Dict[str, Any]:
        path = self._first(["residual", "manifest"])
        if not path:
            raise KeyError("residual stream manifest entry not found")
        data = self.reader.read_json(path)
        data["_entry_path"] = path
        return data

    def load_component_grid_if_present(self) -> Dict[str, Any]:
        path = self._first(["component"]) or ""
        if not path:
            return {"_missing": True}
        data = self.reader.read_json(path)
        data["_entry_path"] = path
        return data

    def summarize_manifest(self) -> Dict[str, Any]:
        native = self.load_native_manifest()
        residual = self.load_residual_stream_manifest()
        component = self.load_component_grid_if_present()
        return {
            "native_manifest_entry": native.get("_entry_path"),
            "residual_stream_manifest_entry": residual.get("_entry_path"),
            "component_grid_present": not component.get("_missing", False),
            "payload_included": bool(native.get("payload_included", residual.get("payload_included", False))),
            "variant_id": native.get("variant_id", residual.get("variant_id")),
            "codec_strategy": native.get("codec_strategy", residual.get("codec_strategy")),
            "frame_count": native.get("frame_count"),
            "width": native.get("width"),
            "height": native.get("height"),
            "exact_lossy_flag": native.get("exact_lossy_flag"),
            "checksums_available": True,
            "dependency_mode": "manifest/index-driven",
            "archive_format_version": native.get("amcf_version", native.get("test_id", "missing")),
            "missing_fields": [k for k in ["frame_count", "width", "height", "codec_strategy"] if native.get(k) is None],
        }
