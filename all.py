import subprocess
import requests
import time
import logging
from concurrent.futures import ThreadPoolExecutor

# 设置全局变量
TIMEOUT = 10  # 请求超时时间
URL = "https://cf.xiu2.xyz/url"  # 下载测速地址，端口号为8080
BUFFER_SIZE = 1024  # 缓冲区大小
PING_COUNT = 1  # ping次数

# 配置日志记录
logging.basicConfig(filename='log.txt', level=logging.ERROR)

def ping_ipv6(ipv6_address):
    try:
        # 对每个IPv6地址执行ping命令
        output = subprocess.check_output(["ping", "-c", str(PING_COUNT), ipv6_address], 
                                         stderr=subprocess.STDOUT, 
                                         timeout=5).decode('utf-8')  # timeout set to 500ms
        # 从输出中提取延迟时间
        latency = output.split('time=')[-1].split()[0]
        return ipv6_address, float(latency[:-2])
    except subprocess.CalledProcessError as e:
        logging.error(f'Ping to {ipv6_address} failed with return code {e.returncode}')
    except subprocess.TimeoutExpired as e:
        logging.error(f'Ping to {ipv6_address} timed out')

def download_speed_test(ip):
    start_time = time.time()
    try:
        # 发送GET请求
        response = requests.get(URL, timeout=TIMEOUT, stream=True)
        total_data = 0
        for data in response.iter_content(chunk_size=BUFFER_SIZE):
            total_data += len(data)
            if time.time() - start_time > TIMEOUT:
                break
        speed = total_data / (time.time() - start_time)
        return ip, speed / (1024)  # convert speed to MB/s
    except requests.exceptions.RequestException:
        logging.error(f'Download speed test for {ip} failed')

def main():
    try:
        # 读取ip.txt中的所有IP
        with open("ts.txt", "r") as file:
            ip_list = [line.strip() for line in file.readlines()]
        
        if not ip_list:
            logging.error('IP list is empty')
            return

        # 使用线程池进行并发ping
        with ThreadPoolExecutor(max_workers=32) as executor:
            ping_results = list(executor.map(ping_ipv6, ip_list))

        # 过滤出有延迟的IP
        ip_with_latency = [result[0] for result in ping_results if result and result[1] is not None]

        if not ip_with_latency:
            logging.error('No IP with latency')

        # 使用线程池进行并发测速
        with ThreadPoolExecutor(max_workers=32) as executor:
            speed_results = list(executor.map(download_speed_test, ip_with_latency))

        # 合并ping和测速的结果
        combined_results = [(ip, next(result[1] for result in ping_results if result and result[0] == ip), 
                            next(result[1] for result in speed_results if result and result[0] == ip))
                            for ip in ip_with_latency]

        # 按速度和延迟综合考虑排序结果
        sorted_results = sorted(
            combined_results, key=lambda x: (x[2], -x[1]), reverse=True
        )

        # 输出结果并保存到txt文件
        with open("combined_results.txt", "w") as file:
            file.write("ip\tping(ms)\tspeed(MB/s)\n")  # write column names
            for result in sorted_results:
                file.write(f"{result[0]}\t{result[1]}\t{result[2]}\n")

        # 将IP地址保存到speed_ip.txt文件中
        with open("speed_ip.txt", "w") as file:
            for ip in ip_with_latency:
                file.write(f"{ip}\n")

    except Exception as e:
        logging.error(f'An error occurred: {str(e)}')

if __name__ == "__main__":
    main()