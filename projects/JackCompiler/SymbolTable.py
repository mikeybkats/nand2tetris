from enum import Enum


# the Kind corresponds to grammatical reading of the jack code and does not translate directly to the vm code.
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

    def start_class(self):
        """Starts a new class scope"""
        self._scope = CurrentScope.CLASS
        self._table_class.clear()

    def not_scope(self):
        return CurrentScope.CLASS if self._scope == CurrentScope.SUBROUTINE else CurrentScope.SUBROUTINE

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
        if not self.is_var(i_name):
            if i_kind == IdentifierKind.FIELD.value or i_kind == IdentifierKind.STATIC.value:
                self._scope = CurrentScope.CLASS
            if i_kind == IdentifierKind.VAR.value or i_kind == IdentifierKind.ARGUMENT.value:
                self._scope = CurrentScope.SUBROUTINE

            self._tables[self._scope][i_name] = {
                "name": i_name,
                "type": i_type,
                "kind": i_kind,
                "#": self.var_count(i_kind)
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
        if name in self._tables[self._scope]:
            return self._tables[self._scope][name]["kind"]
        elif name in self._tables[self.not_scope()]:
            return self._tables[self.not_scope()][name]["kind"]
        return None

    def type_of(self, name):
        """
        Returns the type of the named identifier in the current scope.

        :param name:
            string
        :return:
            string
        """
        if name in self._tables[self._scope]:
            return self._tables[self._scope][name]["type"]
        elif name in self._tables[self.not_scope()]:
            return self._tables[self.not_scope()][name]["type"]

    def index_of(self, name):
        """
        Returns the index assigned to the named identifier.

        :param name:
            string
        :return:
            int
        """
        if name in self._tables[self._scope]:
            return self._tables[self._scope][name]["#"]
        elif name in self._tables[self.not_scope()]:
            return self._tables[self.not_scope()][name]["#"]

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
