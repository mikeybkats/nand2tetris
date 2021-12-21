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
        type = commandType()
        if type == "L_COMMAND" or type == "A_COMMAND":
            symbol()
        else:
            dest()


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
        ("null", "000"),
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
        if(char == "="):
            if(i == 1):
                print(destTable[word[0]])
                return destTable[word[0]]
            if(i == 2):
                print(destTable[word[:2]])
                return destTable[word[:2]]
            if(i == 3):
                print(destTable[word[:3]])
                return destTable[word[:3]]


def comp():
    """Returns the comp mnemonic in the current C-command (28 possibilities). Should be called only when commandType() is C_COMMAND.

    Returns:
        string
    """


def jump():
    """
    Returns the jump mnemonic in the current C-command (8 possibilities). Should be called only when commandType() is C_COMMAND.

    Returns:
        string
    """


if __name__ == '__main__':
    outputPath = 'output.txt'
    if len(sys.argv) == 3:
        outputPath = sys.argv[2]

    main(filename=sys.argv[1], outputPath=outputPath)
