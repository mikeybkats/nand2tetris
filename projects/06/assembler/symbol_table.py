# symbol table: manages the symbols in the application

def build_default_table():
    global symbols
    symbols = dict([
        ("R0", 0),
        ("R1", 1),
        ("R2", 2),
        ("R3", 3),
        ("R4", 4),
        ("R5", 5),
        ("R6", 6),
        ("R7", 7),
        ("R8", 8),
        ("R9", 9),
        ("R10", 10),
        ("R11", 11),
    ])


def add_symbol_to_table(symbol, address):
    # check if already exists
    pass


def check_for_symbol():
    # returns boolean
    pass


def get_symbol_by_address(address):
    # return symbol
    pass
