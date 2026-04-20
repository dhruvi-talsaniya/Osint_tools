import socket
import ssl
import datetime
from typing import Dict, List, Optional, Union

import dns.resolver
import whois


def get_whois_info(domain: str) -> dict:
    """Retrieve WHOIS information for a domain.

    Args:
        domain: The domain name to look up.

    Returns:
        A dict with WHOIS data, or an ``error`` key on failure.
    """
    try:
        w = whois.whois(domain)
        # Convert the whois object to a plain dict for consistency.
        # python-whois may return a WhoisEntry object or a plain dict;
        # handle both by trying .items() and falling back to vars()/dict().
        try:
            items = w.items()
        except AttributeError:
            items = vars(w).items() if hasattr(w, "__dict__") else dict(w).items()

        result = {}
        for key, value in items:
            if isinstance(value, (datetime.datetime, datetime.date)):
                result[key] = value.isoformat()
            elif isinstance(value, list):
                result[key] = [
                    v.isoformat() if isinstance(v, (datetime.datetime, datetime.date)) else v
                    for v in value
                ]
            else:
                result[key] = value
        return result
    except Exception as exc:
        return {"error": str(exc)}


def get_dns_records(domain: str, record_type: str = "A") -> Union[List[str], dict]:
    """Retrieve DNS records for a domain.

    Args:
        domain: The domain name.
        record_type: The DNS record type (e.g. ``'A'``, ``'MX'``, ``'TXT'``).

    Returns:
        A list of record strings, or a dict with an ``error`` key on failure.
    """
    try:
        records = dns.resolver.resolve(domain, record_type)
        return [record.to_text() for record in records]
    except Exception as exc:
        return {"error": str(exc)}


def get_all_dns_records(domain: str) -> dict:
    """Retrieve common DNS record types for a domain.

    Args:
        domain: The domain name.

    Returns:
        A dict mapping record type to a list of record strings.
    """
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]
    results: Dict[str, Union[List[str], dict]] = {}
    for rtype in record_types:
        results[rtype] = get_dns_records(domain, rtype)
    return results


def get_ssl_certificate_info(domain: str, port: int = 443) -> dict:
    """Retrieve SSL/TLS certificate information for a domain.

    Args:
        domain: The domain name.
        port: The port to connect on (default ``443``).

    Returns:
        A dict with certificate details, or an ``error`` key on failure.
    """
    try:
        context = ssl.create_default_context()
        # Enforce TLS 1.2+ to avoid insecure older protocol versions
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        with socket.create_connection((domain, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()

        # Parse relevant fields
        subject = dict(x[0] for x in cert.get("subject", []))
        issuer = dict(x[0] for x in cert.get("issuer", []))
        not_before = cert.get("notBefore", "")
        not_after = cert.get("notAfter", "")
        san = [
            value
            for ext_type, value in cert.get("subjectAltName", [])
            if ext_type == "DNS"
        ]

        return {
            "subject": subject,
            "issuer": issuer,
            "valid_from": not_before,
            "valid_until": not_after,
            "subject_alt_names": san,
            "serial_number": cert.get("serialNumber"),
            "version": cert.get("version"),
        }
    except Exception as exc:
        return {"error": str(exc)}
