"""Unified HTTP request handler with retries, rate limiting, and proxy support."""

import time
from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .error_handlers import handle_http_error


def _build_session(retries: int = 3, backoff_factor: float = 0.5) -> requests.Session:
    """Build a :class:`requests.Session` with retry logic.

    Args:
        retries: Number of times to retry on transient failures.
        backoff_factor: Backoff multiplier between retries.

    Returns:
        A configured :class:`requests.Session`.
    """
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST", "HEAD"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


class RequestHandler:
    """Centralised HTTP client for OSINT Tools.

    Supports retries, rate limiting (delay between requests), proxy
    configuration, and consistent error handling.

    Args:
        timeout: Default request timeout in seconds.
        retries: Number of retry attempts on transient errors.
        rate_limit_delay: Minimum seconds between consecutive requests.
        proxies: Optional dict mapping protocol to proxy URL, e.g.
            ``{"http": "http://proxy:8080", "https": "http://proxy:8080"}``.
        headers: Default headers merged into every request.
    """

    def __init__(
        self,
        timeout: int = 15,
        retries: int = 3,
        rate_limit_delay: float = 0.5,
        proxies: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self.timeout = timeout
        self.rate_limit_delay = rate_limit_delay
        self.proxies = proxies or {}
        self._default_headers: Dict[str, str] = {
            "User-Agent": "osint-tools/1.0 (+https://github.com/dhruvi-talsaniya/Osint_tools)",
            **(headers or {}),
        }
        self._session = _build_session(retries=retries)
        self._last_request_time: float = 0.0

    def _throttle(self) -> None:
        """Sleep if necessary to honour the rate-limit delay."""
        elapsed = time.monotonic() - self._last_request_time
        wait = self.rate_limit_delay - elapsed
        if wait > 0:
            time.sleep(wait)
        self._last_request_time = time.monotonic()

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        raise_on_error: bool = True,
    ) -> requests.Response:
        """Send an HTTP GET request.

        Args:
            url: The URL to request.
            params: Optional query-string parameters.
            headers: Extra headers (merged with defaults).
            raise_on_error: When ``True`` (default), raises an
                :class:`~osint_tools.utils.error_handlers.OsintToolsError`
                subclass on non-2xx responses.

        Returns:
            The :class:`requests.Response` object.
        """
        self._throttle()
        merged_headers = {**self._default_headers, **(headers or {})}
        response = self._session.get(
            url,
            params=params,
            headers=merged_headers,
            timeout=self.timeout,
            proxies=self.proxies,
        )
        if raise_on_error:
            handle_http_error(response)
        return response

    def post(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        raise_on_error: bool = True,
    ) -> requests.Response:
        """Send an HTTP POST request.

        Args:
            url: The URL to request.
            data: Form-encoded body data.
            json: JSON-serialisable body (mutually exclusive with *data*).
            headers: Extra headers (merged with defaults).
            raise_on_error: Raise on non-2xx responses when ``True``.

        Returns:
            The :class:`requests.Response` object.
        """
        self._throttle()
        merged_headers = {**self._default_headers, **(headers or {})}
        response = self._session.post(
            url,
            data=data,
            json=json,
            headers=merged_headers,
            timeout=self.timeout,
            proxies=self.proxies,
        )
        if raise_on_error:
            handle_http_error(response)
        return response

    def close(self) -> None:
        """Close the underlying :class:`requests.Session`."""
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
