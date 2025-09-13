





import requests
TOKEN = '8477268497:AAHwB-2H9EDx2dQ'
ids = '550177'

message='placed order buy at price 200'
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ids}&parse_mode=Markdown&text={message}"
print(requests.get(url).json())