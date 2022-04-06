import sys
import os
from commands import Commands, CommandTable


class VMParser:
    def __init__(self, app_state, command_table):
        self._command_table = command_table
        self._state = app_state

    def state(self):
        return self._state

    @property
    def current_command(self):
        return self._state.current_command

    def has_more_commands(self):
        """
        checks to see if there are more input commands

        Returns: 
            boolean
        """
        currentLocation = self._state.infile.tell()
        fileContents = self._state.infile.read()
        isEndOfFile = False if fileContents else True
        self._state.infile.seek(currentLocation)
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
        word = self._state.infile.readline()

        # TODO: why is this not working correctly?
        # while (self.is_empty_line(self._state.current_command) and self.has_more_commands()):
        # self._state.current_command = self._state.infile.readline()

        if word and word[:2] != "//":
            self._state.current_command = self.remove_comments(word)
            self._state.current_command_type = self.command_type()
            print(self._state.current_command)

    def command_type(self) -> Commands:
        """
        Returns the type of the current VM command C_ARITHMETIC is returned for all the arithmetic commands

        Returns: 
            Command
        """
        command = self._state.current_command
        if command:
            return self._command_table.get_command_type(command.split()[0].lower())
        return "NO_COMMAND"

    def arg1(self):
        """
        Returns the first argument of the current command. In the case of C_ARITHMETIC the command itself (add, sub, etc) is returned. Should not be called if the current command is C_RETURN.

        Returns:
            string
        """
        current = self._state.current_command
        if len(current.split()) > 1:
            return current.split()[1]
        return None

    def arg2(self):
        """
        Returns the second argument of the current command. Should be called only if the current command is C_PUSH, C_POP, C_FUNCTION, or C_CALL.

        Returns: 
            int
        """
        current = self._state.current_command
        if current.split()[2]:
            return int(current.split()[2])
