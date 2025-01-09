import portalocker
import pandas as pd
import requests
import os
import logging
import time

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
def read_user_csv():
    """
    读取User.csv文件并返回DataFrame。
    如果文件不存在或读取失败，返回None。
    """
    try:
        with open('User.csv', 'rb') as file:
            #print("File content:")
            #print(file.read())
            file.seek(0)  # 重置文件指针到文件开头
            portalocker.lock(file, portalocker.LOCK_EX)
            try:
                user_df = pd.read_csv(file)
            # 检查DataFrame是否为空
                if user_df.empty:
                    user_df.columns = ['wxid', 'hiveid', 'autonum', 'server', 'email', 'vip', 'vipcode']
                return user_df
            except pd.errors.EmptyDataError:
                return pd.DataFrame(columns=['wxid', 'hiveid', 'autonum', 'server', 'email', 'vip', 'vipcode'])
            except Exception as e:
                print(f"读取User.csv失败: {e}") 
                logging.debug(f"读取User.csv失败: {e}")
                return None
            finally:
                portalocker.unlock(file)
    except Exception as e:
        print(f"读取User.csv失败: {e}") 
        return None

def write_user_csv(user_df):
    """
    将DataFrame写入User.csv文件。
    如果写入失败，返回False，否则返回True。
    """
    try:
        with open('User.csv', 'w', encoding='utf-8') as file:
            portalocker.lock(file, portalocker.LOCK_EX)
            try:
                user_df.to_csv(file, index=False, encoding='utf-8')
                return True
            except Exception as e:
                print(f"写入User.csv失败: {e}")
                logging.debug(f"写入User.csv失败: {e}")
                return False
            finally:
                portalocker.unlock(file)
    except Exception as e:
        print(f"写入User.csv失败: {e}")
        return False

def checkUser(hiveid,server,redeem):
    """
    检查用户是否存在。
    如果用户存在，返回True，否则返回False。
    """
    # 构建请求URL
    url = 'https://event.withhive.com/ci/smon/evt_coupon/useCoupon'
    # 构建表单数据
    form_data = {
            'country': 'HK',
            'lang': 'zh-hans',
            'server': server,
            'hiveid': hiveid,
            'coupon': redeem
        }
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://event.withhive.com',
        'Referer': 'https://event.withhive.com/ci/smon/evt_coupon',
        'host': "event.withhive.com",
        'X-Requested-With': "XMLHttpRequest",
    }
    #加延迟
    time.sleep(3)
    # 发送POST请求
    response = requests.post(url, data=form_data,headers=headers)
    #返回内容包含 "retCode": 503，代表用户不存在
    if response.status_code == 200:
        data = response.json()
        if data['retCode'] == 503:
            print(f"{'hiveid'}用户不存在")
            logging.debug(f"{'hiveid'}用户不存在")
            return False   
        else:
            print(f"{'hiveid'}用户存在")
            logging.debug(f"{'hiveid'}用户存在")
            return True
    else:
        #打印返回的数据
        print(response.text)
        logging.debug(f"请求失败",response.text)
        return False
def web_bind_player_info(wxid, hiveid, autonum, server, email, vip, vipcode):
    # 构建绑定信息的字典
    bind_info = {
        'wxid': wxid,
        'hiveid': hiveid,
        'autonum': autonum,
        'server': server,
        'email': email,
        'vip': vip,
        'vipcode': vipcode
    }
    # 读取User.csv文件
    user_df = read_user_csv()
    # 检查user_df是否成功加载
    if user_df is not None:
        # 检查是否已经存在相同的hiveid
        bind_hiveid = bind_info['hiveid']
        #print(bind_hiveid)
        #print(user_df)
        if bind_hiveid in user_df['hiveid'].values:
            # 如果已存在相同的hiveid，返回错误消息:bind_hiveid值已存在，请重新输入
            #print("bind_hiveid值已存在，请重新输入")
            return f"{bind_hiveid}已存在，请重新输入"
        else:
            #检查vipcode是否存在相同的值
            if vipcode in user_df['vipcode'].values:
                # 如果存在相同的vipcode，将新的绑定信息添加到DataFrame中
                # 将新的绑定信息添加到DataFrame中
                new_row = pd.DataFrame([bind_info])
                user_df = pd.concat([user_df, new_row], ignore_index=True)
                # 将更新后的数据保存回User.csv文件
                if write_user_csv(user_df):
                    return "绑定信息已成功添加。光暗发货中"
                else:
                    return "绑定信息添加失败。页面底部私信联系"
            else:
                return "vip code错误，请重新输入"

    else:
        # 如果user_df加载失败，打印错误信息
        print("从User.csv加载数据失败。")   
def test():
    # 定义玩家信息
    wxid = "player_wxid"
    hiveid = "samuer007"
    autonum = "10" 
    server = "china"
    email = "player_email"
    vip = "0"
    vipcode = "blackcat"
    redeem="sw2025jan6a8"
    # 调用绑定信息函数
    result = web_bind_player_info(wxid,hiveid,autonum,server,email,vip,vipcode)
    print(result)
    #调用checkUser函数
    result = checkUser(hiveid,server,redeem)
    print(result)
    """ user_df = read_user_csv()
    print(user_df) """
