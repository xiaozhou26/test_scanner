# txt文件的路径，替换为你的实际路径
file_path = 'ts.txt'

try:
    with open(file_path, 'r') as file:
        ip_addresses = [line.strip() for line in file]

    # 使用set删除重复的IP地址
    unique_ip_addresses = set(ip_addresses)

    # 将结果写入新的txt文件
    with open('ts.txt', 'w') as f:
        for address in unique_ip_addresses:
            f.write(address + '\n')
except FileNotFoundError:
    print("The file was not found. Please check the file path.")
except Exception as e:
    print(f'An error occurred: {e}')