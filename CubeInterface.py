import re
import GspreadIO
import ScryfallIO
from Card import Card
from Converter import prettify


class CubeInterface():
    def __init__(self, credentials, filename=None, sheetname=None):
        self._currentClient = GspreadIO.openGsClient(credentials)
        if self._currentClient is None:
            raise ValueError
        self._currentFile = GspreadIO.openGsFile(self._currentClient, filename) if type(filename) is str else None
        self._currentSheet = self._currentFile.worksheet(sheetname) if type(sheetname) is str else None

    @property
    def currentFile(self):
        return self._currentFile

    @currentFile.setter
    def currentFile(self, filename):
        if type(filename) is str:
            self._currentFile = GspreadIO.openGsFile(self._currentClient, filename)
        else:
            print("inappropriate file name")

    @currentFile.getter
    def currentFile(self):
        return self._currentFile

    @property
    def currentSheet(self):
        return self._currentSheet

    @currentSheet.setter
    def currentSheet(self, sheetname):
        if type(sheetname) is str:
            self._currentSheet = self._currentFile.worksheet(sheetname)
        else:
            print("inappropriate sheet name")

    @currentSheet.getter
    def currentSheet(self):
        return self._currentSheet

    def exportCard(self, Card):
        self._currentSheet.append_row(prettify(Card.gsExport()))

    def searchExportCard(self, cardname, sets='f'):
        card = Card(ScryfallIO.getCard(cardname, sets=sets))
        print("{0} is recorded in {1}".format(card.name, self._currentSheet.title))
        self._currentSheet.append_row(prettify(card.gsExport()))

    def exportMass(self, cardlist):
        for datum in cardlist:
            print("{0} is recorded in {1}".format(card.name, self._currentSheet.title))
            self._currentSheet.append_row(prettify(card.gsExport()))

    def searchExportMass(self, searchquery, sets='f', sort=None, order=None):
        cardlist = ScryfallIO.getMass(searchquery, sets=sets, sort=sort, order=order)
        for datum in cardlist:
            card = Card(datum)
            print("{0} is recorded in {1}".format(card.name, self._currentSheet.title))
            self._currentSheet.append_row(prettify(card.gsExport()))

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
        regexp = re.compile(r'([\s]*|^)' + query)
        try:
            return self._currentSheet.find(regexp)
        except GspreadIO.gspread.exceptions.CellNotFound:  # gspread는 GspreadIO에 import되어있음
            print('Cannot find "%s" in %s' % (query, self._currentSheet.title))
            return None

    def findcardname(self, query):
        regexp = re.compile(r'([\s]*|^)' + query)
        try:
            result = self._currentSheet.find(regexp)
            return self._currentSheet.cell(result.row, 1)
        except GspreadIO.gspread.exceptions.CellNotFound:  # gspread는 GspreadIO에 import되어있음
            print('Cannot find "%s" in %s' % (query, self._currentSheet.title))
            return None

    def findincol(self, query, *columns):
        found_row = set()
        for i in columns:  # columns = tuple
            row_list = set([found.row for found in self._currentSheet.range("{0}1:{0}{1}".format(i, self._currentSheet.row_count)) if re.search(query, found.value)])  # r'([\s]|^)' + query
            found_row |= row_list  # set 합집합연산자 |의 __iadd__

        return sorted(list(found_row))

    def copyrows(self, rows, mode="newfile"):  # rows = list of row values(=int).
        rowlist = []
        for i in rows:
            rowlist.append(self._currentSheet.row_values(i))

        print(rowlist)

        if mode == "newfile":
            newsheet = self._currentFile.add_worksheet("asdfasdf", 20, 18)

            for i in range(len(rowlist)):
                for j in range(18):
                    newsheet.update_cell(i+1, j+1, rowlist[i][j])  # 너무느림, 구글 Quota 넘김...
        return rowlist




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
        foundrow = MyCube.findincol(searchquery, "H", "K")
        print(foundrow)
        MyCube.copyrows(foundrow)

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
