import requests

def send_message_to_wecomchan(msg, msg_type='text'):
    url = f'http://192.168.0.14:32772/wecomchan?sendkey=abcde007&msg={msg}&msg_type={msg_type}'
    response = requests.get(url)
    return response.text



# 使用示例
#sendkey = 'abcde007'
#msg = 'test'

