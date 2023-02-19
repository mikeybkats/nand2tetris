from unittest import TestCase
from CompilationEngine import CompilationEngine
from SymbolTable import SymbolTable, IdentifierKind, IdentifierType, CurrentScope

from io import StringIO
from textwrap import dedent


class TestCompileExpression(TestCase):

    def test_compile_expression_simple(self):
        jack_mock_expression_simple = dedent("""\
        a[3] + 3;
        """)

        jack_mock_in_file = StringIO(jack_mock_expression_simple)

        self._comp_eng = CompilationEngine(input_stream=jack_mock_in_file, output_stream=StringIO())
        self._comp_eng._class_name = "Main"
        self._comp_eng._symbol_table.start_class()
        self._comp_eng._symbol_table.start_subroutine()
        self._comp_eng._symbol_table.define(i_name="a", i_type="Array", i_kind="var")
        self._comp_eng._symbol_table.define(i_name="b", i_type="Array", i_kind="var")
        self._comp_eng._symbol_table.define(i_name="c", i_type="Array", i_kind="var")

        self._comp_eng.tokenizer.advance()
        self.assertEqual(self._comp_eng.tokenizer.currentToken, "a")
        self._comp_eng.compile_expression()

        correct_output = dedent("""\
        push constant 3
        push local 0
        add
        pop pointer 1
        push that 0
        push constant 3
        add
        """)
        mock_correct_output = StringIO(correct_output)
        expected_result = mock_correct_output.readlines()

        self._comp_eng._vm_writer.outfile.seek(0)
        compiler_output_lines = self._comp_eng._vm_writer.outfile.readlines()

        self.assertEqual(expected_result, compiler_output_lines)

    def test_compile_expression_complex(self):
        jack_mock_expression_complex = dedent("""\
        a[a[5]] * b[((7 - a[3]) - Main.double(2)) + 1];
        """)

        jack_mock_in_file = StringIO(jack_mock_expression_complex)

        self._comp_eng = CompilationEngine(input_stream=jack_mock_in_file, output_stream=StringIO())
        self._comp_eng._class_name = "Main"
        self._comp_eng._symbol_table.start_class()
        self._comp_eng._symbol_table.start_subroutine()
        self._comp_eng._symbol_table.define(i_name="a", i_type="Array", i_kind="var")
        self._comp_eng._symbol_table.define(i_name="b", i_type="Array", i_kind="var")
        self._comp_eng._symbol_table.define(i_name="c", i_type="Array", i_kind="var")

        self._comp_eng.tokenizer.advance()
        self.assertEqual(self._comp_eng.tokenizer.currentToken, "a")
        self._comp_eng.compile_expression()

        correct_output = dedent("""\
            push constant 5
            push local 0
            add
            pop pointer 1
            push that 0
            push local 0
            add
            pop pointer 1
            push that 0
            push constant 7
            push constant 3
            push local 0
            add
            pop pointer 1
            push that 0
            sub
            push constant 2
            call Main.double 1
            sub
            push constant 1
            add
            push local 1
            add
            pop pointer 1
            push that 0
            call Math.multiply 2
            pop temp 0
            pop pointer 1
            push temp 0
            pop that 0
        """)
        mock_correct_output = StringIO(correct_output)
        expected_result = mock_correct_output.readlines()

        self._comp_eng._vm_writer.outfile.seek(0)
        compiler_output_lines = self._comp_eng._vm_writer.outfile.readlines()

        self.assertEqual(expected_result, compiler_output_lines)
