"""Unit tests for osint_tools.utils.helpers."""

import pytest

from osint_tools.utils.helpers import batch_process, format_json, validate_url


class TestValidateUrl:
    @pytest.mark.parametrize(
        "url",
        [
            "http://example.com",
            "https://example.com/path?q=1",
            "https://sub.domain.co.uk/path",
        ],
    )
    def test_valid_urls(self, url):
        assert validate_url(url) is True

    @pytest.mark.parametrize(
        "url",
        [
            "not-a-url",
            "ftp://example.com",
            "example.com",
            "",
        ],
    )
    def test_invalid_urls(self, url):
        assert validate_url(url) is False


class TestFormatJson:
    def test_formats_dict(self):
        result = format_json({"key": "value"})
        assert '"key": "value"' in result

    def test_handles_non_serialisable(self):
        import datetime

        result = format_json({"ts": datetime.date(2024, 1, 1)})
        assert "2024-01-01" in result


class TestBatchProcess:
    def test_applies_function_to_all_items(self):
        result = batch_process([1, 2, 3], lambda x: x * 2)
        assert result == [2, 4, 6]

    def test_passes_extra_args(self):
        result = batch_process([10, 20], lambda x, y: x + y, 5)
        assert result == [15, 25]
