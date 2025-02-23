import json
import csv
import pandas as pd
import sys
import requests
import os
import logging
import random
import time
from datetime import datetime
from wxclub import send_message_to_wecomchan

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

def load_reward_data(file_path='Reward_swq.json'):
    """
    从指定的JSON文件中加载奖励数据
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        logging.error(f"{file_path} 文件未找到")
        return []
    except json.JSONDecodeError:
        logging.error(f"{file_path} 文件格式错误")
        return []

def load_existing_rewards(file_path='Reward.csv'):
    """
    从指定的CSV文件中加载现有的奖励记录
    """
    existing_rewards = set()
    try:
        with open(file_path, 'r', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            existing_rewards = {row['redeem'] for row in reader}
    except FileNotFoundError:
        logging.error(f"{file_path} 文件未找到")
    except csv.Error:
        logging.error(f"{file_path} 文件格式错误")
    return existing_rewards

#发送请求判断兑换码是否有效
def check_redeem_code(redeem):
    """
    检查兑换码是否存在
    如果redeem小于8个字母,则直接返回False
    如果redeem大于8个字母,则发送请求判断兑换码是否存在
    如果redeem存在于Reward.csv文件中,则返回exist
    检查兑换码是否过期
    如果redeem过期,则返回expired
    如果redeem有效,则返回True
    """
    #打印开始检查兑换码是否有效
    logging.info(f"开始检查兑换码 {redeem} 是否有效")
    print(f"开始检查兑换码 {redeem} 是否有效")

    if len(redeem) < 8:
        logging.info(f"兑换码 {redeem} 长度不够")
        print(f"兑换码 {redeem} 长度不够")
        return False
    #    如果redeem存在于Reward.csv文件中,则返回exist
    if redeem in load_existing_rewards():
        logging.info(f"兑换码 {redeem} 已存在于 Reward.csv 文件中")
        print(f"兑换码 {redeem} 已存在于奖励表中")
        return 'exist'
    #redeem = 'sw2024decs9q'
    url = f"https://withhive.me/313/{redeem}"
    #模拟手机请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }
    #随机延迟
    time.sleep(random.randint(3, 15))
    response = requests.get(url, headers=headers)
    #如果返回信息包含Invalid coupon code，则兑换码不存在
    if 'Invalid coupon code' in response.text:
        logging.info(f"兑换码 {redeem} 不存在")
        print(f"兑换码 {redeem} 不存在")
        #打印返回信息
        #print(response.text)
        return False
    #如果返回信息包含expired，则兑换码失效
    elif 'expired' in response.text:
        logging.info(f"兑换码 {redeem} 已过期")
        print(f"兑换码 {redeem} 已过期")
        #打印返回信息
        #print(response.text)
        return 'expired'
    else:
        logging.info(f"兑换码 {redeem} 格式有效")
        print(f"兑换码 {redeem} 格式有效")
        #打印返回信息
        #print(response.text)
        return True
    
def update_reward_csv(reward_data, existing_rewards, file_path='Reward.csv'):
    """
    更新Reward.csv文件中的奖励记录
    """

    filtered_records = []
    for record in reward_data:
        #从Reward.csv中删除失效的兑换码
        if record['vote'] == 'expired' and record['code'] in existing_rewards:
            #从Reward.csv中删除对应的兑换码行
            df = pd.read_csv('Reward.csv')
            df = df[df['redeem'] != record['code']]
            df.to_csv('Reward.csv', index=False)
            logging.info(f"已删除失效的兑换码: {record['code']}")
            print(f"已删除失效的兑换码: {record['code']}")
        # 使用check_redeem_code检查redeem是否失效,删除失效兑换码
        if check_redeem_code(record['code'])=='expired':
            #从Reward.csv中删除对应的兑换码行
            df = pd.read_csv('Reward.csv')
            df = df[df['redeem']!= record['code']]
            df.to_csv('Reward.csv', index=False)
            logging.info(f"已删除失效的兑换码: {record['code']}")
            print(f"已删除失效的兑换码: {record['code']}")
        # 使用check_redeem_code检查redeem是否有效,更新有效的兑换码
        if record['vote'] != 'expired' and record['code'] not in existing_rewards and check_redeem_code(record['code'])==True:
            filtered_records.append({
                'redeem': record['code'],
                'reward': record['reward'],
                'from': 'auto'
            })
            logging.info(f"已添加新的兑换码: {record['code']}")
            print(f"已添加新的兑换码: {record['code']}")
            #延迟2s
            time.sleep(2)
            # 发送企业微信通知：发现新的兑换码redeem，奖励内容为record['reward']
            msg = f"发现新的兑换码{record['code']}，奖励内容为{record['reward']}"
            send_message_to_wecomchan(msg, msg_type='text')
            #打印企业微信通知发送完成
            logging.info("企业微信通知发送完成")
            print("企业微信通知发送完成")
    if not filtered_records:
        logging.debug("没有新的奖励记录需要更新。")
        return
    try:
        with open(file_path, 'a', newline='', encoding='ISO-8859-1') as csvfile:
            fieldnames = ['redeem', 'reward', 'from']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerows(filtered_records)
        logging.info(f"已追加 {len(filtered_records)} 条记录到 {file_path}")
    except IOError:
        logging.error("无法写入Reward.csv文件")
def check_expired_redeem_code(redeem):
    """
    检查兑换码是否过期
    """
    url = f"https://withhive.me/313/{redeem}"
    #模拟手机请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }
    #随机延迟
    time.sleep(random.randint(3, 15))
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        logging.info(f"请求 {url} 成功，状态码: {response.status_code}")
        # 如果返回信息包含expired，则兑换码失效
        if 'expired' in response.text:
            logging.info(f"兑换码 {redeem} 已过期，返回信息: {response.text}")
            print(f"兑换码 {redeem} 已过期")
            return 'expired'
        else:
            logging.info(f"兑换码 {redeem} 未过期，返回信息: {response.text}")
            return None
    except requests.RequestException as e:
        logging.error(f"请求 {url} 失败: {e}")
        return None
#清楚失效过期兑换码
def clear_expired_codes(file_path='Reward.csv'):
    """
    清除过期的兑换码
    """
    try:
        logging.info(f"开始读取 {file_path} 文件")
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
        logging.info(f"成功读取 {file_path} 文件，共 {len(df)} 行")
        logging.info(f"df['redeem'] 列的数据类型: {df['redeem'].dtype}")
        df['expired'] = df['redeem'].apply(check_expired_redeem_code)
        df = df[df['expired'] != 'expired']
        df.drop(columns=['expired'], inplace=True)
        logging.info(f"开始写入 {file_path} 文件，共 {len(df)} 行")
        df.to_csv(file_path, index=False)
        logging.info("已清除过期的兑换码")
    except Exception as e:
        logging.error(f"清除过期兑换码时发生错误: {e}")


def update_user_csv(from_value, user_file_path='User.csv'):
    """
    根据from_value值匹配User.csv中的hiveid值，并将同一行的autonum值加10
    """
    try:
        user_df = pd.read_csv(user_file_path)
        if not pd.api.types.is_numeric_dtype(user_df['autonum']):
            user_df['autonum'] = pd.to_numeric(user_df['autonum'], errors='coerce')
        match_found = False
        for index, row in user_df.iterrows():
            if row['hiveid'] == from_value:
                logging.info(f"已找到匹配的hiveid: {from_value}")
                user_df.at[index, 'autonum'] = row['autonum'] + 10
                match_found = True
                break
        if not match_found:
            logging.info(f"未找到匹配的hiveid: {from_value}")
        user_df.to_csv(user_file_path, index=False)
        logging.info("User.csv文件已更新")
    except Exception as e:
        logging.error(f"更新 {user_file_path} 文件时发生错误: {e}")

def main():
    reward_data = load_reward_data()
    existing_rewards = load_existing_rewards()
    #打印开始更新奖励表
    logging.info("开始更新奖励表")
    print("开始更新奖励表")
    update_reward_csv(reward_data, existing_rewards)
    #打印更新奖励表完成
    logging.info("更新奖励表完成")
    print("更新奖励表完成")
    #打印开始清除过期兑换码
    logging.info("开始清除过期兑换码")
    print("开始清除过期兑换码")
    clear_expired_codes(file_path='Reward.csv')
    #打印清除过期兑换码完成
    logging.info("清除过期兑换码完成")
    print("清除过期兑换码完成")
if __name__ == "__main__":
    main()
    #check_redeem_code("c2uday2inv")
