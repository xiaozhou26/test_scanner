# txt文件的路径，替换为你的实际路径
file_path = 'speed_ip.txt'

def replace_ipv6_address(ipv6_address, replacement):
    replaced_address = ipv6_address.replace("[240e:914:6:d:3c8e:fc17:e3ca:138]", replacement)
    return replaced_address

try:
    with open(file_path, 'r') as file:
        ipv6_addresses = [line.strip() for line in file]  # 每行一个IPv6地址

        with open('xray.txt', 'w') as output_file:
            for address in ipv6_addresses:
                replaced_address = replace_ipv6_address(address, "[your_replacement_here]")
                output_file.write(f"vless://77ac6719-ba62-488b-b47b-47fbea8b61aa@[{replaced_address}]:443?security=tls&sni=us.angelxf.tk&fp=chrome&type=ws&path=/zxjbws&host=us.angelxf.tk&encryption=none#ws-us\n")
except FileNotFoundError:
    print("文件未找到，请检查文件路径。")
    pass
except Exception as e:
    print(f'发生错误：{e}')
    pass