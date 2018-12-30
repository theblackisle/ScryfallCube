import re
import gspread

import GspreadIO
import ScryfallIO
from Card import Card
from Converter import prettify


class GsClient(gspread.Client):
    """
    ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
    '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__',
    '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__',
    '__subclasshook__', '__weakref__',
    'copy', 'create', 'del_spreadsheet', 'import_csv', 'insert_permission', 'list_permissions',
    'list_spreadsheet_files', 'login', 'open', 'open_by_key', 'open_by_url', 'openall', 'remove_permission', 'request']
    """

    def __init__(self, gsclient):
        self.__gsclient = gsclient

    def __setattr__(self, attr, val):
        if attr == '_GsClient__gsclient':
            super().__setattr__(attr, val)
            # _GsClient__gsclient 만 예외적으로 자기 attr에 두기 위한 목적의 코드
            # 그냥 __setattr__호출시 무한루프
            # super().__setattr__(attr, val) 또는 object.__setattr__(attr, val)로 빠져나가야.

        else:
            setattr(self.__gsclient, attr, val)
            # setattr(self.__a, attr, val)
            # GsClient의 모든 attr을 '__gsclient'에 set하는 기능. GsClient는 깡통.
            # 따라서 __getattr__도 '__gsclient'에서 꺼내오게 구현해야암
            # is equivalent to self.'__gsclient'."attr" = val 그러나 불가능한 style.

    def __getattr__(self, attr):
        return getattr(self.__gsclient, attr)
        # Remember that __getattr__ is only used for missing attribute lookup.
        # 이경우 GsClient에 아무 attr이 없으므로 모든 attr은 __getattr__을 튱해 gspread.Client instance에서 꺼내온다.
        # 따라서 만약 self.__gsclient가 없을 경우 이 코드는 getattr이 __getattr__을 부르고 __getattr__이 gatattr을 부르게 되어 무한루프
        # 참고로 getattr(self.__gsclient, attr) is equivalent to self.__gsclient."attr" 그러나 불가능한 style.

    def copy(self, file_id, title=None, copy_permissions=False):  # Spreadsheet을 return하는 모든 함수를 GsFile을 return하게끔 override
        content = super().copy(file_id, title=title, copy_permissions=copy_permissions)
        return GsFile(content)

    def create(self, title):
        content = super().create(title)
        return GsFile(content)

    def open(self, title):
        content = super().open(title)
        return GsFile(content)

    def open_by_key(self, key):
        content = super().open_by_key(key)
        return GsFile(content)

    def open_by_url(self, url):
        content = super().open_by_url(url)
        return GsFile(content)

    def openall(self, title=None):
        contents = super().openall(title)
        return [GsFile(content) for content in contents]


class GsFile(gspread.models.Spreadsheet):
    """
    ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
    '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__',
    '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__',
    '__subclasshook__', '__weakref__',
    'copy', 'create', 'del_spreadsheet', 'import_csv', 'insert_permission', 'list_permissions',
    'list_spreadsheet_files', 'login', 'open', 'open_by_key', 'open_by_url', 'openall', 'remove_permission', 'request']
    """

    def __init__(self, gsspreadsheet):
        self.__gsspreadsheet = gsspreadsheet

    def __setattr__(self, attr, val):
        if attr == '_GsFile__gsspreadsheet':
            super().__setattr__(attr, val)
        else:
            setattr(self.__gsspreadsheet, attr, val)

    def __getattr__(self, attr):
        return getattr(self.__gsspreadsheet, attr)

    def get_worksheet(self, index):
        content = super().get_worksheet(index)
        return GsSheet(content)

    def worksheet(self, title):
        content = super().worksheet(title)
        return GsSheet(content)

    def worksheets(self):
        contents = super().worksheets()
        return [GsSheet(content) for content in contents]


class GsSheet(gspread.models.Worksheet):
    """
    ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
    '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__',
    '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__',
    '__subclasshook__', '__weakref__',
    'copy', 'create', 'del_spreadsheet', 'import_csv', 'insert_permission', 'list_permissions',
    'list_spreadsheet_files', 'login', 'open', 'open_by_key', 'open_by_url', 'openall', 'remove_permission', 'request']
    """

    def __init__(self, gsworksheet):
        self.__gsworksheet = gsworksheet

    def __setattr__(self, attr, val):
        if attr == '_GsSheet__gsworksheet':
            super().__setattr__(attr, val)
        else:
            setattr(self.__gsworksheet, attr, val)

    def __getattr__(self, attr):
        return getattr(self.__gsworksheet, attr)


class CubeInterface:
    def __init__(self, credentials, filename=None, sheetname=None, email=None):
        self._email = email if email is not None else input("Enter User's email address: ")
        self._currentClient = GspreadIO.openGsClient(credentials)
        if self._currentClient is None:
            raise ValueError

        self.currentFile = filename
        self.currentSheet = sheetname  # setter 사용

    @property
    def currentFile(self):
        return self._currentFile

    @currentFile.setter
    def currentFile(self, param):
        if param is None:  # if type(A) is type(None) || if A is None 형식으로 써야
            self._currentFile = None

        elif type(param) is str:
            if param in [found.title for found in self._currentClient.openall()]:  # param is file name
                self._currentFile = self._currentClient.open(param)
                self._currentSheet = self._currentFile.get_worksheet(0)
                print("File '%s' is open" % param)
            elif param in [found.id for found in self._currentClient.openall()]:  # param is file ID
                self._currentFile = self._currentClient.open_by_key(param)
                self._currentSheet = self._currentFile.get_worksheet(0)
                print("File '%s: %s' is open" % (self._currentFile.title, param))
            else:
                self._currentFile = self._currentClient.create(param)
                self._currentSheet = self._currentFile.get_worksheet(0)
                self._currentFile.share(self._email, perm_type='user', role='writer')
                print("File '%s' is created" % param)

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
        row_count = self._currentSheet.row_count
        self._currentSheet.add_rows(1)
        for card in cardlist:
            self._currentSheet.insert_row(prettify(card.gsExport()), row_count+cardlist.index(card)+1)
            print("{0} is recorded in {1}".format(card.name, self._currentSheet.title))

    def searchExportMass(self, searchquery, sets='f', sort=None, order=None):
        cardlist = ScryfallIO.getMass(searchquery, sets=sets, sort=sort, order=order)
        for datum in cardlist:
            card = Card(datum)
            self._currentSheet.append_row(prettify(card.gsExport()))
            print("{0} is recorded in {1}".format(card.name, self._currentSheet.title))

    def importinsheet(self, start=None, end=None, *columns):
        """가공되지 않은 sheet에서 cardname을 받아 Card의 list로 return"""
        cardnamelist = []
        for col in columns:
            for row in range(int(start), int(end)+1):
                print("{0}{1}".format(col, row))
                cardnamelist.append(self._currentSheet.acell("{0}{1}".format(col, row)).value)

        cardlist = []
        for cardname in cardnamelist:
            cardlist.append(Card(ScryfallIO.getCard(cardname)))

        return cardlist

    def importCard(self, row):
        """가공된 row값을 받아 Card로 return"""
        card = Card(prettify(self._currentSheet.row_values(row), mode="reverse"))
        return card

    def importMass(self, start=1, end=None):  # spread sheet의 start는 0이 아님
        """가공된 row들 값을 받아 Card의 list로 return"""
        if end is None:
            end = self._currentSheet.row_count

        cardlist = []
        for i in range(start, end+1):  # 1에서 'end'까지
            cardlist.append(self.importCard(i))

        return cardlist

    def findcell(self, query):
        """query를 가지는 첫 cell을 찾아 cell instance를 return"""
        regexp = re.compile(r'([\s]|^)' + query)
        try:
            return self._currentSheet.find(regexp)
        except GspreadIO.gspread.exceptions.CellNotFound:  # gspread는 GspreadIO에 import되어있음
            print('Cannot find "%s" in %s' % (query, self._currentSheet.title))
            return None

    def findcardname(self, query):
        """특정 query를 만족하는 cell이 위치하는 곳의 Card name을 return"""
        regexp = re.compile(r'([\s]|^)' + query)
        try:
            result = self._currentSheet.find(regexp)
            return self._currentSheet.cell(result.row, 1)
        except GspreadIO.gspread.exceptions.CellNotFound:  # gspread는 GspreadIO에 import되어있음
            print('Cannot find "%s" in %s' % (query, self._currentSheet.title))
            return None

    def findincol(self, query, *columns):
        """특정 column들 내에서 quert를 만족하는 card들의 row값들을 list로 return"""
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
