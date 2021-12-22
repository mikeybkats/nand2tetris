# parser: unpacks each instruction into its underlying field
import sys
from init import ParserFileHandler
from symbol_table import SymbolTable
from parserAppState import ParserAppState
from code import *


def main(filename, outputPath):
    fileHandler = ParserFileHandler(filename, outputPath)
    symbolTable = SymbolTable()
    global AppState
    AppState = ParserAppState(fileHandler, symbolTable)
    parse()


def parse():
    instSym = ""
    romAddress = 0
    # scan one
    # loop through all commands
    while hasMoreCommands():
        advance()
        # check what kind of instruction
        AppState.instructionType = commandType()
        # Each time a pseudocommand (Xxx) is encountered, add a new entry to the symbol table
        if AppState.instructionType == "L_COMMAND":
            instSym = symbol()
            # add the symbol to the table
            AppState.addSymbolToTable(instSym, str(romAddress))
        # if instruction is A_COMMAND or C_COMMAND count
        if AppState.instructionType == "C_COMMAND" or "A_COMMAND":
            romAddress += 1

    # scan two
    # go back to the begginning of the file
    AppState.inFile().seek(0)
    # # start at 16 because this is where the variables are stored in the RAM
    romAddress = 16
    # # loop through all commands
    while hasMoreCommands():
        advance()
        # check what kind of instruction
        AppState.instructionType = commandType()
        # if instruction is A_COMMAND
        if AppState.instructionType == "A_COMMAND":
            instSym = symbol()
            if not bool(instSym.isnumeric()):
                # if the symbol is in the table
                if bool(AppState._symbolTable.contains(instSym)):
                    # If the symbol is found in the table, get the address
                    address = AppState._symbolTable.getAddress(instSym)
                # if the symbol is not found add it to the table
                else:
                    AppState.addSymbolToTable(instSym, romAddress)
            else:
                # add the symbol to the table
                AppState.addSymbolToTable(instSym, instSym)
            # set the current instruction binary
            address = int(AppState._symbolTable.getAddress(instSym))
            AppState.instructionBin = convert_to_base16_and_format(address)
            romAddress += 1
        elif AppState.instructionType == "C_COMMAND":
            AppState.instructionBin = determine_c_instruction()
        print(AppState.current, AppState.instructionBin)
        AppState.write_to_output_file()
    AppState.close_output_file()


def determine_c_instruction():
    # print("AppCurrent:", AppState.current)
    # print("comp:", comp())
    # print("dest:", dest())
    # print("jump:", jump())
    compI = code_comp(comp())
    destI = code_dest(dest())
    jumpI = code_jump(jump())
    address = "111" + compI + destI + jumpI
    address = add_whitespace_to_base16(address)
    return address


def convert_to_base16_and_format(number):
    number = f'0{number:015b}'
    number = add_whitespace_to_base16(number)
    return number


def insert_space(string, integer):
    return string[0:integer] + ' ' + string[integer:]


def add_whitespace_to_base16(address):
    address = insert_space(address, 4)
    address = insert_space(address, 9)
    address = insert_space(address, 14)
    return address


def hasMoreCommands():
    """
    Are there more commands in the input?

    Returns:
        boolean
    """
    currentLocation = AppState.inFile().tell()
    fileContents = AppState.inFile().read()
    isEndOfFile = False if fileContents else True
    AppState.inFile().seek(currentLocation)
    return not isEndOfFile


def advance():
    """
    Reads the next command from the input and makes it the current command. Should be called only if hasMoreCommands() is true. Initially there is no current command.
    """
    AppState.current = AppState.inFile().readline()
    while(isEmptyLine(AppState.current)):
        AppState.current = AppState.inFile().readline()


def isEmptyLine(line):
    return line[:2] == "//" or line == "/n" or line.isspace() or not len(line.strip())


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
    word = ""
    for char in AppState.current:
        if char.isalnum() or char == "_":
            word = word + char
    return word


def dest():
    """
    Returns the dest mnemonic in the current C-command (8 possibilities). Should be called only when commandType() is C_COMMAND.
    """
    word = AppState.current.strip()
    print("word:", word)
    if len(word) == 0:
        return "0"
    if ";" in word:
        return "0"
    for i, char in enumerate(word):
        if(char == "="):
            if(i == 1):
                return word[0]
            if(i == 2):
                return word[:2]
            if(i == 3):
                return word[:3]


def comp():
    """Returns the comp mnemonic in the current C-command (28 possibilities). Should be called only when commandType() is C_COMMAND.

    Returns:
        string
    """
    word = AppState.current.strip()
    if (len(word)) == 0:
        return ""

    compCommand = ""
    count = False
    if ";" in word:
        count = True
    for i, char in enumerate(word):
        if(char == ";"):
            return compCommand
        if(bool(count)):
            # if(not char.isspace()):
            compCommand = compCommand + char
        if(char == "="):
            count = True

    return compCommand


def jump():
    """
    Returns the jump mnemonic in the current C-command (8 possibilities). Should be called only when commandType() is C_COMMAND.

    Returns:
        string
    """
    word = AppState.current.strip()
    if len(word) == 0:
        return ""
    if ";" in word:
        return word[-3:]
    return ""


if __name__ == '__main__':
    outputPath = 'output.hack'
    if len(sys.argv) == 3:
        outputPath = sys.argv[2]

    main(filename=sys.argv[1], outputPath=outputPath)
