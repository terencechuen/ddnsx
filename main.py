import os
import json
from main_func.GetMyIP import *

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
        from main_func.HeDynDNS import *

        for k in config_json[i]:
            password = k['password']
            full_domain = k['full_domain']
            my_ip = get_my_ip(k['ip_version'])

            req_content = HeDynamicDNS(password, full_domain, my_ip).req_content()

    elif i == "gandi.net":
        from main_func.GandiDynDNS import *

        for k in config_json[i]:
            api_key = k['api_key']
            domain_name = k['domain_name']
            sub_domain = k['sub_domain']
            record_type = k['record_type']
            my_ip = get_my_ip(k['ip_version'])

            get_info_main = GandiGetInfo(api_key, domain_name)
            modify_main = GandiModifyRecord(api_key, domain_name, sub_domain)

            chk_domain = get_info_main.chk_domain()

            if chk_domain:
                domain_records = get_info_main.get_domain_records(sub_domain)
            else:
                print('域名不存在')
                continue

            if domain_records is None:
                add_record = modify_main.add_record(record_type, my_ip)
            elif domain_records == my_ipv4:
                print('same')
            else:
                update_record = modify_main.update_record(record_type, my_ip)
                print(update_record)
