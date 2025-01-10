# 兑换码领取器，领取后企业微信通知对方
import logging
import requests
import random
import time
import json
import csv
from datetime import datetime
import os
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

# 预定义的User-Agent列表
user_agents = [
    # ... (省略了之前的User-Agent列表)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"
]

def main():
    #打印开始执行领取操作
    logging.info("开始执行领取操作")
    print("开始执行领取操作")
    # 读取task.json文件
    with open('task.json', 'r') as json_file:
        task_data = json.load(json_file)

    # global全球服务器, korea韩国服务器, japan日本服务器, china中国服务器, asia亚洲服务器, europe欧洲服务器

    # 遍历task.json中的每组数据
    for data in task_data:
        # 提取所需字段
        server = data.get('server')
        hiveid = data.get('hiveid')
        coupon = data.get('coupon')

        # 表单数据
        form_data = {
            'country': 'HK',
            'lang': 'zh-hans',
            'server': server,
            'hiveid': hiveid,
            'coupon': coupon
        }
        # debug打印表单数据
        logging.debug("表单数据: %s", form_data)
        # 如果表单数据已经存在于post.log文件中，则跳过发送POST请求。
        form_data_str = json.dumps(form_data)
        if os.path.exists('post.log'):
            with open('post.log', 'r') as log_file:
                if form_data_str in log_file.read():
                    logging.debug("表单数据已存在于post.log文件中，跳过发送POST请求。")
                    continue
        # 如果表单数据不存在于post.log，则写入日志并提交表单,并将表单数据写入post.log文件中.
        with open('post.log', 'a') as log_file:
            log_file.write(f"{datetime.now()}: {form_data_str}\n")
        logging.debug("表单数据: %s", form_data)
        # 随机等待一段时间，避免被服务器拒绝
        # 等待时间范围为1到3秒
        wait_time = random.uniform(1, 3)
        time.sleep(wait_time)    
        # 表单提交的URL
        url = 'https://event.withhive.com/ci/smon/evt_coupon/useCoupon'
        # 随机选择一个User-Agent
        selected_user_agent = random.choice(user_agents)
        # 设置请求头，包含随机User-Agent
        headers = {
            'User-Agent': selected_user_agent,
            'referer': "https://event.withhive.com/ci/smon/evt_coupon",
            'cookie': "language=zh-CN; _ga=GA1.1.1644757241.1734775297; inquiry_language=zh_CN; _ga_FWV2C4HMXW=GS1.1.1734802553.3.0.1734802555.0.0.0",
            'host': "event.withhive.com",
            'X-Requested-With': "XMLHttpRequest",
            'Origin': "https://event.withhive.com"
        }
        # 发送POST请求
        response = requests.post(url, data=form_data, headers=headers)
        logging.info("响应状态码: %s", response.status_code)
        logging.debug("响应内容: %s", response.text)
        # 检查响应状态码
        if response.status_code == 200:
            # 打印响应内容
            print("响应内容:", response.text)
            # 尝试解析JSON数据
            try:
                response_json = response.json()
                # 打印解析后的JSON数据
                print("解析后的JSON数据:", response_json)
                # 'retCode': '(H304)', 'retMsg': '已使用过的优惠券代码。'
                #'retCode': '(H302)', 'retMsg': '无效的优惠券代码。<br/>请重新确认。'}
                # {'retCode': '(H306)', 'retMsg': '无效的优惠券代码。<br/>请重新确认。'}
                # "retCode": 100, "retMsg": "优惠券礼物已支付。"
                # {'retCode': 500, 'retMsg': ''}
                # "retCode": 503, "retMsg": "无效的Hive ID。<br/>请重新确认。"
                # 将JSON数据写入文件response_log.txt
                # 检查response_log.txt文件是否存在，如果不存在则创建
                if not os.path.exists('response_log.txt'):
                    open('response_log.txt', 'a').close()
                with open('response_log.txt', 'a') as log_file:
                    log_file.write(f"{datetime.now()}: {response_json}\n")
                # 打开history.csv文件，准备写入数据
                with open('history.csv', 'a', newline='') as csvfile:
                    fieldnames = ['redeem', 'reward', 'hiveid', 'server', 'date', 'status']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    # 如果文件为空，则写入表头
                    if csvfile.tell() == 0:
                        writer.writeheader()
                    # 'retCode': '(H304)', 'retMsg': '已使用过的优惠券代码。'
                    #如果返回内容包括无效的优惠券代码，将相关信息新增写入history.csv文件并在status字段写入已领取
                    if '已使用过的优惠券代码' in str(response.text):
                        # 根据redeem从Reward_swq.json中获取reward字段的值
                        # 打开Reward_swq.json文件，准备读取数据
                        with open('Reward_swq.json', 'r', encoding='utf-8') as json_file:
                            reward_data = json.load(json_file)
                        # 遍历reward_data中的每个字典
                        for item in reward_data:
                            # 检查redeem字段是否与目标redeem匹配
                            if item.get('code') == coupon:
                                # 如果匹配，获取reward字段的值
                                reward_value = item.get('reward')
                            else:
                            # 如果没有找到匹配的字典，打印提示信息
                                print(f"兑换码 {coupon} 奖励未记录")
                                reward_value = ''
                        # 写入数据到history.csv文件
                        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                        writer.writerow({
                            'redeem': coupon,
                            'reward': reward_value,
                            'hiveid': hiveid,
                            'server': server,
                            'date': current_time,
                            'status': '已领取'
                        })
                    # 如果返回内容包含100，也就是领取成功，将相关信息新增写入history.csv文件
                    if '优惠券礼物已支付' in str(response.text):
                        # 根据redeem从Reward_swq.json中获取reward字段的值
                        # 打开Reward_swq.json文件，准备读取数据
                        with open('Reward_swq.json', 'r', encoding='utf-8') as json_file:
                            reward_data = json.load(json_file)
                        # 遍历reward_data中的每个字典
                        for item in reward_data:
                            # 检查redeem字段是否与目标redeem匹配
                            if item.get('code') == coupon:
                                # 如果匹配，获取reward字段的值
                                reward_value = item.get('reward')
                                # 打印reward字段的值
                                print(f"reward字段的值: {reward_value}")
                                # 在这里可以使用reward_value做进一步的处理
                                # 发送企业微信通知：hiveid已自动领取redeem：reward，领取时间：date
                                msg = f"{hiveid}已自动领取{coupon}:{reward_value}，领取时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                                send_message_to_wecomchan(msg, msg_type='text')
                                #打印企业微信通知发送完成
                                print("企业微信通知发送完成")
                            else:
                            # 如果没有找到匹配的字典，打印提示信息
                                print(f"兑换码 {coupon} 奖励未记录")
                                reward_value = ''
                                # 发送企业微信通知：hiveid已自动领取redeem：reward，领取时间：date
                                msg = f"{hiveid}已自动领取{coupon}，领取时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                                send_message_to_wecomchan(msg, msg_type='text')
                                #打印企业微信通知发送完成
                                print("企业微信通知发送完成")

                            # 写入数据到history.csv文件
                            current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                            writer.writerow({
                                    'redeem': coupon,
                                    'reward': reward_value,
                                    'hiveid': hiveid,
                                    'server': server,
                                    'date': current_time,
                                    'status': '领取成功'
                                })
                            # 打印写入的内容
                            print(f"写入数据: {coupon}, {hiveid}, {server}, {current_time}")
            except json.JSONDecodeError:
                print("无法从响应中解析JSON")
        else:
            # 打印提交表单失败返回的数据
            print("提交表单失败，状态码:", response.text)
            #写入auto_redeem.log文件
            with open('auto_redeem.log', 'a') as log_file:
                log_file.write(f"{datetime.now()}: 提交表单失败，状态码: {response.status_code}\n")
        # 随机延迟，避免过于频繁的请求  
        time.sleep(random.uniform(15, 120)) 
if __name__ == "__main__":
    main()
