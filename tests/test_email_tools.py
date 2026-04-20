"""Unit tests for osint_tools.core.email_tools."""

import pytest
from osint_tools.core.email_tools import validate_email


class TestValidateEmail:
    """Tests for :func:`validate_email`."""

    @pytest.mark.parametrize(
        "email",
        [
            "user@example.com",
            "first.last@subdomain.example.co.uk",
            "user+tag@example.org",
            "user123@domain.io",
        ],
    )
    def test_valid_emails(self, email):
        assert validate_email(email) is True

    @pytest.mark.parametrize(
        "email",
        [
            "notanemail",
            "missing@dot",
            "@nodomain.com",
            "spaces in@domain.com",
            "",
        ],
    )
    def test_invalid_emails(self, email):
        assert validate_email(email) is False
