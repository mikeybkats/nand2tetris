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


class CommandTable:
    def __init__(self):
        self._table = self.build_default_table()

    def build_default_table(self):
        symbols = dict([
            ('add', Commands.C_ARITHMETIC),
            ('sub', Commands.C_ARITHMETIC),
            ('neg', Commands.C_ARITHMETIC),
            ('eq', Commands.C_ARITHMETIC),
            ('gt', Commands.C_ARITHMETIC),
            ('lt', Commands.C_ARITHMETIC),
            ('and', Commands.C_ARITHMETIC),
            ('or', Commands.C_ARITHMETIC),
            ('not', Commands.C_ARITHMETIC),
        ])

    def get_command_type(self, symbol):
        """Returns the command type associated with the operation.

        Returns:
            Command
        """
        return self._table.get(symbol)
