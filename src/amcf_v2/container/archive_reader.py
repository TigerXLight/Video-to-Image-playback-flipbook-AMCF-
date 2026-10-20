"""Read-only AMCF V2 archive reader implementation for 14B."""
import fnmatch
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional


class ArchiveReader:
    def __init__(self, archive_path: str):
        self.archive_path = Path(archive_path)
        self._zip: Optional[zipfile.ZipFile] = None

    def open(self):
        if not self.archive_path.exists():
            raise FileNotFoundError(self.archive_path)
        self._zip = zipfile.ZipFile(self.archive_path, "r")
        return self

    def close(self) -> None:
        if self._zip is not None:
            self._zip.close()
            self._zip = None

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False

    @property
    def zip(self) -> zipfile.ZipFile:
        if self._zip is None:
            raise RuntimeError("ArchiveReader is not open")
        return self._zip

    def list_entries(self) -> List[str]:
        return self.zip.namelist()

    def has_entry(self, path: str) -> bool:
        return path in set(self.list_entries())

    def read_bytes(self, path: str) -> bytes:
        if not self.has_entry(path):
            raise KeyError(f"archive entry not found: {path}")
        return self.zip.read(path)

    def read_text(self, path: str, encoding: str = "utf-8") -> str:
        return self.read_bytes(path).decode(encoding)

    def read_json(self, path: str) -> Dict[str, Any]:
        return json.loads(self.read_text(path))

    def entry_info(self, path: str) -> Dict[str, Any]:
        info = self.zip.getinfo(path)
        return {
            "path": info.filename,
            "compressed_size": info.compress_size,
            "uncompressed_size": info.file_size,
            "crc": info.CRC,
            "date_time": list(info.date_time),
            "compression_type": info.compress_type,
            "header_offset": info.header_offset,
        }

    def sha256_entry(self, path: str) -> str:
        return hashlib.sha256(self.read_bytes(path)).hexdigest()

    def find_entries(self, pattern_or_suffix: str) -> List[str]:
        entries = self.list_entries()
        if any(ch in pattern_or_suffix for ch in "*?[]"):
            return [name for name in entries if fnmatch.fnmatch(name, pattern_or_suffix)]
        return [name for name in entries if name.endswith(pattern_or_suffix) or pattern_or_suffix in name]
