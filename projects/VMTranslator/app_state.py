
class AppState:
    """
    Arg1:
        Parser File Handler
    Arg2:
        List of Commands. Type Command from commands.py
    """

    def __init__(self, file_handler, command_table):
        self._file_handler = file_handler
        self._command_table = command_table

        self._infile = file_handler.infile()
        self._outfile = file_handler.outfile()
        self._current_command = ""

    def file_handler(self):
        return self._file_handler

    # def write_output(self):
    #     self._file_handler.write_to_output_file(self.instruction_bin)
    #     self._file_handler.write_to_output_file("\n")

    # def close_output(self):
    #     self._outfile.close()

    def command_table_contains(self, symbol):
        return self._command_table.contains(symbol)

    def current_command(self):
        return self._current_command

    def current_command(self, new_val):
        self._current_command = new_val

    def infile(self):
        return self._infile
