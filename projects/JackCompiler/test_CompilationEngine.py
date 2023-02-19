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
            input_stream=jack_mock_in_file, output_stream=StringIO())

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

#     def test_compile_subroutine_xml(self):
#         mock_sub_routine = """
#         method void moveSquare() {
#             if (direction = 1) { do square.moveUp(); }
#             if (direction = 2) { do square.moveDown(); }
#             if (direction = 3) { do square.moveLeft(); }
#             if (direction = 4) { do square.moveRight(); }
#             do Sys.wait(5);  // delays the next movement
#             return;
#          }
#         """
#         jack_mock_in_file = StringIO(mock_sub_routine)
#         mock_output_file = StringIO()
#         comp_eng = CompilationEngine(
#             input_stream=jack_mock_in_file, output_stream=mock_output_file, write_xml=True)
#
#         # while comp_eng.tokenizer.has_more_tokens():
#         comp_eng.tokenizer.advance()
#         comp_eng.compile_subroutine()
#
#         comp_eng.outfile.seek(0)
#         file_lines = comp_eng.outfile.readlines()
#
#         result = dedent("""\
#         <subroutineDec>
#         <keyword> method </keyword>
#         <keyword> void </keyword>
#         <identifier> moveSquare </identifier>
#         <symbol> ( </symbol>
#         <parameterList>
#         </parameterList>
#         <symbol> ) </symbol>
#         <subroutineBody>
#         <symbol> { </symbol>
#         <statements>
#         <ifStatement>
#         <keyword> if </keyword>
#         <symbol> ( </symbol>
#         <expression>
#         <term>
#         <identifier> direction </identifier>
#         </term>
#         <symbol> = </symbol>
#         <term>
#         <integerConstant> 1 </integerConstant>
#         </term>
#         </expression>
#         <symbol> ) </symbol>
#         <symbol> { </symbol>
#         <statements>
#         <doStatement>
#         <keyword> do </keyword>
#         <identifier> square </identifier>
#         <symbol> . </symbol>
#         <identifier> moveUp </identifier>
#         <symbol> ( </symbol>
#         <expressionList>
#         </expressionList>
#         <symbol> ) </symbol>
#         <symbol> ; </symbol>
#         </doStatement>
#         </statements>
#         <symbol> } </symbol>
#         </ifStatement>
#         <ifStatement>
#         <keyword> if </keyword>
#         <symbol> ( </symbol>
#         <expression>
#         <term>
#         <identifier> direction </identifier>
#         </term>
#         <symbol> = </symbol>
#         <term>
#         <integerConstant> 2 </integerConstant>
#         </term>
#         </expression>
#         <symbol> ) </symbol>
#         <symbol> { </symbol>
#         <statements>
#         <doStatement>
#         <keyword> do </keyword>
#         <identifier> square </identifier>
#         <symbol> . </symbol>
#         <identifier> moveDown </identifier>
#         <symbol> ( </symbol>
#         <expressionList>
#         </expressionList>
#         <symbol> ) </symbol>
#         <symbol> ; </symbol>
#         </doStatement>
#         </statements>
#         <symbol> } </symbol>
#         </ifStatement>
#         <ifStatement>
#         <keyword> if </keyword>
#         <symbol> ( </symbol>
#         <expression>
#         <term>
#         <identifier> direction </identifier>
#         </term>
#         <symbol> = </symbol>
#         <term>
#         <integerConstant> 3 </integerConstant>
#         </term>
#         </expression>
#         <symbol> ) </symbol>
#         <symbol> { </symbol>
#         <statements>
#         <doStatement>
#         <keyword> do </keyword>
#         <identifier> square </identifier>
#         <symbol> . </symbol>
#         <identifier> moveLeft </identifier>
#         <symbol> ( </symbol>
#         <expressionList>
#         </expressionList>
#         <symbol> ) </symbol>
#         <symbol> ; </symbol>
#         </doStatement>
#         </statements>
#         <symbol> } </symbol>
#         </ifStatement>
#         <ifStatement>
#         <keyword> if </keyword>
#         <symbol> ( </symbol>
#         <expression>
#         <term>
#         <identifier> direction </identifier>
#         </term>
#         <symbol> = </symbol>
#         <term>
#         <integerConstant> 4 </integerConstant>
#         </term>
#         </expression>
#         <symbol> ) </symbol>
#         <symbol> { </symbol>
#         <statements>
#         <doStatement>
#         <keyword> do </keyword>
#         <identifier> square </identifier>
#         <symbol> . </symbol>
#         <identifier> moveRight </identifier>
#         <symbol> ( </symbol>
#         <expressionList>
#         </expressionList>
#         <symbol> ) </symbol>
#         <symbol> ; </symbol>
#         </doStatement>
#         </statements>
#         <symbol> } </symbol>
#         </ifStatement>
#         <doStatement>
#         <keyword> do </keyword>
#         <identifier> Sys </identifier>
#         <symbol> . </symbol>
#         <identifier> wait </identifier>
#         <symbol> ( </symbol>
#         <expressionList>
#         <expression>
#         <term>
#         <integerConstant> 5 </integerConstant>
#         </term>
#         </expression>
#         </expressionList>
#         <symbol> ) </symbol>
#         <symbol> ; </symbol>
#         </doStatement>
#         <returnStatement>
#         <keyword> return </keyword>
#         <symbol> ; </symbol>
#         </returnStatement>
#         </statements>
#         <symbol> } </symbol>
#         </subroutineBody>
#         </subroutineDec>
#         """)
#
#         result_buffer = StringIO(result)
#         result_lines = result_buffer.readlines()
#
#         self.assertEqual(result_lines, file_lines)
#         self.assertEqual(len(result_lines), len(file_lines))
#
#         count = 0
#         for line in result_lines:
#             self.assertEqual(line, file_lines[count])
#             count = count + 1
#
#         mock_sub_routine = """
#         method void moveDown() {
#            if ((y + size) < 254) {
#               do Screen.setColor(false);
#               do Screen.drawRectangle(x, y, x + size, y + 1);
#               let y = y + 2;
#               do Screen.setColor(true);
#               do Screen.drawRectangle(x, (y + size) - 1, x + size, y + size);
#            }
#            return;
#         }
#         """
#         jack_mock_in_file = StringIO(mock_sub_routine)
#         mock_output_file = StringIO()
#         comp_eng = CompilationEngine(
#             input_stream=jack_mock_in_file, output_stream=mock_output_file, write_xml=True)
#
#         # while comp_eng.tokenizer.has_more_tokens():
#         comp_eng.tokenizer.advance()
#         comp_eng.compile_subroutine()
#
#         comp_eng.outfile.seek(0)
#         file_lines = comp_eng.outfile.readlines()
#
#         result = dedent("""\
# <subroutineDec>
# <keyword> method </keyword>
# <keyword> void </keyword>
# <identifier> moveDown </identifier>
# <symbol> ( </symbol>
# <parameterList>
# </parameterList>
# <symbol> ) </symbol>
# <subroutineBody>
# <symbol> { </symbol>
# <statements>
# <ifStatement>
# <keyword> if </keyword>
# <symbol> ( </symbol>
# <expression>
# <term>
# <symbol> ( </symbol>
# <expression>
# <term>
# <identifier> y </identifier>
# </term>
# <symbol> + </symbol>
# <term>
# <identifier> size </identifier>
# </term>
# </expression>
# <symbol> ) </symbol>
# </term>
# <symbol> &lt; </symbol>
# <term>
# <integerConstant> 254 </integerConstant>
# </term>
# </expression>
# <symbol> ) </symbol>
# <symbol> { </symbol>
# <statements>
# <doStatement>
# <keyword> do </keyword>
# <identifier> Screen </identifier>
# <symbol> . </symbol>
# <identifier> setColor </identifier>
# <symbol> ( </symbol>
# <expressionList>
# <expression>
# <term>
# <keyword> false </keyword>
# </term>
# </expression>
# </expressionList>
# <symbol> ) </symbol>
# <symbol> ; </symbol>
# </doStatement>
# <doStatement>
# <keyword> do </keyword>
# <identifier> Screen </identifier>
# <symbol> . </symbol>
# <identifier> drawRectangle </identifier>
# <symbol> ( </symbol>
# <expressionList>
# <expression>
# <term>
# <identifier> x </identifier>
# </term>
# </expression>
# <symbol> , </symbol>
# <expression>
# <term>
# <identifier> y </identifier>
# </term>
# </expression>
# <symbol> , </symbol>
# <expression>
# <term>
# <identifier> x </identifier>
# </term>
# <symbol> + </symbol>
# <term>
# <identifier> size </identifier>
# </term>
# </expression>
# <symbol> , </symbol>
# <expression>
# <term>
# <identifier> y </identifier>
# </term>
# <symbol> + </symbol>
# <term>
# <integerConstant> 1 </integerConstant>
# </term>
# </expression>
# </expressionList>
# <symbol> ) </symbol>
# <symbol> ; </symbol>
# </doStatement>
# <letStatement>
# <keyword> let </keyword>
# <identifier> y </identifier>
# <symbol> = </symbol>
# <expression>
# <term>
# <identifier> y </identifier>
# </term>
# <symbol> + </symbol>
# <term>
# <integerConstant> 2 </integerConstant>
# </term>
# </expression>
# <symbol> ; </symbol>
# </letStatement>
# <doStatement>
# <keyword> do </keyword>
# <identifier> Screen </identifier>
# <symbol> . </symbol>
# <identifier> setColor </identifier>
# <symbol> ( </symbol>
# <expressionList>
# <expression>
# <term>
# <keyword> true </keyword>
# </term>
# </expression>
# </expressionList>
# <symbol> ) </symbol>
# <symbol> ; </symbol>
# </doStatement>
# <doStatement>
# <keyword> do </keyword>
# <identifier> Screen </identifier>
# <symbol> . </symbol>
# <identifier> drawRectangle </identifier>
# <symbol> ( </symbol>
# <expressionList>
# <expression>
# <term>
# <identifier> x </identifier>
# </term>
# </expression>
# <symbol> , </symbol>
# <expression>
# <term>
# <symbol> ( </symbol>
# <expression>
# <term>
# <identifier> y </identifier>
# </term>
# <symbol> + </symbol>
# <term>
# <identifier> size </identifier>
# </term>
# </expression>
# <symbol> ) </symbol>
# </term>
# <symbol> - </symbol>
# <term>
# <integerConstant> 1 </integerConstant>
# </term>
# </expression>
# <symbol> , </symbol>
# <expression>
# <term>
# <identifier> x </identifier>
# </term>
# <symbol> + </symbol>
# <term>
# <identifier> size </identifier>
# </term>
# </expression>
# <symbol> , </symbol>
# <expression>
# <term>
# <identifier> y </identifier>
# </term>
# <symbol> + </symbol>
# <term>
# <identifier> size </identifier>
# </term>
# </expression>
# </expressionList>
# <symbol> ) </symbol>
# <symbol> ; </symbol>
# </doStatement>
# </statements>
# <symbol> } </symbol>
# </ifStatement>
# <returnStatement>
# <keyword> return </keyword>
# <symbol> ; </symbol>
# </returnStatement>
# </statements>
# <symbol> } </symbol>
# </subroutineBody>
# </subroutineDec>
#         """)
#
#         result_buffer = StringIO(result)
#         result_lines = result_buffer.readlines()
#
#         self.assertEqual(result_lines, file_lines)
#         self.assertEqual(len(result_lines), len(file_lines))
#
#         count = 0
#         for line in result_lines:
#             self.assertEqual(line, file_lines[count])
#             count = count + 1

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
            input_stream=jack_mock_in_file, output_stream=StringIO())
        self._comp_eng._class_name = "Square"
        self._comp_eng._symbol_table.start_class()
        self._comp_eng._symbol_table.define(
            i_name="x", i_type=IdentifierType.INT.value, i_kind=IdentifierKind.FIELD.value)
        self._comp_eng._symbol_table.define(
            i_name="y", i_type=IdentifierType.INT.value, i_kind=IdentifierKind.FIELD.value)

        self._comp_eng._tokenizer.advance()
        self._comp_eng.compile_subroutine()

        self.assertEqual(4, len(self._comp_eng._symbol_table._table_subroutine))

        item_this = self._comp_eng._symbol_table._table_subroutine.get("this")
        self.assertEqual({"name": "this", "type": "Square", "kind": "argument", "#": 0}, item_this)

        item_other = self._comp_eng._symbol_table._table_subroutine.get("other")
        self.assertEqual({"name": "other", "type": "Point", "kind": "argument", "#": 1}, item_other)

        item_dx = self._comp_eng._symbol_table._table_subroutine.get("dx")
        self.assertEqual({"name": "dx", "type": "int", "kind": "var", "#": 0}, item_dx)

        item_dy = self._comp_eng._symbol_table._table_subroutine.get("dy")
        self.assertEqual({"name": "dy", "type": "int", "kind": "var", "#": 1}, item_dy)

        correct_output = dedent("""\
        push argument 0
        pop pointer 0
        push this 0
        push argument 1
        call Point.getx 1
        sub
        pop local 0
        push this 1
        push argument 1
        call Point.gety 1
        sub
        pop local 1
        push local 0
        push local 1
        call Math.multiply 2
        push local 1
        push local 1
        call Math.multiply 2
        add
        call Math.sqrt 1
        return
        """)
        mock_output = StringIO(correct_output)
        expected_result = mock_output.readlines()

        self._comp_eng._vm_writer.outfile.seek(0)
        lines = self._comp_eng._vm_writer.outfile.readlines()

        self.assertEqual(expected_result, lines)

    def add_subroutine_scope(self):
        self._comp_eng._symbol_table.start_class()
        self._comp_eng._symbol_table.define("total", IdentifierType.INT.value, IdentifierKind.FIELD.value)

        self._comp_eng._symbol_table.start_subroutine()
        self._comp_eng._symbol_table.define("x", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self._comp_eng._symbol_table.define("a", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self._comp_eng._symbol_table.define("b", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self._comp_eng._symbol_table.define("c", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self._comp_eng._symbol_table.define("sum", IdentifierType.INT.value, IdentifierKind.VAR.value)

    def add_class_scope(self):
        self._comp_eng._symbol_table.start_class()
        self._comp_eng._symbol_table.define("other", "Other", IdentifierKind.FIELD.value)

    def add_subroutine_scope_2(self):
        self._comp_eng._symbol_table.start_subroutine()
        self._comp_eng._symbol_table.define("a", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self._comp_eng._symbol_table.define("b", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self._comp_eng._symbol_table.define("c", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self._comp_eng._symbol_table.define("d", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self._comp_eng._symbol_table.define("x", IdentifierType.INT.value, IdentifierKind.VAR.value)

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
        call Math.multiply 2
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
        call Math.multiply 2
        add
        """)
        mock_output = StringIO(correct_output)
        mock_result = mock_output.readlines()

        self._comp_eng._vm_writer.outfile.seek(0)
        lines = self._comp_eng._vm_writer.outfile.readlines()

        self.assertEqual(mock_result, lines)

        # more priority
        jack_mock_expression = dedent("""\
        a + (b + (c * d));
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
        push local 3
        call Math.multiply 2
        add
        add
        """)
        mock_output = StringIO(correct_output)
        mock_result = mock_output.readlines()

        self._comp_eng._vm_writer.outfile.seek(0)
        lines = self._comp_eng._vm_writer.outfile.readlines()

        self.assertEqual(mock_result, lines)

    def test_compile_expression_object(self):
        # class foo {
        #   field Other other;
        #   method bar(){
        #       var int x;
        #       var Point point;
        #       var int newX;
        #       let point = Point.new();
        #       let newX = x - other.getX(point);
        #   }
        # }
        jack_mock_expression = dedent("""\
        x - other.getX(point);
        """)

        jack_mock_in_file = StringIO(jack_mock_expression)

        self._comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=StringIO(), write_xml=False)

        self.add_class_scope()
        self._comp_eng._symbol_table.start_subroutine()
        self._comp_eng._symbol_table.define("this", "foo", "argument")
        self._comp_eng._symbol_table.define("x", IdentifierType.INT.value, IdentifierKind.VAR.value)
        self._comp_eng._symbol_table.define("point", "Point", IdentifierKind.VAR.value)

        self._comp_eng._tokenizer.advance()

        self._comp_eng.compile_expression()

        self._comp_eng._vm_writer.outfile.seek(0)
        output_lines = self._comp_eng._vm_writer.outfile.readlines()

        self.assertEqual("x-other.getX(point)", self._comp_eng.exp)

        # push this 0 is the value of the field
        correct_output = dedent("""\
        push local 0
        push this 0
        push local 1
        call Other.getX 2
        sub
        """)
        mock_output = StringIO(correct_output)
        mock_result = mock_output.readlines()

        self.assertEqual(mock_result, output_lines)

    def test_compile_parameter_list(self):
        # class BlackJack {
        #     field Prompt prompt;
        #     field String promptString;
        #     field int gameActive;
        #     field Deck deck;
        #     field Score score;
        #
        #     field Array playerCards;
        #     field Array dealerCards;
        #
        #     field int randomizer;
        #
        #     field Boolean hitPlayer;
        #     method void printCard(Card card, int positionY, int offsetX, int shift){
        #         do card.setLocationY(positionY);
        #         do card.setLocationX((shift * 4) + 6 + offsetX);
        #         do card.render();
        #         return;
        #     }
        jack_mock_expression = dedent("""\
        (Card card, int positionY, int offsetX, int shift)
        """)

        jack_mock_in_file = StringIO(jack_mock_expression)

        self._comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=StringIO(), write_xml=False)

        self._comp_eng._symbol_table.start_subroutine()
        self._comp_eng._symbol_table.define("this", "BlackJack", "argument")

        self._comp_eng._tokenizer.advance()
        self._comp_eng.compile_parameter_list()

        subroutine_table = self._comp_eng._symbol_table._table_subroutine

        self.assertEqual({"name": "this", "type": "BlackJack", "kind": "argument", "#": 0}, subroutine_table.get("this"))
        self.assertEqual({"name": "card", "type": "Card", "kind": "argument", "#": 1}, subroutine_table.get("card"))
        self.assertEqual({"name": "positionY", "type": "int", "kind": "argument", "#": 2}, subroutine_table.get("positionY"))
        self.assertEqual({"name": "offsetX", "type": "int", "kind": "argument", "#": 3}, subroutine_table.get("offsetX"))
        self.assertEqual({"name": "shift", "type": "int", "kind": "argument", "#": 4}, subroutine_table.get("shift"))

    def add_blackjack_class_scope(self):
        self._comp_eng._symbol_table.start_class()
        self._comp_eng._symbol_table.define("prompt", "Prompt", "field")
        self._comp_eng._symbol_table.define("promptString", "String", "field")
        self._comp_eng._symbol_table.define("gameActive", "int", "field")
        self._comp_eng._symbol_table.define("deck", "Deck", "field")
        self._comp_eng._symbol_table.define("score", "Score", "field")
        self._comp_eng._symbol_table.define("playerCards", "Array", "field")
        self._comp_eng._symbol_table.define("dealerCards", "Array", "field")
        self._comp_eng._symbol_table.define("randomizer", "int", "field")
        self._comp_eng._symbol_table.define("hitPlayer", "Boolean", "field")

    def test_compile_let(self):
        # class BlackJack {
        #     field Prompt prompt;
        #     field String promptString;
        #     field int gameActive;
        #     field Deck deck;
        #     field Score score;
        #
        #     field Array playerCards;
        #     field Array dealerCards;
        #
        #     field int randomizer;
        #
        #     field Boolean hitPlayer;
        #
        #     constructor BlackJack new() {
        #         let prompt = Prompt.new();
        #         let gameActive = 0;
        #         let playerCards = Array.new(9);
        #         let dealerCards = Array.new(9);
        #         let score = Score.new(0, 0);
        #         let hitPlayer = true;
        #         let deck = Deck.new();
        #
        #         return this;
        #     }
        # }
        jack_mock_expression = dedent("""\
        let prompt = Prompt.new();
        let gameActive = 0;
        let playerCards = Array.new(9);
        let dealerCards = Array.new(9);
        let score = Score.new(0, 0);
        let hitPlayer = true;
        let deck = Deck.new();
        """)

        jack_mock_in_file = StringIO(jack_mock_expression)

        self._comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=StringIO(), write_xml=False)

        self.add_blackjack_class_scope()
        self._comp_eng._symbol_table.start_subroutine()
        self._comp_eng._symbol_table.define("this", "BlackJack", "argument")

        self._comp_eng._tokenizer.advance()
        self._comp_eng.compile_statements()

        self._comp_eng._vm_writer.outfile.seek(0)
        output_lines = self._comp_eng._vm_writer.outfile.readlines()

        correct_output = dedent("""\
        call Prompt.new 0
        pop this 0
        push constant 0
        pop this 2
        push constant 9
        call Array.new 1
        pop this 5
        push constant 9
        call Array.new 1
        pop this 6
        push constant 0
        push constant 0
        call Score.new 2
        pop this 4
        push constant 1
        neg
        pop this 8
        call Deck.new 0
        pop this 3
        """)
        mock_output = StringIO(correct_output)
        expected_result = mock_output.readlines()

        self.assertEqual(expected_result, output_lines)

    def test_compile_do(self):
        pass

    def test_compile_while(self):
        pass

    def test_compile_if(self):
        pass

    def test_compile_else(self):
        pass

    def test_compile_return(self):
        pass

    def test_compile_term(self):
        pass

    def test_compile_expression_list(self):
        pass

    def test_compile_var_declaration(self):
        pass

    def test_compile_statements(self):
        pass

