# parser: unpacks each instruction into its underlying field
import sys
from init import ParserFileHandler
from symbol_table import SymbolTable
from parserAppState import ParserAppState


def main(filename, outputPath):
    fileHandler = ParserFileHandler(filename, outputPath)
    symbolTable = SymbolTable()
    global AppState
    AppState = ParserAppState(fileHandler, symbolTable)

    while hasMoreCommands():
        advance()
        AppState.instructionType = commandType()
        if AppState.instructionType == "L_COMMAND" or AppState.instructionType == "A_COMMAND":
            symbol()
        else:
            dest()
            comp()


def hasMoreCommands():
    """
    Are there more commands in the input?

    Returns:
        boolean
    """
    currentLocation = AppState.inFile().tell()
    returnVal = True if AppState.inFile().read() else False
    AppState.inFile().seek(currentLocation)
    return returnVal


def advance():
    """
    Reads the next command from the input and makes it the current command. Should be called only if hasMoreCommands() is true. Initially there is no current command.
    """
    AppState.current = AppState.inFile().readline()
    while(isEmptyLine(AppState.current)):
        AppState.current = AppState.inFile().readline()
    # print("Current:", AppState.current)


def isEmptyLine(line):
    # if(not line):
    #     return False
    return line[:2] == "//" or line == "/n" or line.isspace()


def commandType():
    """
    Returns the type of the current command:
        - A_COMMAND for @Xxx where Xxx is either a symbol or a decimal number
        - C_COMMAND for dest=comp;jump
        - L_COMMAND (actually, pseudocommand) for (Xxx) where Xxx is a symbol.

    Returns:
        the type of the current command A_COMMAND | C_COMMAND | L_COMMAND
    """
    word = ""
    currentCommand = AppState.current
    for char in currentCommand:
        if(not char.isspace()):
            word = word + char
    AppState.current = word
    if bool(word):
        if word[0] == "@":
            return "A_COMMAND"
        if word[0] == "(" and word[1].isalpha():
            return "L_COMMAND"
        if word[0].isalpha():
            return "C_COMMAND"
    return "NO_COMMAND"


def symbol():
    """
    Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx). Should be called only when commandType() is A_COMMAND or L_COMMAND.

    Returns:
        string
    """
    # get current word
    word = ""
    for char in AppState.current:
        if char.isalnum():
            word = word + char
    return word


def dest():
    """
    Returns the dest mnemonic in the current C-command (8 possibilities). Should be called only when commandType() is C_COMMAND.
    """
    destTable = dict([
        ("0", "000"),
        ("M", "001"),
        ("D", "010"),
        ("MD", "011"),
        ("A", "100"),
        ("AM", "101"),
        ("AD", "110"),
        ("AMD", "111"),
    ])
    word = AppState.current
    if len(word) == 0:
        return destTable[null]
    for i, char in enumerate(word):
        # print(i, char)
        if(char == "=" or char == ";"):
            if(i == 1):
                return destTable[word[0]]
            if(i == 2):
                return destTable[word[:2]]
            if(i == 3):
                return destTable[word[:3]]


def comp():
    """Returns the comp mnemonic in the current C-command (28 possibilities). Should be called only when commandType() is C_COMMAND.

    Returns:
        string
    """
    compTableA0 = dict([
        ("0", "101010"),
        ("1", "111111"),
        ("-1", "111010"),
        ("D", "001100"),
        ("A", "110000"),
        ("!D", "001101"),
        ("!A", "110001"),
        ("-D", "001111"),
        ("-A", "110011"),
        ("D+1", "011111"),
        ("A+1", "110111"),
        ("D-1", "001110"),
        ("A-1", "110010"),
        ("D+A", "000010"),
        ("A-D", "000111"),
        ("D-A", "010011"),
        ("D&A", "000000"),
        ("D|A", "010101"),
    ])
    compTableA1 = dict([
        ("M", "110000"),
        ("!M", "110001"),
        ("-M", "110011"),
        ("M+1", "110111"),
        ("M-1", "110010"),
        ("D+M", "000010"),
        ("M-D", "000111"),
        ("D-M", "010011"),
        ("D&M", "000000"),
        ("D|M", "010101"),
    ])
    compTable = None
    word = AppState.current
    if len(word) == 0:
        return ""
    if "A" in word:
        compTable = compTableA0
    else:
        compTable = compTableA1

    compCommand = ""
    count = False
    for i, char in enumerate(word):
        if(bool(count)):
            if(not char.isspace()):
                compCommand = compCommand + char
        if(char == "="):
            count = True

    print(compCommand)
    # return compTable[compCommand]


def jump():
    """
    Returns the jump mnemonic in the current C-command (8 possibilities). Should be called only when commandType() is C_COMMAND.

    Returns:
        string
    """
    pass


if __name__ == '__main__':
    outputPath = 'output.txt'
    if len(sys.argv) == 3:
        outputPath = sys.argv[2]

    main(filename=sys.argv[1], outputPath=outputPath)
