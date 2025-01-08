#获取网页内容，并写入配置表中    
from datetime import datetime
import time
import requests
import json
import logging
import os

from reward import check_redeem_code
# 读取环境变量
DEBUG = os.environ.get("DEBUG", False)

# 初始化日志配置
logging.basicConfig(
    filename='auto_redeem.log',
    level=logging.DEBUG if os.getenv("DEBUG", "False").lower() == "true" else logging.INFO,
    format="[%(asctime)s][%(levelname)s] %(message)s",
    datefmt="%m-%d %H:%M:%S",
)
# 确保日志文件存在
if not os.path.exists('auto_redeem.log'):
    open('auto_redeem.log', 'a').close()

def write_to_json(data, filename='swq.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"数据已成功写入 {filename}")
    except Exception as e:
        print(f"写入JSON文件时发生错误: {e}")
def main():
    # 发送 GET 请求
    url = "https://swq.jp/_special/rest/Sw/Coupon"
    response = requests.get(url)
    # 确保请求成功
    if response.status_code == 200:
        # 解析 JSON 数据
            data = response.json()
            # 打印 JSON 数据
            #print(json.dumps(data, indent=4)) 
            # 写入JSON文件
            #保证网站数据有更新时才写入
            if data != json.load(open('swq.json', 'r')):
                print("数据更新，开始写入swq.json")
                write_to_json(data)
                #debug打印信息记录到auto_redeem.log
                logging.debug(f"数据已成功写入 swq.json")
            else:
                print("数据未更新，未写入 swq.json")
                #debug打印信息记录到auto_redeem.log
                logging.debug(f"数据未更新，未写入 swq.json")        
    else:
            print("请求失败，状态码：", response.status_code)
            logging.debug(f"请求失败",response.text)

    # 定义要读取的 JSON 文件名
    file_name = 'swq.json'

    # 打开文件并读取内容
    with open(file_name, 'r') as file:
        # 使用 json.load() 将文件内容转换为字典
        data_dict = json.load(file)

    # 打印转换后的字典
    #print(data_dict)
    # 创建一个空列表来存储提取的数据
    result_list = []

    # 遍历 JSON 数据中的 'data' 部分
    for entry in data_dict['data']:
        # 提取 code（Label 的值）
        code = entry.get('Label', 'N/A')
        
        # 提取 reward（Sw_Resource 中 Label 的值拼接 Resources 中 Quantity 的值）
        reward_values = []
        if 'Resources' in entry and isinstance(entry['Resources'], list):
            for resource in entry['Resources']:
                sw_resource = resource.get('Sw_Resource', {})
                label = sw_resource.get('Label', 'N/A')
                quantity = resource.get('Quantity', 'N/A')
                reward_values.append(f"{label} x{quantity}")
        reward = ', '.join(reward_values)
        # 提取 vote（Status 的值）
        vote = entry.get('Status', 'N/A')
        # 将提取的数据作为一个字典添加到结果列表中
        result_list.append({'code': code, 'reward': reward, 'vote': vote})

    #print(result_list)
    # 定义输出文件名
    output_file_name='Reward_swq.json'
    #使用check_redeem_code排除无效数据
    for item in result_list:
        if check_redeem_code(item['code'])==False:
            result_list.remove(item)
            print(f"已排除无效数据: {item}")
            logging.debug(f"已排除无效数据: {item}")
        #加个延迟，防止被封
        time.sleep(5)
    # 将结果列表写入到 JSON 文件
    with open(output_file_name, 'w') as file:
        json.dump(result_list, file, indent=4)
    print(f"数据已成功写入 {output_file_name}")
    logging.debug(f"数据已成功写入 {output_file_name}")

if __name__ == "__main__":
    main()


