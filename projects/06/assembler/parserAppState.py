
class ParserAppState:
    def __init__(self, file_handler, symbol_table):
        self._file_handler = file_handler
        self._symbol_table = symbol_table

        self._infile = file_handler.infile
        self._outfile = file_handler.outfile()
        self._current = ""
        self._instruction_bin = ""

    def write_output(self):
        self._file_handler.write_to_output_file(self.instruction_bin)
        self._file_handler.write_to_output_file("\n")

    def close_output(self):
        self._outfile.close()

    def symbol_table_add_symbol(self, symbol, address):
        self._symbol_table.add_entry(symbol, address)

    def symbol_table_contains(self, symbol):
        return self._symbol_table.contains(symbol)

    def symbol_table_get_address(self, symbol):
        return self._symbol_table.get_address(symbol)

    def current(self):
        return self._current

    def current(self, new_val):
        self._current = new_val

    def infile(self):
        return self._infile

    def instruction_bin(self):
        return self._instruction_bin

    def instruction_bin(self, new_val):
        self._instruction_bin = new_val
