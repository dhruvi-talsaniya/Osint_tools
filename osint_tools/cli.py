"""Command-line interface for OSINT Tools.

Usage::

    osint-tools --help
    osint-tools ip 8.8.8.8
    osint-tools domain example.com
    osint-tools email test@example.com
    osint-tools username johndoe
    osint-tools scrape https://example.com
"""

import json
import sys
from typing import Optional

try:
    import click
except ImportError:  # pragma: no cover
    print(
        "The 'click' package is required for the CLI. "
        "Install it with: pip install click",
        file=sys.stderr,
    )
    sys.exit(1)

from .core.domain_info import (
    get_all_dns_records,
    get_dns_records,
    get_ssl_certificate_info,
    get_whois_info,
)
from .core.email_tools import check_breach, discover_accounts, validate_email
from .core.ip_lookup import get_ip_info, get_ip_isp, get_ip_location
from .core.username_tools import check_username
from .core.web_scraper import scrape_page_info


def _print_result(data, output_format: str = "json") -> None:
    """Print *data* in the requested format."""
    if output_format == "json":
        click.echo(json.dumps(data, indent=2, default=str))
    else:
        # Plain text key=value
        if isinstance(data, dict):
            for key, value in data.items():
                click.echo(f"{key}: {value}")
        elif isinstance(data, list):
            for item in data:
                click.echo(item)
        else:
            click.echo(str(data))


@click.group()
@click.version_option(package_name="osint-tools")
def cli() -> None:
    """OSINT Tools – Open Source Intelligence gathering toolkit."""


# ──────────────────────────────────────────────────────────────────────────────
# IP
# ──────────────────────────────────────────────────────────────────────────────


@cli.command("ip")
@click.argument("ip_address")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "text"]),
    default="json",
    show_default=True,
    help="Output format.",
)
def ip_lookup_cmd(ip_address: str, output_format: str) -> None:
    """Look up geolocation information for an IP address."""
    result = get_ip_info(ip_address)
    _print_result(result, output_format)


# ──────────────────────────────────────────────────────────────────────────────
# Domain
# ──────────────────────────────────────────────────────────────────────────────


@cli.command("domain")
@click.argument("domain")
@click.option("--whois", "do_whois", is_flag=True, default=True, help="Show WHOIS info.")
@click.option("--dns", "do_dns", is_flag=True, default=False, help="Show DNS records.")
@click.option("--ssl", "do_ssl", is_flag=True, default=False, help="Show SSL certificate info.")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "text"]),
    default="json",
    show_default=True,
)
def domain_cmd(
    domain: str, do_whois: bool, do_dns: bool, do_ssl: bool, output_format: str
) -> None:
    """Gather information about a domain (WHOIS, DNS, SSL)."""
    result = {}
    if do_whois:
        result["whois"] = get_whois_info(domain)
    if do_dns:
        result["dns"] = get_all_dns_records(domain)
    if do_ssl:
        result["ssl"] = get_ssl_certificate_info(domain)
    _print_result(result, output_format)


# ──────────────────────────────────────────────────────────────────────────────
# Email
# ──────────────────────────────────────────────────────────────────────────────


@cli.command("email")
@click.argument("email")
@click.option(
    "--breach", is_flag=True, default=False, help="Check Have I Been Pwned."
)
@click.option(
    "--discover", is_flag=True, default=False, help="Attempt account discovery."
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "text"]),
    default="json",
    show_default=True,
)
def email_cmd(email: str, breach: bool, discover: bool, output_format: str) -> None:
    """Validate an email address and optionally check for breaches."""
    result: dict = {"email": email, "valid": validate_email(email)}
    if breach:
        result["breaches"] = check_breach(email)
    if discover:
        result["accounts"] = discover_accounts(email)
    _print_result(result, output_format)


# ──────────────────────────────────────────────────────────────────────────────
# Username
# ──────────────────────────────────────────────────────────────────────────────


@cli.command("username")
@click.argument("username")
@click.option(
    "--found-only",
    is_flag=True,
    default=False,
    help="Only show platforms where the username was found.",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "text"]),
    default="json",
    show_default=True,
)
def username_cmd(username: str, found_only: bool, output_format: str) -> None:
    """Check username availability across popular platforms."""
    results = check_username(username)
    if found_only:
        results = {k: v for k, v in results.items() if v.get("found") is True}
    _print_result(results, output_format)


# ──────────────────────────────────────────────────────────────────────────────
# Web scrape
# ──────────────────────────────────────────────────────────────────────────────


@cli.command("scrape")
@click.argument("url")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "text"]),
    default="json",
    show_default=True,
)
def scrape_cmd(url: str, output_format: str) -> None:
    """Scrape basic metadata from a web page."""
    result = scrape_page_info(url)
    _print_result(result, output_format)


if __name__ == "__main__":
    cli()
