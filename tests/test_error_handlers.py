"""Unit tests for osint_tools.utils.error_handlers."""

import pytest
from unittest.mock import MagicMock

from osint_tools.utils.error_handlers import (
    APIKeyError,
    NetworkError,
    OsintToolsError,
    RateLimitError,
    ValidationError,
    handle_http_error,
)


class TestExceptionHierarchy:
    def test_all_inherit_from_base(self):
        for exc_class in (NetworkError, RateLimitError, APIKeyError, ValidationError):
            assert issubclass(exc_class, OsintToolsError)


class TestHandleHttpError:
    def _mock_response(self, status_code: int, url: str = "http://example.com"):
        resp = MagicMock()
        resp.status_code = status_code
        resp.url = url
        return resp

    def test_raises_rate_limit_error_on_429(self):
        resp = self._mock_response(429)
        with pytest.raises(RateLimitError):
            handle_http_error(resp)

    def test_raises_api_key_error_on_401(self):
        resp = self._mock_response(401)
        with pytest.raises(APIKeyError):
            handle_http_error(resp)

    def test_raises_api_key_error_on_403(self):
        resp = self._mock_response(403)
        with pytest.raises(APIKeyError):
            handle_http_error(resp)

    def test_raises_network_error_on_500(self):
        resp = self._mock_response(500)
        resp.raise_for_status.side_effect = Exception("server error")
        with pytest.raises(NetworkError):
            handle_http_error(resp)

    def test_does_not_raise_on_200(self):
        resp = self._mock_response(200)
        resp.raise_for_status = MagicMock()  # no-op
        # Should not raise
        handle_http_error(resp)
