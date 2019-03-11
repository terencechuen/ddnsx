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
    service_provider = input()
    print("\n")
    output_dict = {"domain_name": domain_name, "sub_domain": sub_domain, "service_provider": service_provider}
    return output_dict


class HeNetConfig:

    def __init__(self, full_domain, password):
        self.full_domain = full_domain
        self.password = password

    @staticmethod
    def get_he_net_info():
        print("# 请输入您 he.net 的账户密码")
        print("# Please enter your he.net account password")
        he_net_password = input()
        return he_net_password

    def gen_he_net_config(self):
        output_dict = {"full_domain": self.full_domain, "password": self.password}
        return output_dict


def run():
    basic_info = get_basic_info()
    if basic_info['service_provider'] == "1":
        he_net_password = HeNetConfig.get_he_net_info()
        he_net_config = HeNetConfig(basic_info["sub_domain"] + basic_info["domain_name"], he_net_password)
        print(he_net_config.gen_he_net_config())


if __name__ == "__main__":
    run()
