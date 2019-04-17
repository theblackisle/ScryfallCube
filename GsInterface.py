import re
import gspread
import time

import GspreadIO
import ScryfallIO
from Card import Card
from Converter import prettify, number_to_colchar, colchar_to_number


class GsClient(gspread.Client):
    """
    ['copy', 'create', 'del_spreadsheet', 'import_csv', 'insert_permission', 'list_permissions',
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
    ['copy', 'create', 'del_spreadsheet', 'import_csv', 'insert_permission', 'list_permissions',
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

    def add_worksheet(self, title, rows, cols):
        content = super().add_worksheet(title, rows, cols)
        return GsSheet(content)

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
    ['copy', 'create', 'del_spreadsheet', 'import_csv', 'insert_permission', 'list_permissions',
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

    def append_row(self, values, value_input_option='RAW'):
        """gsspread의 원본 method와 달리 무조건 column A부터 append하도록 개조"""
        params = {
            'valueInputOption': value_input_option
        }

        body = {
            'values': [values]
        }
        title_range = self.title + '!A1:A%s' % self.row_count
        return self.spreadsheet.values_append(title_range, params, body)

    def importCard(self, card):
        self.append_row(prettify(card))
        print("{:25} is recorded in '{}'".format(card.properties["nominal"]["name"], self.title))

    def import_rows(self, row_data):  # row_data = list of row data(=list).
        """가공된 row값들을 받아 sheet에 붙여넣기"""
        for i in range(len(row_data)):
            while True:
                try:
                    self.append_row(row_data[i])
                    print("{:25} is recorded in '{}'".format(row_data[i][0], self.title))
                    break
                except gspread.exceptions.APIError:
                    print("{:25} failed to record in '{}' due to quota limit ".format(row_data[i][0], self.title))
                    sleeper = 20
                    print("Program paused for %s seconds." % sleeper)
                    time.sleep(sleeper)


    def importMass(self, cardlist):
        for index, card in enumerate(cardlist, 1):
            while True:
                try:
                    print("{:3}. ".format(index), end='')
                    self.importCard(card)
                    break
                except gspread.exceptions.APIError:
                    # "code": 429,
                    # "status": "RESOURCE_EXHAUSTED",
                    # "message": "Quota exceeded for quota group 'WriteGroup' and limit 'USER-100s'
                    print("{:25} failed to record in '{}' due to quota limit ".format(card.properties["nominal"]["name"], self.title))
                    sleeper = 20
                    print("Program paused for %s seconds." % sleeper)
                    time.sleep(sleeper)

    def searchImportCard(self, cardname, sets='f', indent=0, mode='default'):
        card = Card(ScryfallIO.getCard(cardname, sets=sets), reference="Scryfall", mode=mode)
        self.append_row(prettify(card))
        print(" "*indent + "{:25} is recorded in '{}'".format(card.properties["nominal"]["name"], self.title))

    def searchImportMass(self, namelist, mode='default'):
        for index, cardname in enumerate(namelist, 1):
            while True:
                try:
                    print("{:3}. ".format(index), end='')
                    self.searchImportCard(cardname, indent=5, mode=mode)
                    break
                except gspread.exceptions.APIError:
                    print(" "*5 + "{:25} failed to record in '{}' due to quota limit ".format(cardname, self.title))
                    sleeper = 20
                    print("Program paused for %s seconds." % sleeper)
                    time.sleep(sleeper)

    def export_to_card(self, row):
        """가공된 row값을 받아 Card로 return"""
        card = Card(self.row_values(row), reference="Gspread")
        return card

    def export_rows(self, rows):  # rows = list of row values(=int).
        """
        가공된 sheet에서 사용
        입력받은 row상의 data를 list로 return
        """
        row_data = []
        for i in rows:
            while True:
                try:
                    gsdata = self.row_values(i)
                    row_data.append(gsdata)
                    print("{:25} is copied from '{}'".format(gsdata[0], self.title))
                    break
                except gspread.exceptions.APIError:
                    print("Failed to copy data from row '{}' due to quota limit ".format(i, self.title))
                    sleeper = 20
                    print("Program paused for %s seconds." % sleeper)
                    time.sleep(sleeper)

        return row_data

    def export_from_sheet(self, rows, columns):
        """
        가공되지 않은 sheet에서 사용
        cardname을 받아 list로 return
        """
        namelist = []
        for col in columns:
            coldata = self.col_values(colchar_to_number(col))
            rows = [row for row in rows if row <= len(coldata)]
            for row in rows:
                content = coldata[row-1].replace('\n//', ' //')
                location = "{0}{1}".format(col, row)
                if content is not "":
                    namelist.append(content)
                    print("{:3}. {:25} at {:3} is exported.".format(len(namelist), content, location))
                # else print(" "*29 + "{:3} is an empty cell".format(location))

        return namelist

    def export_sheet_to_card(self, offset):
        """
        가공된 sheet에서 사용
        offset'부터' sheet의 모든 data를 card의 list로 return
        """
        sheet_list = self.get_all_values()[offset-1:]
        cardlist = []
        for row_value in sheet_list:
            cardlist.append(Card(row_value, reference="Gspread"))
        return cardlist


    def delete_rows(self, rows):
        """
        Args:
            rows (list): ist of row numbers

        Returns:
            None
        """
        reversed_rows = sorted(rows, reverse=True)

        for row in reversed_rows:
            self.delete_row(row)
            print("row {:3} in sheet '{}' is deleted".format(row, self.title))

    def find_duplicated(self, *cols):
        vals_in_col = []
        for col in cols:
            vals_in_col.append(self.col_values(colchar_to_number(col)))

        vals_in_row = []
        for i in range(len(vals_in_col[0])):  # rows
            col_val_set = []
            for j in range(len(cols)):  # columns
                col_val_set.append(vals_in_col[j][i])
            vals_in_row.append(tuple(col_val_set))

        seen = set()
        duplicated = set()
        for i, x in enumerate(vals_in_row):
            if x not in seen:
                seen.add(x)
            else:  # x in seen:
                duplicated.add((x, i+1))
                duplicated.add((x, vals_in_row.index(x)+1))

        dupl_list = {}
        for value_set, index in sorted(list(duplicated)):
            dupl_list.setdefault(value_set[0], []).append(index)

        return dupl_list

    def findcell(self, query, mode="cell"):
        """
        가공된 sheet에서 사용
        mode == cell: 특정 query를 만족하는 첫 cell을 찾아 cell instance를 return
        mode == name: 특정 query를 만족하는 첫 cell이 위치하는 곳의 Card name을 return
        mode == row: 특정 query를 만족하는 첫 cell이 위치하는 곳의 row 값(int)을 return
        """
        regexp = re.compile(r'([\s]|^)' + query)
        try:
            result = self.find(regexp)
            if mode == "cell":
                return result
            if mode == "name":
                return self.cell(result.row, 1).value
            if mode == "row":
                return result.row
        except GspreadIO.gspread.exceptions.CellNotFound:  # gspread는 GspreadIO에 import되어있음
            print('Cannot find "%s" in %s' % (query, self.title))
            return None

    def queries_in_cols(self, searchset):
        """
        가공된 sheet에서 사용
        특정 column들 내에서 query들을 만족하는 card들의 row값(int)들을 list로 return

        Args:
            searchset (list): list of (tuple)s, each of which has 2 elements,
                The first element represents column name. Single character(str) or (list) of characters(str)
                The second element represents query to search. A single word(str) or (list) of words(str).
                    The list may contain other (list)s of words as an element for nested query.

        Returns:
            found_row: (list): list of (int)
        """

        flag = "init"
        result = set()
        for column, query in searchset:

            if query in ("OR", "AND", "EXCEPT"):
                flag = query

            else:
                if type(column) is list:
                    row_list = []
                    for i in column:
                        col_values = self.col_values(colchar_to_number(i))
                        row_list |= self.queries_in_col(query, col_values)
                else:  # if column is single char.
                    col_values = self.col_values(colchar_to_number(column))
                    row_list = self.queries_in_col(query, col_values)
                if flag == "init":
                    result = row_list
                if flag == "AND":
                    result &= row_list
                if flag == "OR":
                    result |= row_list
                if flag == "EXCEPT":
                    result -= row_list
                flag = "AND"

        return sorted(list(result))

    def queries_in_col(self, query_list, col_values):
        """
        queries_in_cols이 사용하는 내부 함수
        특정 column 내에서 query들을 만족하는 card들의 row값(int)들을 list로 return

        Args:
            query_list (str / list): [golbin, OR, elf] - list of a split string by blank
            col_values (str): list of all values of a single column

        Returns:
            found_row: (set): set of (int)
        """

        flag = "init"
        result = set()

        if type(query_list) is str:
            result = self.query_in_col(query_list, col_values)

        elif type(query_list) is list:
            for query in query_list:

                if query in ("OR", "AND", "EXCEPT"):
                    flag = query

                else:
                    if type(query) is list:  # nested query
                        row_list = self.queries_in_col(query, col_values)
                    else:  # if query is a single word
                        row_list = self.query_in_col(query, col_values)
                    if flag == "init":
                        result = row_list
                    if flag == "AND":
                        result &= row_list
                    if flag == "OR":
                        result |= row_list
                    if flag == "EXCEPT":
                        result -= row_list
                    flag = "AND"

        return result

    def query_in_col(self, query, col_values, offset = 2):
        """
        queries_in_cols이 사용하는 내부 함수
        특정 column 내에서 틀정 searchword를 만족하는 card들의 row값(int)들을 list로 return

        Args:
            query (str): -goblin, elf, discard ... a single word
            col_values (str): list of all values of a column

        Returns:
            found_row: (set): set of (int)
        """
        is_negative = False
        is_case_sensitive = re.IGNORECASE  # case insensitive by default

        query = query.replace("_", " ")  # First_strike -> First strike

        if re.match(r'^(-|!)', query):  # negative search
            is_negative = True
            query = query[1:]

        if re.search(r'\^', query):  # case sensitive search
            is_case_sensitive = 0
            query = query.replace("^", "")

        if re.search(r'#', query):  # exact search
            query = query.replace("#", "")
            query = r'(^|[\W]|[\s]+)' + query + r'([\s]+|[\W]|$)'  # r'(\b|\s+)' + query + r'(\s+|\b)' test 해보기

        found_row = set([index for index, value in enumerate(col_values, 1) if re.search(query, value,
                                                                                      flags=is_case_sensitive)])

        if is_negative:
            total = set(range(offset+1, len(col_values)+1))
            return total - found_row
        else:  # positive(=normal) search
            return found_row


class GsInterface:
    def __init__(self, credentials, filename=None, sheetname=None, email=None, mode='default'):
        self._email = email if email is not None else input("Enter User's email address: ")
        gspread = GspreadIO.openGsClient(credentials)
        if gspread is None:
            raise ValueError
        self._mode = mode
        self._client = GsClient(GspreadIO.openGsClient(credentials))

        self.file = filename
        self.sheet = sheetname  # setter 사용

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, param):
        if type(param) is str:
            self._mode = param
        else:
            print("Not appropriate variable for mode.")

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, param):
        if param is None:  # if type(A) is type(None) || if A is None 형식으로 써야
            self._file = None

        elif type(param) is GsFile:  # param is Gsfile itself
            self._file = param
            if self._mode is "default":
                print("File is synced to '%s'" % param.title)

        elif re.match(r'[\d]+$', param):  # param is file index
            param = int(param)
            filelist = self._client.openall()
            if 0 < param <= len(filelist):
                self._file = filelist[param-1]
                self._sheet = self._file.get_worksheet(0)
                if self._mode is "default":
                    print("File '%d. %s' is open" % (param, self._file.title))
            else:
                print("%s is out of index range" % param)
                raise IndexError

        else:
            if param in [found.title for found in self._client.openall()]:  # param is file name
                self._file = self._client.open(param)
                self._sheet = self._file.get_worksheet(0)
                if self._mode is "default":
                    print("File '%s' is open" % param)
            elif param in [found.id for found in self._client.openall()]:  # param is file ID
                self._file = self._client.open_by_key(param)
                self._sheet = self._file.get_worksheet(0)
                if self._mode is "default":
                    print("File '%s: %s' is open" % (self._file.title, param))
            else:
                if input("No such file found. Will you create one?(Y/N): ")[0].lower() == "y":
                    self._file = self._client.create(param)
                    self._sheet = self._file.get_worksheet(0)
                    self._file.share(self._email, perm_type='user', role='writer')
                    print("File '%s' is created" % param)

    @file.getter
    def file(self):
        return self._file

    @file.deleter
    def file(self):
        try:
            if self._mode is not "silent":
                print("File '%s' is deleted" % self._file.title)
            self._client.del_spreadsheet(self._file.id)
            self._file = None
            self._sheet = None
        except AttributeError:
            print("Deletion process cannot be completed")

    @property
    def sheet(self):
        return self._sheet

    @sheet.setter
    def sheet(self, param):
        if param is None:
            self._sheet = None

        elif re.match(r'[\d]+$', param):  # param is sheet index
            param = int(param)
            sheetlist = self._file.worksheets()
            if 0 < param <= len(sheetlist):
                self._sheet = sheetlist[param-1]
                if self._mode is "default":
                    print("Sheet '%s. %s' is open" % (param, self._sheet.title))
            else:
                print("%s is out of index range" % param)
                raise IndexError

        else:  # param is sheet name
            if param in [found.title for found in self._file.worksheets()]:
                self._sheet = self._file.worksheet(param)
                if self._mode is "default":
                   print("Sheet '%s' is open" % param)
            else:
                if input("No such sheet found. Will you create one?(Y/N): ")[0].lower() == "y":
                    self._sheet = self._file.add_worksheet(param, 1, 21)
                    print("Sheet '%s' is created" % param)

    @sheet.getter
    def sheet(self):
        return self._sheet

    @sheet.deleter
    def sheet(self):
        try:
            if self._mode is not "silent":
                print("Sheet '%s' is deleted" % self._sheet.title)
            self._file.del_worksheet(self._sheet)
            self._sheet = None
        except gspread.exceptions.APIError:
            print("You can't remove all the sheets in a document.")
        except AttributeError:
            print("Deletion process cannot be completed")



if __name__ == '__main__':
    myCube = GsInterface('ScryfallCube-80b58226a864.json')
    myCube.file = 'ScryfallCubeIO'
    myCube.sheet = "Test"
    # MyCube.currentSheet("시트1")은 안통함. property에는 __call__ method가 없음!

    print(myCube.sheet.get_all_records())
