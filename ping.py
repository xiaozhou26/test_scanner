import subprocess
import concurrent.futures

# txt文件的路径，替换为你的实际路径
file_path = 'ts.txt'
# 结果txt文件的路径
results_txt_path = 'ping_results.txt'

def ping_ipv6(ipv6_address):
    try:
        # 对每个IPv6地址执行ping命令
        output = subprocess.check_output(["ping", "-c", "1", ipv6_address], 
                                         stderr=subprocess.STDOUT, 
                                         timeout=5).decode('utf-8')  # timeout set to 500ms
        # 从输出中提取延迟时间
        latency = output.split('time=')[-1].split()[0]
        return ipv6_address
    except subprocess.CalledProcessError as e:
        # print(f'Ping to {ipv6_address} failed with return code {e.returncode}')
        pass
    except subprocess.TimeoutExpired as e:
        # print(f'Ping to {ipv6_address} timed out')
        pass
try:
    with open(file_path, 'r') as file, open(results_txt_path, 'w') as txtfile:
        ipv6_addresses = [line.strip() for line in file]  # assuming the IP address is in each line

        # 使用ThreadPoolExecutor并行执行ping命令
        with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
            results = executor.map(ping_ipv6, ipv6_addresses)
            for result in results:
                if result is not None:
                    txtfile.write(result + '\n')
                    # print(f'Successful Ping to {result}')
except FileNotFoundError:
    print("The file was not found. Please check the file path.")
except Exception as e:
    print(f'An error occurred: {e}')