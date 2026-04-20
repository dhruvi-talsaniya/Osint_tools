import requests


def get_ip_info(ip):
    """Fetches basic information about the given IP address."""
    url = f'https://api.ipgeolocation.io/ipgeo?apiKey=YOUR_API_KEY&ip={ip}'
    response = requests.get(url)
    return response.json()


def get_ip_location(ip):
    """Fetches location information for the given IP address."""
    info = get_ip_info(ip)
    return {'city': info.get('city'), 'country': info.get('country_name')}


def get_ip_isp(ip):
    """Fetches the ISP information for the given IP address."""
    info = get_ip_info(ip)
    return info.get('isp')
