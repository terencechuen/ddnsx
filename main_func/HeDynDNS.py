import requests


def he_dyn_dns(he_passwd, he_domain, my_ip):
    post_url = "https://dyn.dns.he.net/nic/update"
    post_data = {
        "password": he_passwd,
        "hostname": he_domain,
        "myip": my_ip
    }
    req = requests.post(post_url, data=post_data)
    req_content = req.content.decode()
    if req_content == "badauth":
        return req_content
    else:
        req_content_list = req_content.split(' ')
        if req_content_list[0] == "good" or "nochg":
            return True
    return req_content
