#激活码生成器
#制定规则，一个激活码只能用十次
#设置环境变量作为激活码使用次数
#生成vipcode.json文件存放激活码
import os
import pandas as pd # 导入pandas库
import logging
import csv
import random   # 导入random库
# 定义颜色和动物列表
colors = ["red", "blue", "green", "yellow", "black", "white", "purple", "orange", "pink", "brown"]
animals = ["cat", "dog", "elephant", "lion", "tiger", "bear", "monkey", "rabbit", "horse", "sheep"]
# 读取环境变量
DEBUG = os.environ.get("DEBUG", False)
set_usenum = os.environ.get("USENUM", 10)
#设置文件地址
vipcode_file = 'vipcode.csv'
User_file = 'User.csv'



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

#写入vipcode到CSV文件函数
def write_to_csv(file_path, new_data):
    """
    将新数据写入CSV文件
    """
    try:
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_data)
        return True
    except Exception as e:
        logging.error(f"Error writing to CSV file: {e}")
        return False


# 读取CSV文件函数
def read_csv(file_path):
    """
    读取CSV文件并返回DataFrame对象
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        return None

# 生成激活码
def generate_vipcode():
    """
    生成随机的激活码，使用颜色和动物
    """
    while True:
        # 随机选择颜色和动物
        code = random.choice(colors) + random.choice(animals)
        # 检查激活码是否已经存在
        if not is_vipcode_exists(code):
            # 新增激活码到vipcode.csv文件中
            new_data = [code, 0]
            # 写入新数据到CSV文件           
            write_to_csv(vipcode_file, new_data)
            return code
        else:
            # 激活码已经存在，重新生成
            continue


def is_vipcode_exists(vipcode):
    """
    检查激活码是否已经存在于vipcode.csv文件中
    """
    # 读取CSV文件
    vipcodes = read_csv(vipcode_file)
    # 检查激活码是否已经生成过
    if vipcodes is not None and vipcode in vipcodes['vipcode'].values:
        return True
    else:
        return False

#激活码验证器
def validate_vipcode(vipcode):
    """
    验证激活码是否有效，制定规则，一个激活码只能用十次。超出10次返回False
    """
    # 在这里添加你的激活码验证逻辑
    # 你可以使用pandas库来读取CSV文件并进行验证
    # 激活码存在于vipcode.csv文件中时从User.csv判断使用次数超过10次返回激活码超出使用次数
    # 激活码不存在时返回False
    # 读取CSV文件
    vipcodes = read_csv(vipcode_file)
    # 读取CSV文件
    df = read_csv(User_file)
    # 检查激活码是否已经生成过
    if vipcode in vipcodes['vipcode'].values:
        # 激活码使用次数定义为激活码存在于User.csv文件中vipcode列重复出现的次数
        # 统计到User.csv中的激活码使用次数并写入vipcode中的usenum列
        #激活码如果未使用过返回True
        if vipcode not in df['vipcode'].values:
            return True
        else:
            #激活码如果使用过则统计到User.csv中的激活码使用次数并写入vipcode中的usenum列
            # 统计激活码使用次数
            usenum = df['vipcode'].value_counts()[vipcode]
            # 打印激活码使用次数
            logging.debug(f"激活码 {vipcode} 已经使用 {usenum} 次")
            # 写入激活码使用次数到vipcode.csv文件中
            vipcodes.loc[vipcodes['vipcode'] == vipcode, 'usenum'] = usenum
            # 写入CSV文件
            vipcodes.to_csv(vipcode_file, index=False)
            # 判断激活码使用次数是否超过10次
            if usenum < int(set_usenum):
                return True
            else:
                return f"激活码超出使用次数{usenum}，页面底部私信黑猫获取新的激活码"
    else:
        #return vipcode不存在,请重新输入
        return "vipcode不存在,请重新输入"
    
    

# 主函数
def main():
    # 生成新的激活码
    new_vipcode = generate_vipcode()
    print("生成新的激活码:", new_vipcode)
    # 验证激活码
    vipcode='bluedog'
    validation_result = validate_vipcode(vipcode)
    print(f"{validation_result}")

if __name__ == "__main__":
    main()


