from QcloudApi.qcloudapi import QcloudApi
import json


class DnspodDynDNS:

    def __init__(self, secret_id, secret_key, domain_name, sub_domain, rr_type, my_ip):
        self.domain_name = domain_name
        self.sub_domain = sub_domain
        self.rr_type = rr_type
        self.my_ip = my_ip
        self.config = {
            'Region': 'ap-guangzhou',
            'secretId': secret_id,
            'secretKey': secret_key,
            'method': 'GET',
            'SignatureMethod': 'HmacSHA1'
        }

    def get_record_info(self):
        action_params = {
            "domain": self.domain_name,
            "subDomain": self.sub_domain,
            "recordType": self.rr_type
        }
        services = QcloudApi('cns', self.config)
        call_api = services.call('RecordList', action_params)
        get_records = json.loads(call_api.decode())
        get_records = get_records['data']['records']

        if len(get_records) > 0:
            for i in get_records:
                if i['type'] == self.rr_type:
                    return i['value'], i['id']
            return None
        else:
            return None

    def create_record(self):
        action_params = {
            "domain": self.domain_name,
            "subDomain": self.sub_domain,
            "recordType": self.rr_type,
            "recordLine": "默认",
            "value": self.my_ip,
            "ttl": 600
        }
        services = QcloudApi('cns', self.config)
        call_api = services.call('RecordCreate', action_params)
        response_content = json.loads(call_api.decode())

        if response_content['codeDesc'] == "Success":
            return True, response_content['data']['record']['id']
        else:
            return False, response_content

    def update_record(self, rr_id):
        action_params = {
            "domain": self.domain_name,
            "recordId": rr_id,
            "subDomain": self.sub_domain,
            "recordType": self.rr_type,
            "recordLine": "默认",
            "value": self.my_ip,
            "ttl": 600
        }
        services = QcloudApi('cns', self.config)
        call_api = services.call('RecordModify', action_params)
        response_content = json.loads(call_api.decode())

        if response_content['codeDesc'] == "Success":
            return True
        else:
            return response_content
