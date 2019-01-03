import urllib.request
import pprint
import json
import re

from Card import Card


def urlize(searchquery, sets="f", mode="exact", sort=None, order=None):

    if mode == "exact" and (sets == "f" or sets == "l" or sets == "default") and searchquery.find("set:") == -1:
        #  Scryfall api bug: exact mode + set검색 = 에러
        url = "https://api.scryfall.com/cards/search?&q=%22{0}%22".format(re.sub(r' ', r'+', searchquery))
        # ""없으면 "fire // ice"와 "Sword of Fire and Ice"이 같이 검색됨
    else:
        url = "https://api.scryfall.com/cards/search?&q={0}".format(re.sub(r' ', r'+', searchquery))

    if sets == "f" and searchquery.find("is:firstprint") == -1 and searchquery.find("set:") == -1:
        #  searchquery에서 직접 set 정해줄때는 "is:firstprint"를 붙이지 않는다.
        #  testcase: (oracle:pay oracle:2 oracle:life) type:land set:rtr
        url = url + "+is%3Afirstprint"
    elif sets == "l" or sets == "default":
        pass  # "lastprint"가 default임
    elif type(sets) == str:
        url = url + "+set%3A" + sets

    if type(sort) == str:
        url = url + "&order=" + sort

    if type(order) == str:
        url = url + "&dir=" + order

    # debug - print("sets=%s, mode=%s, sort=%s, order=%s" % (sets, mode, sort, order) )
    # debug - print(url)
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


def getCard(searchquery, sets="f", mode="exact"):

    response = getResponse(urlize(searchquery, sets=sets, mode=mode))
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
            for single_json in json_structure["data"]:  # query에 xxxquery, queryxxx가 반환된 경우
                if single_json['name'].lower() == searchquery.lower():  # 정확한 카드 매칭 찾기
                    return single_json

            print('''"%s" has not unique search result: %d many cards are found'''
                  % (searchquery, json_structure["total_cards"]))
            return None
        else:  # (json_structure["total_cards"]==0)
            print("no such card: %s" % searchquery)
            return None
    else:
        print("getCard: HTTP %d error" % response.getcode())
        return None

def getMass(namelist, sets="f", mode="exact"):
    jsons = []
    for name in namelist:
        jsons.append(getCard(name, sets=sets, mode=mode))

    return jsons

def massive_data_to_Card(jsons):
    cardlist = []
    for single_json in jsons:
        cardlist.append(Card(single_json))
    return cardlist


def get_from_query(searchquery, sets="f", sort=None, order=None):
    #  sets = "l" if searchquery.find("is:firstprint") != -1 or searchquery.find("set:") != -1 else "f"
    #  searchquery에서 직접 set 정해줄때 조건

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

def row_to_card():
    pass



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
    for card in get_from_query(searchquery):
        prettyprint(card, 4)


while __name__ == '__main__':
    searchquery = input("search for: ")
    if searchquery == "quit":
        break
    prettyprint(getCard(searchquery), 4)
