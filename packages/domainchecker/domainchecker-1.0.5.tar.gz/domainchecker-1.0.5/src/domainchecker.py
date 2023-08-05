from typing import Dict

import requests
import urllib

ONAMAE_DOMAIN_STATUS_API_ENDPOINT = 'https://www.onamae.com/advanced/?getDomainStatus'


def prepare_data(domain_name: str, domain_list_to_check: list) -> str:
    return urllib.parse.urlencode({
        'domain_name': domain_name
    }) + ''.join([f'&tlds%5B%5D={x}' for x in domain_list_to_check])


def check_domain(domain_name: str, domain_list_to_check: list) -> Dict[str, bool]:
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    data = prepare_data(domain_name, domain_list_to_check)
    response = requests.post(url=ONAMAE_DOMAIN_STATUS_API_ENDPOINT, headers=headers, data=data)

    if not response.status_code == 200:
        raise Exception('request failure')

    response_json = response.json()
    result = {}

    for item in response_json['items']:
        full_domain = item['domain']
        is_available = item['status'] == 1
        result[full_domain] = is_available

    return result