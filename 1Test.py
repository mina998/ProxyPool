from db import RedisClient
import requests
from fake_useragent import UserAgent

headers = {'User-Agent': UserAgent().random}

# print(headers)

redis = RedisClient()

ip = redis.pop()

if ip == '': exit('88')

proxy = {'http': ip, 'https': ip}

print(ip)

url = 'http://2019.ip138.com/ic.asp'

try:

    h = requests.get(url, headers=headers, proxies=proxy, timeout=3)
    h.encoding = 'gbk'

    print(h.status_code)

    print(h.text)

except Exception as e:

    print(e)
