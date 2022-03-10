import sys
import os
from file_handler import FileHandler
from parser_state import ParserState
from commands import Commands, CommandTable


class Parser:
    def __init__(self, infile_path, outfile_path):
        self._infile_path = infile_path
        self._current_command = ""
        self._file_handler = FileHandler(infile_path, outfile_path)
        self._command_table = CommandTable()
        self._state = ParserState(self._file_handler, self._command_table)

    def infile_path(self):
        return os.path.basename(os.path.normpath(self._infile_path))

    def file_handler(self):
        return self._file_handler

    def has_more_commands(self):
        """
        checks to see if there are more input commands

        Returns: 
            boolean
        """
        currentLocation = app_state.infile().tell()
        fileContents = app_state.infile().read()
        isEndOfFile = False if fileContents else True
        app_state.infile().seek(currentLocation)
        return not isEndOfFile

    def advance(self):
        """
        reads the next command from input and makes it the current command. should be called only if has_more_commands is true. initially there is no current command
        returns undefined
        """

    def command_type(self):
        """
        Returns the type of the current VM command C_ARITHMETIC is returned for all the arithmetic commands

        Returns: 
            COMMAND
        """
        return Commands.C_ARITHMETIC

    def arg1(self):
        """
        Returns the first argument of the current command. In the case of C_ARITHMETIC the command itself (add, sub, etc) is returned. Should not be called if the current command is C_RETURN.

        Returns:
            string
        """
        return ""

    def arg2(self):
        """
        Returns the second argument of the current command. Should be called only if the current command is C_PUSH, C_POP, C_FUNCTION, or C_CALL.

        Returns: 
            int
        """
        return 0


if __name__ == '__main__':
    outfile_path = 'output.asm'
    if len(sys.argv) == 3:
        outfile_path = sys.argv[2]

    parser = Parser(infile_path=sys.argv[1], outfile_path=outfile_path)
    # parser.
