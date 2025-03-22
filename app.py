# 导入所需的模块
import hashlib
import json
import subprocess
import threading
from flask import (
    Flask, 
    request, 
    jsonify,
    send_file,
    send_from_directory,
    render_template, 
    redirect, 
    url_for, 
    session
)
import pandas as pd
import logging
import os
import sys
import time
import requests

from bind import checkUser, web_bind_player_info
from reward import check_redeem_code

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)
#文件路径
CONFIG_PATH = os.environ.get("CONFIG_PATH", "./config.json")
# 配置常量
CSV_FILE = 'Reward.csv'
CSV_ENCODING = 'utf-8'
LOCK = threading.Lock()  # 文件操作锁
# 读取环境变量
DEBUG = os.environ.get("DEBUG", False)

# 初始化日志配置
logging.basicConfig(
    filename='my_log.log',
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="[%(asctime)s][%(levelname)s] %(message)s",
    datefmt="%m-%d %H:%M:%S",
)
# 确保日志文件存在
if not os.path.exists('my_log.log'):
    open('my_log.log', 'a').close()

def gen_md5(string):
    md5 = hashlib.md5()
    md5.update(string.encode("utf-8"))
    return md5.hexdigest()

# 读取User.csv文件
def userread_csv():
    df = pd.read_csv('User.csv', encoding='utf-8')
    return df

# 写入User.csv文件
def userwrite_csv(df):
    df.to_csv('User.csv', encoding="utf-8",index=False)

# 读取 JSON 文件内容
def read_json():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

# 将数据写入 JSON 文件
def write_json(data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, sort_keys=False, indent=2)

def is_login():
    data = read_json()
    username = data["webui"]["username"]
    password = data["webui"]["password"]
    if session.get("login") == gen_md5(username + password):
        return True
    else:
        return False

# 创建 Flask 应用对象
app = Flask(__name__)
app.secret_key = "EoMUmW3PnmjY1Y"

# 设置icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )

# 登录页面
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = read_json()
        username = data["webui"]["username"]
        password = data["webui"]["password"]
        # 验证用户名和密码
        if (username == request.form.get("username")) and (
            password == request.form.get("password")
        ):
            logging.info(f">>> 用户 {username} 登录成功")
            session["login"] = gen_md5(username + password)
            return redirect(url_for("index"))
        else:
            logging.info(f">>> 用户 {username} 登录失败")
            return render_template("login.html", message="登录失败")

    return render_template("login.html", error=None)

# 退出登录
@app.route("/logout")
def logout():
    session.pop("login", None)
    return redirect(url_for("login"))

# 绑定页面
@app.route('/bind', methods=['GET', 'POST'])
def bind():
    if request.method == 'GET':
        return jsonify({'message': 'This is a GET request to /bind!'})
    elif request.method == 'POST':
        client_ip = request.remote_addr
        key = f'bind:cd:{client_ip}'
        current_time = time.time()

        # 获取当前 IP 的上次操作时间
        last_attempt = session.get(key, 0)

        # 检查是否在冷却时间内
        if current_time - last_attempt < 3:  # 3秒冷却时间
            return jsonify({'message': '操作过于频繁，请稍后再试'},content_type='text/plain; charset=utf-8'), 429

        # 执行绑定操作
        data = request.get_json()
        # 处理 POST 请求的数据wxid,hiveid,autonum,server,email,vip,vipcode
        wxid = data.get('wxid')
        hiveid = data.get('hiveid')
        autonum = data.get('autonum')
        server = data.get('server')
        email = data.get('email')
        vip = data.get('vip')
        vipcode = data.get('vipcode')

        # 调用函数检查用户是否存在checkUser(hiveid,server,redeem)
        redeem='sw2025jan6a8'
        if checkUser(hiveid,server,redeem)==False:
            # 终止绑定操作  
            return jsonify({'message': '无效的Hive ID。请重新确认或联系黑猫。'})

        # 调用函数进行绑定
        result = web_bind_player_info(wxid, hiveid, autonum, server, email, vip, vipcode)

        # 更新最后操作时间
        session[key] = current_time

        return jsonify({'message': result})
    else:
        return jsonify({'message': 'Invalid request method'})

# 管理页面
@app.route('/')
def index():
    return render_template('index.html')

# 获取最新奖励
@app.route('/reward')
def get_reward():
    return send_file('Reward.csv', mimetype='text/csv')

# 新增兑换码
@app.route('/add_code', methods=['POST'])
def add_code():
    data = request.get_json()
    # 处理 POST 请求的数据
    code = data.get('code')
     # 单次状态检查
    check_result = check_redeem_code(code)

    # 判断兑换码是否存在check_redeem_code(code)
    if check_result==False:
        return jsonify({'message': '兑换码格式错误或无效'})
    # 检查 code 是否已经存在
    if check_result== 'exist':
        return jsonify({'message': '兑换码已记录过,谢谢参与'})
    #检测兑换码是否过期
    if check_result== 'expired':
        return jsonify({'message': '兑换码已过期'})
    # # 读取 CSV 文件
    # df = pd.read_csv('Reward.csv', encoding='utf-8')

    # # 添加新行,包含redeem,reward,from
    # new_row = {'redeem': code,'reward': '','from': 'web'}
    # new_row_df = pd.DataFrame([new_row])  # 将字典转换为 DataFrame
    # df = pd.concat([df, new_row_df], ignore_index=True)  # 现在可以正确地拼接

    # # 保存更新后的 CSV 文件
    # df.to_csv('Reward.csv', encoding="utf-8",index=False)

    # return jsonify({'message': '兑换码新增成功，恭喜发财'})
    # 线程安全的文件操作
    with LOCK:
        # 自动创建不存在的文件
        if not os.path.exists(CSV_FILE):
            pd.DataFrame(columns=['redeem', 'reward', 'from']).to_csv(
                CSV_FILE, 
                encoding=CSV_ENCODING, 
                index=False
            )

        # 追加新记录
        new_record = pd.DataFrame([{
            'redeem': code,
            'reward': '',
            'from': 'web'
        }])
        
        # 使用追加模式写入（更高效）
        new_record.to_csv(
            CSV_FILE,
            mode='a',
            header=False,
            encoding=CSV_ENCODING,
            index=False
        )

    return jsonify({
        'status': 201,
        'message': '兑换码添加成功',
        'data': {
            'code': code,
            'source': 'web'
        }
    }), 201

# 获取历史记录
@app.route('/history')
def get_history():
    return send_file('history.csv', mimetype='text/csv')
# 新增接口：接收消息并运行 swq.py 脚本
@app.route('/trigger_swq', methods=['POST'])
def trigger_swq():
    try:
        data = request.get_json()
        message = data.get('message')
        if message == '抓取兑换码':
            logging.info("收到消息：抓取兑换码，开始运行 swq.py 脚本")
            result = subprocess.run(['python', 'swq.py'], capture_output=True, text=True)
            if result.returncode == 0:
                logging.info("swq.py 脚本执行成功")
                return jsonify({'message': 'swq.py 脚本执行成功'}), 200
            else:
                logging.error(f"swq.py 脚本执行失败: {result.stderr}")
                return jsonify({'message': f'swq.py 脚本执行失败: {result.stderr}'}), 500
        else:
            logging.info("收到的消息不是 '抓取兑换码'")
            return jsonify({'message': '收到的消息不是 "抓取兑换码"'}), 200
    except Exception as e:
        logging.error(f"处理请求时发生错误: {e}")
#新增接口：接收消息并运行task.py脚本
@app.route('/get_code', methods=['POST'])
def get_code():
    try:
        data = request.get_json()
        message = data.get('message')
        if message == '领取兑换码':
            logging.info("收到消息：领取兑换码，开始运行 task.py 脚本")
            result = subprocess.run(['python', 'task.py'], capture_output=True, text=True)
            if result.returncode == 0:
                logging.info("task.py 脚本执行成功")
                return jsonify({'message': 'task.py 脚本执行成功'}), 200
            else:
                logging.error(f"task.py 脚本执行失败: {result.stderr}")
                return jsonify({'message': f'task.py 脚本执行失败: {result.stderr}'}), 500
        else:
            logging.info("收到的消息不是 '领取兑换码'")
            return jsonify({'message': '收到的消息不是 "领取兑换码"'}), 200
    except Exception as e:
        logging.error(f"处理请求时发生错误: {e}")

@app.route('/get_rta_rank')
def get_rta_rank():
    try:
        # 发送GET请求获取数据
        response = requests.get('https://m.swranking.com/api/player/nowline')
        data = response.json()
        
        if data['retCode'] == 0 and 'data' in data:
            rank_data = data['data']
            
            # 提取各区域的分数
            gold_scores = f"{rank_data['c1']['score']},{rank_data['c2']['score']},{rank_data['c3']['score']}"
            green_scores = f"{rank_data['s1']['score']},{rank_data['s2']['score']},{rank_data['s3']['score']}"
            red_scores = f"{rank_data['g1']['score']},{rank_data['g2']['score']},{rank_data['g3']['score']}"
            
            # 组织返回数据
            result = f"金区{gold_scores}；绿区{green_scores}；红区{red_scores}"
            return jsonify({'message': result})
        else:
            return jsonify({'message': '获取数据失败'}), 500
            
    except Exception as e:
        logging.error(f"获取RTA分数线数据时发生错误: {e}")
        return jsonify({'message': '获取数据失败'}), 500

if __name__ == '__main__':
    # 启动 Flask 应用
    app.run(debug=DEBUG, host="0.0.0.0", port=5006)
