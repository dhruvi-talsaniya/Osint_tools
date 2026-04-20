"""Simple in-memory cache with TTL support."""

import time
from typing import Any, Optional


class CacheManager:
    """Thread-unsafe, in-memory key/value cache with time-to-live expiry.

    Example::

        cache = CacheManager(default_ttl=300)
        cache.set("my_key", {"data": 1})
        value = cache.get("my_key")   # returns the dict
        cache.delete("my_key")
        cache.clear()

    Args:
        default_ttl: Default number of seconds before an entry expires.
            Use ``0`` or a negative value for entries that never expire.
    """

    def __init__(self, default_ttl: int = 3600) -> None:
        self._store: dict = {}
        self.default_ttl = default_ttl

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store *value* under *key*.

        Args:
            key: Cache key.
            value: Value to store (any Python object).
            ttl: Seconds until expiry.  Defaults to :attr:`default_ttl`.
                 Use ``0`` or negative for no expiry.
        """
        expires_at = None
        effective_ttl = ttl if ttl is not None else self.default_ttl
        if effective_ttl and effective_ttl > 0:
            expires_at = time.monotonic() + effective_ttl
        self._store[key] = {"value": value, "expires_at": expires_at}

    def get(self, key: str) -> Optional[Any]:
        """Retrieve *key* from the cache.

        Args:
            key: Cache key.

        Returns:
            The stored value, or ``None`` if the key is absent or expired.
        """
        entry = self._store.get(key)
        if entry is None:
            return None
        if entry["expires_at"] is not None and time.monotonic() > entry["expires_at"]:
            del self._store[key]
            return None
        return entry["value"]

    def delete(self, key: str) -> None:
        """Remove *key* from the cache (no-op if absent).

        Args:
            key: Cache key.
        """
        self._store.pop(key, None)

    def clear(self) -> None:
        """Remove all entries from the cache."""
        self._store.clear()

    def purge_expired(self) -> int:
        """Delete all expired entries.

        Returns:
            The number of entries removed.
        """
        now = time.monotonic()
        expired = [
            k
            for k, v in self._store.items()
            if v["expires_at"] is not None and now > v["expires_at"]
        ]
        for key in expired:
            del self._store[key]
        return len(expired)

    def __len__(self) -> int:
        return len(self._store)

    def __contains__(self, key: str) -> bool:
        return self.get(key) is not None


# Module-level default cache instance
cache = CacheManager()
