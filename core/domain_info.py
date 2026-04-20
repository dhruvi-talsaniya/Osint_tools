import whois
import dns.resolver

def get_whois_info(domain):
    """Retrieve WHOIS information for a given domain."""
    try:
        return whois.whois(domain)
    except Exception as e:
        return str(e)


def get_dns_records(domain, record_type='A'):
    """Retrieve DNS records for a given domain."""
    try:
        records = dns.resolver.resolve(domain, record_type)
        return [record.to_text() for record in records]
    except Exception as e:
        return str(e)
