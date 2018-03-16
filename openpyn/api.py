from openpyn import filters
import requests
from ipaddress import IPv4Address
from typing import List

ENDPOINT = 'https://api.nordvpn.com/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
}


def server_info() -> dict:
    '''Return detailed server information.'''
    url = ENDPOINT + 'server'
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    return response.json()


def server_usage(domain=None) -> dict:
    '''Returns server usage for all servers, or the specified server'''
    url = ENDPOINT + 'server/stats{}'.format('/' + domain if domain else '')
    resp = requests.get(url)
    resp.raise_for_status()

    return resp.json()


def ovpn_files() -> bytes:
    '''Returns the bytes representing a zipv2 archive of the .ovpn
    connection configuration files.'''
    url = ENDPOINT + '/files/zipv2'
    resp = requests.get(url)
    resp.raise_for_status()

    return resp.content


def ip_addr_nord() -> IPv4Address:
    '''Get the IP address NordVPN believes you have'''
    url = ENDPOINT + '/user/address'
    resp = requests.get(url)
    resp.raise_for_status()

    return IPv4Address(resp.content.decode(encoding='utf-8'))


def dns_smart() -> List[IPv4Address]:
    '''Returns DNS information from NordVPN'''
    url = ENDPOINT + '/dns/smart'
    resp = requests.get(url)
    resp.raise_for_status()

    return [
        IPv4Address(item)
        for item in resp.json()
    ]




# Gets json data, from api.nordvpn.com. filter servers by type, country, area.
def get_data_from_api(country_code, area, p2p, dedicated, double_vpn, tor_over_vpn, anti_ddos, netflix):
    json_response = server_info()

    type_filtered_servers = filters.filter_by_type(
        json_response, p2p, dedicated, double_vpn, tor_over_vpn, anti_ddos, netflix)
    if country_code != "all":       # if "-l" had country code with it. e.g "-l au"
        type_country_filtered = filters.filter_by_country(country_code, type_filtered_servers)
        if area is None:
            return type_country_filtered
        else:
            type_country_area_filtered = filters.filter_by_area(area, type_country_filtered)
            return type_country_area_filtered
    return type_filtered_servers


def get_countries():
    json_response = server_info()

    countries_mapping = {
        r['flag']: r['country']
        for r in json_response
    }

    return countries_mapping


def get_country_code(country):
    json_response = server_info()
    for res in json_response:
        if res["country"].lower() == country.lower():
            return res['flag']
