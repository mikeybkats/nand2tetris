from unittest import TestCase
from CompilationEngine import CompilationEngine
from SymbolTable import SymbolTable, IdentifierKind, IdentifierType, CurrentScope
from VMWriter import  VMWriter
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

    def test_compile_subroutine_xml(self):
        mock_sub_routine = """
        method void moveSquare() {
            if (direction = 1) { do square.moveUp(); }
            if (direction = 2) { do square.moveDown(); }
            if (direction = 3) { do square.moveLeft(); }
            if (direction = 4) { do square.moveRight(); }
            do Sys.wait(5);  // delays the next movement
            return;
         }
        """
        jack_mock_in_file = StringIO(mock_sub_routine)
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file, write_xml=True)

        # while comp_eng.tokenizer.has_more_tokens():
        comp_eng.tokenizer.advance()
        comp_eng.compile_subroutine()

        comp_eng.outfile.seek(0)
        file_lines = comp_eng.outfile.readlines()

        result = dedent("""\
        <subroutineDec>
        <keyword> method </keyword>
        <keyword> void </keyword>
        <identifier> moveSquare </identifier>
        <symbol> ( </symbol>
        <parameterList>
        </parameterList>
        <symbol> ) </symbol>
        <subroutineBody>
        <symbol> { </symbol>
        <statements>
        <ifStatement>
        <keyword> if </keyword>
        <symbol> ( </symbol>
        <expression>
        <term>
        <identifier> direction </identifier>
        </term>
        <symbol> = </symbol>
        <term>
        <integerConstant> 1 </integerConstant>
        </term>
        </expression>
        <symbol> ) </symbol>
        <symbol> { </symbol>
        <statements>
        <doStatement>
        <keyword> do </keyword>
        <identifier> square </identifier>
        <symbol> . </symbol>
        <identifier> moveUp </identifier>
        <symbol> ( </symbol>
        <expressionList>
        </expressionList>
        <symbol> ) </symbol>
        <symbol> ; </symbol>
        </doStatement>
        </statements>
        <symbol> } </symbol>
        </ifStatement>
        <ifStatement>
        <keyword> if </keyword>
        <symbol> ( </symbol>
        <expression>
        <term>
        <identifier> direction </identifier>
        </term>
        <symbol> = </symbol>
        <term>
        <integerConstant> 2 </integerConstant>
        </term>
        </expression>
        <symbol> ) </symbol>
        <symbol> { </symbol>
        <statements>
        <doStatement>
        <keyword> do </keyword>
        <identifier> square </identifier>
        <symbol> . </symbol>
        <identifier> moveDown </identifier>
        <symbol> ( </symbol>
        <expressionList>
        </expressionList>
        <symbol> ) </symbol>
        <symbol> ; </symbol>
        </doStatement>
        </statements>
        <symbol> } </symbol>
        </ifStatement>
        <ifStatement>
        <keyword> if </keyword>
        <symbol> ( </symbol>
        <expression>
        <term>
        <identifier> direction </identifier>
        </term>
        <symbol> = </symbol>
        <term>
        <integerConstant> 3 </integerConstant>
        </term>
        </expression>
        <symbol> ) </symbol>
        <symbol> { </symbol>
        <statements>
        <doStatement>
        <keyword> do </keyword>
        <identifier> square </identifier>
        <symbol> . </symbol>
        <identifier> moveLeft </identifier>
        <symbol> ( </symbol>
        <expressionList>
        </expressionList>
        <symbol> ) </symbol>
        <symbol> ; </symbol>
        </doStatement>
        </statements>
        <symbol> } </symbol>
        </ifStatement>
        <ifStatement>
        <keyword> if </keyword>
        <symbol> ( </symbol>
        <expression>
        <term>
        <identifier> direction </identifier>
        </term>
        <symbol> = </symbol>
        <term>
        <integerConstant> 4 </integerConstant>
        </term>
        </expression>
        <symbol> ) </symbol>
        <symbol> { </symbol>
        <statements>
        <doStatement>
        <keyword> do </keyword>
        <identifier> square </identifier>
        <symbol> . </symbol>
        <identifier> moveRight </identifier>
        <symbol> ( </symbol>
        <expressionList>
        </expressionList>
        <symbol> ) </symbol>
        <symbol> ; </symbol>
        </doStatement>
        </statements>
        <symbol> } </symbol>
        </ifStatement>
        <doStatement>
        <keyword> do </keyword>
        <identifier> Sys </identifier>
        <symbol> . </symbol>
        <identifier> wait </identifier>
        <symbol> ( </symbol>
        <expressionList>
        <expression>
        <term>
        <integerConstant> 5 </integerConstant>
        </term>
        </expression>
        </expressionList>
        <symbol> ) </symbol>
        <symbol> ; </symbol>
        </doStatement>
        <returnStatement>
        <keyword> return </keyword>
        <symbol> ; </symbol>
        </returnStatement>
        </statements>
        <symbol> } </symbol>
        </subroutineBody>
        </subroutineDec>
        """)

        result_buffer = StringIO(result)
        result_lines = result_buffer.readlines()

        self.assertEqual(result_lines, file_lines)
        self.assertEqual(len(result_lines), len(file_lines))

        count = 0
        for line in result_lines:
            self.assertEqual(line, file_lines[count])
            count = count + 1

        mock_sub_routine = """
        method void moveDown() {
           if ((y + size) < 254) {
              do Screen.setColor(false);
              do Screen.drawRectangle(x, y, x + size, y + 1);
              let y = y + 2;
              do Screen.setColor(true);
              do Screen.drawRectangle(x, (y + size) - 1, x + size, y + size);
           }
           return;
        }
        """
        jack_mock_in_file = StringIO(mock_sub_routine)
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file, write_xml=True)

        # while comp_eng.tokenizer.has_more_tokens():
        comp_eng.tokenizer.advance()
        comp_eng.compile_subroutine()

        comp_eng.outfile.seek(0)
        file_lines = comp_eng.outfile.readlines()

        result = dedent("""\
<subroutineDec>
<keyword> method </keyword>
<keyword> void </keyword>
<identifier> moveDown </identifier>
<symbol> ( </symbol>
<parameterList>
</parameterList>
<symbol> ) </symbol>
<subroutineBody>
<symbol> { </symbol>
<statements>
<ifStatement>
<keyword> if </keyword>
<symbol> ( </symbol>
<expression>
<term>
<symbol> ( </symbol>
<expression>
<term>
<identifier> y </identifier>
</term>
<symbol> + </symbol>
<term>
<identifier> size </identifier>
</term>
</expression>
<symbol> ) </symbol>
</term>
<symbol> &lt; </symbol>
<term>
<integerConstant> 254 </integerConstant>
</term>
</expression>
<symbol> ) </symbol>
<symbol> { </symbol>
<statements>
<doStatement>
<keyword> do </keyword>
<identifier> Screen </identifier>
<symbol> . </symbol>
<identifier> setColor </identifier>
<symbol> ( </symbol>
<expressionList>
<expression>
<term>
<keyword> false </keyword>
</term>
</expression>
</expressionList>
<symbol> ) </symbol>
<symbol> ; </symbol>
</doStatement>
<doStatement>
<keyword> do </keyword>
<identifier> Screen </identifier>
<symbol> . </symbol>
<identifier> drawRectangle </identifier>
<symbol> ( </symbol>
<expressionList>
<expression>
<term>
<identifier> x </identifier>
</term>
</expression>
<symbol> , </symbol>
<expression>
<term>
<identifier> y </identifier>
</term>
</expression>
<symbol> , </symbol>
<expression>
<term>
<identifier> x </identifier>
</term>
<symbol> + </symbol>
<term>
<identifier> size </identifier>
</term>
</expression>
<symbol> , </symbol>
<expression>
<term>
<identifier> y </identifier>
</term>
<symbol> + </symbol>
<term>
<integerConstant> 1 </integerConstant>
</term>
</expression>
</expressionList>
<symbol> ) </symbol>
<symbol> ; </symbol>
</doStatement>
<letStatement>
<keyword> let </keyword>
<identifier> y </identifier>
<symbol> = </symbol>
<expression>
<term>
<identifier> y </identifier>
</term>
<symbol> + </symbol>
<term>
<integerConstant> 2 </integerConstant>
</term>
</expression>
<symbol> ; </symbol>
</letStatement>
<doStatement>
<keyword> do </keyword>
<identifier> Screen </identifier>
<symbol> . </symbol>
<identifier> setColor </identifier>
<symbol> ( </symbol>
<expressionList>
<expression>
<term>
<keyword> true </keyword>
</term>
</expression>
</expressionList>
<symbol> ) </symbol>
<symbol> ; </symbol>
</doStatement>
<doStatement>
<keyword> do </keyword>
<identifier> Screen </identifier>
<symbol> . </symbol>
<identifier> drawRectangle </identifier>
<symbol> ( </symbol>
<expressionList>
<expression>
<term>
<identifier> x </identifier>
</term>
</expression>
<symbol> , </symbol>
<expression>
<term>
<symbol> ( </symbol>
<expression>
<term>
<identifier> y </identifier>
</term>
<symbol> + </symbol>
<term>
<identifier> size </identifier>
</term>
</expression>
<symbol> ) </symbol>
</term>
<symbol> - </symbol>
<term>
<integerConstant> 1 </integerConstant>
</term>
</expression>
<symbol> , </symbol>
<expression>
<term>
<identifier> x </identifier>
</term>
<symbol> + </symbol>
<term>
<identifier> size </identifier>
</term>
</expression>
<symbol> , </symbol>
<expression>
<term>
<identifier> y </identifier>
</term>
<symbol> + </symbol>
<term>
<identifier> size </identifier>
</term>
</expression>
</expressionList>
<symbol> ) </symbol>
<symbol> ; </symbol>
</doStatement>
</statements>
<symbol> } </symbol>
</ifStatement>
<returnStatement>
<keyword> return </keyword>
<symbol> ; </symbol>
</returnStatement>
</statements>
<symbol> } </symbol>
</subroutineBody>
</subroutineDec>
        """)

        result_buffer = StringIO(result)
        result_lines = result_buffer.readlines()

        self.assertEqual(result_lines, file_lines)
        self.assertEqual(len(result_lines), len(file_lines))

        count = 0
        for line in result_lines:
            self.assertEqual(line, file_lines[count])
            count = count + 1

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

    def add_subroutine_scope(self):
        self._comp_eng._symbol_table.start_class()
        self._comp_eng._symbol_table.define("total", IdentifierType.INT.value, IdentifierKind.FIELD.value)

        self._comp_eng._symbol_table.start_subroutine()
        self._comp_eng._symbol_table.define("x", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self._comp_eng._symbol_table.define("a", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self._comp_eng._symbol_table.define("b", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self._comp_eng._symbol_table.define("c", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self._comp_eng._symbol_table.define("sum", IdentifierType.INT.value, IdentifierKind.VAR.value)

    def add_subroutine_scope_2(self):
        self._comp_eng._symbol_table.start_subroutine()
        self._comp_eng._symbol_table.define("a", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self._comp_eng._symbol_table.define("b", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self._comp_eng._symbol_table.define("c", IdentifierType.INT.value, IdentifierKind.VAR.value)

    def test_compile_expression_simple(self):
        jack_mock_expression = dedent("""\
        x - 10;
        """)
        jack_mock_in_file = StringIO(jack_mock_expression)

        self._comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=StringIO(), write_xml=False)

        self.add_subroutine_scope()

        self.assertEqual("var", self._comp_eng._symbol_table.kind_of("x"))

        self._comp_eng._tokenizer.advance()
        self._comp_eng.compile_expression()

        correct_output = dedent("""\
        push local 0
        push constant 10
        sub
        """)
        mock_output = StringIO(correct_output)
        mock_result = mock_output.readlines()

        self._comp_eng._vm_writer.outfile.seek(0)
        lines = self._comp_eng._vm_writer.outfile.readlines()

        self.assertEqual(mock_result, lines)

        jack_mock_expression = dedent("""\
        a + b * c;
        """)
        jack_mock_in_file = StringIO(jack_mock_expression)

        self._comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=StringIO(), write_xml=False)
        self.add_subroutine_scope_2()

        self._comp_eng._tokenizer.advance()
        self._comp_eng.compile_expression()

        correct_output = dedent("""\
        push local 0
        push local 1
        add
        push local 2
        Math.multiply 2
        """)
        mock_output = StringIO(correct_output)
        mock_result = mock_output.readlines()

        self._comp_eng._vm_writer.outfile.seek(0)
        lines = self._comp_eng._vm_writer.outfile.readlines()

        self.assertEqual(mock_result, lines)

    def test_compile_expression_priority(self):
        jack_mock_expression = dedent("""\
        a + (b * c);
        """)
        jack_mock_in_file = StringIO(jack_mock_expression)

        self._comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=StringIO(), write_xml=False)
        self.add_subroutine_scope_2()

        self._comp_eng._tokenizer.advance()
        self._comp_eng.compile_expression()

        correct_output = dedent("""\
        push local 0
        push local 1
        push local 2
        Math.multiply 2
        add
        """)
        mock_output = StringIO(correct_output)
        mock_result = mock_output.readlines()

        self._comp_eng._vm_writer.outfile.seek(0)
        lines = self._comp_eng._vm_writer.outfile.readlines()

        self.assertEqual(mock_result, lines)

    def test_compile_expression_object(self):
        jack_mock_expression = dedent("""\
        x - other.getx(point);
        """)

        jack_mock_in_file = StringIO(jack_mock_expression)

        self._comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=StringIO(), write_xml=False)

        self._comp_eng._symbol_table.start_class()
        self._comp_eng._symbol_table.define("other", "Other", IdentifierKind.FIELD)

        self._comp_eng._symbol_table.start_subroutine()
        self._comp_eng._symbol_table.define("x", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self._comp_eng._symbol_table.define("point", "Point", IdentifierKind.VAR.value)

        self._comp_eng._tokenizer.advance()

        self._comp_eng.compile_expression()

        self.assertEqual("x-other.getx()", self._comp_eng.exp)

        correct_output = dedent("""\
        push local 0
        push local 1
        call other.getX 1
        sub
        """)
        mock_output = StringIO(correct_output)
        mock_result = mock_output.readlines()

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

    def test_compile_term(self):
        self.fail()

    def test_compile_expression_list(self):
        self.fail()
