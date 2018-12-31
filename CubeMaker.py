import re
import pprint

import gspread
import ScryfallIO
from Card import Card
from GsInterface import GsInterface

def printmenu():
    menu = []
    menu.append("1. Manage files and sheets.")
    menu.append("2. Search exact card from Scryfall.")
    menu.append("3. Search with Scryfall syntax.")
    menu.append("4. Read card data from sheet")

    print("Menu\n{0}\n{1}\n{2}\n{3}".format(menu[0], menu[1], menu[2], menu[3]))
    choice = input("Select: ")
    try:
        print(menu[int(choice[0])-1][3:])
    except:
        pass

    return choice

def printfilemenu():
    menu = []
    menu.append("1. Open or create file")
    menu.append("2. Open or create sheet")
    menu.append("3. Delete file")
    menu.append("4. Delete Sheet")

    print("{0}\n{1}\n{2}\n{3}".format(menu[0], menu[1], menu[2], menu[3]))
    choice = input("Select: ")
    try:
        print(menu[int(choice[0])-1][3:])
    except:
        pass

    return choice

def printlocation(cube):
    filename = cube.file.title if cube.file is not None else "None"
    sheetname = cube.sheet.title if cube.sheet is not None else "None"
    print('Current file: {0}\nCurrent sheet: {1}'.format(filename, sheetname))

if __name__ == '__main__':
    myCube = GsInterface('ScryfallCube-80b58226a864.json', 'ScryfallCubeIO', "2C", "gattuk24@gmail.com")
    print("")

    while True:
        choice = printmenu()
        print("")

        if choice[0] == '1':
            while True:
                filechoice = printfilemenu()
                if filechoice[0:2] == "^q":
                    print("")
                    break
                print("")
                printlocation(myCube)

                while filechoice[0] == '1':
                    pprint.PrettyPrinter(2).pprint(myCube._currentClient.openall())
                    query = input('Enter file name or ID: ')
                    if query[0:2] == "^q":
                        print("")
                        break
                    myCube.file = query
                    print("")
                    printlocation(myCube)

                while filechoice[0] == '2':
                    pprint.PrettyPrinter(2).pprint(myCube.file.worksheets())
                    query = input('Enter sheet name: ')
                    if query[0:2] == "^q":
                        print("")
                        break
                    myCube.sheet = query
                    print("")
                    printlocation(myCube)

                while filechoice[0] == '3':
                    pprint.PrettyPrinter(2).pprint(myCube._currentClient.openall())
                    query = input('Enter file name or ID: ')
                    if query[0:2] == "^q":
                        print("")
                        break
                    myCube.deleteFile(query)
                    print("")
                    printlocation(myCube)

                while filechoice[0] == '4':
                    pprint.PrettyPrinter(2).pprint(myCube.file.worksheets())
                    query = input('Enter sheet name: ')
                    if query[0:2] == "^q":
                        print("")
                        break
                    myCube.deleteSheet(query)
                    print("")
                    printlocation(myCube)

        if choice[0] == '2':
            while True:
                query = input('Enter cardname (and setcode) in "name @set" form: ')
                if query[0:2] == "^q":
                    print("")
                    break
                query = query.split("@", 1)
                result = ScryfallIO.getCard(query[0],
                                            sets=query[1].upper().strip() if len(query) > 1 else "f")

                if result is not None:
                    card = Card(result)
                    print("")
                    card.showCard()
                    print("")

                    if input("Export this card to current sheet(Y/N): ")[0].lower() == "y":
                        myCube.exportCard(card)
                    print("")

                else:
                    print("No search result.")

        if choice[0] == '3':
            while True:
                query = input('Enter search query with Scryfall syntax: ')
                if query[0:2] == "^q":
                    print("")
                    break

                result = ScryfallIO.getMass(query)

                try:
                    cards = [Card(datum) for datum in result]
                    print("\ntotal %s cards are found." % len(result))

                    for card in cards:
                        print("%2d. %s" % (cards.index(card)+1, card.name))

                    selections = re.sub(r'[\W]+', r' ', input("\nEnter card indices to export OR press Y to export all: ") ).split(" ")
                    if selections[0].lower() == "y":
                        for card in cards:
                            myCube.exportCard(card)
                    if re.match(r'\d', selections[0]):
                        try:
                            for selection in selections:
                                myCube.exportCard(cards[int(selection)-1])
                        except TypeError:
                            print("Inappropriate index input.")

                    print("")
                except TypeError:
                    print("\nNo search result.\n")

        if choice[0] == '4':
            while True:
                columninput = re.sub(r'[\W]+', r' ', input('\nEnter source column values: ')).split(" ")
                print(columninput)

                rowinput = re.sub(r'[\W]+', r' ', input('\nEnter source row range: ')).split(" ")
                print(rowinput)

                savedestine = input('Save to: ')

                cardlist = myCube.importinsheet(rowinput[0], rowinput[1], *tuple(columninput))

                tempsheet = myCube.sheet
                myCube.sheet = savedestine
                myCube.exportMass(cardlist)
                myCube.sheet = tempsheet



