
class ParserAppState:
    def __init__(self, fileHandler, symbolTable):
        self._fileHandler = fileHandler
        self._symbolTable = symbolTable

        self._inFile = fileHandler.inFile()
        self._current = ""

    def current(self):
        return self._current

    def current(self, newVal):
        self._current = newVal

    def inFile(self):
        return self._inFile
