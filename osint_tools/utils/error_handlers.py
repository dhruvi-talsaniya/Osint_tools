"""Custom exceptions and error-handling utilities for OSINT Tools."""


class OsintToolsError(Exception):
    """Base exception for all OSINT Tools errors."""


class NetworkError(OsintToolsError):
    """Raised when an HTTP/network request fails."""


class RateLimitError(OsintToolsError):
    """Raised when a remote API returns a rate-limit response (HTTP 429)."""


class APIKeyError(OsintToolsError):
    """Raised when a required API key is missing or invalid."""


class ValidationError(OsintToolsError):
    """Raised when input validation fails (e.g. invalid IP or email format)."""


class ParseError(OsintToolsError):
    """Raised when a response cannot be parsed as expected."""


def handle_http_error(response) -> None:
    """Raise an appropriate :class:`OsintToolsError` for a failed response.

    Args:
        response: A :class:`requests.Response` object.

    Raises:
        RateLimitError: If ``status_code`` is 429.
        APIKeyError: If ``status_code`` is 401 or 403.
        NetworkError: For all other 4xx / 5xx status codes.
    """
    status = response.status_code
    if status == 429:
        raise RateLimitError(
            f"Rate limit exceeded (HTTP 429) for URL: {response.url}"
        )
    if status in (401, 403):
        raise APIKeyError(
            f"Authentication/authorisation error (HTTP {status}) for URL: {response.url}"
        )
    try:
        response.raise_for_status()
    except Exception as exc:
        raise NetworkError(str(exc)) from exc
