import csv
import logging
import os

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
def load_reward_data():
    """
    从Reward.csv文件中加载奖励数据
    """
    reward_data = {}
    try:
        with open('Reward.csv', 'r') as reward_file:
            reward_reader = csv.DictReader(reward_file)
            for row in reward_reader:
                reward_data[row['redeem']] = row['reward']
    except FileNotFoundError:
        logging.error("Reward.csv文件未找到")
    except csv.Error:
        logging.error("Reward.csv文件格式错误")
    return reward_data

def load_history_data():
    """
    从history.csv文件中加载历史数据
    """
    history_data = []
    try:
        with open('history.csv', 'r') as history_file:
            history_reader = csv.DictReader(history_file)
            history_data = list(history_reader)
    except FileNotFoundError:
        print("history.csv文件未找到")
        logging.error("history.csv文件未找到")
    except csv.Error:
        print("history.csv文件格式错误")
        logging.error("history.csv文件格式错误")
    return history_data

def save_history_data(history_data):
    """
    将历史数据保存到history.csv文件
    """
    try:
        with open('history.csv', 'w', newline='', encoding='utf-8') as history_file:
            fieldnames = history_data[0].keys() if history_data else []
            history_writer = csv.DictWriter(history_file, fieldnames=fieldnames)
            history_writer.writeheader()
            history_writer.writerows(history_data)
    except IOError:
        print("无法写入history.csv文件")
        logging.error("无法写入history.csv文件")

def update_reward_field(reward_data, history_data):
    """
    更新history.csv文件中的reward字段
    """
    print("开始匹配奖励字段操作")
    logging.info("开始匹配奖励字段操作")
    updated = False
    for row in history_data:
        if row['redeem'] in reward_data:
            row['reward'] = reward_data[row['redeem']]
            print(f"已更新reward字段：{row['redeem']} {row['reward']}")
            updated = True
        else:
            print(f"未找到匹配的reward字段：{row['redeem']}")
            logging.debug(f"未找到匹配的reward字段：{row['redeem']}")
    return updated
def update_histary():
    """
    更新历史数据，从task_log里提取数据写入history.csv文件
    """
    print("开始执行更新历史数据操作")
    logging.info("开始执行更新历史数据操作")
    #创建history.csv文件
    if not os.path.exists('history.csv'):
        open('history.csv', 'a').close()
    # 打开history.csv文件，准备写入数据
    with open('history.csv', 'a', newline='') as csvfile:
        fieldnames = ['redeem', 'reward', 'hiveid', 'server', 'date', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # 如果文件为空，则写入表头
        if csvfile.tell() == 0:
            writer.writeheader()
        # 'retCode': '(H304)', 'retMsg': '已使用过的优惠券代码。'
        #'retCode': '(H302)', 'retMsg': '无效的优惠券代码。<br/>请重新确认。'}
        # {'retCode': '(H306)', 'retMsg': '无效的优惠券代码。<br/>请重新确认。'}
        # "retCode": 100, "retMsg": "优惠券礼物已支付。"
        # {'retCode': 500, 'retMsg': ''}
        # "retCode": 503, "retMsg": "无效的Hive ID。<br/>请重新确认。"
        history_data = load_history_data()
        #读取task_log.csv文件
        with open('task_log.csv', 'r') as task_log_file:
            task_log_reader = csv.DictReader(task_log_file)
            # 遍历task_log.csv文件中的每一行数据
            for row in task_log_reader:
                    coupon = row['redeem']
                    hiveid = row['hiveid']
                    server = row['server']
                    retcode = row['retcode']

                    # 检查是否已经存在相同的redeem和reward值，如果存在则跳过
                    existing_record = next((r for r in history_data if r['redeem'] == coupon and r['hiveid'] == hiveid), None)
                    if existing_record:
                        print(f"已存在相同的兑换记录：{coupon} {hiveid}")
                        continue
                    else:
                        if retcode == '100':
                            status = '已自动领取'

                        elif retcode == '(H304)':
                            status = '手动领取过'
                            print("手动领取过")

                        elif retcode == '500':
                            status = '服务器错误'

                        elif retcode == '503':
                            status = '无效的Hive ID'
                        else:
                            continue
                        # 写入数据到history.csv文件
                        writer.writerow({
                            'redeem': coupon,
                            'reward': '',
                            'hiveid': hiveid,
                            'server': server,
                            'date': row['date'],
                            'status': status
                        })
                        print(f"已更新历史数据：{coupon}  {hiveid}")
                        logging.debug(f"已更新历史数据：{coupon}  {hiveid}")
def main():
    """
    先更新history，后续更新reward字段
    """
    # 更新历史数据
    update_histary()

    # 创建奖励数据
    reward_data = load_reward_data()
    # 加载历史数据
    history_data = load_history_data()
    # 检查数据是否为空
    if not reward_data or not history_data:
        return
    # 更新reward字段
    updated = update_reward_field(reward_data, history_data)
    # 保存更新后的数据
    if updated:
        save_history_data(history_data)

if __name__ == "__main__":
    main()
