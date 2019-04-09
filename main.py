import os
import json
import time
import subprocess
from dns import resolver
from main_func.GetMyIP import *

script_path = os.getcwd()
config_file_path = script_path + '/config.json'
log_file_path = script_path + '/ddnsx.log'

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


# 比较新旧IP
def compare_ip_with_dig(full_domain, rr_type, ip_now):
    dig_content = resolver.query(full_domain, rr_type)
    if dig_content[0] == ip_now:
        return False
    else:
        return dig_content[0]


# 写日志
def write_to_log(domain, ip, rr_type, req_status, msg, service_provider):
    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_content = time_now + ' ' + service_provider + ' ' + domain + ' ' + str(
        ip) + ' ' + rr_type + ' ' + req_status + ' ' + msg + '\n'
    o_log = open(log_file_path, "a")
    o_log.write(log_content)
    o_log.close()


def run():
    # 遍历配置文件
    for service_provider, config_list in config_json.items():
        func_filename = service_provider.replace(".", "_") + ".py"
        for i in config_list:
            domain_name = i['domain_name']
            sub_domain = i['sub_domain']
            full_domain = sub_domain + '.' + domain_name
            record_type = i['record_type']

            # 获取IP地址
            if i["ip_version"] == "4":
                myip = ipv4()
            else:
                myip = ipv6()

            # 获取IP地址失败
            if myip[0]:
                myip = myip[1]
            else:
                write_to_log(full_domain, myip, record_type, "get_ip_fail", "获取本地公网IP失败", service_provider)
                continue

            # 与DNS解析比对IP地址
            if compare_ip_with_dig(full_domain, record_type, myip) is False:
                pass
            else:
                i["myip"] = myip
                req_content = subprocess.Popen(["python3", script_path + '/main_func/' + func_filename, json.dumps(i)],
                                               stdout=subprocess.PIPE)
                req_content = req_content.communicate()[0].decode()
                print(req_content)
                req_content_json = json.loads(req_content)
                if req_content_json["update_status"]:
                    write_to_log(full_domain, myip, record_type, "update_success", req_content_json["content"],
                                 service_provider)
                else:
                    write_to_log(full_domain, myip, record_type, "update_fail", req_content_json["content"],
                                 service_provider)


if __name__ == "__main__":
    run()
