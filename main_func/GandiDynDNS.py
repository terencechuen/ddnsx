import requests
import json


class GandiDynDNS:

    def __init__(self, api_key, domain_name, sub_domain):
        self.api_key = api_key
        self.domain_name = domain_name
        self.sub_domain = sub_domain

    def get_domain_records(self):
        url = 'https://dns.api.gandi.net/api/v5/domains/' + self.domain_name + '/records'
        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key
        }
        r = requests.get(url, headers=headers, timeout=30)
        r_content = r.content.decode()
        r_content = json.loads(r_content)

        for i in r_content:
            if i['rrset_name'] == self.sub_domain:
                return i['rrset_values'][0]
            else:
                pass
        return None

    def create_record(self, rr_type, rr_ip):
        url = 'https://dns.api.gandi.net/api/v5/domains/' + self.domain_name + '/records'
        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key
        }
        payload = {
            "rrset_name": self.sub_domain,
            "rrset_type": rr_type,
            "rrset_ttl": 300,
            "rrset_values": [rr_ip]
        }
        r = requests.post(url, data=json.dumps(payload), headers=headers, timeout=30)
        r_content = r.content.decode()
        r_content = json.loads(r_content)
        if r_content['message'] == "DNS Record Created":
            return r_content
        else:
            return r_content

    def update_record(self, rr_type, rr_ip):
        url = 'https://dns.api.gandi.net/api/v5/domains/' + self.domain_name + '/records/' + self.sub_domain + '/' + rr_type

        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key
        }
        payload = {
            "rrset_ttl": 300,
            "rrset_values": [rr_ip]
        }

        r = requests.put(url, data=json.dumps(payload), headers=headers, timeout=30)
        r_content = r.content.decode()
        r_content = json.loads(r_content)
        if r_content['message'] == "DNS Record Created":
            return True
        else:
            return r_content
