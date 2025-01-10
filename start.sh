#!/bin/sh

# 运行第一个 Python 脚本
python ./run.py &

# 运行第二个 Python 脚本
python ./app.py &

# 等待所有后台进程
wait
