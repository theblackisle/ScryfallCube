import re
import pprint



import ScryfallIO
from Card import Card
from GsInterface import GsInterface


def printMenu():
    menu = []
    menu.append("1. Manage files and sheets.")
    menu.append("2. Search from Scryfall for exact card.")
    menu.append("3. Search from Scryfall with query.")
    menu.append("4. Prepare card data from unprepared sheet")
    menu.append("5. Match card for query from prepared sheet")

    for item in menu:
        print(item)

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

    for item in menu:
        print(item)

    choice = input("Select: ")
    try:
        print(menu[int(choice[0])-1][3:])
    except IndexError and ValueError:
        pass

    return choice

def printLocation(pointer):
    filename = pointer.file.title if pointer.file is not None else "None"
    sheetname = pointer.sheet.title if pointer.sheet is not None else "None"
    print('Open file: {0}\nOpen sheet: {1}'.format(filename, sheetname))

def selectFile(client, prompt):
    try:
        files = client.openall()
        for file in files:
            print("%2d. %-18s id:%s" % (files.index(file)+1, file.title, file.id))

        return input(prompt)

    except:
        print("Unable to open Google Spreadsheet")
        return None

def selectSheet(file, prompt):
    try:
        sheets = file.worksheets()
        for sheet in sheets:
            print("%2d. %s, id:%s" % (sheets.index(sheet)+1, sheet.title, sheet.id))

        return input(prompt)

    except:
        print("Unable to open spreadsheet file")
        return None

def parseIndex(inputs):
    indexlist = re.sub(r'[^\w-]+', r' ', inputs).split(" ")

    elselist = []
    intlist = set()
    exceptlist = set()
    for item in indexlist:
        if re.match(r'^[\d]+$', item):  # item이 정수
            intlist.add(int(item))
        elif re.match(r'^[\d]+-[\d]+$', item):  # item이 범위 지정
            item = list(map(int, item.split("-")))
            for i in range(min(item), max(item) + 1):
                intlist.add(i)
        elif re.match(r'^-[\d]+$', item):  # item이 예외 지정
            exceptlist.add(int(item.replace("-", "")))
        else:  # item이 숫자가 아님
            elselist.append(item)

    return elselist + list(intlist - exceptlist)  # 예외문자가 앞에 오게 조정

def parsecolumn(inputs):
    columnlist = re.sub(r'[^\w-]+', r' ', inputs).split(" ")

    elselist = []
    charlist = set()
    exceptlist = set()
    for item in columnlist:
        if re.match(r'^[\d]+$', item):  # item이 정수
            charlist.add(number_to_colchar(item))
        elif re.match(r'^[\d]+-[\d]+$', item):  # item이 범위 지정
            item = list(map(int, item.split("-")))
            for i in range(min(item), max(item) + 1):
                charlist.add(number_to_colchar(i))
        elif re.match(r'^-[\d]+$', item):  # item이 예외 지정
            exceptlist.add(number_to_colchar(int(item.replace("-", ""))))

        elif re.match(r'^[a-zA-Z]+$', item):  # item이 A1 notation
            charlist.add(item.upper())
        elif re.match(r'^[a-zA-Z]+-[a-zA-Z]+$', item):  # item이 A1 notation으로 범위 지정
            item = [colchar_to_number(component.upper()) for component in item.split("-")]
            for i in range(min(item), max(item) + 1):
                charlist.add(number_to_colchar(i))
        elif re.match(r'^-[a-zA-Z]+$', item):  # item이 A1 notation으로 예외 지정
            exceptlist.add((item.replace("-", "")).upper())

        else:  # item이 다른 어떤 것
            elselist.append(item)

    return elselist + sorted(list(charlist - exceptlist), key=lambda x: (len(x), x))  # sort 후 예외문자가 앞에 오게 조정

def number_to_colchar(value):

    div = int(value)
    column_label = ''

    while div:
        (div, mod) = divmod(div, 26)
        if mod == 0:
            mod = 26
            div -= 1
        column_label += chr(mod + 64)

    return column_label[::-1]

def colchar_to_number(value):

    col = 0
    for index, item in enumerate(value[::-1]):
        col += (ord(item) - 64) * (26 ** index)

    return col





if __name__ == '__main__':
    pointer = GsInterface('ScryfallCube-80b58226a864.json', 'ScryfallCubeIO', "2C", email="gattuk24@gmail.com")
    target = GsInterface('ScryfallCube-80b58226a864.json', email="gattuk24@gmail.com")
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
                    query = selectFile(pointer._client, 'Enter file index, name or ID: ')
                    if query[0:2] == "^q":
                        print("")
                        break
                    pointer.file = query
                    print("")
                    printLocation(pointer)

                while filechoice[0] == '2':  # 2. Open or create sheet
                    query = selectSheet(pointer.file, "Enter sheet index or name: ")
                    if query[0:2] == "^q":
                        print("")
                        break
                    pointer.sheet = query
                    print("")
                    printLocation(pointer)

                while filechoice[0] == '3':  # 3. Delete file
                    query = selectFile(pointer._client, 'Enter file index, name or ID to delete: ')
                    if query[0:2] == "^q":
                        print("")
                        break
                    if pointer.file.title == query:
                        pointer.mode = "deletion"
                        del pointer.file
                        pointer.mode = "default"
                    else:
                        target.mode = "deletion"
                        target.file = query
                        del target.file
                    print("")
                    printLocation(pointer)

                while filechoice[0] == '4':  # 4. Delete Sheet
                    query = selectSheet(pointer.file, "Enter sheet index or name to delete: ")
                    if query[0:2] == "^q":
                        print("")
                        break
                    if pointer.sheet.title == query:
                        pointer.mode = "deletion"
                        del pointer.sheet
                        pointer.mode = "default"
                    else:
                        target.mode = "deletion"
                        target.file = pointer.file
                        target.sheet = query
                        del target.sheet
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
                        pointer.sheet.importCard(card)
                    print("")

                else:
                    print("No search result.")


        if choice[0] == '3':  # 3. Search with Scryfall syntax.
            while True:
                query = input('Enter search query with Scryfall syntax: ')
                if query[0:2] == "^q":
                    print("")
                    break

                result = ScryfallIO.get_from_query(query)

                try:
                    cards = [Card(datum) for datum in result]
                    print("\nTotal %s cards are found." % len(result))

                    for card in cards:
                        print("%2d. %s" % (cards.index(card)+1, card.name))

                    selections = parseIndex(input("\nEnter card indices to import or range. Press Y to import all: "))

                    if type(selections[0]) is int:
                        for selection in selections:
                            pointer.sheet.importCard(cards[int(selection) - 1])
                    elif selections[0].lower() == "y":
                        pointer.sheet.importMass(cards)
                    else:
                        print("Import process aborted")

                    print("")
                except TypeError:
                    print("\nNo search result.\n")


        if choice[0] == '4':  # 4. Read card data from sheet
            while True:
                printLocation(pointer)
                columninput = parsecolumn(input('Enter source column values: '))
                rowinput = parseIndex(input("Enter source row index or range: "))

                sheetname = selectSheet(pointer.file, "Enter sheet index or name to save: ")
                if sheetname[0:2] == "^q":
                    print("")
                    break
                target.file = pointer.file
                target.sheet = sheetname

                print("")
                namelist = pointer.sheet.export_in_sheet(rowinput, columninput)
                datalist = ScryfallIO.getMass(namelist)
                cardlist = ScryfallIO.massive_data_to_Card(datalist)
                print("")
                target.sheet.importMass(cardlist)


        if choice[0] == '5':  # 5. Match card for query from prepared sheet
            while True:
                printLocation(pointer)

                query = input("Enter query to search: ")
                while query[0:2] == "^h":
                    print("")
                    print("prepend ! for negative search.      e.g) !Goblin")
                    print("add ^c for case-sensitive search. e.g) First strike ^c")
                    query = input("Enter query to search: ")

                columninput = parsecolumn(input('Enter column values to search in: '))

                mode = "default"
                case = "insensitive"
                if query[0] == "!":
                    mode = "negative"
                    query = query[1:]
                if re.search(r'\^c', query):
                    case = "sensitive"
                    query = re.sub(r'\^c', '', query)

                rowlist = pointer.sheet.findincol(query, columninput, mode=mode, case=case)

                print("\nSearch result:")
                for i in rowlist:
                    print(pointer.sheet.cell(i, 1).value)
                print("")

                sheetname = selectSheet(pointer.file, "Enter sheet index or name to save: ")
                if sheetname[0:2] == "^q":
                    print("")
                    break

                target.file = pointer.file
                target.sheet = sheetname
                print("")

                dataline = pointer.sheet.copyrows(rowlist)
                print("")
                target.sheet.pasterows(dataline)
                print("")

