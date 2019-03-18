import requests
import json


class GodaddyDynDNS:

    def __init__(self, api_key, api_secret, domain_name, sub_domain, rr_type, my_ip):
        self.api_key = api_key
        self.api_secret = api_secret
        self.domain_name = domain_name
        self.sub_domain = sub_domain
        self.rr_type = rr_type
        self.my_ip = my_ip

    def get_record(self):
        url = 'https://api.godaddy.com/v1/domains/' + self.domain_name + '/records/' + self.rr_type + '/' + self.sub_domain
        headers = {
            "Content-Type": "application/json",
            "Authorization": "sso-key " + self.api_key + ":" + self.api_secret
        }
        r = requests.get(url, headers=headers)
        r_content = r.content.decode()
        r_content = json.loads(r_content)

        if r.status_code is 200:
            if len(r_content) == 0:
                return None, None
            else:
                return True, r_content[0]["data"]
        else:
            return False, r_content

    def add_record(self):
        url = 'https://api.godaddy.com/v1/domains/' + self.domain_name + '/records'
        headers = {
            "Content-Type": "application/json",
            "Authorization": "sso-key " + self.api_key + ":" + self.api_secret
        }
        payload = [
            {
                "name": self.sub_domain,
                "data": self.my_ip,
                "ttl": 600,
                "type": self.rr_type
            }
        ]

        r = requests.patch(url, data=json.dumps(payload), headers=headers)
        if r.status_code is 200:
            return True
        else:
            return r.content.decode()

    def update_record(self):
        url = 'https://api.godaddy.com/v1/domains/' + self.domain_name + '/records/' + self.rr_type + '/' + self.sub_domain
        headers = {
            "Content-Type": "application/json",
            "Authorization": "sso-key " + self.api_key + ":" + self.api_secret
        }
        payload = [
            {
                "data": self.my_ip,
                "ttl": 600,
            }
        ]

        r = requests.put(url, data=json.dumps(payload), headers=headers)
        print(r.content.decode())
        if r.status_code is 200:
            return True
        else:
            return r.content.decode()
