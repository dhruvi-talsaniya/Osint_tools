"""Configuration management for OSINT Tools.

Reads settings from:
1. A YAML config file (``config.yaml`` in the current directory, or the path
   given by the ``OSINT_CONFIG`` environment variable).
2. Environment variables (highest priority, override the config file).
"""

import os
from pathlib import Path
from typing import Any, Optional

try:
    import yaml  # type: ignore
    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


_DEFAULTS: dict = {
    "log_level": "INFO",
    "log_file": "osint_tools.log",
    "cache_ttl": 3600,
    "request_timeout": 15,
    "request_retries": 3,
    "rate_limit_delay": 0.5,
    "ipgeolocation_api_key": "",
    "hibp_api_key": "",
}


class ConfigManager:
    """Centralised configuration manager.

    Example::

        cfg = ConfigManager()
        api_key = cfg.get("ipgeolocation_api_key")
    """

    def __init__(self, config_file: Optional[str] = None) -> None:
        self._config: dict = dict(_DEFAULTS)

        # Load YAML config file
        path = config_file or os.environ.get("OSINT_CONFIG", "config.yaml")
        if _YAML_AVAILABLE and Path(path).is_file():
            with open(path, encoding="utf-8") as fh:
                file_cfg = yaml.safe_load(fh) or {}
            self._config.update(file_cfg)

        # Environment variables override everything (case-insensitive keys)
        env_map = {
            "OSINT_LOG_LEVEL": "log_level",
            "OSINT_LOG_FILE": "log_file",
            "OSINT_CACHE_TTL": "cache_ttl",
            "OSINT_REQUEST_TIMEOUT": "request_timeout",
            "OSINT_REQUEST_RETRIES": "request_retries",
            "OSINT_RATE_LIMIT_DELAY": "rate_limit_delay",
            "IPGEOLOCATION_API_KEY": "ipgeolocation_api_key",
            "HIBP_API_KEY": "hibp_api_key",
        }
        # Env vars are strings; cast numeric keys to the appropriate type
        _numeric_int = {"cache_ttl", "request_timeout", "request_retries"}
        _numeric_float = {"rate_limit_delay"}

        for env_key, cfg_key in env_map.items():
            value = os.environ.get(env_key)
            if value is not None:
                if cfg_key in _numeric_int:
                    try:
                        self._config[cfg_key] = int(value)
                    except ValueError:
                        self._config[cfg_key] = value
                elif cfg_key in _numeric_float:
                    try:
                        self._config[cfg_key] = float(value)
                    except ValueError:
                        self._config[cfg_key] = value
                else:
                    self._config[cfg_key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Return a configuration value.

        Args:
            key: The configuration key.
            default: Value to return if the key is not set.

        Returns:
            The configuration value, or *default*.
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Override a configuration value at runtime.

        Args:
            key: The configuration key.
            value: The new value.
        """
        self._config[key] = value

    def all(self) -> dict:
        """Return a copy of all configuration values."""
        return dict(self._config)


# Module-level singleton for convenience
config = ConfigManager()
