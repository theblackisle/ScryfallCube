import urllib.request
import pprint
import json
import re
import http



def urlize(searchquery, sets="f", mode="exact", sort=None, order=None):
    if mode == "exact":
        url = "https://api.scryfall.com/cards/search?&q=%22{0}%22".format(re.sub(r' ', r'+', searchquery))  # ""없으면 "fire // ice"와 "Sword of Fire and Ice"이 같이 검색됨
    elif mode == "query":
        url = "https://api.scryfall.com/cards/search?&q={0}".format(re.sub(r' ', r'+', searchquery))

    if sets == "f":
        url = url + "+is%3Afirstprint"
    elif sets == "l":
        pass
    elif type(sets) == str:
        url = url + "+set%3A" + sets

    if type(sort) == str:
        url = url + "&order=" + sort

    if type(order) == str:
        url = url + "&dir=" + order

    return url

def getResponse(url):
    try:
        return urllib.request.urlopen(url)
        # requested = urllib.request.Request(url)
        # response = urllib.request.urlopen(requested) 로 쓸수도 있음
        # url can be either a string or a Request object.
    except UnicodeEncodeError:
        print("getCard: Unicode error")
        return "Unicode error"
    except urllib.error.HTTPError as error:
        print("getCard: HTTP %d error" % error.code)
        return "HTTP %d error" % error.code
    except Exception as e:
        print("getCard: unknown error")
        return "unknown error: %s" % e


def getCard(searchquery, sets="f"):

    response = getResponse(urlize(searchquery, sets=sets, mode="exact"))
    if type(response) == str:
        return None

    # 참고
    # type of reponse == http.client.HTTPResponse
    # type of reponse.read() == bytes
    # type of response.read().decode('utf-8') == str
    # type of json.loads(s=response.read().decode('utf-8')) == dict

    if response.getcode() == 200:  # HTTP Status codes 200 == OK
        json_structure = json.loads(s=response.read().decode('utf-8'))
        # 둘다 str이지만 인자로 response.read()를 넣어야지 json_dump를 넣으면 pretty printing 안됨.
        if json_structure["total_cards"] == 1:  # 정확한 카드 매칭
            return json_structure["data"][0]
        elif json_structure["total_cards"] > 1:
            for datum in json_structure["data"]:  # query에 ~~query, query~~가 반환된 경우
                if datum['name'].lower() == searchquery.lower():  # 정확한 카드 매칭 찾기
                    return datum

            print('''"%s" has not unique search result: %d many cards are found''' % (searchquery, json_structure["total_cards"]))
            return None
        else:  # (json_structure["total_cards"]==0)
            print("no such card: %s" % searchquery)
            return None
    else:
        print("getCard: HTTP %d error" % response.getcode())
        return None


def getMass(searchquery, sets="f", sort=None, order=None):

    response = getResponse(urlize(searchquery, sets=sets, mode="query", sort=sort, order=order))
    if type(response) == str:
        return None

    if response.getcode() == 200:  # HTTP Status codes 200 == OK
        json_structure = json.loads(s=response.read().decode('utf-8'))

        if json_structure["total_cards"] >= 1:
            return json_structure["data"]  # type == list

        else:  # (json_structure["total_cards"]==0)
            print("no such card: %s" % searchquery)
            return None
    else:
        print("getCard: HTTP %d error" % response.getcode())
        return None


def prettyprint(data, indent=2, mode="pprint"):
    if type(data) is dict:
        if mode == "pprint":
            pp = pprint.PrettyPrinter(indent)  # List object의 pretty printer.
            pp.pprint(data)
        elif mode == "json.dump":
            print(json.dumps(data, indent=indent))
        else:
            print("no such print mode")
    else:
        print('''prettyprinter: input "%s" is not dict type''' % data)


while __name__ == '__main__':
    searchquery = input("search for: ")
    if searchquery == "quit":
        break
    for card in getMass(searchquery):
        prettyprint(card, 4)


while __name__ == '__main__':
    searchquery = input("search for: ")
    if searchquery == "quit":
        break
    prettyprint(getCard(searchquery), 4)
