import os
import json
import time
from dns import resolver
from main_func.GetMyIP import *

config_file_path = os.getcwd() + '/config.json'
log_file_path = os.getcwd() + '/ddnsx.log'

# 尝试读取配置文件
config_json = ''
try:
    o = open(config_file_path, 'r')
except Exception as e:
    print("# 读取配置文件错误，以下为错误信息：")
    print(e)
    print("# 程序退出")
    exit(1)
else:
    config_content = o.read()
    o.close()
    config_json = json.loads(config_content)

service_provider = list(config_json.keys())

# 获取IPv4的IP地址
my_ipv4 = ipv4()
if my_ipv4[0]:
    my_ipv4 = my_ipv4[1]
else:
    my_ipv4 = False

# 获取IPv6的IP地址
my_ipv6 = ipv6()
if my_ipv6[0]:
    my_ipv6 = my_ipv6[1]
else:
    my_ipv6 = False


def get_my_ip(ip_ver):
    if ip_ver == '4':
        return my_ipv4
    elif ip_ver == '6':
        return my_ipv6


# 比较新旧BI
def compare_ip_with_dig(full_domain, rr_type, ip_now):
    dig_content = resolver.query(full_domain, rr_type)
    if dig_content[0] == ip_now:
        return False
    else:
        return dig_content[0]


# 写日志
def write_to_log(full_domain, newest_ip, rr_type, update_status, output_msg):
    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_content = time_now + ' ' + full_domain + " " + newest_ip + " " + rr_type + " " + update_status + " " + str(
        output_msg) + '\n'
    o_log = open(log_file_path, "a")
    o_log.write(log_content)
    o_log.close()


# 遍历配置文件
for i in service_provider:

    # he.net
    if i == "he.net":
        from main_func.HeDynDNS import *

        for k in config_json[i]:
            password = k['password']
            full_domain = k['full_domain']
            record_type = k['record_type']
            my_ip = get_my_ip(k['ip_version'])

            if compare_ip_with_dig(full_domain, record_type, my_ip) is False:
                pass
            else:
                req_content = he_dyn_dns(password, full_domain, my_ip)
                if req_content:
                    write_to_log(full_domain, my_ip, record_type, "update_success", req_content)
                else:
                    write_to_log(full_domain, my_ip, record_type, "update_fail", req_content)

    # gandi.net
    elif i == "gandi.net":
        from main_func.GandiDynDNS import *

        for k in config_json[i]:
            api_key = k['api_key']
            domain_name = k['domain_name']
            sub_domain = k['sub_domain']
            record_type = k['record_type']
            my_ip = get_my_ip(k['ip_version'])

            gandi_main = GandiDynDNS(api_key, domain_name, sub_domain)

            domain_record = gandi_main.get_domain_records()

            # 若不存在子域名则建立
            if domain_record is None:
                req_content = gandi_main.create_record(record_type, my_ip)
                if req_content:
                    write_to_log(sub_domain + '.' + domain_name, my_ip, record_type, "create_success", '')
                else:
                    write_to_log(sub_domain + '.' + domain_name, my_ip, record_type, "create_fail", req_content)
            # 若子域名的记录与当前IP一直则pass，否则则更新记录
            elif domain_record == my_ip:
                pass
            else:
                req_content = gandi_main.update_record(record_type, my_ip)
                if req_content:
                    write_to_log(sub_domain + '.' + domain_name, my_ip, record_type, "update_success", '')
                else:
                    write_to_log(sub_domain + '.' + domain_name, my_ip, record_type, "update_fail", req_content)

    # godaddy.com
    elif i == "godaddy.com":
        from main_func.GodaddyDynDNS import *

        for k in config_json[i]:
            api_key = k['api_key']
            api_secret = k['api_secret']
            domain_name = k['domain_name']
            sub_domain = k['sub_domain']
            record_type = k['record_type']
            my_ip = get_my_ip(k['ip_version'])

            godaddy_main = GodaddyDynDNS(api_key, api_secret, domain_name, sub_domain, record_type, my_ip)

            domain_record = godaddy_main.get_record()
            # 若子域名的记录与当前IP一直则pass，否则则更新记录
            if domain_record[0]:
                if domain_record[1] == my_ip:
                    pass
                else:
                    req_content = godaddy_main.update_record()
                    if req_content:
                        write_to_log(sub_domain + '.' + domain_name, my_ip, record_type, "update_success", '')
                    else:
                        write_to_log(sub_domain + '.' + domain_name, my_ip, record_type, "update_fail", req_content)
            # 若不存在子域名则建立
            elif domain_record[0] is None:
                req_content = godaddy_main.add_record()
                if req_content:
                    write_to_log(sub_domain + '.' + domain_name, my_ip, record_type, "create_success", '')
                else:
                    write_to_log(sub_domain + '.' + domain_name, my_ip, record_type, "create_fail", req_content)
            else:
                write_to_log(sub_domain + '.' + domain_name, my_ip, record_type, "fail", domain_record[1])


    elif i == "dnspod.cn":
        from main_func.DnspodDynDNS import *

        for k in config_json[i]:
            secret_id = k['secret_id']
            secret_key = k['secret_key']
            domain_name = k['domain_name']
            sub_domain = k['sub_domain']
            record_type = k['record_type']
            my_ip = get_my_ip(k['ip_version'])

            dnspod_main = DnspodDynDNS(secret_id, secret_key, domain_name, sub_domain, record_type, my_ip)

            record_info = dnspod_main.get_record()
            # 若不存在子域名则建立
            if record_info is None:
                req_content = dnspod_main.create_record()
                if req_content[0]:
                    write_to_log(sub_domain + '.' + domain_name, my_ip, record_type, "create_success", '')
                else:
                    write_to_log(sub_domain + '.' + domain_name, my_ip, record_type, "create_fail", req_content[1])
            elif record_info[0] is False:
                write_to_log(sub_domain + '.' + domain_name, my_ip, record_type, "update_fail", record_info[1])
            # 若子域名的记录与当前IP一直则pass，否则则更新记录
            else:
                if record_info[0] == my_ip:
                    continue
                else:
                    req_content = dnspod_main.update_record(record_info[1])
                    if req_content:
                        write_to_log(sub_domain + '.' + domain_name, my_ip, record_type, "update_success", '')
                    else:
                        write_to_log(sub_domain + '.' + domain_name, my_ip, record_type, "update_fail", req_content[1])
