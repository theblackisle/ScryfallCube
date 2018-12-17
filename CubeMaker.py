import GspreadIO
import ScryfallIO

class CubeInterface():
    def __init__(self, credentials, filename, sheetname):
        currentClient = GspreadIO.openGsClient(credentials)
        currentFile = GspreadIO.openGsFile(currentClient, filename)
        currentSheet = currentFile.worksheet(sheetname)

    def moveFile(self, filename):
        currentFile = GspreadIO.openGsFile(currentClient, filename)

    def moveSheet(self, sheetname):
        currentSheet = currentFile.workdsheet(sheetname)

def putCard(cardname, sheetname):
    card = ScryfallIO.getCard(cardname)

if(__name__ == '__main__'):
    MyCube = CubeInterface('ScryfallCube-80b58226a864.json', 'ScryfallCubeIO', "시트1")
    print(MyCube.currentSheet.get_all_records())
