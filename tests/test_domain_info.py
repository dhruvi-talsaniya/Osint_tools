"""Unit tests for osint_tools.core.domain_info (mocked)."""

from unittest.mock import MagicMock, patch

import pytest

from osint_tools.core.domain_info import get_dns_records, get_whois_info


class TestGetWhoisInfo:
    """Tests for :func:`get_whois_info`."""

    def test_returns_dict(self):
        mock_whois = {"domain_name": "EXAMPLE.COM", "registrar": "IANA"}
        with patch("osint_tools.core.domain_info.whois.whois", return_value=mock_whois):
            result = get_whois_info("example.com")

        assert isinstance(result, dict)

    def test_returns_error_on_exception(self):
        with patch(
            "osint_tools.core.domain_info.whois.whois",
            side_effect=Exception("lookup failed"),
        ):
            result = get_whois_info("invalid.example")

        assert "error" in result


class TestGetDnsRecords:
    """Tests for :func:`get_dns_records`."""

    def test_returns_list_of_strings(self):
        mock_record = MagicMock()
        mock_record.to_text.return_value = "93.184.216.34"
        with patch(
            "osint_tools.core.domain_info.dns.resolver.resolve",
            return_value=[mock_record],
        ):
            result = get_dns_records("example.com", "A")

        assert result == ["93.184.216.34"]

    def test_returns_error_dict_on_exception(self):
        import dns.exception

        with patch(
            "osint_tools.core.domain_info.dns.resolver.resolve",
            side_effect=dns.exception.DNSException("NXDOMAIN"),
        ):
            result = get_dns_records("nonexistent.invalid", "A")

        assert isinstance(result, dict)
        assert "error" in result
