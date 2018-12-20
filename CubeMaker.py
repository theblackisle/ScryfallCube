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

    def exportCard(self, cardname):
        card = Card(ScryfallIO.getCard(cardname))
        self._currentSheet.append_row(prettify(card.gsExport()))

    def importCard(self, row):
        card = Card(prettify(self._currentSheet.row_values(row), mode="reverse"))
        return card


if __name__ == '__main__':
    MyCube = CubeInterface('ScryfallCube-80b58226a864.json')
    MyCube.currentFile = 'ScryfallCubeIO'
    MyCube.currentSheet = "시트1"
    # MyCube.currentSheet("시트1")은 안통함. property에는 __call__ method가 없음!

    while True:
        searchquery = input("put card: ")
        if searchquery == "quit":
            break
        MyCube.exportCard(searchquery)

    print(MyCube.importCard(2).showCard())
    #print(MyCube.currentSheet.get_all_records())