from unittest import TestCase
from CompilationEngine import CompilationEngine
from io import StringIO
from textwrap import dedent


class TestCompilationEngine(TestCase):
    def test_compile_class(self):
        pass

    def test_compile_class_var_declaration(self):
        jack_mock_class = dedent("""\
        class Square {
           field int x, y;
           field int size;
        """)
        jack_mock_in_file = StringIO(jack_mock_class)

        self._comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=StringIO(), write_xml=False)

        self._comp_eng.compile_class()

        self.assertEqual(3, len(self._comp_eng._symbol_table._table_class))

        item_x = self._comp_eng._symbol_table._table_class.get("x")
        self.assertEqual({"name": "x", "type": "int", "kind": "field", "#": 0}, item_x)

        item_y = self._comp_eng._symbol_table._table_class.get("y")
        self.assertEqual({"name": "y", "type": "int", "kind": "field", "#": 1}, item_y)

        item_size = self._comp_eng._symbol_table._table_class.get("size")
        self.assertEqual({"name": "size", "type": "int", "kind": "field", "#": 2}, item_size)

    def test_compile_subroutine(self):
        self.fail()

    def test_compile_parameter_list(self):
        self.fail()

    def test_compile_var_declaration(self):
        self.fail()

    def test_compile_statements(self):
        self.fail()

    def test_compile_let(self):
        self.fail()

    def test_compile_do(self):
        self.fail()

    def test_compile_while(self):
        self.fail()

    def test_compile_if(self):
        self.fail()

    def test_compile_else(self):
        self.fail()

    def test_compile_return(self):
        self.fail()

    def test_compile_expression(self):
        self.fail()

    def test_compile_term(self):
        self.fail()

    def test_compile_expression_list(self):
        self.fail()
