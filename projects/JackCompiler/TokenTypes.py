from enum import Enum


class Token_Type(Enum):
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    IDENTIFIER = "IDENTIFIER"
    INT_CONST = "INT_CONST"
    STRING_CONST = "STRING_CONST"


def is_op(token):
    if (token == "+" or
            token == "-" or
            token == "*" or
            token == "/" or
            token == "|" or
            token == "<" or
            token == ">" or
            token == "~" or
            token == "&" or
            token == "="):
        return True
    else:
        return False


def is_prefix_operator(token):
    if token == "-" or token == "~":
        return True
    else:
        return False


class TokenTypeTable:
    def __init__(self):
        self._table = self.build_token_table()

    def get_token_type(self, token):
        if token.isnumeric():
            token = Token_Type.INT_CONST.value.lower()
            return self._table.get(token)
        if token[0] == "\'" or token[0] == "\"":
            token = Token_Type.STRING_CONST.value.lower()
            return self._table.get(token)
        if (
            self._table.get(token) != Token_Type.KEYWORD and
            self._table.get(token) != Token_Type.SYMBOL
        ):
            token = "identifier"
            return self._table.get(token)

        return self._table.get(token)

    def build_token_table(self):
        return dict([
            ("class", Token_Type.KEYWORD),
            ("constructor", Token_Type.KEYWORD),
            ("function", Token_Type.KEYWORD),
            ("method", Token_Type.KEYWORD),
            ("field", Token_Type.KEYWORD),
            ("static", Token_Type.KEYWORD),
            ("var", Token_Type.KEYWORD),
            ("int", Token_Type.KEYWORD),
            ("char", Token_Type.KEYWORD),
            ("boolean", Token_Type.KEYWORD),
            ("void", Token_Type.KEYWORD),
            ("true", Token_Type.KEYWORD),
            ("false", Token_Type.KEYWORD),
            ("null", Token_Type.KEYWORD),
            ("this", Token_Type.KEYWORD),
            ("let", Token_Type.KEYWORD),
            ("do", Token_Type.KEYWORD),
            ("if", Token_Type.KEYWORD),
            ("else", Token_Type.KEYWORD),
            ("while", Token_Type.KEYWORD),
            ("return", Token_Type.KEYWORD),

            ("{", Token_Type.SYMBOL),
            ("}", Token_Type.SYMBOL),
            ("(", Token_Type.SYMBOL),
            (")", Token_Type.SYMBOL),
            ("[", Token_Type.SYMBOL),
            ("]", Token_Type.SYMBOL),
            (".", Token_Type.SYMBOL),
            (",", Token_Type.SYMBOL),
            (";", Token_Type.SYMBOL),

            ("+", Token_Type.SYMBOL),
            ("-", Token_Type.SYMBOL),
            ("*", Token_Type.SYMBOL),
            ("/", Token_Type.SYMBOL),
            ("&", Token_Type.SYMBOL),
            ("|", Token_Type.SYMBOL),
            ("<", Token_Type.SYMBOL),
            (">", Token_Type.SYMBOL),
            ("=", Token_Type.SYMBOL),
            ("~", Token_Type.SYMBOL),

            ("int_const", Token_Type.INT_CONST),
            ("string_const", Token_Type.STRING_CONST),
            ("identifier", Token_Type.IDENTIFIER)

        ])


class GrammarLanguage(Enum):
    ARRAY = "array"
    OBJECT = "object"
    BOOLEAN = "boolean"
    CHAR = "char"
    CLASS = "class"
    INT_CONSTANT = "integerConstant"
    CONSTRUCTOR = "constructor"
    DO = "do"
    DO_STATEMENT = "doStatement"
    EXPRESSION = "expression"
    EXPRESSION_LIST = "expressionList"
    ELSE = "else"
    FALSE = "false"
    FIELD = "field"
    FUNCTION = "function"
    IDENTIFIER = "identifier"
    IF_STATEMENT = "ifStatement"
    IF = "if"
    INT = "int"
    KEYWORD = "keyword"
    LET = "let"
    LET_STATEMENT = "letStatement"
    METHOD = "method"
    NULL = "null"
    PARAMETER_LIST = "parameterList"
    RETURN = "return"
    RETURN_STATEMENT = "returnStatement"
    SYMBOL = "symbol"
    STATEMENTS = "statements"
    STATIC = "static"
    STRING_CONST = "stringConstant"
    SUB_ROUTINE_DEC = "subroutineDec"
    SUB_ROUTINE_BOD = "subroutineBody"
    TERM = "term"
    THIS = "this"
    TRUE = "true"
    VOID = "void"
    VAR = "var"
    VAR_DEC = "varDec"
    WHILE_STATEMENT = "whileStatement"
    WHILE = "while"
    CLASS_VAR_DEC = "classVarDec"


class TerminalType(Enum):
    TERMINAL = "terminal"
    NON_TERMINAL = "non_terminal"


class TerminalTypeTable:
    def __init__(self):
        self._table = self.build_terminal_tag_table()

    def build_terminal_tag_table(self):
        return dict([
            (GrammarLanguage.SYMBOL.value, TerminalType.TERMINAL),
            (GrammarLanguage.KEYWORD.value, TerminalType.TERMINAL),
            (GrammarLanguage.INT_CONSTANT.value, TerminalType.TERMINAL),
            (GrammarLanguage.STRING_CONST.value, TerminalType.TERMINAL),
            (GrammarLanguage.IDENTIFIER.value, TerminalType.TERMINAL),

            (GrammarLanguage.CLASS.value, TerminalType.NON_TERMINAL),
            (GrammarLanguage.CLASS_VAR_DEC.value, TerminalType.NON_TERMINAL),
            (GrammarLanguage.SUB_ROUTINE_DEC.value, TerminalType.NON_TERMINAL),
            (GrammarLanguage.PARAMETER_LIST.value, TerminalType.NON_TERMINAL),
            (GrammarLanguage.SUB_ROUTINE_BOD.value, TerminalType.NON_TERMINAL),
            (GrammarLanguage.VAR_DEC.value, TerminalType.NON_TERMINAL),

            (GrammarLanguage.STATEMENTS.value, TerminalType.NON_TERMINAL),
            (GrammarLanguage.WHILE_STATEMENT.value, TerminalType.NON_TERMINAL),
            (GrammarLanguage.IF_STATEMENT.value, TerminalType.NON_TERMINAL),
            (GrammarLanguage.RETURN_STATEMENT.value, TerminalType.NON_TERMINAL),
            (GrammarLanguage.LET_STATEMENT.value, TerminalType.NON_TERMINAL),
            (GrammarLanguage.DO_STATEMENT.value, TerminalType.NON_TERMINAL),

            (GrammarLanguage.EXPRESSION.value, TerminalType.NON_TERMINAL),
            (GrammarLanguage.TERM.value, TerminalType.NON_TERMINAL),
            (GrammarLanguage.EXPRESSION_LIST.value, TerminalType.NON_TERMINAL)
        ])

    def is_terminal(self, tag_name):
        if self._table.get(tag_name) == TerminalType.TERMINAL:
            return True
        else:
            return False
