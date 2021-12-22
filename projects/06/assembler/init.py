import sys
# init: initializes the I/O files and drives the process


class ParserFileHandler:

    def __init__(self, filename, outputPath):
        """
        initializer - Opens the input file/stream and gets ready to parse it
        """
        self._inFile = self.open_input_file(filename)
        self._outFile = self.create_output_file(outputPath)
        self._outFilePath = outputPath

    def inFile(self):
        return self._inFile

    def outFile(self):
        return self._outFile

    def outFilePath(self):
        return self._outFilePath

    def open_input_file(self, inputFile):
        return open(inputFile, mode='rt', encoding='utf-8')

    def create_output_file(self, filename):
        return open(filename, mode='w+', encoding='utf-8')

    def write_to_output_file(self, value):
        self._outFile.write(value)

    def print_output_file(self):
        outputFileContents = open(
            self._outFilePath, mode='rt', encoding='utf-8')
        for line in outputFileContents:
            sys.stdout.write(line)
