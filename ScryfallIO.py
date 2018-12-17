import urllib.request
import pprint
import json
import re

def getCard(searchquery):
    url = "https://api.scryfall.com/cards/search?&q=" + re.sub(r' ', r'+', searchquery) + "+is%3Afirstprint"

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
        # 둘다 str이지만 인자로 response.read()를 넣어야지 json_dump를 넣으면 pretty printing 안됨.
        if (json_structure["total_cards"]==1):  # 정확한 카드 매칭
            return json_structure["data"][0]
        elif (json_structure["total_cards"]>1):
            print('''"%s" has not unique search result: %d many cards are found''' % (searchquery, json_structure["total_cards"]))
            return searchquery
        else:  # (json_structure["total_cards"]==0)
            print("no such card: %s" % searchquery)
            return searchquery
    else:
        print("Error Code:" + rescode)

def prettyprint(data, indent=2, mode="pprint"):
    if (type(data)==dict):
        if (mode=="pprint"):
            pp = pprint.PrettyPrinter(indent)  # List object의 pretty printer.
            pp.pprint(data)
        elif (mode=="json.dump"):
            print(json.dumps(data, indent=indent))
        else:
            print("no such print mode")
    else:
        print('''prettyprinter: input "%s" is not a Mtg card''' % data)

while(__name__ == '__main__'):
    searchquery = input("search for: ")
    if searchquery == "quit":
        break
    prettyprint(getCard(searchquery), 4)