import urllib.request
import pprint
import json

def scryprint(string, indent=0):
    if string == list:
        for index in string:
            print(string)
    elif string == dict:
        pass
    else:
        print(string)

def getCard(searchquery):
    url = "https://api.scryfall.com/cards/search?&q=" + "is%3Afirstprint+oracle%3A" + searchquery

    response = urllib.request.urlopen(url)
    # requested = urllib.request.Request(url)
    # response = urllib.request.urlopen(requested) 로 쓸수도 있음
    # url can be either a string or a Request object.

    # 참고
    # type of reponse == http.client.HTTPResponse
    # type of reponse.read() == bytes
    # type of response.read().decode('utf-8') == str
    # type of json.loads(s=response.read().decode('utf-8')) == dict

    if (response.getcode() == 200):  # HTTP Status codes 200 == OK
        json_structure = json.loads(s=response.read().decode('utf-8'))
        # json_structure is <class 'dict'>
        # 둘다 str이지만 인자로 response.read()를 넣어야지 json_dump를 넣으면 pretty printing 안됨.
        if (json_structure["total_cards"]==1):  # 정확한 카드 매칭
            return json_structure["data"][0]
        elif (json_structure["total_cards"]>1):
            print("/"%s/" has not unique search result: %d many cards are found" % (searchquery, json_structure["total_cards"]))
        else:  # (json_structure["total_cards"]==0)
            print("no such card: %s" % searchquery)
    else:
        print("Error Code:" + rescode)

def prettyprint(data, indent=2, mode="pprint"):
    if (mode=="pprint"):
        pp = pprint.PrettyPrinter(indent)  # List object의 pretty printer.
        pp.pprint(data)
    elif (mode=="json.dump"):
        print(json.dumps(data, indent=indent))
    else:
        print("no such print mode")

# client_id = "MY_CLIENT_ID"  # 애플리케이션 등록시 발급 받은 값 입력
# client_secret = "MY_CLIENT_SECRET"  # 애플리케이션 등록시 발급 받은 값 입력

searchquery = input("search for: ")
result = getCard(searchquery)

prettyprint(result, 10, "json.dump")