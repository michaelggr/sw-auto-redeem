#!/bin/sh

# 运行第一个 Python 脚本
python ./swq.py &

# 运行第二个 Python 脚本
python ./reward.py &

# 运行第二个 Python 脚本
python ./task.py &
# 等待所有后台进程
wait
