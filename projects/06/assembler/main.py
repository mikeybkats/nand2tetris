import sys
# main: initializes the I/O files and drives the process


def print_output_state(outputPath):
    outputFileContents = open(outputPath, mode='rt', encoding='utf-8')
    for line in outputFileContents:
        sys.stdout.write(line)


def open_input_file(inputFile):
    global inputFileContents
    inputFileContents = open(inputFile, mode='rt', encoding='utf-8')


def create_output_file(filename):
    global outputFile
    outputFile = open(filename, mode='w+', encoding='utf-8')


def write_to_output_file(data="no data"):
    # with outputFile:
    # for line in outputFile:
    outputFile.write(data)


def scan_input():
    # with inputFileContents:
    for line in inputFileContents:
        binary = "0000000000000000\n"
        # binary = parse_instruction(line)
        write_to_output_file(binary)
    outputFile.close()


def main(filename, outputPath):
    # create_symbol_table()
    open_input_file(filename)
    create_output_file(outputPath)
    scan_input()
    print_output_state(outputPath)


if __name__ == '__main__':
    outputPath = 'output.txt'
    if len(sys.argv) == 3:
        outputPath = sys.argv[2]

    main(filename=sys.argv[1], outputPath=outputPath)
