"""Unit tests for osint_tools.core.ip_lookup (mocked)."""

from unittest.mock import MagicMock, patch

import pytest

from osint_tools.core.ip_lookup import get_ip_info, get_ip_isp, get_ip_location


class TestGetIpInfo:
    """Tests for :func:`get_ip_info`."""

    def test_returns_dict_on_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "city": "Mountain View",
            "country": "United States",
            "isp": "Google LLC",
            "query": "8.8.8.8",
        }
        mock_response.raise_for_status = MagicMock()

        with patch("osint_tools.core.ip_lookup.requests.get", return_value=mock_response):
            result = get_ip_info("8.8.8.8")

        assert isinstance(result, dict)
        assert result["city"] == "Mountain View"
        assert result["isp"] == "Google LLC"

    def test_returns_error_on_network_failure(self):
        import requests as req

        with patch(
            "osint_tools.core.ip_lookup.requests.get",
            side_effect=req.RequestException("timeout"),
        ):
            result = get_ip_info("8.8.8.8")

        assert "error" in result


class TestGetIpLocation:
    """Tests for :func:`get_ip_location`."""

    def test_extracts_city_and_country(self):
        with patch(
            "osint_tools.core.ip_lookup.get_ip_info",
            return_value={"city": "London", "country": "United Kingdom"},
        ):
            loc = get_ip_location("1.2.3.4")

        assert loc["city"] == "London"
        assert loc["country"] == "United Kingdom"


class TestGetIpIsp:
    """Tests for :func:`get_ip_isp`."""

    def test_returns_isp_string(self):
        with patch(
            "osint_tools.core.ip_lookup.get_ip_info",
            return_value={"isp": "Cloudflare, Inc."},
        ):
            isp = get_ip_isp("1.1.1.1")

        assert isp == "Cloudflare, Inc."

    def test_falls_back_to_org(self):
        with patch(
            "osint_tools.core.ip_lookup.get_ip_info",
            return_value={"org": "AS15169 Google LLC"},
        ):
            isp = get_ip_isp("8.8.8.8")

        assert isp == "AS15169 Google LLC"
