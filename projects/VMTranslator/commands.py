from enum import Enum


class Commands(Enum):
    C_ARITHMETIC = "C_ARITHMETIC"
    C_PUSH = "C_PUSH"
    C_POP = "C_POP"
    C_LABEL = "C_LABEL"
    C_GOTO = "C_GOTO"
    C_IF = "C_IF"
    C_FUNCTION = "C_FUNCTION"
    C_RETURN = "C_RETURN"
    C_CALL = "C_CALL"
    NO_COMMAND = "NO_COMMAND"


class CommandTable:
    '''
    CommandTable stores the different kinds of commands in the application:

    Arithmetic and Logical Commands: add, sub, neg, eq, gt, lt, and, or, not
    Memory Access: push and pop
    Program Flow: label, goto, if-goto
    Function Calling: function, call, return

    '''

    def __init__(self):
        self._table = self.build_default_table()

    def build_default_table(self):
        return dict([
            ('add', Commands.C_ARITHMETIC),
            ('sub', Commands.C_ARITHMETIC),
            ('neg', Commands.C_ARITHMETIC),
            ('eq', Commands.C_ARITHMETIC),
            ('gt', Commands.C_ARITHMETIC),
            ('lt', Commands.C_ARITHMETIC),
            ('and', Commands.C_ARITHMETIC),
            ('or', Commands.C_ARITHMETIC),
            ('not', Commands.C_ARITHMETIC),
            ('push', Commands.C_PUSH),
            ('pop', Commands.C_POP),
            ('label', Commands.C_LABEL),
            ('goto', Commands.C_GOTO),
            ('if-goto', Commands.C_IF),
            ('function', Commands.C_FUNCTION),
            ('return', Commands.C_RETURN),
            ('call', Commands.C_CALL)
        ])

    def get_command_type(self, symbol) -> Commands:
        """Returns the command type associated with the operation.

        Returns:
            Command
        """
        command = self._table.get(symbol)
        if command:
            return command
        return Commands.NO_COMMAND
