
class AppState:
    """
    Arg1:
        Parser File Handler
    Arg2:
        List of Commands. Type Command from commands.py

    TODO: Incorporate the observer pattern with app state
    """

    def __init__(self, file_handler, command_table):
        self._file_handler = file_handler
        self._command_table = command_table

        self._infile = file_handler.infile
        self._infile_path = file_handler.infile_path
        self._outfile = file_handler.outfile
        self._current_command = ""
        self._current_command_type = ""

    def file_handler(self):
        return self._file_handler

    def command_table_contains(self, symbol):
        return self._command_table.contains(symbol)

    @property
    def current_command(self):
        return self._current_command

    @current_command.setter
    def current_command(self, new_val):
        self._current_command = new_val

    @property
    def current_command_type(self):
        return self._current_command_type

    @current_command_type.setter
    def current_command_type(self, new_val):
        self._current_command_type = new_val

    @property
    def outfile(self):
        return self._outfile

    @outfile.setter
    def outfile(self, new_outfile):
        self._outfile = new_outfile

    @property
    def infile_path(self):
        return self._infile_path

    @infile_path.setter
    def infile_path(self, new_path):
        self._infile_path = new_path

    @property
    def infile(self):
        return self._infile

    @infile.setter
    def infile(self, new_infile):
        self._infile = new_infile
