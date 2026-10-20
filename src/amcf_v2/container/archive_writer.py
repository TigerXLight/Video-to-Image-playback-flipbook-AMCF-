"""AMCF V2 architecture skeleton. Interfaces only; no media processing."""


class ArchiveWriter:
    """Future archive writer. Disabled in 14A to avoid modifying accepted archives."""

    def write_archive(self, *args, **kwargs):
        raise NotImplementedError("Archive writing is outside 14A architecture skeleton.")
