class GilmenelError(Exception):
    """Base class for exceptions in this module."""

    pass


class CatalogUnavailableError(GilmenelError):
    """Raised when the requested catalogue is not available."""

    pass


class NoStarsFoundError(GilmenelError):
    """Raised when no stars are returned in field."""

    pass
