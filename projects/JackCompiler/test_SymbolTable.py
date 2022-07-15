import unittest
from SymbolTable import SymbolTable, IdentifierKind, IdentifierType, CurrentScope


class SymbolTableTest(unittest.TestCase):
    def setUp(self):
        self.symbol_table = SymbolTable()

    def tearDown(self):
        self.symbol_table.start_subroutine()
        self.symbol_table.start_class()

    def test_constructor(self):
        self.assertEqual(self.symbol_table.scope, CurrentScope.CLASS)

    def add_class_scope(self):
        self.symbol_table.define("nAccounts", IdentifierType.INT.value, IdentifierKind.STATIC.value)
        self.symbol_table.define("bankCommission", IdentifierType.INT.value, IdentifierKind.STATIC.value)
        self.symbol_table.define("id", IdentifierType.INT.value, IdentifierKind.FIELD.value)
        self.symbol_table.define("name", IdentifierType.STRING.value, IdentifierKind.FIELD.value)
        self.symbol_table.define("owner", IdentifierType.STRING.value, IdentifierKind.FIELD.value)
        self.symbol_table.define("balance", IdentifierType.INT.value, IdentifierKind.FIELD.value)

    def add_subroutine_scope(self):
        self.symbol_table.define("this", "BankAccount", IdentifierKind.ARGUMENT.value)
        self.symbol_table.define("sum", IdentifierType.INT.value, IdentifierKind.ARGUMENT.value)
        self.symbol_table.define("from", "BankAccount", IdentifierKind.ARGUMENT.value)
        self.symbol_table.define("when", "Date", IdentifierKind.ARGUMENT.value)
        self.symbol_table.define("i", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self.symbol_table.define("j", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self.symbol_table.define("due", "Date", IdentifierKind.VAR.value)

    def test_define(self):
        self.add_class_scope()
        self.assertEqual(CurrentScope.CLASS, self.symbol_table.scope)
        self.assertEqual(
            {"name": "nAccounts", "type": IdentifierType.INT.value, "kind": IdentifierKind.STATIC.value, "#": 0},
            self.symbol_table._table_class["nAccounts"]
        )
        self.assertEqual(
            {"name": "id", "type": IdentifierType.INT.value, "kind": IdentifierKind.FIELD.value, "#": 0},
            self.symbol_table._table_class["id"])

        self.assertEqual(
            {"name": "owner", "type": IdentifierType.STRING.value, "kind": IdentifierKind.FIELD.value, "#": 2},
            self.symbol_table._table_class["owner"])

        self.assertEqual(
            {"name": "balance", "type": IdentifierType.INT.value, "kind": IdentifierKind.FIELD.value, "#": 3},
            self.symbol_table._table_class["balance"]
        )

    def test_start_subroutine(self):
        self.add_class_scope()
        self.symbol_table.start_subroutine()
        self.assertEqual(0, self.symbol_table._current_kind_index)

        self.symbol_table.define("this", "Point", IdentifierKind.ARGUMENT)
        self.assertEqual(0, self.symbol_table._current_kind_index)
        self.symbol_table.define("x", IdentifierType.INT.value, IdentifierKind.ARGUMENT)
        self.assertEqual(1, self.symbol_table._current_kind_index)

        self.assertEqual(CurrentScope.SUBROUTINE, self.symbol_table.scope)

    def test_var_count(self):
        self.add_class_scope()
        self.assertEqual(
            {"name": "balance", "type": IdentifierType.INT.value, "kind": IdentifierKind.FIELD.value},
            self.symbol_table._table_class["balance"]
        )
        self.assertEqual(CurrentScope.CLASS, self.symbol_table.scope)
        self.assertEqual(3, self.symbol_table.var_count(IdentifierKind.FIELD.value))

    def test_kind_of(self):
        self.add_class_scope()
        kind_of = self.symbol_table.kind_of("id")
        self.assertEqual(IdentifierKind.FIELD.value, kind_of)

        kind_of = self.symbol_table.kind_of("nAccounts")
        self.assertEqual(IdentifierKind.STATIC.value, kind_of)

        kind_of = self.symbol_table.kind_of("balance")
        self.assertEqual(IdentifierKind.FIELD.value, kind_of)

    def test_type_of(self):
        self.add_class_scope()
        type_of = self.symbol_table.type_of("id")
        self.assertEqual(IdentifierType.INT.value, type_of)

    def test_index_of(self):
        self.add_class_scope()
        index_of = self.symbol_table.index_of("balance")
        self.assertEqual(2, index_of)

        index_of = self.symbol_table.index_of("id")
        self.assertEqual(1, index_of)

        self.test_start_subroutine()
        self.add_subroutine_scope()

        index_of = self.symbol_table.index_of("j")
        self.assertEqual(1, index_of)

        index_of = self.symbol_table.index_of("when")
        self.assertEqual(3, index_of)




