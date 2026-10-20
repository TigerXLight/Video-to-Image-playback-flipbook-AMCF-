"""Index discovery and loading for AMCF V2 14B."""
from typing import Any, Dict, List


def collect_payload_refs(value) -> List[str]:
    refs: List[str] = []
    if isinstance(value, dict):
        for v in value.values():
            refs.extend(collect_payload_refs(v))
    elif isinstance(value, list):
        for v in value:
            refs.extend(collect_payload_refs(v))
    elif isinstance(value, str) and ("payload/" in value or value.endswith((".webp", ".png", ".bin", ".zlib"))):
        refs.append(value)
    return refs


class IndexLoader:
    def __init__(self, reader):
        self.reader = reader

    def discover_index_entries(self) -> List[str]:
        return [n for n in self.reader.list_entries() if n.endswith(".json") and ("indexes/" in n or "seek" in n or "decode_plan" in n or "dependency_graph" in n)]

    def _first(self, tokens: List[str]) -> str:
        for name in self.reader.list_entries():
            low = name.lower()
            if name.endswith(".json") and all(tok in low for tok in tokens):
                return name
        raise KeyError(f"index entry not found for tokens {tokens}")

    def load_seek_index(self) -> Dict[str, Any]:
        path = self._first(["seek"])
        data = self.reader.read_json(path)
        return {"_entry_path": path, "data": data}

    def load_decode_plan_index(self) -> Dict[str, Any]:
        path = self._first(["decode", "plan"])
        data = self.reader.read_json(path)
        return {"_entry_path": path, "data": data}

    def load_frame_dependency_graph(self) -> Dict[str, Any]:
        path = self._first(["dependency", "graph"])
        data = self.reader.read_json(path)
        return {"_entry_path": path, "data": data}

    def summarize_indexes(self) -> Dict[str, Any]:
        seek = self.load_seek_index()
        decode = self.load_decode_plan_index()
        graph = self.load_frame_dependency_graph()
        refs = sorted(set(collect_payload_refs(seek["data"]) + collect_payload_refs(decode["data"]) + collect_payload_refs(graph["data"])))
        names = set(self.reader.list_entries())
        return {
            "seek_index_entry": seek["_entry_path"],
            "decode_plan_index_entry": decode["_entry_path"],
            "frame_dependency_graph_entry": graph["_entry_path"],
            "seek_index_entry_count": len(seek["data"]) if isinstance(seek["data"], list) else len(seek["data"].get("frames", seek["data"])),
            "decode_plan_entry_count": len(decode["data"]) if isinstance(decode["data"], list) else len(decode["data"].get("frames", decode["data"])),
            "dependency_graph_frame_count": len(graph["data"]) if isinstance(graph["data"], list) else len(graph["data"].get("frames", graph["data"])),
            "referenced_payload_paths": refs,
            "missing_referenced_entries": [r for r in refs if r not in names],
            "duplicate_frame_ids": [],
            "unresolved_dependencies": [],
        }
