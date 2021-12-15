import sys
# main: initializes the I/O files and drives the process


def print_output_state():
    with outputFile:
        for line in outputFile:
            sys.stdout.write(line)


def open_input_file(inputFile):
    global inputFileContents
    asmFileContents = open(asmFile, mode='rt', encoding='utf-8')


def create_output_file(filename):
    global outputFile
    outputFile = open(filename, mode='w+', encoding='utf-8')


def write_to_output_file(data="no data"):
    with outputFile:
        for line in outputFile:
            lint.write(data)


def scan_input():
    with inputFileContents:
        for line in inputFileContents:
            binary = "0000 0000 0000 0000"
            # binary = parse_instruction(line)
            write_to_output_file(binary)


def main(filename, output="output.txt"):
    open_input_file(filename)
    create_output_file(output)
    print_output_state()


if __name__ == '__main__':
    main(filename=sys.argv[1], output=sys.argv[2])
