import unittest
import io
from io import StringIO
from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer
from TokenTypes import Token_Type


class CompilationEngineTest(unittest.TestCase):
    def test_init(self):
        jack_mock_in_file = StringIO()
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)

        # test retrieval of outfile
        outfile = comp_eng.outfile
        self.assertIs(outfile, mock_output_file)

        # test if tokenizer was created
        tokenizer = comp_eng.tokenizer
        self.assertIsInstance(tokenizer, JackTokenizer)

    def test_tokenizer(self):
        jack_mock_in_file = StringIO()
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)

        # test if tokenizer was created
        self.assertIsInstance(comp_eng.tokenizer, JackTokenizer)

    def test_outfile(self):
        jack_mock_in_file = StringIO()
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)

        self.assertIsInstance(comp_eng.outfile, io.StringIO)

    def test_write_xml_tag(self):
        jack_mock_in_file = StringIO()
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)
        comp_eng.write_xml_tag("lolwat")

        comp_eng.outfile.seek(0)
        self.assertEqual(comp_eng.outfile.read(), "<lolwat>")

    def test_write_xml_closing_tag(self):
        jack_mock_in_file = StringIO()
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)
        comp_eng.write_xml_closing_tag("lolwat")

        comp_eng.outfile.seek(0)
        self.assertEqual(comp_eng.outfile.read(), "</lolwat>\n")

    def test_compile_class(self):
        jack_mock_class = """ 
        class Main {
            var String io;
            let io = "foo"
        }
        """
        jack_mock_in_file = StringIO(jack_mock_class)
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)

        comp_eng.compile_class()
        comp_eng.outfile.seek(0)

        # self.assertGreater(len(comp_eng.outfile.read()), 1)
        comp_eng.outfile.seek(0)
        count = 0
        for line in comp_eng.outfile:
            self.assertEqual(True, "foo")
            if count == 0:
                self.assertEqual(line, "<class>\n")
            if count == 1:
                self.assertEqual(line, "<keyword> class </keyword>\n")
            if count == 2:
                self.assertEqual(line, "<identifier> Main </identifier>\n")
            if count == 3:
                self.assertEqual(line, "<symbol> { </symbol>\n")
            if count == 12:
                self.assertEqual(line, "<symbol> } </symbol>\n")
            if count == 13:
                self.assertEqual(line, "</class>\n")
            count = count + 1

    def test_compile_term(self):
        jack_mock_class = """
        count < 100
        """
        jack_mock_in_file = StringIO(jack_mock_class)
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)

        while comp_eng.tokenizer.has_more_tokens():
            comp_eng.tokenizer.advance()
            comp_eng.compile_term()

        comp_eng.outfile.seek(0)
        count = 0
        for line in comp_eng.outfile:
            if count == 0:
                self.assertEqual(line, "<term>\n")
            if count == 1:
                self.assertEqual(line, "<identifier> count </identifier>\n")
            if count == 2:
                self.assertEqual(line, "</term>\n")
            if count == 3:
                self.assertEqual(line, "<symbol> < </symbol>\n")
            if count == 4:
                self.assertEqual("<term>\n", line)
            if count == 5:
                self.assertEqual(comp_eng.tokenizer.currentToken, '100')
                self.assertEqual(comp_eng.tokenizer.token_type(), Token_Type.INT_CONST)
                self.assertEqual(comp_eng.tokenizer.token_type() == Token_Type.INT_CONST, True)
                self.assertEqual("<intConstant> 100 </intConstant>\n", line)
            if count == 6:
                self.assertEqual("</term>\n", line)
            count = count + 1

    def test_compile_class_var_declaration(self):
        jack_mock_class = """
        static boolean test;
        field int count;
        """
        jack_mock_in_file = StringIO(jack_mock_class)
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)

        while comp_eng.tokenizer.has_more_tokens():
            comp_eng.tokenizer.advance()
            comp_eng.compile_class_var_declaration()

        comp_eng.outfile.seek(0)
        count = 0
        for line in comp_eng.outfile:
            if count == 0:
                self.assertEqual("<classVarDec>\n", line)
            if count == 1:
                self.assertEqual("<keyword> static </keyword>\n", line)
            if count == 2:
                self.assertEqual("<keyword> boolean </keyword>\n", line)
            if count == 3:
                self.assertEqual("<identifier> test </identifier>\n", line)
            if count == 4:
                self.assertEqual("<symbol> ; </symbol>\n", line)
            if count == 5:
                self.assertEqual("</classVarDec>\n", line)
            if count == 6:
                self.assertEqual("<classVarDec>\n", line)
            if count == 7:
                self.assertEqual("<keyword> field </keyword>\n", line)
            if count == 8:
                self.assertEqual("<keyword> int </keyword>\n", line)
            if count == 9:
                self.assertEqual("<identifier> count </identifier>\n", line)
            if count == 10:
                self.assertEqual("<symbol> ; </symbol>\n", line)
            if count == 11:
                self.assertEqual("</classVarDec>\n", line)

            count = count + 1

    def test_compile_subroutine(self):
        jack_mock_class = """
        function void main(x, y) {
            var SquareGame game;
            let game = game;
            do game.run();
            do game.dispose();
            return;
        }
        """

        jack_mock_in_file = StringIO(jack_mock_class)
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)

        while comp_eng.tokenizer.has_more_tokens():
            comp_eng.tokenizer.advance()
            comp_eng.compile_subroutine()

        comp_eng.outfile.seek(0)
        count = 0
        file_lines = comp_eng.outfile.readlines()
        self.assertEqual("<subroutineDec>\n", file_lines[0])
        self.assertEqual("<keyword> function </keyword>\n", file_lines[1])
        self.assertEqual("<keyword> void </keyword>\n", file_lines[2])
        self.assertEqual("<identifier> main </identifier>\n", file_lines[3])
        self.assertEqual("<symbol> ( </symbol>\n", file_lines[4])
        self.assertEqual("<parameterList>\n", file_lines[5])
        self.assertEqual("<term>\n", file_lines[6])
        self.assertEqual("<identifier> x </identifier>\n", file_lines[7])
        self.assertEqual("</term>\n", file_lines[8])
        self.assertEqual("<symbol> , </symbol>\n", file_lines[9])
        self.assertEqual("<term>\n", file_lines[10])
        self.assertEqual("<identifier> y </identifier>\n", file_lines[11])
        self.assertEqual("</term>\n", file_lines[12])
        self.assertEqual("</parameterList>\n", file_lines[13])
        self.assertEqual("<symbol> ) </symbol>\n", file_lines[14])
        self.assertEqual("<subroutineBody>\n", file_lines[15])
        self.assertEqual("<symbol> { </symbol>\n", file_lines[16])
        # self.assertEqual("<varDec>\n", file_lines[17])
    #  <subroutineDec>
      #      <keyword> function </keyword>
      #      <keyword> void </keyword>
      #      <identifier> main </identifier>
      #      <symbol> ( </symbol>
      #      <parameterList>
      #      </parameterList>
      #      <symbol> ) </symbol>
      #      <subroutineBody>
      #        <symbol> { </symbol>
      #        <varDec>
      #          <keyword> var </keyword>
      #          <identifier> SquareGame </identifier>
      #          <identifier> game </identifier>
      #          <symbol> ; </symbol>
      #        </varDec>
      #        <statements>
      #          <letStatement>
      #            <keyword> let </keyword>
      #            <identifier> game </identifier>
      #            <symbol> = </symbol>
      #            <expression>
      #              <term>
      #                <identifier> game </identifier>
      #              </term>
      #            </expression>
      #            <symbol> ; </symbol>
      #          </letStatement>
      #          <doStatement>
      #            <keyword> do </keyword>
      #            <identifier> game </identifier>
      #            <symbol> . </symbol>
      #            <identifier> run </identifier>
      #            <symbol> ( </symbol>
      #            <expressionList>
      #            </expressionList>
      #            <symbol> ) </symbol>
      #            <symbol> ; </symbol>
      #          </doStatement>
      #          <doStatement>
      #            <keyword> do </keyword>
      #            <identifier> game </identifier>
      #            <symbol> . </symbol>
      #            <identifier> dispose </identifier>
      #            <symbol> ( </symbol>
      #            <expressionList>
      #            </expressionList>
      #            <symbol> ) </symbol>
      #            <symbol> ; </symbol>
      #          </doStatement>
      #          <returnStatement>
      #            <keyword> return </keyword>
      #            <symbol> ; </symbol>
      #          </returnStatement>
      #        </statements>
      #        <symbol> } </symbol>
      #      </subroutineBody>
      # </subroutineDec>



def test_compile_parameter_list():
    assert False


def test_compile_var_declaration():
    assert False


def test_compile_statements():
    assert False


def test_compile_do():
    assert False


def test_compile_let():
    assert False


def test_compile_while():
    assert False


def test_compile_return():
    assert False


def test_compile_if():
    assert False


def test_compile_expression():
    assert False

def test_compile_expression_list():
    assert False