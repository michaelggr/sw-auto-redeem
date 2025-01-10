#获取网页内容，并写入配置表中    

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
def deep_clean(data, fields_to_remove):
    if isinstance(data, dict):
        for key in list(data.keys()):  # 使用list()避免在迭代时修改字典
            if key in fields_to_remove:
                del data[key]  # 删除指定的字段
            else:
                deep_clean(data[key], fields_to_remove)  # 递归清理嵌套的数据
    elif isinstance(data, list):
        for item in data:
            deep_clean(item, fields_to_remove)  # 递归清理列表中的每个元素
def fetch_and_write_sq_data():
    """
    抓取数据并写入swq.json文件，如果数据有更新。
    """
    # 发送 GET 请求
    url = "https://swq.jp/_special/rest/Sw/Coupon"
    response = requests.get(url)

    # 确保请求成功
    if response.status_code == 200:
        # 解析 JSON 数据
        current_data = response.json()

        # 要删除的字段
        fields_to_remove = ['request_id', 'time', 'Score', 'Successive_Down_Votes']

        # 清理数据
        deep_clean(current_data, fields_to_remove)

        # 检测数据是否更新
        if current_data != json.load(open('swq.json', 'r')):
            print("数据更新，开始写入swq.json")
            write_to_json(current_data)
            # debug打印信息记录到auto_redeem.log
            logging.debug(f"数据已成功写入 swq.json")
            return True
        else:
            # 打印数据未更新
            print("数据未更新")
            # debug打印信息记录到auto_redeem.log
            logging.debug(f"数据未更新，未写入 swq.json")
            #返回false
            return False            
    else:
        print("请求失败，状态码：", response.status_code)
        logging.debug(f"请求失败", response.text)
        return response.status_code

def filter_and_write_reward_json ():
    """
    提取特定字段值 拼接后排除无效和已有值后写入Reward_swq.json
    """
  # 定义要读取的 JSON 文件名
    file_name = 'swq.json'

    # 打开文件并读取内容
    with open(file_name, 'r') as file:
        data_dict = json.load(file)

    # 打印转换后的字典
    # print(data_dict)

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

    # 打印结果列表
    logging.debug(result_list)

    # 定义输出文件名
    output_file_name = 'Reward_swq.json'
    
    # 排除掉已经存在于Reward_swq.json中相同的数据
    with open(output_file_name, 'r') as file:
        data_dict = json.load(file)

    # 遍历 result_list 中的每个字典
    for item in result_list:
        # 检查当前字典是否已经存在于 data_dict 中
        if item in data_dict:
            # 如果存在，则将其删除
            result_list.remove(item)
            print(f"已排除存在的兑换码: {item}")
            logging.debug(f"已排除存在的兑换码: {item}")

    # 打印结果列表
    logging.debug(result_list)

    # 使用check_redeem_code排除无效数据,不等于true的数据
    for item in result_list:
        # 调用 check_redeem_code 函数
        if check_redeem_code(item['code']) != True:
            result_list.remove(item)
            print(f"已排除无效数据: {item}")
            logging.debug(f"已排除无效数据: {item}")

    # 将结果列表写入到 JSON 文件
    with open(output_file_name, 'w') as file:
        json.dump(result_list, file, indent=4)
    print(f"数据已成功写入 {output_file_name}")
    logging.info(f"数据已成功写入 {output_file_name}")

def main():
    # 打印开始抓取兑换码
    logging.info("开始抓取兑换码")
    print("开始抓取兑换码")
    # 调用抓取数据并写入的函数
    fetch_and_write_sq_data()
    # 打印抓取兑换码完成
    logging.info("抓取兑换码完成")
    print("抓取兑换码完成")
    #当兑换码有更新时才过滤兑换码
    if fetch_and_write_sq_data() == True:
        # 打印开始过滤兑换码
        logging.info("开始过滤兑换码")
        filter_and_write_reward_json()
        # 打印过滤兑换码完成
        logging.info("过滤兑换码完成")
        print("过滤兑换码完成")
        return True
    else:
        # 打印兑换码未更新
        logging.info("兑换码未更新")
        print("兑换码未更新")
        return False
if __name__ == "__main__":
    fetch_and_write_sq_data()
    filter_and_write_reward_json()




