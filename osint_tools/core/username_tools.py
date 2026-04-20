"""Username enumeration across public platforms."""

import requests
from typing import Dict, List, Optional


# Platforms to check. Each entry maps a platform name to a URL template
# where ``{username}`` is replaced with the target username.
PLATFORMS: Dict[str, str] = {
    "GitHub": "https://github.com/{username}",
    "GitLab": "https://gitlab.com/{username}",
    "Twitter": "https://twitter.com/{username}",
    "Instagram": "https://www.instagram.com/{username}/",
    "Reddit": "https://www.reddit.com/user/{username}",
    "Pinterest": "https://www.pinterest.com/{username}/",
    "Twitch": "https://www.twitch.tv/{username}",
    "YouTube": "https://www.youtube.com/@{username}",
    "TikTok": "https://www.tiktok.com/@{username}",
    "Keybase": "https://keybase.io/{username}",
    "HackerNews": "https://news.ycombinator.com/user?id={username}",
    "Dev.to": "https://dev.to/{username}",
    "Medium": "https://medium.com/@{username}",
}


def check_username(
    username: str,
    platforms: Optional[Dict[str, str]] = None,
    timeout: int = 10,
) -> Dict[str, dict]:
    """Check whether a username exists on popular platforms.

    Sends a HEAD request to each platform URL and considers a 200 response
    as "found".  Results may vary as some sites block automated requests.

    Args:
        username: The username to look up.
        platforms: Optional dict of ``{name: url_template}`` to override the
            built-in list.
        timeout: HTTP request timeout in seconds.

    Returns:
        A dict mapping platform name to a result dict containing:
        - ``url``: the profile URL checked
        - ``found``: ``True`` / ``False`` / ``"unknown"``
        - ``status_code``: the HTTP status code returned (or ``None``)
    """
    targets = platforms or PLATFORMS
    results: Dict[str, dict] = {}

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; osint-tools/1.0; "
            "+https://github.com/dhruvi-talsaniya/Osint_tools)"
        )
    }

    for name, url_template in targets.items():
        url = url_template.format(username=username)
        try:
            response = requests.head(
                url, headers=headers, timeout=timeout, allow_redirects=True
            )
            status = response.status_code
            found = status == 200
        except requests.RequestException:
            status = None
            found = "unknown"

        results[name] = {"url": url, "found": found, "status_code": status}

    return results


def get_found_platforms(
    username: str,
    platforms: Optional[Dict[str, str]] = None,
    timeout: int = 10,
) -> List[str]:
    """Return a list of platform names where the username was found.

    Args:
        username: The username to look up.
        platforms: Optional platform override (see :func:`check_username`).
        timeout: HTTP request timeout in seconds.

    Returns:
        A list of platform names where ``found`` is ``True``.
    """
    results = check_username(username, platforms=platforms, timeout=timeout)
    return [name for name, data in results.items() if data.get("found") is True]
