# symbol table: manages the symbols in the application

class SymbolTable:
    def __init__(self):
        self.table = self.build_default_table()

    def build_default_table(self):
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

    def addEntry(self, symbol, address):
        """Adds the pair (symbol, address) to the table."""
        self.table[symbol] = address

    def contains(self, symbol):
        """Does the symbol table contain the given symbol?

        Returns:
            boolean
        """
        if not self._table.get(symbol) == None:
            return True
        else:
            return False

    def getAddress(self, symbol):
        """Returns the address associated with the symbol.

        Returns:
            int
        """
        return self._table.get(symbol)
