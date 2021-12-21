# parser: unpacks each instruction into its underlying field
import sys
from init import ParserFileHandler


def main(filename, outputPath):
    global FileHandler
    FileHandler = ParserFileHandler(filename, outputPath)
    global inFile
    inFile = FileHandler.inFile()

    while hasMoreCommands():
        advance()
        commandType()


def hasMoreCommands():
    """
    Are there more commands in the input?

    Returns:
        boolean
    """
    currentLocation = inFile.tell()
    returnVal = True if inFile.read() else False
    inFile.seek(currentLocation)
    return returnVal


def advance():
    """
    Reads the next command from the input and makes it the current command. Should be called only if hasMoreCommands() is true. Initially there is no current command.
    """
    # hasCommands = hasMoreCommands()
    # if hasCommands == True:
    newCurrent = inFile.readline()
    while(isEmptyLine(newCurrent)):
        newCurrent = inFile.readline()
    # print("Readline:", newCurrent)
    FileHandler.current = newCurrent
    # print("Current:", FileHandler.current)


def isEmptyLine(line):
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
    currentCommand = FileHandler.current
    word = ""

    for char in currentCommand:
        if(not char.isspace()):
            word = word + char

    if word[0] == "@":
        return "A_COMMAND"
    if word[0] == "(" and word[1].isalpha():
        return "L_COMMAND"
    if word[0].isalpha():
        print(word)
        return "C_COMMAND"
    return "NO_COMMAND"


def symbol():
    """
     Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx). Should be called only when commandType() is A_COMMAND or L_COMMAND.

    Returns:
        string
    """


def dest():
    """
     Returns the dest mnemonic in the current C-command (8 possibilities). Should be called only when commandType() is C_COMMAND."""


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
