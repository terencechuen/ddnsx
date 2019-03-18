import requests


def ipv4():
    ipv4_url = 'https://ipv4.ngx.hk'
    try:
        req = requests.request('GET', ipv4_url)
    except Exception as e:
        return False, e
    else:
        req_content = req.content.decode()
        return True, req_content


def ipv6():
    ipv6_url = 'https://ipv6.ngx.hk/'
    try:
        req = requests.request('GET', ipv6_url)
    except Exception as e:
        return False, e
    else:
        req_content = req.content.decode()
        return True, req_content
