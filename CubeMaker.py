from typing import Optional

from gspread import Client

import GspreadIO
import ScryfallIO

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

    def putCard(self, cardname):
        card = ScryfallIO.getCard(cardname)


if __name__ == '__main__':
    try:
        MyCube = CubeInterface('ScryfallCube-80b58226a864.json')
        MyCube.currentFile = 'ScryfallCubeIO'
        MyCube.currentSheet = "시트1"
        # MyCube.currentSheet("시트1")은 안통함. property에는 __call__ method가 없음

        print(MyCube.currentSheet.get_all_records())
    except:
        print("Failed to load google spreadsheet")



