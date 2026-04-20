"""OSINT Tools – Open Source Intelligence gathering toolkit.

Quick start::

    from osint_tools.core.ip_lookup import get_ip_info, get_ip_location
    from osint_tools.core.domain_info import get_whois_info, get_dns_records
    from osint_tools.core.email_tools import validate_email, check_breach
    from osint_tools.core.username_tools import check_username
    from osint_tools.core.web_scraper import scrape_page_info
"""

__version__ = "1.0.0"
__author__ = "Dhruvi Talsaniya"

# Re-export the most commonly used functions for convenience
from .core.ip_lookup import get_ip_info, get_ip_location, get_ip_isp
from .core.domain_info import get_whois_info, get_dns_records, get_ssl_certificate_info
from .core.email_tools import validate_email, check_breach
from .core.username_tools import check_username, get_found_platforms
from .core.web_scraper import scrape_page_info

__all__ = [
    # IP
    "get_ip_info",
    "get_ip_location",
    "get_ip_isp",
    # Domain
    "get_whois_info",
    "get_dns_records",
    "get_ssl_certificate_info",
    # Email
    "validate_email",
    "check_breach",
    # Username
    "check_username",
    "get_found_platforms",
    # Web scraping
    "scrape_page_info",
]
