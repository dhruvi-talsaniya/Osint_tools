"""Safe web-scraping utilities."""

import time
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


_DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; osint-tools/1.0; "
        "+https://github.com/dhruvi-talsaniya/Osint_tools)"
    )
}


def fetch_page(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 15,
    delay: float = 0.5,
) -> Optional[str]:
    """Fetch the HTML content of a URL.

    Args:
        url: The URL to fetch.
        headers: Optional custom HTTP headers (merged with the default).
        timeout: Request timeout in seconds.
        delay: Seconds to sleep before the request (basic rate-limiting).

    Returns:
        The response text on success, or ``None`` on failure.
    """
    merged_headers = {**_DEFAULT_HEADERS, **(headers or {})}
    time.sleep(delay)
    try:
        response = requests.get(url, headers=merged_headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def extract_links(html: str, base_url: str = "") -> List[str]:
    """Extract all hyperlinks from an HTML page.

    Args:
        html: Raw HTML string.
        base_url: Base URL for resolving relative links.

    Returns:
        A deduplicated list of absolute URLs found in ``<a href>`` tags.
    """
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        if href.startswith("#") or href.startswith("mailto:"):
            continue
        if base_url and not href.startswith(("http://", "https://")):
            href = urljoin(base_url, href)
        if href.startswith(("http://", "https://")):
            links.add(href)
    return sorted(links)


def extract_text(html: str) -> str:
    """Extract visible text from an HTML page.

    Args:
        html: Raw HTML string.

    Returns:
        Plain text with whitespace normalised.
    """
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "head", "nav", "footer"]):
        tag.decompose()
    text = soup.get_text(separator=" ")
    return " ".join(text.split())


def extract_emails(html: str) -> List[str]:
    """Extract email addresses mentioned in an HTML page.

    Args:
        html: Raw HTML string.

    Returns:
        A deduplicated, sorted list of email addresses.
    """
    import re

    text = extract_text(html)
    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    return sorted(set(re.findall(pattern, text)))


def scrape_page_info(url: str) -> dict:
    """Scrape basic metadata from a web page.

    Args:
        url: The URL to scrape.

    Returns:
        A dict with keys ``title``, ``description``, ``links``, ``emails``,
        and ``text_preview`` (first 500 characters of visible text).
    """
    html = fetch_page(url)
    if html is None:
        return {"error": f"Failed to fetch {url}"}

    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title else ""
    description_tag = soup.find("meta", attrs={"name": "description"})
    description = (
        description_tag.get("content", "").strip() if description_tag else ""
    )
    links = extract_links(html, base_url=url)
    emails = extract_emails(html)
    text = extract_text(html)

    return {
        "url": url,
        "title": title,
        "description": description,
        "links": links[:50],  # return first 50 to keep output manageable
        "emails": emails,
        "text_preview": text[:500],
    }
