import urllib.request
import pprint
import json

client_id = "MY_CLIENT_ID"  # 애플리케이션 등록시 발급 받은 값 입력
client_secret = "MY_CLIENT_SECRET"  # 애플리케이션 등록시 발급 받은 값 입력

#searchquery = input("search for: ")
url = "https://api.scryfall.com/cards/search?&q=" + "is%3Afirstprint+oracle%3A" + "spelltwine" #searchquery
#requested = urllib.request.Request(url)
#response = urllib.request.urlopen(requested) #url can be either a string or a Request object.
response = urllib.request.urlopen(url)


rescode = response.getcode()
if (rescode == 200): #HTTP Status codes 200 == OK
    response_body = response.read().decode('utf-8') # response_body is <class 'str'>
    #type of reponse.read() == bytes
    #type of response.read().decode() == str

    #json_dump = json.dumps(response_body) # json_dump is <class 'str'>
    json_structure = json.loads(s=response_body) # json_structure is <class 'dict'> #인자로 response_body를 넣으면 pretty printing 됨. json_dump를 넣으면 안됨.


    pp = pprint.PrettyPrinter(indent=4) #List object의 pretty printer.
    pp.pprint(response.getheaders())
    print("\n")
    print("response_body is %s" % type(response_body))
    #print("json_body is %s" % type(json_dump))
    print("json_structure is %s" % type(json_structure))
    print("\n")
    print(json.dumps((json_structure), indent=4))
else:
    print("Error Code:" + rescode)