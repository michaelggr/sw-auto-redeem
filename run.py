from apscheduler.schedulers.background import BackgroundScheduler
import time
import logging
import os
import evt_coupon
import history
import reward
from send_email import send_daily_reward_emails
import swq
import task
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


# 定义任务函数
def check_and_run_evt_coupon():
    if os.path.getsize('task.json') > 0:
        evt_coupon.main()
        logging.info("evt_coupon.py运行完毕")
        logger.info("evt_coupon.py运行完毕")
    else:
        logging.info("task.json文件为空")
        logger.info("task.json文件为空")

def send_email_task():
    send_daily_reward_emails()
    logging.info("每天指定时间执行发邮件执行完毕")
    logger.info("每天指定时间执行发邮件执行完毕")

def swq_task():
    swq.main()
    logging.info("swq抓取兑换码任务执行完毕")
    logger.info("swq抓取兑换码任务执行完毕")

def reward_task():
    reward.main()
    logging.info("reward更新reward.csv任务执行完毕")
    logger.info("reward更新reward.csv任务执行完毕")

def task_task():
    task.main()
    logging.info("task更新task.json任务执行完毕")
    logger.info("task更新task.json任务执行完毕")

def history_task():
    history.main()
    logging.info("history更新history.csv任务执行完毕")
    logger.info("history更新history.csv任务执行完毕")

def get_env_var(var_name, default_value, var_type=int):
    value = os.getenv(var_name, default_value)
    if value is None:
        print(f"警告：{var_name} 环境变量未设置，使用默认值 {default_value}。")
        value = default_value
    return var_type(value)

# 从环境变量中读取时间间隔（以分钟为单位）环境变量叫redeem_time
redeem_time = get_env_var('REDEEM_TIME', '15')
# 从环境变量中读取发邮件时间（以小时为单位）环境变量叫EMAIL_TIME
email_time = get_env_var('EMAIL_TIME', '08:30', var_type=str)
# 从环境变量中读取抓取兑换码时间（以小时为单位）环境变量叫SWQ_TIME
swq_time = get_env_var('SWQ_TIME', '3')
# 从环境变量中读取生成reward.csv时间（以小时为单位）环境变量叫REWARD_TIME
reward_time = get_env_var('REWARD_TIME', '5')
# 从环境变量中读取生成task.json时间（以小时为单位）环境变量叫TASK_TIME
task_time = get_env_var('TASK_TIME', '5') 
# 从环境变量中读取生成history.csv时间（以小时为单位）环境变量叫HISTORY_TIME
history_time = get_env_var('HISTORY_TIME', '5')

def start_scheduler():
    scheduler = BackgroundScheduler()

    # 添加任务
    scheduler.add_job(swq_task, 'interval', minutes=swq_time)
    logger.info(f"swq抓取兑换码任务已添加，时间间隔为{swq_time}分钟")
    scheduler.add_job(reward_task, 'interval', minutes=reward_time)
    logger.info(f"reward更新reward.csv任务已添加，时间间隔为{reward_time}分钟")
    scheduler.add_job(task_task, 'interval', minutes=task_time)
    logger.info(f"task更新task.json任务已添加，时间间隔为{task_time}分钟")
    scheduler.add_job(history_task, 'interval', minutes=history_time)
    logger.info(f"history更新history.csv任务已添加，时间间隔为{history_time}分钟")
    scheduler.add_job(check_and_run_evt_coupon, 'interval', minutes=redeem_time)
    logger.info(f"evt_coupon.py任务已添加，时间间隔为{redeem_time}分钟")
    scheduler.add_job(send_email_task, 'cron', hour=email_time.split(':')[0], minute=email_time.split(':')[1])
    logger.info(f"每天指定时间执行发邮件任务已添加，时间为{email_time}")
    #每天5点重启app.py任务
    #scheduler.add_job(app.restart_app, 'cron', hour=5, minute=0)
    #logger.info(f"每天0点重启app.py任务已添加")
    # 启动调度器
    scheduler.start()
    logger.info(f"现有任务: {scheduler.get_jobs()}")
    # 保持主线程运行
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        # 关闭调度器
        scheduler.shutdown()
if __name__ == '__main__':
    print("主程序开始")
    start_scheduler()
    print("程序结束")