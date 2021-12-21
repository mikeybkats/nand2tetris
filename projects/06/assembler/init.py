import sys
# init: initializes the I/O files and drives the process


# def write_to_output_file(data="no data"):
#     # with outputFile:
#     # for line in outputFile:
#     outputFile.write(data)


# def scan_input(inputFileContents):
#     for line in inputFileContents:
#         binary = "0000000000000000\n"
#         # binary = parse_instruction(line)
#         write_to_output_file(binary)
#     outputFile.close()


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

    def print_output_file(self):
        outputFileContents = open(
            self._outFilePath, mode='rt', encoding='utf-8')
        for line in outputFileContents:
            sys.stdout.write(line)
