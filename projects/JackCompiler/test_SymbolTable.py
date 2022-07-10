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
        self.symbol_table.define("id", IdentifierType.INT.value, IdentifierKind.FIELD.value)
        self.symbol_table.define("name", IdentifierType.STRING.value, IdentifierKind.FIELD.value)
        self.symbol_table.define("balance", IdentifierType.INT.value, IdentifierKind.FIELD.value)

    def test_define(self):
        self.add_class_scope()
        self.assertEqual(CurrentScope.CLASS, self.symbol_table.scope)
        self.assertEqual(4, self.symbol_table.index)
        self.assertEqual(
            {"name": "nAccounts", "type": IdentifierType.INT.value, "kind": IdentifierKind.STATIC.value},
            self.symbol_table._table_class[0]
        )
        self.assertEqual(
            {"name": "balance", "type": IdentifierType.INT.value, "kind": IdentifierKind.FIELD.value},
            self.symbol_table._table_class[3]
        )

    def test_start_subroutine(self):
        self.add_class_scope()
        self.symbol_table.start_subroutine()
        self.symbol_table.define("this", "Point", IdentifierKind.ARGUMENT)

        self.assertEqual(CurrentScope.SUBROUTINE, self.symbol_table.scope)
        self.assertEqual(1, self.symbol_table.index)

    def test_var_count(self):
        self.add_class_scope()
        self.assertEqual(
            {"name": "balance", "type": IdentifierType.INT.value, "kind": IdentifierKind.FIELD.value},
            self.symbol_table._table_class[3]
        )
        self.assertEqual(CurrentScope.CLASS, self.symbol_table.scope)
        self.assertEqual(3, self.symbol_table.var_count(IdentifierKind.FIELD.value))






