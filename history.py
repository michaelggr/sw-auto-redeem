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
        with open('Reward.csv', 'r', encoding='utf-8') as reward_file:
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
        with open('history.csv', 'r', encoding='utf-8') as history_file:
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
    updated = False
    for row in history_data:
        if row['redeem'] in reward_data:
            row['reward'] = reward_data[row['redeem']]
            updated = True
    return updated

def main():
    """
    主函数
    """
    print("开始执行reward更新操作")
    logging.info("开始执行reward更新操作")
    reward_data = load_reward_data()
    history_data = load_history_data()
    if not reward_data or not history_data:
        return
    initial_file_size = os.path.getsize('history.csv')
    updated = update_reward_field(reward_data, history_data)
    save_history_data(history_data)
    final_file_size = os.path.getsize('history.csv')

    if final_file_size == initial_file_size:
        print("无更新。")
        logging.debug("reward无更新。")
    elif updated:
        print("reward字段已更新。")
        logging.debug("reward字段已更新。")
    else:
        print("文件大小发生了变化，但reward字段未更新。")
        logging.debug("文件大小发生了变化，但reward字段未更新。")

if __name__ == "__main__":
    main()
