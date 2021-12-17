# symbol table: manages the symbols in the application

def build_default_table():
    global symbols
    symbols = dict([
        ('SP', 0),
        ('LCL', 1),
        ('ARG', 2),
        ('THIS', 3),
        ('THAT', 4),
        ('SCREEN', 16384),
        ('KBD', 24576)
    ])
    for n in range(16):
        symbols['R'+str(n)] = n

    return symbols


def add_symbol_to_table(symbol, address):
    # check if already exists
    pass


def check_for_symbol():
    # returns boolean
    pass


def get_symbol_by_address(address):
    # return symbol
    pass
