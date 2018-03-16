from openpyn import filters
import requests
import sys

ENDPOINT = 'https://api.nordvpn.com/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
}


# Using requests, GETs and returns json from a url.
def server_info():
    url = ENDPOINT + 'server'

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        json_response = response.json()

    except requests.exceptions.HTTPError:
        sys.exit("Cannot GET the json from nordvpn.com, Manually Specify a Server"
                 "using '-s' for example '-s au10'")

    except requests.exceptions.RequestException:
        sys.exit("There was an ambiguous exception, Check Your Network Connection."
                 "forgot to flush iptables? (openpyn -x)")

    return json_response


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
