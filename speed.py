import requests
import time
from concurrent.futures import ThreadPoolExecutor

# 设置全局变量
TIMEOUT = 10  # 请求超时时间
URL = "https://cf.xiu2.xyz/url"  # 下载测速地址，端口号为8080
BUFFER_SIZE = 1024  # 缓冲区大小

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
        return ip, speed / (1024 * 1024)  # convert speed to MB/s
    except requests.exceptions.RequestException:
        return ip, 0

def main():
    # 读取ip.txt中的所有IP
    with open("ping_results.txt", "r") as file:
        ip_list = [line.strip() for line in file.readlines()]

    # 使用线程池进行并发测速
    with ThreadPoolExecutor(max_workers=32) as executor:
        results = list(executor.map(download_speed_test, ip_list))

    # 按速度从大到小排序结果
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

    # 输出测速结果并保存到txt文件
    with open("speed_results.txt", "w") as file:
        file.write("ip\tspeed(MB/s)\n")  # write column names
        for result in sorted_results:
            file.write(f"{result[0]}\t{result[1]}\n")

    # 将IP地址保存到speed_ip.txt文件中
    with open("speed_ip.txt", "w") as file:
        for ip in ip_list:
            file.write(f"{ip}\n")

if __name__ == "__main__":
    main()