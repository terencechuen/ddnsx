import os
import json
from main_func import *

config_file_path = os.getcwd() + '/config.json'

# 尝试读取配置文件
config_json = ''
try:
    o = open(config_file_path, 'r')
except Exception as e:
    print("# 出现错误，以下为错误信息：")
    print(e)
    print("# 程序退出")
    exit(1)
else:
    config_content = o.read()
    config_json = json.loads(config_content)
    service_provider = list(config_json.keys())

my_ipv4 = GetMyIP.ipv4()
my_ipv6 = GetMyIP.ipv6()


def get_my_ip(ip_version):
    if ip_version == 4:
        return my_ipv4
    else:
        return my_ipv6


for i in service_provider:
    if i == "he.net":
        for k in config_json[i]:
            password = k['password']
            full_domain = k['full_domain']
            my_ip = get_my_ip(k['ip_version'])
            print(my_ip)
            req_content = HeDynamicDNS(password, full_domain, my_ip).req_content()
            print(req_content)
