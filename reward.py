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
    filename='auto_redeem.log',
    level=logging.DEBUG if os.getenv("DEBUG", "False").lower() == "true" else logging.INFO,
    format="[%(asctime)s][%(levelname)s] %(message)s",
    datefmt="%m-%d %H:%M:%S",
)
# 确保日志文件存在
if not os.path.exists('auto_redeem.log'):
    open('auto_redeem.log', 'a').close()

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
    检查兑换码是否存在,如果小于8个字母,则直接返回False
    """
    if len(redeem) < 8:
        return False
    #redeem = 'sw2024decs9q'
    url = f"https://withhive.me/313/{redeem}"
    #模拟手机请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }
    #随机延迟
    time.sleep(random.randint(3, 15))
    response = requests.get(url, headers=headers)
    #如果返回信息包含Invalid coupon code，则兑换码存在
    if 'Invalid coupon code' in response.text:
        return False
    else:
        logging.debug(f"兑换码 {redeem} 存在")
        return True
def update_reward_csv(reward_data, existing_rewards, file_path='Reward.csv'):
    """
    更新Reward.csv文件中的奖励记录
    """
    filtered_records = []
    for i, record in enumerate(reward_data):
        #从Reward.csv中删除失效的兑换码
        if record['vote'] == 'expired' and record['code'] in existing_rewards:
            #从Reward.csv中删除对应的兑换码行
            df = pd.read_csv('Reward.csv')
            df = df[df['redeem'] != record['code']]
            df.to_csv('Reward.csv', index=False)
            logging.info(f"已删除过期的兑换码: {record['code']}")
            continue
        # 使用check_redeem_code检查redeem是否有效,更新有效的兑换码
        if record['vote'] != 'expired' and record['code'] not in existing_rewards and check_redeem_code(record['code'])==True:
            filtered_records.append({
                'redeem': record['code'],
                'reward': record['reward'],
                'from': 'auto'
            })
            # 发送企业微信通知：发现新的兑换码redeem，奖励内容为record['reward']
            msg = f"发现新的兑换码{record['code']}，奖励内容为{record['reward']}"
            send_message_to_wecomchan(msg, msg_type='text')
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
 
def updata_from_wechat(redeem, hiveid, file_path='Reward.csv'):
    """
    从微信更新数据到CSV文件
    """
    redeem_value = redeem
    from_value = hiveid
    try:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
        if redeem_value not in df['redeem'].values and check_redeem_code(redeem_value):
            new_row = pd.DataFrame({
                'redeem': [redeem_value],
                'reward': [''],
                'from': [from_value]
            })
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(file_path, index=False)
            logging.info("新增微信来源兑换码")

            # 运行 task.py 生成 task.json 文件
            import task
            task.generate_task_data()
            # 运行 evt_coupon.py 提交表单
            import evt_coupon
            evt_coupon.main()

            try:
                with open('response_log.txt', 'r') as file:
                    lines = file.readlines()
                    last_line = lines[-1].strip()
                    if '优惠券礼物已支付' in last_line:
                        logging.info("兑换码有效")
                        # 更新User.csv文件
                        update_user_csv(from_value)
                    else:
                        logging.error("兑换码无效")
                        sys.exit(1)  # 停止脚本并返回状态码1，表示失败
            except FileNotFoundError:
                logging.error("response_log.txt 文件未找到")
                sys.exit(1)  # 停止脚本并返回状态码1，表示失败
        else:
            logging.info("兑换码已存在，无需更新")
    except Exception as e:
        logging.error(f"更新 {file_path} 文件时发生错误: {e}")

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
                logging.info(f"Found matching hiveid: {from_value}")
                user_df.at[index, 'autonum'] = row['autonum'] + 10
                match_found = True
                break
        if not match_found:
            logging.info(f"No match found for from_value: {from_value}")
        user_df.to_csv(user_file_path, index=False)
        logging.info("User.csv has been updated and saved.")
    except Exception as e:
        logging.error(f"更新 {user_file_path} 文件时发生错误: {e}")

def main():
    reward_data = load_reward_data()
    existing_rewards = load_existing_rewards()
    update_reward_csv(reward_data, existing_rewards)

if __name__ == "__main__":
    main()
