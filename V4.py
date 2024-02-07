import subprocess
import concurrent.futures

# txt文件的路径，替换为你的实际路径
file_path = 'ipv4.txt'
# 结果txt文件的路径
results_txt_path = 'ping_results.txt'

def ping_ipv4(ipv4_address):
    try:
        # 对每个IPv4地址执行ping命令
        output = subprocess.check_output(["ping", "-c", "1", ipv4_address], 
                                         stderr=subprocess.STDOUT, 
                                         timeout=5).decode('utf-8')  # timeout set to 5 seconds
        # 从输出中提取延迟时间
        latency = output.split('time=')[-1].split()[0]
        return ipv4_address
    except subprocess.CalledProcessError as e:
        print(f'Ping to {ipv4_address} failed with return code {e.returncode}')
    except subprocess.TimeoutExpired as e:
        print(f'Ping to {ipv4_address} timed out')

try:
    with open(file_path, 'r') as file, open(results_txt_path, 'w') as txtfile:
        ipv4_addresses = [line.strip() for line in file]  # assuming the IP address is in each line

        # 使用ThreadPoolExecutor并行执行ping命令
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(ping_ipv4, ipv4_addresses)
            for result in results:
                if result is not None:
                    txtfile.write(result + '\n')
                    print(f'Successful Ping to {result}')
except FileNotFoundError:
    print("The file was not found. Please check the file path.")
except Exception as e:
    print(f'An error occurred: {e}')