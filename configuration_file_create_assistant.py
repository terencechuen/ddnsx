import json, os


def get_basic_info():
    print("# 请输入您的域名")
    print("# Please enter your domain name")
    domain_name = input()
    print("\n")

    print("# 请输入您的子域名")
    print("# Please enter your subdomain")
    sub_domain = input()
    print("\n")

    print("# 请选择您的DNS服务商")
    print("# Please choose your DNS service provider")
    print("1. he.net")
    print("2. gandi.net")
    print("3. godaddy.com")
    service_provider = input()
    print("\n")

    while True:
        print("# 请选择您的DNS记录类型")
        print("# Please select your DNS record type")
        print("1. A")
        print("2. AAAA")
        print("3. TXT")

        record_type = input()

        if record_type is not "1" and not "2" and not "3":
            print("# 请输入正确的DNS记录类型")
        elif record_type is "1":
            record_type = "A"
            break
        elif record_type is "2":
            record_type = "AAAA"
            break
        else:
            record_type = "TXT"
            break

    print("\n")

    if record_type == "3":
        print("# 请选择您的IP版本")
        print("# Please choose your DNS service provider")
        print("1. IPv4")
        print("2. IPv6")
        ip_version = input()
        print("\n")
    elif record_type == "1":
        ip_version = "4"
    else:
        ip_version = "6"

    output_dict = {
        "domain_name": domain_name,
        "sub_domain": sub_domain,
        "service_provider": service_provider,
        "record_type": record_type,
        "ip_version": ip_version
    }
    return output_dict


class HeNetConfig:

    def __init__(self, basic_info, password):
        self.basic_info = basic_info
        self.password = password

    @staticmethod
    def get_he_net_info():
        print("# 请输入您 he.net 的账户密码")
        print("# Please enter your he.net account password")
        he_net_password = input()
        return he_net_password

    def gen_he_net_config(self):
        full_domain = self.basic_info['sub_domain'] + '.' + self.basic_info['domain_name']
        self.basic_info['password'] = self.password
        self.basic_info['full_domain'] = full_domain
        return self.basic_info


class GandiNetConf:
    def __init__(self, basic_info, api_key):
        self.basic_info = basic_info
        self.api_key = api_key

    @staticmethod
    def get_gandi_net_info():
        print("# 请输入您 gandi.net 的API KEY")
        print("# Please enter your he.net API KEY")
        gandi_api_key = input()
        return gandi_api_key

    def gen_gandi_net_config(self):
        self.basic_info['api_key'] = self.api_key
        return self.basic_info


class GodaddyComConf:
    def __init__(self, basic_info, api_key, api_secret):
        self.basic_info = basic_info
        self.api_key = api_key
        self.api_secret = api_secret

    @staticmethod
    def get_godaddy_com_info():
        print("# 请输入您 godaddy.com 的API KEY")
        print("# Please enter your  godaddy.com API KEY")
        godaddy_com_api_key = input()

        print("# 请输入您 godaddy.com 的API SECRET")
        print("# Please enter your  godaddy.com API SECRET")
        godaddy_com_api_secret = input()

        return {"api_key": godaddy_com_api_key, "api_secret": godaddy_com_api_secret}

    def gen_godaddy_com_config(self):
        self.basic_info['api_key'] = self.api_key
        self.basic_info['api_secret'] = self.api_secret
        return self.basic_info


def proc_config():
    basic_info = get_basic_info()

    if basic_info['service_provider'] == "1":
        del basic_info['service_provider']
        he_net_password = HeNetConfig.get_he_net_info()
        he_net_config = HeNetConfig(basic_info, he_net_password)
        return he_net_config.gen_he_net_config(), "he.net"

    if basic_info['service_provider'] == "2":
        del basic_info['service_provider']
        gandi_net_api_key = GandiNetConf.get_gandi_net_info()
        gandi_net_config = GandiNetConf(basic_info, gandi_net_api_key)
        return gandi_net_config.gen_gandi_net_config(), "gandi.net"

    if basic_info['service_provider'] == "3":
        del basic_info['service_provider']
        godaddy_com_api_info = GodaddyComConf.get_godaddy_com_info()
        godaddy_com_config = GodaddyComConf(basic_info, godaddy_com_api_info['api_key'],
                                            godaddy_com_api_info['api_secret'])
        return godaddy_com_config.gen_godaddy_com_config(), "godaddy.com"


def proc_config_final(config_final, config_input, service_provider):
    if service_provider in config_final:
        config_final[service_provider].append(config_input)
    else:
        config_final[service_provider] = [config_input]
    return config_final


def write_config_to_file(i):
    config_file_path = os.getcwd() + '/config.json'
    o = open(config_file_path, 'w')
    o.write(i)
    o.close()


if __name__ == "__main__":
    config_output = dict()

    while True:
        config_temp = proc_config()
        config_output = proc_config_final(config_output, config_temp[0], config_temp[1])
        print("# 请确认您的配置信息\n")
        print("###### 以下为您的配置信息 ######")
        print(json.dumps(config_output, indent=1, sort_keys=True))
        print("###### 以上为您的配置信息 ######")
        print("请根据实际情况选择，回车确认：")
        print("# 1. 完成DDNS域名信息，保存配置到文件并退出")
        print("# 2. 继续添加DDNS域名信息")
        print("# 3. 终止DDNS域名信息的添加，丢弃已配置的信息并退出")
        req_input = input()
        if req_input == "1":
            break
        elif req_input == "2":
            continue
        elif req_input == "3":
            print("# 程序退出")
            exit(1)
        else:
            print("# 请输入正确的数字")

    config_output = json.dumps(config_output)
    write_config_to_file(config_output)
    print("# 文件保存完毕，配置信息已保存到\"config.json\"文件中")
    print("# 程序退出")
