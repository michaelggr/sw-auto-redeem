
#!/bin/bash

# 启动第一个Python脚本
python run.py &

# 启动第二个Python脚本
python app.py &

# 等待所有后台任务完成
wait
