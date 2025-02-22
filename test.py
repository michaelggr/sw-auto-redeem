#
# test
import requests
url = 'https://swar.520199405.xyz:16666/add_code'
#提取兑换码，去掉兑换码前缀
msg='兑换码swelishere'
code = msg.replace('兑换码', '').strip()
print(code)
data = {'code': code}
headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=data, headers=headers)
print(response.json())