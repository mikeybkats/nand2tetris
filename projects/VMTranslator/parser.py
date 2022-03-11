import sys
import os
from file_handler import FileHandler
from parser_state import ParserState
from commands import Commands, CommandTable


class Parser:
    def __init__(self, infile_path, outfile_path):
        self._infile_path = infile_path
        self._command_table = CommandTable()
        self._file_handler = FileHandler(infile_path, outfile_path)
        self._state = ParserState(self._file_handler, self._command_table)

    def state(self):
        return self._state

    def infile_path(self):
        return os.path.basename(os.path.normpath(self._infile_path))

    def file_handler(self):
        return self._file_handler

    def current_command(self):
        return self._state.current_command

    def has_more_commands(self):
        """
        checks to see if there are more input commands

        Returns: 
            boolean
        """
        currentLocation = self._state.infile().tell()
        fileContents = self._state.infile().read()
        isEndOfFile = False if fileContents else True
        self._state.infile().seek(currentLocation)
        return not isEndOfFile

    def is_empty_line(self, line):
        return line[:2] == "//" or line == "/n" or line.isspace() or not len(line.strip())

    def remove_comments(self, word):
        newWord = ""
        addLetter = True
        for char in word:
            if char == "/":
                addLetter = False
            if addLetter == True:
                newWord += char
        return newWord.strip()

    def advance(self):
        """
        reads the next command from input and makes it the current command. should be called only if has_more_commands is true. initially there is no current command
        returns undefined
        """
        word = self._state.infile().readline()
        if word:
            self._state.current_command = self.remove_comments(word)

        while(self.is_empty_line(self._state.current_command)):
            self._state.current = self._state.infile().readline()

    def command_type(self):
        """
        Returns the type of the current VM command C_ARITHMETIC is returned for all the arithmetic commands

        Returns: 
            COMMAND
        """
        return self._state.current_command()

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
