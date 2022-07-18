from enum import Enum


class IdentifierKind(Enum):
    STATIC = "static"
    FIELD = "field"
    ARGUMENT = "argument"
    VAR = "var"
    NONE = "none"


class IdentifierType(Enum):
    INT = "int"
    STRING = "String"
    BOOLEAN = "boolean"
    CHAR = "char"


class CurrentScope(Enum):
    CLASS = "class"
    SUBROUTINE = "subroutine"


class SymbolTable:
    _current_kind = None
    _current_kind_index = 0
    """
    :field _current_scope:
        CurrentScope "class" | "subroutine
    """
    _scope = None
    """
    :field _table_subroutine:
        dictionary
    """
    _table_subroutine = dict()
    """
    :field _table_class:
        dictionary
    """
    _table_class = dict()

    _tables = dict({CurrentScope.CLASS: _table_class, CurrentScope.SUBROUTINE: _table_subroutine})

    def __init__(self):
        """Creates a new empty symbol tables"""
        self._scope = CurrentScope.CLASS
        self._index = 0

    @property
    def scope(self):
        return self._scope

    @scope.setter
    def scope(self, scope):
        self._scope = scope

    def start_subroutine(self):
        """Starts a new subroutine scope (i.e., resets the subroutine's symbol table)"""
        self._scope = CurrentScope.SUBROUTINE
        self._table_subroutine.clear()
        self._current_kind_index = 0

    def start_class(self):
        """Starts a new class scope"""
        self._scope = CurrentScope.CLASS
        self._table_class.clear()
        self._current_kind_index = 0

    # private method
    def __reset_cc_index(self, kind):
        if not self._current_kind == kind:
            self._current_kind = kind
            self._current_kind_index = 0
        else:
            self._current_kind_index = self._current_kind_index + 1

    def define(self, i_name, i_type, i_kind):
        """
        Defines a new identifier of a given name, type, and kind and assigns it a running index. STATIC and FIELD
        identifiers have a class scope, while ARG and VAR identifiers have a subroutine scope.

        :param i_name:
            string identifier name
        :param i_type:
            IdentifierKind identifier type
        :param i_kind:
            IdentifierKind STATIC, FIELD, ARG, VAR, NONE
        :return:
        """
        self.__reset_cc_index(i_kind)

        self._tables[self._scope][i_name] = {
            "name": i_name,
            "type": i_type,
            "kind": i_kind,
            "#": self._current_kind_index
        }
        # creates entry like this: (i_name, { "name": xxx, "type": xxx, "kind": xxx, "#": xxx })

    def var_count(self, kind):
        """
        Returns the number of variables of the given kind already defined in the current scope.

        :param kind:
            IdentifierKind STATIC, int, FIELD, ARG or VAR
        :return:
            int
        """
        count = 0
        for symbolEntry in self._tables[self._scope].items():
            if symbolEntry[1]["kind"] == kind:
                count = count + 1

        return count

    def kind_of(self, name):
        """
        Returns the kind of the named identifier in the current scope. If the identifier is
        unknown in the current scope, it returns None.

        :param name:
            string
        :return:
            STATIC, FIELD, ARG, VAR, None
        """
        return self._tables[self._scope][name]["kind"]

    def type_of(self, name):
        """
        Returns the type of the named identifier in the current scope.

        :param name:
            string
        :return:
            string
        """
        return self._tables[self._scope][name]["type"]

    def index_of(self, name):
        """
        Returns the index assigned to the named identifier.

        :param name:
            string
        :return:
            int
        """
        return self._tables[self._scope][name]["#"]

    def is_var(self, name):
        """
        Checks to see if the var is in either scoped table

        :param name:
        :return: Boolean
        """
        for key, value in self._tables.items():
            for entry_key, entry in value.items():
                if entry["name"] == name:
                    return True
        return False
