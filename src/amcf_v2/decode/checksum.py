"""AMCF V2 architecture skeleton. Interfaces only; no media processing."""


import hashlib


class ChecksumVerifier:
    def sha256_bytes(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def verify_sha256(self, data: bytes, expected: str) -> bool:
        return self.sha256_bytes(data) == expected
