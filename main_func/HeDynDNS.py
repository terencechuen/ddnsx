import requests


# he.net
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
