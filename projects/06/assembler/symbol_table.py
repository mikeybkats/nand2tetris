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


def addEntry(symbol, address):
    """Adds the pair (symbol, address) to the table."""
    pass


def contains():
    """Does the symbol table contain the given symbol?

    Returns:
        boolean
    """
    pass


def getAddress(symbol):
    """Returns the address associated with the symbol.

    Returns:
        int
    """
    pass
