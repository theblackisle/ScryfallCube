import urllib.request
import pprint
import json
import re


def getCard(searchquery, sets="f"):

    url = 'https://api.scryfall.com/cards/search?&q=%22{0}%22'.format( re.sub(r' ', r'+', searchquery) )
    if sets == "f":
        url = url + "+is%3Afirstprint"
    elif sets == "l":
        pass
    elif type(sets) == str:
        url = url + "+set%3A" + sets

    try:
        response = urllib.request.urlopen(url)
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
            print('''"%s" has not unique search result: %d many cards are found''' % (
                searchquery, json_structure["total_cards"]))
            return searchquery
        else:  # (json_structure["total_cards"]==0)
            print("no such card: %s" % searchquery)
            return searchquery
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
    prettyprint(getCard(searchquery), 4)
