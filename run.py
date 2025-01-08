import schedule
import time
import logging
import os
import app
import evt_coupon
import history
import reward
from send_email import send_daily_reward_emails
import swq
import task
from concurrent.futures import ThreadPoolExecutor
from logging.handlers import RotatingFileHandler

# 检查环境变量DEBUG，并设置日志级别
debug_mode = os.getenv('DEBUG', 'false').lower() == 'true'
log_level = logging.DEBUG if debug_mode else logging.INFO

# 设置日志格式
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 创建日志器
logger = logging.getLogger('my_logger')
logger.setLevel(log_level)

# 创建一个按大小分割的日志处理器，最多备份5个日志文件，每个日志文件最大10MB
file_handler = RotatingFileHandler('my_log.log', maxBytes=10*1024*1024, backupCount=5)
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

# 添加一个StreamHandler，用于输出日志到控制台
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

# 使用日志器记录信息
logger.info('这是一条信息日志')
logger.debug('这是一条调试日志（仅在DEBUG模式下显示）')

# 启动 Flask 应用
app.app.run(debug=logging.DEBUG, host="0.0.0.0", port=5006)
# 定义任务函数
def check_and_run_evt_coupon():
    if os.path.getsize('task.json') > 0:
        evt_coupon.main()
        logging.info("evt_coupon.py运行完毕")
    else:
        logging.info("task.json文件为空")

def send_email_task():
    send_daily_reward_emails()
    logging.info("已安排在每天的指定时间执行发邮件。")

def swq_task():
    swq.main()
    logging.info("swq抓取兑换码任务执行完毕")

def reward_task():
    reward.main()
    logging.info("reward更新reward.csv任务执行完毕")

def task_task():
    task.main()
    logging.info("task更新task.json任务执行完毕")

def history_task():
    history.main()
    logging.info("history更新history.csv任务执行完毕")

# 从环境变量中读取时间间隔（以分钟为单位）环境变量叫redeem_time
redeem_time = os.getenv('REDEEM_TIME', '15')
if redeem_time is None:
    print("警告：REDEEM_TIME 环境变量未设置，使用默认值 15。")
    redeem_time = '15'
# 转换为整数
redeem_time = int(redeem_time)

# 从环境变量中读取时间
email_time = os.getenv('EMAIL_TIME', '08:30')
if email_time is None:
    print("警告：EMAIL_TIME 环境变量未设置，使用默认值 08:30。")
    email_time = '08:30'


# 从环境变量中读取时间
swq_time = os.getenv('SWQ_TIME', '10')
if swq_time is None:
    print("警告：SWQ_TIME 环境变量未设置，使用默认值 10。")
    swq_time = '10'
# 转换为整数
swq_time = int(swq_time)

# 从环境变量中读取时间
reward_time = os.getenv('REWARD_TIME', '5')
if reward_time is None:
    print("警告：REWARD_TIME 环境变量未设置，使用默认值 5。")
    reward_time = '5'
# 转换为整数
reward_time = int(reward_time)

# 从环境变量中读取时间
task_time = os.getenv('TASK_TIME', '5')
if task_time is None:
    print("警告：TASK_TIME 环境变量未设置，使用默认值 5。")
    task_time = '5' 
# 转换为整数
task_time = int(task_time)

# 从环境变量中读取时间
history_time = os.getenv('HISTORY_TIME', '15')
if history_time is None:
    print("警告：HISTORY_TIME 环境变量未设置，使用默认值 15。")
    history_time = '15'
# 转换为整数
history_time = int(history_time)

# 创建线程池
executor = ThreadPoolExecutor(max_workers=15)

# 每指定分钟数执行一次任务
executor.submit(schedule.every(swq_time).minutes.do, swq_task)
logging.info(f"{swq_time}分钟执行一次swq抓取兑换码")

# 每指定分钟数执行一次任务
executor.submit(schedule.every(reward_time).minutes.do, reward_task)
logging.info(f"{reward_time}分钟执行一次reward更新reward.csv")

# 每指定分钟数执行一次任务
executor.submit(schedule.every(task_time).minutes.do, task_task)
logging.info(f"{task_time}分钟执行一次task更新task.json")

# 每指定分钟数执行一次任务
executor.submit(schedule.every(history_time).minutes.do, history_task)
logging.info(f"{history_time}分钟执行一次history更新history.csv")


# 每指定分钟数执行一次任务
executor.submit(schedule.every(redeem_time).minutes.do, check_and_run_evt_coupon)
logging.info(f"{redeem_time}分钟执行一次领取任务")

# 安排任务在每天的指定时间执行
executor.submit(schedule.every().day.at(email_time).do, send_email_task)
logging.info(f"已安排在每天的 {email_time} 执行发邮件。")


# 启动定时任务
logging.info("定时任务已启动")

# 打印任务列表
logging.info(schedule.jobs)

# 打印正在运行的任务
logging.info(schedule.get_jobs())

# 无限循环，保持程序运行
while True:
    # 运行所有计划的任务
    schedule.run_pending()
    # 等待1秒
    time.sleep(1)
