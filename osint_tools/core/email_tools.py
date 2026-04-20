import hashlib
import os
import re
from typing import Optional

import requests


def validate_email(email: str) -> bool:
    """Validate an email address using a regular expression.

    Args:
        email: The email address to validate.

    Returns:
        ``True`` if the email looks valid, ``False`` otherwise.
    """
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(regex, email))


def check_breach(email: str, api_key: Optional[str] = None) -> Optional[list]:
    """Check whether an email has appeared in known data breaches.

    Queries the Have I Been Pwned v3 API.  A ``hibp-api-key`` is required
    for the ``/breachedaccount`` endpoint – pass it explicitly or set the
    ``HIBP_API_KEY`` environment variable.

    Args:
        email: The email address to check.
        api_key: Optional HIBP API key (overrides the environment variable).

    Returns:
        A list of breach dicts if the account was found, ``None`` if not
        found, or a dict with an ``error`` key on failure.
    """
    key = api_key or os.environ.get("HIBP_API_KEY", "")
    headers = {"User-Agent": "osint-tools/1.0"}
    if key:
        headers["hibp-apikey"] = key

    try:
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 404:
            return None
        response.raise_for_status()
    except requests.RequestException as exc:
        return {"error": str(exc)}  # type: ignore[return-value]

    return None


def discover_accounts(email: str) -> dict:
    """Attempt basic account discovery for an email address.

    Checks several public sources that may expose whether an email is
    registered.  This is a best-effort, unauthenticated check and results
    are not guaranteed.

    Args:
        email: The email address to search for.

    Returns:
        A dict mapping platform name to ``True`` / ``False`` / ``"unknown"``.
    """
    results: dict = {}

    # Gravatar requires MD5 of the email address per their API specification.
    # MD5 is used here solely for the Gravatar lookup, not for security purposes.
    email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()  # noqa: S324
    try:
        r = requests.get(
            f"https://www.gravatar.com/{email_hash}.json",
            timeout=8,
            allow_redirects=False,
        )
        results["gravatar"] = r.status_code == 200
    except requests.RequestException:
        results["gravatar"] = "unknown"

    return results
