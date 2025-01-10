# 使用具体版本的Python镜像
FROM python:3.13-alpine

# 设置工作目录
WORKDIR /app
# 复制应用程序源代码 
COPY . .
# 安装依赖并清理缓存
RUN pip install --no-cache-dir -r requirements.txt && \
    find /usr/local -type f -name '*.pyc' -delete && \
    find /usr/local -type d -name '__pycache__' -delete && \
    rm -rf /root/.cache/pip

# 确保Python脚本中的输出能够立即被打印
ENV PYTHONUNBUFFERED=1

# 端口
EXPOSE 5006
#环境变量
ENV SENDER_EMAIL=19945037382@163.com
ENV SENDER_PASSWORD=ZPMC4NvQEGTe2jfx
ENV TZ=Asia/Shanghai
ENV DEBUG=False
ENV EMAIL_TIME=12:00
ENV HISTORY_TIME=30
ENV REDEEM_TIME=21
ENV REWARD_TIME=11
ENV SWQ_TIME=6
ENV TASK_TIME=16

# 启动命令，先运行 run.py，然后启动 Flask 应用
CMD ["sh", "-c", "python run.py & python -m flask run --host=0.0.0.0 --port=5006"]