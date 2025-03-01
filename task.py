# 任务生成器：读取User.csv文件,读取Reward.csv文件，获取redeem，每一条redeem数据和user获取uid和server的每一行组成一个列表，存入到task.json文件中，hiveid=uid，server=serve,coupon=redeem

# 导入json库，用于处理JSON数据

import json
# 导入pandas库，用于数据处理和分析
import pandas as pd
# 导入os库，用于操作系统相关的功能
import os


#日志记录器
import logging

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

# 定义一个函数，用于加载用户数据
def load_user_data():
    """
    从User.csv文件中加载用户数据
    """
    user_data = []
    try:
        user_data = pd.read_csv('User.csv').to_dict('records')
    except FileNotFoundError:
        print("User.csv文件未找到")
    except Exception as e:
        print(f"读取User.csv文件时发生错误: {e}")
    return user_data

# 定义一个函数，用于加载奖励数据
def load_reward_data():
    """
    从Reward.csv文件中加载奖励数据
    """
    reward_data = []
    try:
        reward_data = pd.read_csv('Reward.csv').to_dict('records')
    except FileNotFoundError:
        print("Reward.csv文件未找到")
    except Exception as e:
        print(f"读取Reward.csv文件时发生错误: {e}")
    return reward_data

# 定义一个函数，用于生成任务数据并保存到task.json文件
def generate_task_data():
    """
    生成任务数据并保存到task.json文件
    """
    #打印开始生成任务数据
    logging.info("开始生成任务数据")
    print("开始生成任务数据")
    # 调用load_user_data函数加载用户数据
    user_data = load_user_data()
    # 调用load_reward_data函数加载奖励数据
    reward_data = load_reward_data()
    # 如果用户数据和奖励数据都不为空
    if user_data and reward_data:
        # 初始化一个空列表，用于存储任务数据
        task_data = []
        # 遍历每一行用户数据
        for user_row in user_data:
            # 遍历每一行奖励数据
            for reward_row in reward_data:
                # 将用户数据和奖励数据组合成一个任务数据字典，并添加到任务数据列表中
                task_data.append({
                    'hiveid': user_row['hiveid'],
                    'server': user_row['server'],
                    'coupon': reward_row['redeem']
                })
        try:
            #从任务数据列表排除掉已领取过的数据，排除规则为三个字段值相同。已领取成功数据在history.csv中
            history_data = pd.read_csv('history.csv').to_dict('records')
            # 遍历每一行历史数据
            for history_row in history_data:
                # 遍历每一行任务数据
                for task_row in task_data:
                    # 如果任务数据和历史数据的hiveid、server和coupon都相同
                    if task_row['hiveid'] == history_row['hiveid'] and task_row['server'] == history_row['server'] and task_row['coupon'] == history_row['redeem']:
                        # 从任务数据列表中删除该任务数据
                        task_data.remove(task_row)
                        # 打印已排除的任务数据
                        logging.debug(f"已排除任务数据: {task_row}")
            # 如果任务数据列表为空
            if not task_data:
                # 打印没有任务数据需要处理
                print("没有任务数据需要处理")
                #写入空数据到task.json文件
                with open('task.json', 'w') as json_file:
                    json.dump([], json_file)
                    # 打印已排除的任务数据
                    logging.debug("没有任务数据需要处理")
                # 返回
                return 
            # 打开task.json文件，如果文件不存在则创建，如果文件存在则清空内容
            with open('task.json', 'w') as json_file:
                # 将任务数据列表转换为JSON格式，并写入到task.json文件中
                json.dump(task_data, json_file)
            # 打印成功保存的任务数据条数
            print(f"成功保存了 {len(task_data)} 条数据到 task.json")
            # 打印成功保存的任务数据条数
            logging.info(f"成功保存了 {len(task_data)} 条数据到 task.json")
        except Exception as e:
            # 打印保存数据到task.json文件失败的错误信息
            print(f"保存数据到task.json文件失败: {e}")
            logging.error(f"保存数据到task.json文件失败: {e}")


def main():
    generate_task_data()
if __name__ == "__main__":
    #如果task.json文件不为空，运行evt_coupon函数
    if os.path.getsize('task.json') > 0:
        import evt_coupon
        evt_coupon.main()
        print("evt_coupon.py运行完毕")
        logging.info("evt_coupon.py运行完毕")
    else:
        print("task.json文件为空")
        logging.info("无任务数据，task.json文件为空")
    main()
