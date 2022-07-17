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
           static int pointCount;
        """)
        jack_mock_in_file = StringIO(jack_mock_class)

        self._comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=StringIO(), write_xml=False)

        self._comp_eng.compile_class()

        self.assertEqual(4, len(self._comp_eng._symbol_table._table_class))

        item_x = self._comp_eng._symbol_table._table_class.get("x")
        self.assertEqual({"name": "x", "type": "int", "kind": "field", "#": 0}, item_x)

        item_y = self._comp_eng._symbol_table._table_class.get("y")
        self.assertEqual({"name": "y", "type": "int", "kind": "field", "#": 1}, item_y)

        item_size = self._comp_eng._symbol_table._table_class.get("size")
        self.assertEqual({"name": "size", "type": "int", "kind": "field", "#": 2}, item_size)

        item_point_count = self._comp_eng._symbol_table._table_class.get("pointCount")
        self.assertEqual({"name": "pointCount", "type": "int", "kind": "static", "#": 0}, item_point_count)

    def test_compile_subroutine(self):
        jack_mock_subroutine = dedent("""\
        method int distance(Point other) {
            var int dx, dy;
            let dx = x - other.getx();
            let dy = y - other.gety();
            return Math.sqrt((dx*dy)+(dy*dy));
        }
        """)
        jack_mock_in_file = StringIO(jack_mock_subroutine)

        self._comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=StringIO(), write_xml=False)
        self._comp_eng._class_name = "Point"
        self._comp_eng._tokenizer.advance()

        self._comp_eng.compile_subroutine()

        self.assertEqual(4, len(self._comp_eng._symbol_table._table_subroutine))

        item_this = self._comp_eng._symbol_table._table_subroutine.get("this")
        self.assertEqual({"name": "this", "type": "Point", "kind": "argument", "#": 0}, item_this)

        item_other = self._comp_eng._symbol_table._table_subroutine.get("other")
        self.assertEqual({"name": "other", "type": "Point", "kind": "argument", "#": 1}, item_other)

        item_dx = self._comp_eng._symbol_table._table_subroutine.get("dx")
        self.assertEqual({"name": "dx", "type": "int", "kind": "local", "#": 0}, item_dx)

        item_dy = self._comp_eng._symbol_table._table_subroutine.get("dy")
        self.assertEqual({"name": "dy", "type": "int", "kind": "local", "#": 1}, item_dy)

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
