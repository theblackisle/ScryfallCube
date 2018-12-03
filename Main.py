import urllib.request
import json

client_id = "MY_CLIENT_ID"  # 애플리케이션 등록시 발급 받은 값 입력
client_secret = "MY_CLIENT_SECRET"  # 애플리케이션 등록시 발급 받은 값 입력ß

searchquery = input("search for: ")
url = "https://api.scryfall.com/cards/search?&q=" + "is%3Afirstprint+oracle%3A" + searchquery
#requested = urllib.request.Request(url)
#response = urllib.request.urlopen(requested)
response = urllib.request.urlopen(url)
rescode = response.getcode()
if (rescode == 200):
    response_body = response.read()
    print(response_body)
else:
    print("Error Code:" + rescode)

#json_rt = response.read().decode('utf-8')
#py_rt = json.loads(json_rt)