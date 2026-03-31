#获取网页内容，并写入配置表中    

import requests
import json
import logging
import os
from wxclub import send_message_to_wecomchan
from reward import check_redeem_code
# 读取环境变量
DEBUG = os.environ.get("DEBUG", False)

# 初始化日志配置
logging.basicConfig(
    filename='my_log.log',
    level=logging.DEBUG if os.getenv("DEBUG", "False").lower() == "true" else logging.INFO,
    format="[%(asctime)s][%(levelname)s] %(message)s",
    datefmt="%m-%d %H:%M:%S",
)
# 确保日志文件存在
if not os.path.exists('my_log.log'):
    open('my_log.log', 'a').close()

def write_to_json(data, filename='swq.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            print(f"数据已成功写入 {filename}")
    except Exception as e:
        # debug打印信息记录到my_log.log
        logging.debug(f"写入JSON文件时发生错误: {e}")
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

def fetch_swq_codes():
    """
    从 https://swq.jp/_special/rest/Sw/Coupon 抓取兑换码
    """
    url = "https://swq.jp/_special/rest/Sw/Coupon"
    response = None
    proxies = {
        'http': 'http://192.168.0.14:7890',
        'https': 'https://192.168.0.14:7890'
    }
    
    # 第一次尝试：不使用代理
    try:
        print("第一次尝试不使用代理抓取 swq.jp")
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"第一次不使用代理请求失败，可能是网络问题或服务器异常。错误信息：{e}")
        logging.debug(f"第一次不使用代理请求失败。错误信息：{e}")
    
    # 第二次尝试：使用代理
    if not response:
        try:
            print("第二次尝试使用代理抓取 swq.jp")
            response = requests.get(url, proxies=proxies, timeout=5)
        except requests.exceptions.RequestException as e:
            print(f"第二次使用代理请求失败，可能是网络问题或服务器异常。错误信息：{e}")
            logging.debug(f"第二次使用代理请求失败。错误信息：{e}")
            return None
    
    # 确保请求成功
    if response and response.status_code == 200:
        try:
            current_data = response.json()
            fields_to_remove = ['request_id', 'time', 'Score', 'Successive_Down_Votes']
            deep_clean(current_data, fields_to_remove)
            return current_data
        except json.JSONDecodeError as e:
            print(f"JSON解析失败：{e}")
            logging.debug(f"JSON解析失败：{e}")
            return None
        except Exception as e:
            print(f"未知错误：{e}")
            logging.debug(f"未知错误：{e}")
            return None
    else:
        print("swq.jp 请求失败，可能是网络问题或服务器异常。")
        logging.debug("swq.jp 请求失败，可能是网络问题或服务器异常。")
        return None

def fetch_q_suisuiaa_codes():
    """
    从 http://q.suisuiaa.fun/api/codes 抓取兑换码
    """
    url = "http://q.suisuiaa.fun/api/codes"
    logging.info(f"开始从 {url} 抓取兑换码")
    print(f"正在从 {url} 抓取兑换码...")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # 提取兑换码
        codes = []
        if isinstance(data, dict) and 'codes' in data:
            for item in data['codes']:
                code = item.get('code')
                if code:
                    codes.append(code)
        elif isinstance(data, list):
            for item in data:
                code = item.get('code')
                if code:
                    codes.append(code)
        
        logging.info(f"成功解析 {len(codes)} 个兑换码")
        print(f"成功解析 {len(codes)} 个兑换码")
        
        # 打印兑换码用于调试
        for code in codes[:10]:
            print(f"  - {code}")
        if len(codes) > 10:
            print(f"  ... 还有 {len(codes) - 10} 个")
        
        return codes
            
    except requests.exceptions.RequestException as e:
        logging.error(f"请求失败：{e}")
        print(f"请求失败：{e}")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"JSON解析失败：{e}")
        print(f"JSON解析失败：{e}")
        return []
    except Exception as e:
        logging.error(f"未知错误：{e}")
        print(f"未知错误：{e}")
        return []

def fetch_and_write_sq_data():
    """
    抓取数据并写入swq.json文件，如果数据有更新。
    """
    # 抓取 swq.jp 的数据
    swq_data = fetch_swq_codes()
    if not swq_data:
        return None
    
    # 检测数据是否更新
    try:
        with open('swq.json', 'r') as f:
            old_data = json.load(f)
    except:
        old_data = None
    
    if old_data != swq_data:
        print("swq.jp 数据更新，开始写入swq.json")
        write_to_json(swq_data)
        logging.debug(f"数据已成功写入 swq.json")
        return True
    else:
        print("swq.jp 数据未更新")
        logging.debug(f"数据未更新，未写入 swq.json")
        return False

def filter_swq_codes():
    """
    从 swq.json 提取兑换码并过滤
    """
    # 定义要读取的 JSON 文件名
    file_name = 'swq.json'
    
    # 打开文件并读取内容
    with open(file_name, 'r') as file:
        data_dict = json.load(file)
    
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
    
    return result_list

def filter_q_suisuiaa_codes():
    """
    从 q_suisuiaa_codes.json 提取兑换码并过滤
    """
    # 定义要读取的 JSON 文件名
    file_name = 'q_suisuiaa_codes.json'
    
    # 打开文件并读取内容
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            data_list = json.load(file)
    except:
        print(f"未找到 {file_name} 文件")
        return []
    
    # 创建一个空列表来存储提取的数据
    result_list = []
    
    # 遍历 JSON 数据
    for entry in data_list:
        # 提取 code
        code = entry.get('code', 'N/A')
        # 提取 reward
        reward = entry.get('reward', '')
        # 提取 vote
        vote = entry.get('vote', 'N/A')
        # 将提取的数据作为一个字典添加到结果列表中
        result_list.append({'code': code, 'reward': reward, 'vote': vote})
    
    return result_list

def filter_and_write_reward_json():
    """
    提取特定字段值 拼接后排除无效和已有值后写入Reward_swq.json
    合并两个网站的兑换码进行统一过滤
    """
    # 定义输出文件名
    output_file_name = 'Reward_swq.json'
    
    # 读取已有的兑换码数据
    try:
        with open(output_file_name, 'r') as file:
            existing_data = json.load(file)
    except:
        existing_data = []
    
    # 收集所有新的兑换码
    all_new_codes = []
    
    # 过滤 swq.jp 的兑换码
    print("\n--- 过滤 swq.jp 兑换码 ---")
    swq_codes = filter_swq_codes()
    print(f"从 swq.json 读取到 {len(swq_codes)} 个兑换码")
    
    for item in swq_codes:
        # 检查当前字典是否已经存在于 existing_data 中
        if item in existing_data:
            print(f"已排除存在的兑换码: {item}")
            logging.debug(f"已排除存在的兑换码: {item}")
            continue
        
        # 调用 check_redeem_code 函数
        if check_redeem_code(item['code']) != True:
            print(f"已排除无效数据: {item}")
            logging.debug(f"已排除无效数据: {item}")
            continue
        
        all_new_codes.append(item)
        print(f"添加新兑换码: {item}")
    
    # 过滤 q.suisuiaa.fun 的兑换码
    print("\n--- 过滤 q.suisuiaa.fun 兑换码 ---")
    q_codes = filter_q_suisuiaa_codes()
    print(f"从 q_suisuiaa_codes.json 读取到 {len(q_codes)} 个兑换码")
    
    for item in q_codes:
        # 检查当前字典是否已经存在于 existing_data 中
        if item in existing_data:
            print(f"已排除存在的兑换码: {item}")
            logging.debug(f"已排除存在的兑换码: {item}")
            continue
        
        # 调用 check_redeem_code 函数
        if check_redeem_code(item['code']) != True:
            print(f"已排除无效数据: {item}")
            logging.debug(f"已排除无效数据: {item}")
            continue
        
        all_new_codes.append(item)
        print(f"添加新兑换码: {item}")
    
    # 合并新旧数据
    all_codes = existing_data + all_new_codes
    
    # 将结果列表写入到 JSON 文件
    try:
        with open(output_file_name, 'w', encoding='utf-8') as file:
            json.dump(all_codes, file, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"写入文件失败: {e}")
        print(f"写入文件失败: {e}")
        return False
    
    print(f"\n数据已成功写入 {output_file_name}")
    print(f"总共 {len(all_codes)} 个兑换码（包含新旧）")
    logging.info(f"数据已成功写入 {output_file_name}，总共 {len(all_codes)} 个兑换码")

def fetch_q_suisuiaa_and_save():
    """
    从 q.suisuiaa.fun 抓取兑换码并保存
    """
    # 抓取兑换码
    codes = fetch_q_suisuiaa_codes()
    
    if not codes:
        print("未抓取到兑换码")
        return False
    
    # 保存到文件
    output = []
    for code in codes:
        output.append({
            'code': code,
            'reward': '',  # 奖励待验证后填充
            'vote': 'verified'  # 初始状态
        })
    
    # 读取已有的兑换码数据
    try:
        with open('q_suisuiaa_codes.json', 'r') as f:
            existing_data = json.load(f)
    except:
        existing_data = []
    
    # 排除已存在的兑换码
    new_codes = []
    for item in output:
        if item not in existing_data:
            new_codes.append(item)
            print(f"发现新兑换码: {item['code']}")
    
    # 合并新旧数据
    all_codes = existing_data + new_codes
    
    # 保存到文件
    with open('q_suisuiaa_codes.json', 'w', encoding='utf-8') as f:
        json.dump(all_codes, f, ensure_ascii=False, indent=4)
    
    logging.info(f"已保存 {len(all_codes)} 个兑换码到 q_suisuiaa_codes.json")
    print(f"已保存 {len(all_codes)} 个兑换码到 q_suisuiaa_codes.json")
    
    return True

def main():
    # 打印开始抓取兑换码
    logging.info("开始抓取兑换码")
    print("=" * 60)
    print("开始抓取兑换码")
    print("=" * 60)
    
    # 抓取 swq.jp 的数据
    print("\n--- 抓取 swq.jp 兑换码 ---")
    swq_updated = fetch_and_write_sq_data()
    
    # 抓取 q.suisuiaa.fun 的数据
    print("\n--- 抓取 q.suisuiaa.fun 兑换码 ---")
    q_suisuiaa_updated = fetch_q_suisuiaa_and_save()
    
    # 打印抓取兑换码完成
    logging.info("抓取兑换码完成")
    print("\n" + "=" * 60)
    print("抓取兑换码完成")
    print("=" * 60)
    
    # 过滤所有网站的兑换码
    print("\n--- 过滤所有兑换码 ---")
    filter_and_write_reward_json()
    # 打印过滤兑换码完成
    logging.info("过滤兑换码完成")
    print("过滤兑换码完成")
    return True

if __name__ == "__main__":
    main()
