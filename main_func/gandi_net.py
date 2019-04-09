import requests
import json
import sys

input_content = sys.argv[1]
input_content = json.loads(input_content)


def get_domain_records(api_key, domain_name, sub_domain):
    url = 'https://dns.api.gandi.net/api/v5/domains/' + domain_name + '/records'
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": api_key
    }
    r = requests.get(url, headers=headers, timeout=30)
    r_content = r.content.decode()
    r_content = json.loads(r_content)

    for i in r_content:
        if i['rrset_name'] == sub_domain:
            return i['rrset_values'][0]
        else:
            return None


def create_record(api_key, domain_name, sub_domain, rr_type, myip):
    url = 'https://dns.api.gandi.net/api/v5/domains/' + domain_name + '/records'
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": api_key
    }
    payload = {
        "rrset_name": sub_domain,
        "rrset_type": rr_type,
        "rrset_ttl": 300,
        "rrset_values": [myip]
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers, timeout=30)
    r_content = r.content.decode()
    r_content_msg = json.loads(r_content)['message']
    if r_content_msg == "DNS Record Created":
        return True, r_content_msg
    else:
        return False, r_content_msg


def update_record(api_key, domain_name, sub_domain, rr_type, myip):
    url = 'https://dns.api.gandi.net/api/v5/domains/' + domain_name + '/records/' + sub_domain + '/' + rr_type

    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": api_key
    }
    payload = {
        "rrset_ttl": 300,
        "rrset_values": [myip]
    }

    r = requests.put(url, data=json.dumps(payload), headers=headers, timeout=30)
    r_content = r.content.decode()
    r_content_msg = json.loads(r_content)['message']
    if r_content_msg == "DNS Record Created":
        return True, r_content_msg
    else:
        return False, r_content_msg


def run():
    myip = input_content['myip']
    api_key = input_content['api_key']
    domain_name = input_content['domain_name']
    sub_domain = input_content['sub_domain']
    rr_type = input_content['record_type']

    get_domain_record = get_domain_records(api_key, domain_name, sub_domain)
    if get_domain_record is None:
        req_content = create_record(api_key, domain_name, sub_domain, rr_type, myip)
    elif get_domain_record == myip:
        req_content = False, "IP地址与DNS记录一致"
    else:
        req_content = update_record(api_key, domain_name, sub_domain, rr_type, myip)

    output_content = {
        "update_status": req_content[0],
        "content": req_content[1]
    }

    return json.dumps(output_content)


if __name__ == "__main__":
    print(run())
