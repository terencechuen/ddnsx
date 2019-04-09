import requests
import sys
import json

input_content = sys.argv[1]
input_content = json.loads(input_content)


def he_dyn_dns(he_passwd, he_domain, ip):
    post_url = "https://dyn.dns.he.net/nic/update"
    post_data = {
        "password": he_passwd,
        "hostname": he_domain,
        "myip": ip
    }
    req = requests.post(post_url, data=post_data)
    req_content = req.content.decode()
    if req_content == "badauth" or "nochg":
        return False, req_content
    else:
        req_content_list = req_content.split(' ')
        if req_content_list[0] == "good":
            return True, req_content
    return False, req_content


def run():
    password = input_content['password']
    full_domain = input_content['full_domain']
    myip = input_content['myip']

    output_content = he_dyn_dns(password, full_domain, myip)
    output_content = {
        "update_status": output_content[0],
        "content": output_content[1]
    }
    return json.dumps(output_content)


if __name__ == "__main__":
    print(run())
