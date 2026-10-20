"""AMCF V2 architecture skeleton. Interfaces only; no media processing."""


class AMCFV2Error(Exception):
    """Base AMCF V2 skeleton error."""


class UnsupportedPayloadCodecError(AMCFV2Error):
    """Raised when no registered codec can handle a payload."""


class ArchiveValidationError(AMCFV2Error):
    """Raised when archive/index validation fails."""


class NotImplementedFeatureError(NotImplementedError):
    """Raised intentionally for V2 features not implemented in 14A."""
