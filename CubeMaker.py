import pprint
import re


import ScryfallIO
from Card import Card
from CubeInterface import CubeInterface


if __name__ == '__main__':
    MyCube = CubeInterface('ScryfallCube-80b58226a864.json', 'ScryfallCubeIO', "시트1")

    while True:
        print('''Current file: {0}
Current sheet: {1}
'''.format(MyCube.currentFile.title, MyCube.currentSheet.title))
        print('''Menu
0. Move to other file and sheet.
1. Search exact card from Scryfall.
2. Search with Scryfall syntax.
3. Search card ''')
        direction = input("Select: ")

        if direction[0] == '0':
            query = input('\nEnter filename: ')
            if query[0:2] == "\\q":
                print("")
            else:
                MyCube.currentFile = query
                print(MyCube._currentClient.openall())
                print("Move to file: %s\n" % query)

            query = input('Enter sheetname: ')
            if query[0:2] == "\\q":
                print("")
            else:
                MyCube.currentSheet = query
                print("Move to Sheet: %s\n" % query)

        if direction[0] == '1':
            while True:
                query = input('\nEnter cardname (and setcode) in "name @set" form: ')
                if query[0:2] == "\\q":
                    print("")
                    break
                query = query.split("@", 1)

                result = ScryfallIO.getCard(query[0],
                                            sets=query[1] if len(query) > 1 else "f",
                                            mode="query" if len(query) > 1 else "exact")

                if result is not None:
                    card = Card(ScryfallIO.getCard(query[0], result))  # exact mode + set검색 = 에러
                    print("")
                    card.showCard()

                    if input("\nExport this card to current sheet(Y/N): ")[0].lower() == "y":
                        MyCube.exportCard(card)
                else:
                    print("\nNo search result.")

        if direction[0] == '2':
            while True:
                query = input('\nEnter search query with Scryfall syntax: ')
                if query[0:2] == "\\q":
                    print("")
                    break

                result = ScryfallIO.getMass(query, sets="l" if query.find("is:firstprint") != -1
                                                               or query.find("set:") != -1
                                                            else "f")  # query에서 직접 set 정해줄때 조건,
                                                            # tescase:(oracle:pay oracle:2 oracle:life) type:land set:rtr

                try:
                    cards = [Card(datum) for datum in result]
                    for card in cards:
                        print(card.name)
                    if input("\nExport those card to current sheet(Y/N): ")[0].lower() == "y":
                        for card in cards:
                            MyCube.exportCard(card)
                except TypeError:
                    print("\nNo search result.")

        if direction[0] == '3':
            pass
