from enum import Enum


class Token_Type(Enum):
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    IDENTIFIER = "IDENTIFIER"
    INT_CONST = "INT_CONST"
    STRING_CONST = "STRING_CONST"


class TokenTypeTable:
    def __init__(self):
        self._table = self.build_token_table()

    def get_token_type(self, token):
        if token.isnumeric():
            token = "int_const"
            return self._table.get(token)
        if token[0] == "\'" or token[0] == "\"":
            token = "string_const"
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


class Keyword(Enum):
    CLASS = "class"
    METHOD = "method"
    FUNCTION = "function"
    CONSTRUCTOR = "constructor"
    INT = "int"
    BOOLEAN = "boolean"
    CHAR = "char"
    VOID = "void"
    VAR = "var"
    STATIC = "static"
    FIELD = "field"
    LET = "let"
    DO = "fo"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    RETURN = "return"
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    THIS = "this"
