class AutoPlaywrightError(Exception):
    """Base exception for all errors raised by Auto Playwright."""
    pass

class UnimplementedError(AutoPlaywrightError):
    """Raised when a feature is not yet implemented."""
    pass