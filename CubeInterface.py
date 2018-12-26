import re
import GspreadIO
import ScryfallIO
from Card import Card
from Converter import prettify


class CubeInterface:
    def __init__(self, credentials, filename=None, sheetname=None, email=None):
        self.email = email if email is not None else input("Enter User's email address: ")
        self._currentClient = GspreadIO.openGsClient(credentials)
        if self._currentClient is None:
            raise ValueError

        self.currentFile = filename
        self.currentSheet = sheetname  # setter 사용

    @property
    def currentFile(self):
        return self._currentFile

    @currentFile.setter
    def currentFile(self, filename):
        if filename is None:  # if type(A) is type(None) || if A is None 형식으로 써야
            self._currentFile = None

        elif type(filename) is str:
            if filename in [found.title for found in self._currentClient.openall()]:
                self._currentFile = self._currentClient.open(filename)
                self._currentSheet = self._currentFile.get_worksheet(0)
                print("File '%s' is open" % filename)
            else:
                self._currentFile = self._currentClient.create(filename)
                self._currentSheet = self._currentFile.get_worksheet(0)
                self._currentFile.share(self.email, perm_type='user', role='writer')
                print("File '%s' is created" % filename)

        else:
            print("inappropriate file name")

    @currentFile.getter
    def currentFile(self):
        return self._currentFile

    @currentFile.deleter
    def currentFile(self):
        self._currentClient.del_spreadsheet(self._currentFile.id)
        self._currentFile = None
        self._currentSheet = None


    @property
    def currentSheet(self):
        return self._currentSheet

    @currentSheet.setter
    def currentSheet(self, sheetname):
        if sheetname is None:
            self._currentSheet = None

        elif type(sheetname) is str:
            if sheetname in [found.title for found in self._currentFile.worksheets()]:
                self._currentSheet = self._currentFile.worksheet(sheetname)
                print("Sheet '%s' is open" % sheetname)
            else:
                self._currentSheet = self._currentFile.add_worksheet(sheetname, 1, 18)
                print("Sheet '%s' is created" % sheetname)

        else:
            print("inappropriate Sheet name")

    @currentSheet.getter
    def currentSheet(self):
        return self._currentSheet

    @currentSheet.deleter
    def currentSheet(self):
        self._currentFile.del_worksheet(self._currentSheet)
        self._currentSheet = None


    def deleteFile(self, query):
        if type(query) is str:
            if query in [found.id for found in self._currentClient.openall()]:  # query is an ID value
                filename = self._currentClient.open_by_key(query).title
                if (self._currentFile is not None) and (self._currentFile.id == query):
                    del self.currentFile  # deleter 사용
                else:
                    self._currentClient.del_spreadsheet(query)
                print("File '%s: %s' is deleted" % (filename, query))

            elif query in [found.title for found in self._currentClient.openall()]:  # query is a name of file
                if (self._currentFile is not None) and (self._currentFile.id == self._currentClient.open(query).id):
                    del self.currentFile
                else:
                    self._currentClient.del_spreadsheet(self._currentClient.open(query).id)
                print("File '%s' is deleted" % query)

            else:
                print("No such name to delete: %s" % query)

        else:
            print("Inappropriate file name")

    def deleteSheet(self, query):
        if type(query) is str:
            if query in [found.title for found in self._currentFile.worksheets()]:  # query is a name of file
                result = self._currentFile.worksheet(query)
                if (self._currentSheet is not None) and (self._currentSheet.id == result.id):
                    del self.currentSheet  # deleter 사용
                else:
                    self._currentFile.del_worksheet(result)
                print("Sheet '%s' is deleted\n" % query)

            else:
                print("No such name to delete: %s" % query)

        else:
            print("Inappropriate sheet name")


    def exportCard(self, card):
        self._currentSheet.append_row(prettify(card.gsExport()))
        print("{0} is recorded in {1}".format(card.name, self._currentSheet.title))


    def searchExportCard(self, cardname, sets='f'):
        card = Card(ScryfallIO.getCard(cardname, sets=sets))
        self._currentSheet.append_row(prettify(card.gsExport()))
        print("{0} is recorded in {1}".format(card.name, self._currentSheet.title))

    def exportMass(self, cardlist):
        for card in cardlist:
            self._currentSheet.append_row(prettify(card.gsExport()))
            print("{0} is recorded in {1}".format(card.name, self._currentSheet.title))

    def searchExportMass(self, searchquery, sets='f', sort=None, order=None):
        cardlist = ScryfallIO.getMass(searchquery, sets=sets, sort=sort, order=order)
        for datum in cardlist:
            card = Card(datum)
            self._currentSheet.append_row(prettify(card.gsExport()))
            print("{0} is recorded in {1}".format(card.name, self._currentSheet.title))

    def importCard(self, row):
        card = Card(prettify(self._currentSheet.row_values(row), mode="reverse"))
        return card

    def importMass(self, start=1, end=None):  # spread sheet의 start는 0이 아님
        if end is None:
            end = self._currentSheet.row_count

        cardlist = []
        for i in range(start, end+1):  # 1에서 'end'까지
            cardlist.append(Card(prettify(self._currentSheet.row_values(i), mode="reverse")))

        return cardlist

    def findcell(self, query):
        regexp = re.compile(r'([\s]|^)' + query)
        try:
            return self._currentSheet.find(regexp)
        except GspreadIO.gspread.exceptions.CellNotFound:  # gspread는 GspreadIO에 import되어있음
            print('Cannot find "%s" in %s' % (query, self._currentSheet.title))
            return None

    def findcardname(self, query):
        regexp = re.compile(r'([\s]|^)' + query)
        try:
            result = self._currentSheet.find(regexp)
            return self._currentSheet.cell(result.row, 1)
        except GspreadIO.gspread.exceptions.CellNotFound:  # gspread는 GspreadIO에 import되어있음
            print('Cannot find "%s" in %s' % (query, self._currentSheet.title))
            return None

    def findincol(self, query, *columns):
        found_row = set()
        if query[0] == "!":  # Not 검색
            query = query[1:]
            for i in columns:  # columns = tuple
                row_list = set([found.row for found
                                in self._currentSheet.range("{0}1:{0}{1}".format(i, self._currentSheet.row_count))
                                if not re.search(query, found.value)])  # r'([\s]|^)' + query
                found_row = found_row & row_list if len(found_row) != 0 else row_list  # 논리적 교집합 구현
        else:
            for i in columns:  # columns = tuple
                row_list = set([found.row for found
                                in self._currentSheet.range("{0}1:{0}{1}".format(i, self._currentSheet.row_count))
                                if re.search(query, found.value)])  # r'([\s]|^)' + query
                found_row |= row_list  # set 합집합연산자 |의 __iadd__

        print("found_row length: %d" % len(found_row))
        return sorted(list(found_row))

    def copyrows(self, rows, sheetname, mode="newfile"):  # rows = list of row values(=int).
        row_data = []
        for i in rows:
            row_data.append(self._currentSheet.row_values(i))


        if mode == "newfile":
            if sheetname in [found.title for found in self._currentFile.worksheets()]:
                newsheet = self._currentFile.worksheet(sheetname)
            else:
                newsheet = self._currentFile.add_worksheet(sheetname, 0, 0)
                print(len(row_data))

            for i in range(len(row_data)):
                print(row_data[i])
                newsheet.insert_row(row_data[i], i+1)
            newsheet.resize(len(row_data), len(row_data[0]))

        return row_data




if __name__ == '__main__':
    MyCube = CubeInterface('ScryfallCube-80b58226a864.json')
    MyCube.currentFile = 'ScryfallCubeIO'
    MyCube.currentSheet = "시트1"
    # MyCube.currentSheet("시트1")은 안통함. property에는 __call__ method가 없음!

    # print(MyCube.importCard(12).showCard())
    # MyCube.importMass()

    while True:
        searchquery = input("findcol: ")
        if searchquery == "quit":
            break
        sheetname = input("sheetname: ")
        foundrow = MyCube.findincol(searchquery, "G")
        MyCube.copyrows(foundrow, sheetname)

    while True:
        searchquery = input("find: ")
        if searchquery == "quit":
            break
        print("%s is in %s" % (searchquery, MyCube.findthatcard(searchquery).value))

    while True:
        searchquery = input("find: ")
        if searchquery == "quit":
            break
        MyCube.findcell(searchquery)
        print("%s is in (%s, %s)" % (searchquery, MyCube.findcell(searchquery).row, MyCube.findcell(searchquery).col))

    while True:
        searchquery = input("put query: ")
        if searchquery == "quit":
            break
        MyCube.searchExportMass(searchquery, sort="released", order="asc")

    while True:
        searchquery = input("put card: ")
        if searchquery == "quit":
            break
        MyCube.searchExportCard(searchquery)

    # print(MyCube.currentSheet.get_all_records())
