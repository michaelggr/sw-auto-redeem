import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import pandas as pd
import os

def send_email(sender_email, sender_password, receiver_email, subject, message, max_retries=3, retry_interval=5):
    for attempt in range(max_retries):
        try:
            # 创建一个多部分邮件对象
            msg = MIMEMultipart()
            msg['From'] = "魔灵召唤"
            msg['To'] = receiver_email
            msg['Subject'] = subject

            # 添加邮件正文
            if isinstance(message, MIMEText):
                msg.attach(message)
            else:
                msg.attach(MIMEText(message, 'plain'))

            # 使用SSL连接连接到SMTP服务器
            server = smtplib.SMTP_SSL('smtp.163.com', 465)
            # server.starttls()  # 启用TLS加密
            server.login(sender_email, sender_password)  # 登录到SMTP服务器
            server.sendmail(sender_email, receiver_email, msg.as_string())  # 发送邮件
            server.quit()  # 关闭SMTP连接
            print("邮件发送成功")
            #打印信息记录到auto_redeem.log
            with open('auto_redeem.log', 'a') as log_file:
                log_file.write(f"邮件发送成功\n")
            return  # 邮件发送成功，退出循环
        except smtplib.SMTPServerDisconnected as e:
            print(f"连接意外关闭，尝试重新连接 (第{attempt + 1}次)")
            time.sleep(retry_interval)  # 等待一段时间后重试
        except Exception as e:
            print(f"邮件发送失败: {str(e)}")
            return  # 其他异常，退出循环

    print("邮件发送失败，已达到最大重试次数")

def send_daily_reward_emails():
    data_list=[]
    email_set_list=[]

    # 读取CSV文件
    try:
        # 使用pandas的read_csv函数读取CSV文件
        history_df = pd.read_csv('history.csv')
    except Exception as e:
        # 如果读取失败，将history_df设置为None，并打印错误信息
        history_df = None
        print(f"读取history.csv失败: {e}")

    # 检查history_df是否成功加载
    if history_df is not None:
        #确定昨天日期的格式，并在 history.csv 中筛选出昨天的数据。
        # 获取昨天的日期
        yesterday = pd.Timestamp.now().date() - pd.Timedelta(days=1)
        # 筛选出昨天的数据
        yesterday_data = history_df[history_df['date'].str.contains(str(yesterday))]
        # 当 hiveid 相同且 server 相同时，将多条 redeem进行拼接
        # 遍历筛选出的昨天数据
        for index, row in yesterday_data.iterrows():
            hiveid = row['hiveid']
            #print(f"hiveid: {hiveid}")
            # 查找与hiveid匹配的行
            matching_rows = yesterday_data[yesterday_data['hiveid'] == hiveid]
            # 检查是否找到匹配的行
            if not matching_rows.empty:
                # 拼接redeem数据
                redeem = ', '.join(matching_rows['redeem'].values)
                # 拼接reward数据
                reward = ', '.join(map(str, matching_rows['reward'].values))

                #print(f"redeem: {redeem}, reward: {reward}, hiveid: {hiveid}")
                 # 将数据存储为一组
                data_set = {                      
                        'redeem': redeem,
                        'reward': reward,
                        'hiveid': hiveid
                    }
                # 将数据组添加到列表中
                data_list.append(data_set)
        #print(data_list)                        
        # 使用pandas的read_csv函数读取CSV文件
        user_df = pd.read_csv('User.csv')
        # 使用 data_list中 的hiveid 在 User.csv 中匹配对应的 email作为新的一列
        for data_set in data_list:
            hiveid = data_set['hiveid']
            # 查找与hiveid匹配的行
            matching_row = user_df[user_df['hiveid'] == hiveid]
            # 检查是否找到匹配的行
            if not matching_row.empty:
                # 获取email的值
                email = matching_row['email'].values[0]
                redeem = data_set['redeem']
                reward = data_set['reward']
                #print(f"email: {email}, redeem: {redeem}, reward: {reward}, hiveid: {hiveid}")
                # 将数据存储为一组
                email_set = {                      
                        'redeem': redeem,
                        'reward': reward,
                        'hiveid': hiveid,
                        'email': email
                    }
                email_set_list.append(email_set)

    # 使用集合来存储唯一的元组表示
    unique_dicts = set()

    # 存储去重后的字典列表
    unique_list = []

    for d in email_set_list:
        # 将字典转换为元组，由于顺序不重要，直接使用元组
        tuple_representation = tuple(d.items())
        # 如果元组不在集合中，则添加到集合和结果列表中
        if tuple_representation not in unique_dicts:
            unique_dicts.add(tuple_representation)
            unique_list.append(d)

    #print(unique_list)
    email_set_list=unique_list
    print(email_set_list)

# 读取email_set_list批量发送多封邮件
    for email_set in email_set_list:
        email = email_set['email']
        redeem = email_set['redeem']
        reward = email_set['reward']
        #print(f"email: {email}, redeem: {redeem}, reward: {reward}")
        # 从环境变量中获取 sender_email
        # 假设环境变量名为 'SENDER_EMAIL'
        sender_email = os.getenv('SENDER_EMAIL')
        # 检查环境变量是否已设置
        if sender_email:
            print(f"The sender email is: {sender_email}")
        else:
            print("The SENDER_EMAIL 环境变量未设置.")
        # 假设环境变量名为 'SENDER_PASSWORD'
        sender_password = os.getenv('SENDER_PASSWORD')
        # 检查环境变量是否已设置
        if sender_password:
            print(f"The sender password is set.")  # 注意：出于安全考虑，不应该打印密码
        else:
            print("The SENDER_PASSWORD environment variable is not set.")
        sender_password = 'ZPMC4NvQEGTe2jfx'
        subject = (f"昨日兑换码：{redeem}")
        message = MIMEText(f"昨日奖励：{reward}")
        send_email(sender_email, sender_password, email, subject, message)
# 使用示例
#send_daily_reward_emails()



