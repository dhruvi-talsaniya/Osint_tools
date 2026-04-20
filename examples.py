"""Usage examples for OSINT Tools.

Run individual sections by invoking this script:
    python examples.py
"""

from osint_tools.core.ip_lookup import get_ip_info, get_ip_location, get_ip_isp
from osint_tools.core.domain_info import (
    get_whois_info,
    get_dns_records,
    get_all_dns_records,
    get_ssl_certificate_info,
)
from osint_tools.core.email_tools import validate_email
from osint_tools.core.username_tools import get_found_platforms
from osint_tools.utils.helpers import format_json, batch_process, validate_url
from osint_tools.utils.cache_manager import CacheManager


# ─────────────────────────────────────────────
# IP Lookup
# ─────────────────────────────────────────────
print("=" * 60)
print("IP LOOKUP")
print("=" * 60)

ip = "8.8.8.8"
info = get_ip_info(ip)
print(f"Info for {ip}:")
print(format_json(info))

location = get_ip_location(ip)
print(f"\nLocation: {location}")

isp = get_ip_isp(ip)
print(f"ISP: {isp}")


# ─────────────────────────────────────────────
# Domain Information
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("DOMAIN INFORMATION")
print("=" * 60)

domain = "example.com"

whois_info = get_whois_info(domain)
print(f"\nWHOIS for {domain}:")
print(format_json(whois_info))

dns_a = get_dns_records(domain, "A")
print(f"\nA records: {dns_a}")

ssl_info = get_ssl_certificate_info(domain)
print(f"\nSSL certificate info:")
print(format_json(ssl_info))


# ─────────────────────────────────────────────
# Email Tools
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("EMAIL VALIDATION")
print("=" * 60)

emails = ["user@example.com", "invalid-email", "test@domain.co.uk"]
for email in emails:
    valid = validate_email(email)
    print(f"  {email!r:35s} -> {'valid' if valid else 'invalid'}")


# ─────────────────────────────────────────────
# Batch Processing
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("BATCH PROCESSING")
print("=" * 60)

results = batch_process(emails, validate_email)
for email, result in zip(emails, results):
    print(f"  {email}: {result}")


# ─────────────────────────────────────────────
# Cache Manager
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("CACHE MANAGER")
print("=" * 60)

cache = CacheManager(default_ttl=60)
cache.set("my_ip_result", {"city": "London"})
cached = cache.get("my_ip_result")
print(f"Cached value: {cached}")
print(f"Cache size: {len(cache)}")


# ─────────────────────────────────────────────
# URL Validation
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("URL VALIDATION")
print("=" * 60)

urls = ["https://example.com", "not-a-url", "http://sub.domain.org/path?q=1"]
for url in urls:
    print(f"  {url!r:45s} -> {validate_url(url)}")
