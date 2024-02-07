import socket
from urllib.parse import urlsplit

# 读取文本文件
with open("url.txt", "r") as file:
    urls = file.readlines()

ipv4_addresses = []

# 遍历每个URL并提取IPv4地址
for url in urls:
    url = url.strip()  # 去除首尾的空格和换行符

    parsed_url = urlsplit(url)
    hostname = parsed_url.hostname

    # 尝试解析hostname为IPv4地址
    try:
        ipv4_address = socket.gethostbyname(hostname)
        ipv4_addresses.append(ipv4_address)
    except socket.gaierror:
        pass  # ignore errors

# 将结果写入到另一个文本文件中
with open("ipv4_addresses.txt", "w") as file:
    for address in ipv4_addresses:
        file.write(address)
        file.write("\n")