import re
import pprint

import ScryfallIO
from Card import Card
from GsInterface import GsInterface


def printMenu():
    menu = []
    menu.append("1. Manage files and sheets.")
    menu.append("2. Search exact card from Scryfall.")
    menu.append("3. Search with Scryfall syntax.")
    menu.append("4. Read card data from sheet")

    print("Menu\n{0}\n{1}\n{2}\n{3}".format(menu[0], menu[1], menu[2], menu[3]))
    choice = input("Select: ")
    try:
        print(menu[int(choice[0])-1][3:])
    except IndexError and ValueError:
        pass

    return choice


def printFileMenu():
    menu = []
    menu.append("1. Open or create file")
    menu.append("2. Open or create sheet")
    menu.append("3. Delete file")
    menu.append("4. Delete Sheet")

    print("{0}\n{1}\n{2}\n{3}".format(menu[0], menu[1], menu[2], menu[3]))
    choice = input("Select: ")
    try:
        print(menu[int(choice[0])-1][3:])
    except IndexError and ValueError:
        pass

    return choice


def printLocation(pointer):
    filename = pointer.file.title if pointer.file is not None else "None"
    sheetname = pointer.sheet.title if pointer.sheet is not None else "None"
    print('Opened file: {0}\nOpened sheet: {1}'.format(filename, sheetname))


def selectFile(client):
    try:
        files = client.openall()
        for file in files:
            print("%2d. %-18s id:%s" % (files.index(file)+1, file.title, file.id))

        return input('Enter file index, name or ID: ')

    except:
        print("Unable to open Google Spreadsheet")
        return None


def selectSheet(file):
    try:
        sheets = file.worksheets()
        for sheet in sheets:
            print("%2d. %s, id:%s" % (sheets.index(sheet)+1, sheet.title, sheet.id))

        return input('Enter sheet index or name: ')

    except:
        print("Unable to open spreadsheet file")
        return None


def parseIndex(inputs):
    indexlist = re.sub(r'[^\w-]+', r' ', inputs).split(" ")

    charlist = []
    intlist = set()
    exceptlist = set()
    for item in indexlist:
        if re.match(r'^[\d]+$', item):  # item이 정수
            intlist.add(int(item))
        elif re.match(r'^[\d]-[\d]', item):  # item이 범위 지정
            item = list(map(int, item.split("-")))
            for i in range(min(item), max(item) + 1):
                intlist.add(i)
        elif re.match(r'^-[\d]', item):  # item이 예외 지정
            exceptlist.add(int(item.replace("-", "")))
        else:  # item이 숫자가 아님
            charlist.append(item)

    totallist = charlist + list(intlist - exceptlist)
    print(totallist)

    return totallist # 문자가 앞에 오게 조정


if __name__ == '__main__':
    pointer = GsInterface('ScryfallCube-80b58226a864.json', 'ScryfallCubeIO', "시트1", email="gattuk24@gmail.com")#'ScryfallCubeIO', "2C",
    print("")

    while True:
        choice = printMenu()
        if choice[0:2] == "^q":
            break
        print("")

        if choice[0] == '1':  # 1. Manage files and sheets.
            while True:
                filechoice = printFileMenu()
                if filechoice[0:2] == "^q":
                    print("")
                    break
                print("")
                printLocation(pointer)

                while filechoice[0] == '1':  # 1. Open or create file
                    query = selectFile(pointer._client)
                    if query[0:2] == "^q":
                        print("")
                        break
                    pointer.file = query
                    print("")
                    printLocation(pointer)

                while filechoice[0] == '2':  # 2. Open or create sheet
                    query = selectSheet(pointer.file)
                    if query[0:2] == "^q":
                        print("")
                        break
                    pointer.sheet = query
                    print("")
                    printLocation(pointer)

                while filechoice[0] == '3':  # 3. Delete file
                    pprint.PrettyPrinter(2).pprint(pointer._client.openall())
                    query = input('Enter file name or ID: ')
                    if query[0:2] == "^q":
                        print("")
                        break
                    pointer._client.del_spreadsheet(pointer._client.open(query).id)
                    print("")
                    printLocation(pointer)

                while filechoice[0] == '4':  # 4. Delete Sheet
                    pprint.PrettyPrinter(2).pprint(pointer.file.worksheets())
                    query = input('Enter sheet name: ')
                    if query[0:2] == "^q":
                        print("")
                        break
                    pointer.file.del_worksheet(pointer.file.worksheet(query))
                    print("")
                    printLocation(pointer)

        if choice[0] == '2':  # 2. Search exact card from Scryfall.
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
                        pointer.sheet.exportCard(card)
                    print("")

                else:
                    print("No search result.")

        if choice[0] == '3':  # 3. Search with Scryfall syntax.
            while True:
                query = input('Enter search query with Scryfall syntax: ')
                if query[0:2] == "^q":
                    print("")
                    break

                result = ScryfallIO.getMass(query)

                try:
                    cards = [Card(datum) for datum in result]
                    print("\nTotal %s cards are found." % len(result))

                    for card in cards:
                        print("%2d. %s" % (cards.index(card)+1, card.name))

                    selections = parseIndex(input("\nEnter card indices to export OR press Y to export all: "))

                    if type(selections[0]) is int:
                        try:
                            for selection in selections:
                                pointer.sheet.exportCard(cards[int(selection) - 1])
                        except TypeError:
                            print("Inappropriate index input.")
                    elif selections[0].lower() == "y":
                        pointer.sheet.exportMass(cards)

                    print("")
                except TypeError:
                    print("\nNo search result.\n")

        if choice[0] == '4':  # 4. Read card data from sheet
            while True:
                columninput = re.sub(r'[\W]+', r' ', input('\nEnter source column values: ')).split(" ")
                print(columninput)

                rowinput = re.sub(r'[\W]+', r' ', input('\nEnter source row range: ')).split(" ")
                print(rowinput)

                savedestine = input('Save to: ')

                cardlist = pointer.importinsheet(rowinput[0], rowinput[1], *tuple(columninput))

                tempsheet = pointer.sheet
                pointer.sheet = savedestine
                pointer.exportMass(cardlist)
                pointer.sheet = tempsheet



