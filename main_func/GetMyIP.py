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
