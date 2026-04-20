"""Unit tests for osint_tools.utils.cache_manager."""

import time

import pytest

from osint_tools.utils.cache_manager import CacheManager


class TestCacheManager:
    """Tests for :class:`CacheManager`."""

    def test_set_and_get(self):
        cache = CacheManager()
        cache.set("key1", {"data": 42})
        assert cache.get("key1") == {"data": 42}

    def test_get_missing_key(self):
        cache = CacheManager()
        assert cache.get("nonexistent") is None

    def test_delete(self):
        cache = CacheManager()
        cache.set("key", "value")
        cache.delete("key")
        assert cache.get("key") is None

    def test_clear(self):
        cache = CacheManager()
        cache.set("a", 1)
        cache.set("b", 2)
        cache.clear()
        assert len(cache) == 0

    def test_expiry(self):
        cache = CacheManager(default_ttl=1)
        cache.set("temp", "gone_soon")
        assert cache.get("temp") == "gone_soon"
        time.sleep(1.1)
        assert cache.get("temp") is None

    def test_no_expiry(self):
        cache = CacheManager(default_ttl=0)
        cache.set("perm", "forever")
        time.sleep(0.1)
        assert cache.get("perm") == "forever"

    def test_contains(self):
        cache = CacheManager()
        cache.set("x", 99)
        assert "x" in cache
        assert "y" not in cache

    def test_purge_expired(self):
        cache = CacheManager(default_ttl=1)
        cache.set("expires", "value")
        cache.set("permanent", "value", ttl=0)
        time.sleep(1.1)
        removed = cache.purge_expired()
        assert removed == 1
        assert cache.get("permanent") == "value"
