import os
import requests

# Optional: load from environment if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def get_ip_info(ip: str) -> dict:
    """Fetch geolocation information for an IP address.

    Uses the ip-api.com free endpoint first, then falls back to
    ipgeolocation.io if an API key is provided via the
    ``IPGEOLOCATION_API_KEY`` environment variable.

    Args:
        ip: The IP address to look up.

    Returns:
        A dictionary with geolocation data or an ``error`` key on failure.
    """
    # Primary: free ip-api.com (no key required, 45 req/min on free tier)
    try:
        url = (
            f"http://ip-api.com/json/{ip}"
            "?fields=status,message,country,countryCode,region,regionName,"
            "city,zip,lat,lon,timezone,isp,org,as,query"
        )
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            return data
    except requests.RequestException:
        pass

    # Fallback: ipgeolocation.io (requires API key)
    api_key = os.environ.get("IPGEOLOCATION_API_KEY", "")
    if api_key:
        try:
            url = f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            return {"error": str(exc)}

    return {"error": "IP lookup failed and no IPGEOLOCATION_API_KEY configured."}


def get_ip_location(ip: str) -> dict:
    """Return the city and country for an IP address.

    Args:
        ip: The IP address to look up.

    Returns:
        A dict with ``city`` and ``country`` keys.
    """
    info = get_ip_info(ip)
    return {
        "city": info.get("city"),
        "country": info.get("country") or info.get("country_name"),
    }


def get_ip_isp(ip: str) -> str:
    """Return the ISP name for an IP address.

    Args:
        ip: The IP address to look up.

    Returns:
        The ISP name string, or an empty string on failure.
    """
    info = get_ip_info(ip)
    return info.get("isp") or info.get("org") or ""
