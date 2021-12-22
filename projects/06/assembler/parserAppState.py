
class ParserAppState:
    def __init__(self, fileHandler, symbolTable):
        self._fileHandler = fileHandler
        self._symbolTable = symbolTable

        self._inFile = fileHandler.inFile()
        self._current = ""
        self._instructionType = ""
        self._instructionBin = ""

    def write_to_output_file(self):
        self._fileHandler.write_to_output_file(self._instructionBin)

    def addSymbolToTable(self, symbol):
        self._symbolTable.addEntry(symbol, symbol)

    def current(self):
        return self._current

    def current(self, newVal):
        self._current = newVal

    def inFile(self):
        return self._inFile

    def instructionType(self):
        return self._instructionType

    def instructionType(self, newVal):
        self._instructionType = newVal

    def instructionBin(self):
        return self._instructionBin

    def instructionBin(self, newVal):
        self._instructionBin = newVal