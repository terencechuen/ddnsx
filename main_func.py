import requests


# get public network ip
class GetMyIP:

    @staticmethod
    def ipv4():
        ipv4 = 'https://ipv4.ngx.hk'
        try:
            req = requests.request('GET', ipv4)
        except Exception as e:
            return e
        else:
            req_content = req.content.decode()
            return req_content

    @staticmethod
    def ipv6():
        ipv6 = 'https://ipv6.ngx.hk/'
        try:
            req = requests.request('GET', ipv6)
        except Exception as e:
            return e
        else:
            req_content = req.content.decode()
            return req_content


# HE DDNS
class HeDynamicDNS:

    def __init__(self, password, domain, ip):
        self.password = password
        self.domain = domain
        self.ip = ip

    def req_content(self):
        post_url = "https://dyn.dns.he.net/nic/update"
        post_data = {
            "password": self.password,
            "hostname": self.domain,
            "myip": self.ip
        }
        req = requests.post(post_url, data=post_data)
        req_content = req.content.decode()
        return req_content

# namecheap
