import requests
import re
import json

# Utility functions for HTTP requests, URL validation, JSON formatting, and batch processing

def send_http_request(method, url, data=None, headers=None):
    """Send an HTTP request and return the response."""
    response = requests.request(method, url, json=data, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()


def validate_url(url):
    """Validate a URL using a regular expression."""
    regex = re.compile(r'^(https?://)?([a-z0-9-]+\.)+[a-z]{2,}(/.*)?$')
    return re.match(regex, url) is not None


def format_json(data):
    """Format data as pretty-printed JSON."""
    return json.dumps(data, indent=4)


def batch_process(items, function, *args):
    """Process items in batches using the provided function."""
    results = []
    for item in items:
        results.append(function(item, *args))
    return results
