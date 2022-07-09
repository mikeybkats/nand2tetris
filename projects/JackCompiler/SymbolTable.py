
class SymbolTable:
    """
    :field _current_scope:
        "class" | "subroutine
    """
    _current_scope = None
    """
    :field _table_subroutine:
        dictionary
    """
    _table_subroutine_scope = dict()
    """
    :field _table_class:
        dictionary
    """
    _table_class_scope = dict()

    def __init__(self):
        """Creates a new empty symbol tables"""

    def set_scope(self, scope):
        """
        sets the Symbol table scope

        :param scope:
            "class" | "subroutine"
        :return:
            The current scope
            "class" | "subroutine"
        """
        self._current_scope = scope

        return self._current_scope

    def start_subroutine(self):
        """Starts a new subroutine scope (i.e., resets the subroutine's symbol table)"""
        pass

    def define(self, i_name, i_type, i_kind):
        """
        Defines a new identifier of a given name, type, and kind and assigns it a running index. STATIC and FIELD
        identifiers have a class scope, while ARG and VAR identifiers have a subroutine scope.

        :param i_name:
            string identifier name
        :param i_type:
            string identifier type
        :param i_kind:
            STATIC, FIELD, ARG or VAR
        :return:
        """

    def var_count(self, kind):
        """
        Returns the number of variables of the given kind already defined in the current scope.

        :param kind:
            STATIC, int, FIELD, ARG or VAR
        :return:
            int
        """

    def kind_of(self, name):
        """
        Returns the kind of the named identifier in the current scope. If the identifier is
        unknown in the current scope, it returns None.

        :param name:
            string
        :return:
            STATIC, FIELD, ARG, VAR, None
        """

    def type_of(self, name):
        """
        Returns the type of the named identifier in the current scope.

        :param name:
            string
        :return:
            string
        """

    def index_of(self, name):
        """
        Returns the index assigned to the named identifier.

        :param name:
            string
        :return:
            int
        """