from QcloudApi.qcloudapi import QcloudApi
import json
import sys

input_content = sys.argv[1]
input_content = json.loads(input_content)


def get_record(config, domain_name, sub_domain, rr_type):
    action_params = {
        "domain": domain_name,
        "subDomain": sub_domain,
        "recordType": rr_type
    }
    services = QcloudApi('cns', config)
    call_api = services.call('RecordList', action_params)
    get_records = json.loads(call_api.decode())

    if get_records["codeDesc"] == "Success":
        get_records = get_records['data']['records']
        if len(get_records) == 0:
            return None, None
        else:
            return get_records[0]['value'], get_records[0]['id']
    else:
        return False, get_records


def create_record(config, domain_name, sub_domain, rr_type, myip):
    action_params = {
        "domain": domain_name,
        "subDomain": sub_domain,
        "recordType": rr_type,
        "recordLine": "默认",
        "value": myip,
        "ttl": 600
    }
    services = QcloudApi('cns', config)
    call_api = services.call('RecordCreate', action_params)
    response_content = json.loads(call_api.decode())

    if response_content['codeDesc'] == "Success":
        return True, response_content
    else:
        return False, response_content


def update_record(config, domain_name, sub_domain, rr_type, myip, rr_id):
    action_params = {
        "domain": domain_name,
        "recordId": rr_id,
        "subDomain": sub_domain,
        "recordType": rr_type,
        "recordLine": "默认",
        "value": myip,
        "ttl": 600
    }
    services = QcloudApi('cns', config)
    call_api = services.call('RecordModify', action_params)
    response_content = json.loads(call_api.decode())

    if response_content['codeDesc'] == "Success":
        return True, response_content
    else:
        return False, response_content


def run():
    secret_id = input_content['secret_id']
    secret_key = input_content['secret_key']
    domain_name = input_content['domain_name']
    sub_domain = input_content['sub_domain']
    record_type = input_content['record_type']
    myip = input_content['myip']

    config = {
        'Region': 'ap-guangzhou',
        'secretId': secret_id,
        'secretKey': secret_key,
        'method': 'GET',
        'SignatureMethod': 'HmacSHA1'
    }

    record_info = get_record(config, domain_name, sub_domain, record_type)

    # 若不存在子域名则建立
    if record_info[0] is None:
        req_content = create_record(config, domain_name, sub_domain, record_type, myip)
    # API调用失败
    elif record_info[0] is False:
        req_content = record_info
    # 若子域名的记录与当前IP一直则pass，否则则更新记录
    else:
        if record_info[0] == myip:
            req_content = False, "IP地址与DNS记录一致"
        else:
            req_content = update_record(config, domain_name, sub_domain, record_type, myip, record_info[1])

    output_content = {
        "update_status": req_content[0],
        "content": req_content[1]
    }

    return json.dumps(output_content)


if __name__ == "__main__":
    print(run())
