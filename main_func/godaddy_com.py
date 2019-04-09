import requests
import json
import sys

input_content = sys.argv[1]
input_content = json.loads(input_content)


def get_record(api_key, api_secret, domain_name, sub_domain, rr_type):
    url = 'https://api.godaddy.com/v1/domains/' + domain_name + '/records/' + rr_type + '/' + sub_domain
    headers = {
        "Content-Type": "application/json",
        "Authorization": "sso-key " + api_key + ":" + api_secret
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


def add_record(api_key, api_secret, domain_name, sub_domain, rr_type, myip):
    url = 'https://api.godaddy.com/v1/domains/' + domain_name + '/records'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "sso-key " + api_key + ":" + api_secret
    }
    payload = [
        {
            "name": sub_domain,
            "data": myip,
            "ttl": 600,
            "type": rr_type
        }
    ]

    r = requests.patch(url, data=json.dumps(payload), headers=headers)
    if r.status_code is 200:
        return True, r.content.decode()
    else:
        return False, r.content.decode()


def update_record(api_key, api_secret, domain_name, sub_domain, rr_type, myip):
    url = 'https://api.godaddy.com/v1/domains/' + domain_name + '/records/' + rr_type + '/' + sub_domain
    headers = {
        "Content-Type": "application/json",
        "Authorization": "sso-key " + api_key + ":" + api_secret
    }
    payload = [
        {
            "data": myip,
            "ttl": 600,
        }
    ]

    r = requests.put(url, data=json.dumps(payload), headers=headers)
    if r.status_code is 200:
        return True, r.content.decode()
    else:
        return False, r.content.decode()


def run():
    api_key = input_content['api_key']
    api_secret = input_content['api_secret']
    domain_name = input_content['domain_name']
    sub_domain = input_content['sub_domain']
    record_type = input_content['record_type']
    myip = input_content['myip']

    get_domain_record = get_record(api_key, api_secret, domain_name, sub_domain, record_type)

    # 若子域名的记录与当前IP一直则pass，否则则更新记录
    if get_domain_record[0]:
        if get_domain_record[1] == myip:
            req_content = False, "IP地址与DNS记录一致"
        else:
            req_content = update_record(api_key, api_secret, domain_name, sub_domain, record_type, myip)
    # 若不存在子域名则建立
    elif get_domain_record[0] is None:
        req_content = add_record(api_key, api_secret, domain_name, sub_domain, record_type, myip)
    else:
        req_content = get_domain_record

    output_content = {
        "update_status": req_content[0],
        "content": req_content[1]
    }

    return json.dumps(output_content)


if __name__ == "__main__":
    print(run())
