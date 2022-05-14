from enum import Enum


class TOKEN_TYPE(Enum):
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    IDENTIFIER = "IDENTIFIER"
    INT_CONST = "INT_CONST"
    STRING_CONST = "STRING_CONST"


class KEYWORD(Enum):
    CLASS = "CLASS"
    METHOD = "METHOD"
    FUNCTION = "FUNCTION"
    CONSTRUCTOR = "CONSTRUCTOR"
    INT = "INT"
    BOOLEAN = "BOOLEAN"
    CHAR = "CHAR"
    VOID = "VOID"
    VAR = "VAR"
    STATIC = "STATIC"
    FIELD = "FIELD"
    LET = "LET"
    DO = "DO"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    RETURN = "RETURN"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NULL = "NULL"
    THIS = "THIS"
