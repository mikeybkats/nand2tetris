# parser: unpacks each instruction into its underlying field
import sys
from parserFileHandler import ParserFileHandler
from symbol_table import SymbolTable
from parserAppState import ParserAppState
from code import *


def main(filename, outputPath):
    file_handler = ParserFileHandler(filename, outputPath)
    symbol_table = SymbolTable()
    global app_state
    app_state = ParserAppState(file_handler, symbol_table)
    parse()


def parse():
    scan_one()
    scan_two()


def scan_one():
    rom_address = 0
    while has_more_commands():
        # load the command / advance to the next command
        advance()
        # check what kind of command
        instruction_type = command_type()
        # Each time a pseudocommand / L_COMMAND (Xxx) is encountered, add a new entry to the symbol table
        if instruction_type == "L_COMMAND":
            # add the symbol to the table
            inst_sym = symbol()
            app_state.symbol_table_add_symbol(inst_sym, str(rom_address))
        # if instruction is A_COMMAND or C_COMMAND count
        if instruction_type == "C_COMMAND" or instruction_type == "A_COMMAND":
            rom_address += 1


def scan_two():
    # start at 16 because this is where the variables are stored in the RAM
    rom_address = 16
    # go back to the begginning of the file
    app_state.infile().seek(0)
    # loop through all commands
    while has_more_commands():
        advance()
        # check what kind of instruction
        instruction_type = command_type()
        # if instruction is A_COMMAND
        if instruction_type == "A_COMMAND":
            add_symbols_and_get_addresses()
        elif instruction_type == "C_COMMAND":
            app_state.instruction_bin = determine_c_instruction()
        if instruction_type == "C_COMMAND" or instruction_type == "A_COMMAND":
            # write the instruction binary to output file
            app_state.write_output()
    app_state.close_output()


def add_symbols_and_get_addresses():
    inst_sym = symbol()
    if not bool(inst_sym.isnumeric()):
        # if the symbol is in the table
        if bool(app_state.symbol_table_contains(inst_sym)):
            # If the symbol is found in the table, get the address
            address = app_state.symbol_table_get_address(inst_sym)
        # if the symbol is not found add it to the table
        else:
            app_state.symbol_table_add_symbol(inst_sym, rom_address)
            rom_address += 1
    else:
        # if it is a numeric symbol add it to the table
        app_state.symbol_table_add_symbol(inst_sym, inst_sym)
    # set the current instruction to a binary value
    address = int(app_state.symbol_table_get_address(inst_sym))
    app_state.instruction_bin = convert_to_base16_and_format(address)


def determine_c_instruction():
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


def has_more_commands():
    """
    Are there more commands in the input?

    Returns:
        boolean
    """
    currentLocation = app_state.infile().tell()
    fileContents = app_state.infile().read()
    isEndOfFile = False if fileContents else True
    app_state.infile().seek(currentLocation)
    return not isEndOfFile


def advance():
    """
    Reads the next command from the input and makes it the current command. Should be called only if has_more_commands() is true. Initially there is no current command.
    """
    app_state.current = remove_comments(app_state.infile().readline().strip())
    while(is_empty_line(app_state.current)):
        app_state.current = app_state.infile().readline()


def is_empty_line(line):
    return line[:2] == "//" or line == "/n" or line.isspace() or not len(line.strip())


def command_type():
    """
    Returns the type of the current command:
        - A_COMMAND for @Xxx where Xxx is either a symbol or a decimal number
        - C_COMMAND for dest=comp;jump
        - L_COMMAND (actually, pseudocommand) for (Xxx) where Xxx is a symbol.

    Returns:
        the type of the current command A_COMMAND | C_COMMAND | L_COMMAND
    """
    word = ""
    currentCommand = app_state.current.strip()
    for char in currentCommand:
        if(not char.isspace()):
            word = word + char
    app_state.current = word
    if bool(word):
        if "@" in word:
            return "A_COMMAND"
        if "(" in word or ")" in word:
            return "L_COMMAND"
        if word[0].isalpha() or ";" in word:
            return "C_COMMAND"
    return "NO_COMMAND"


def symbol():
    """
    Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx). Should be called only when command_type() is A_COMMAND or L_COMMAND.

    Returns:
        string
    """
    word = ""
    for char in app_state.current:
        if char.isalnum() or char == "_":
            word = word + char
    return word


def dest():
    """
    Returns the dest mnemonic in the current C-command (8 possibilities). Should be called only when command_type() is C_COMMAND.
    """
    word = app_state.current
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
    """Returns the comp mnemonic in the current C-command (28 possibilities). Should be called only when command_type() is C_COMMAND.

    Returns:
        string
    """
    word = app_state.current
    if (len(word)) == 0:
        return ""

    comp_command = ""
    count = False
    if ";" in word:
        count = True
    for i, char in enumerate(word):
        if(char == ";"):
            return comp_command
        if(bool(count)):
            comp_command = comp_command + char
        if(char == "="):
            count = True

    return comp_command


def remove_comments(word):
    newWord = ""
    addLetter = True
    for char in word:
        if char == "/":
            addLetter = False
        if addLetter == True:
            newWord += char
    return newWord


def jump():
    """
    Returns the jump mnemonic in the current C-command (8 possibilities). Should be called only when command_type() is C_COMMAND.

    Returns:
        string
    """
    word = app_state.current
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
