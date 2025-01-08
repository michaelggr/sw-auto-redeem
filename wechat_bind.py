# wechat机器人交互器
#待完成
import pandas as pd
from reward import updata_from_wechat

#玩家信息绑定器.py
def bind_player_info(wxid,hiveid,autonum,server,email,vip,vipcode):
    """
    绑定玩家信息到微信。

    参数:
    wxid (str): 微信ID。
    hiveid (str): 玩家ID。
    autonum (str): 次数，分享有效兑换码+10次。
    server (str): 服务器。
    email (str): 电子邮箱。
    vip (str): 会员。
    vipcode (str): 会员码。


    返回:
    str: 绑定成功的消息。
    """
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
#新增绑定信息数据，写入User.csv文件中。 
    # 读取User.csv文件
    try:
        # 使用pandas的read_csv函数读取CSV文件
        user_df = pd.read_csv('User.csv')   
    except Exception as e:
        # 如果读取失败，将user_df设置为None，并打印错误信息
        user_df = None
        print(f"读取User.csv失败: {e}") 
    # 检查user_df是否成功加载
    if user_df is not None:
        # 将新的绑定信息添加到DataFrame中
        new_row = pd.DataFrame([bind_info])
        user_df = pd.concat([user_df, new_row], ignore_index=True)
        # 将更新后的数据保存回User.csv文件
        try:
            user_df.to_csv('User.csv', index=False)
            print(f"绑定信息已成功添加到User.csv文件。")
        except Exception as e:
            print(f"保存更新后的数据到User.csv文件失败: {e}")   
    else:
        # 如果user_df加载失败，打印错误信息
        print("从User.csv加载数据失败。")   
    return "绑定成功"                    
    
# 定义玩家信息
wxid = "player_wxid"
hiveid = "player_hiveid"
autonum = "10" 
server = "player_server"
email = "player_email"
vip = "0"
vipcode = "blackcat"

#根据聊天消息获取玩家的微信wxid
#玩家发送/魔灵绑定，回复对方绑定模板：hiveid，server，email，vipcode
#玩家发送字符串，判断为兑换码且对方的wxid存在于User.csv时，调用兑换码生成器，更新 reward表格，更新玩家的兑换次数。
# 领取器领取成功后，调用邮件发送器，发送邮件通知玩家兑换码领取成功。
# 调用 bind_player_info 函数，并传入玩家信息
bind_result = bind_player_info(wxid,hiveid,autonum,server,email,vip,vipcode)

# 打印绑定结果
print(bind_result)


#如果已绑定，返回：
# 定义 redeem 和 hiveid 的值
#redeem = "44889"
#hiveid = "test1"

# 调用 updata_from_wechat 函数，并传入 redeem 和 hiveid 参数
#result = updata_from_wechat(redeem, hiveid)

# 打印返回的结果
#print(result)