import unittest
import io
from io import StringIO
from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer
from textwrap import dedent

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
        jack_mock_class = dedent("""\
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/10/Square/Square.jack

// (same as projects/09/Square/Square.jack)

/** Implements a graphical square. */
class Square {

   field int x, y; // screen location of the square's top-left corner
   field int size; // length of this square, in pixels

   /** Constructs a new square with a given location and size. */
   // this is a parameter list
   constructor Square new(int Ax, int Ay, int Asize) {
      let x = Ax;
      let y = Ay;
      let size = Asize;
      do draw();
      return this;
   }

   /** Disposes this square. */
   method void dispose() {
      do Memory.deAlloc(this);
      return;
   }

   /** Draws the square on the screen. */
   method void draw() {
      do Screen.setColor(true);
      // this is an expression list
      do Screen.drawRectangle(x, y, x + size, y + size);
      return;
   }

   /** Erases the square from the screen. */
   method void erase() {
      do Screen.setColor(false);
      do Screen.drawRectangle(x, y, x + size, y + size);
      return;
   }

    /** Increments the square size by 2 pixels. */
   method void incSize() {
      if (((y + size) < 254) & ((x + size) < 510)) {
         do erase();
         let size = size + 2;
         do draw();
      }
      return;
   }

   /** Decrements the square size by 2 pixels. */
   method void decSize() {
      if (size > 2) {
         do erase();
         let size = size - 2;
         do draw();
      }
      return;
   }

   /** Moves the square up by 2 pixels. */
   method void moveUp() {
      if (y > 1) {
         do Screen.setColor(false);
         do Screen.drawRectangle(x, (y + size) - 1, x + size, y + size);
         let y = y - 2;
         do Screen.setColor(true);
         do Screen.drawRectangle(x, y, x + size, y + 1);
      }
      return;
   }

   /** Moves the square down by 2 pixels. */
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

   /** Moves the square left by 2 pixels. */
   method void moveLeft() {
      if (x > 1) {
         do Screen.setColor(false);
         do Screen.drawRectangle((x + size) - 1, y, x + size, y + size);
         let x = x - 2;
         do Screen.setColor(true);
         do Screen.drawRectangle(x, y, x + 1, y + size);
      }
      return;
   }

   /** Moves the square right by 2 pixels. */
   method void moveRight() {
      if ((x + size) < 510) {
         do Screen.setColor(false);
         do Screen.drawRectangle(x, y, x + 1, y + size);
         let x = x + 2;
         do Screen.setColor(true);
         do Screen.drawRectangle((x + size) - 1, y, x + size, y + size);
      }
      return;
   }
}
        """)
        result_mock = dedent("""\
<class>
<keyword> class </keyword>
<identifier> Square </identifier>
<symbol> { </symbol>
<classVarDec>
<keyword> field </keyword>
<keyword> int </keyword>
<identifier> x </identifier>
<symbol> , </symbol>
<identifier> y </identifier>
<symbol> ; </symbol>
</classVarDec>
<classVarDec>
<keyword> field </keyword>
<keyword> int </keyword>
<identifier> size </identifier>
<symbol> ; </symbol>
</classVarDec>
<subroutineDec>
<keyword> constructor </keyword>
<identifier> Square </identifier>
<identifier> new </identifier>
<symbol> ( </symbol>
<parameterList>
<keyword> int </keyword>
<identifier> Ax </identifier>
<symbol> , </symbol>
<keyword> int </keyword>
<identifier> Ay </identifier>
<symbol> , </symbol>
<keyword> int </keyword>
<identifier> Asize </identifier>
</parameterList>
<symbol> ) </symbol>
<subroutineBody>
<symbol> { </symbol>
<statements>
<letStatement>
<keyword> let </keyword>
<identifier> x </identifier>
<symbol> = </symbol>
<expression>
<term>
<identifier> Ax </identifier>
</term>
</expression>
<symbol> ; </symbol>
</letStatement>
<letStatement>
<keyword> let </keyword>
<identifier> y </identifier>
<symbol> = </symbol>
<expression>
<term>
<identifier> Ay </identifier>
</term>
</expression>
<symbol> ; </symbol>
</letStatement>
<letStatement>
<keyword> let </keyword>
<identifier> size </identifier>
<symbol> = </symbol>
<expression>
<term>
<identifier> Asize </identifier>
</term>
</expression>
<symbol> ; </symbol>
</letStatement>
<doStatement>
<keyword> do </keyword>
<identifier> draw </identifier>
<symbol> ( </symbol>
<expressionList>
</expressionList>
<symbol> ) </symbol>
<symbol> ; </symbol>
</doStatement>
<returnStatement>
<keyword> return </keyword>
<expression>
<term>
<keyword> this </keyword>
</term>
</expression>
<symbol> ; </symbol>
</returnStatement>
</statements>
<symbol> } </symbol>
</subroutineBody>
</subroutineDec>
<subroutineDec>
<keyword> method </keyword>
<keyword> void </keyword>
<identifier> dispose </identifier>
<symbol> ( </symbol>
<parameterList>
</parameterList>
<symbol> ) </symbol>
<subroutineBody>
<symbol> { </symbol>
<statements>
<doStatement>
<keyword> do </keyword>
<identifier> Memory </identifier>
<symbol> . </symbol>
<identifier> deAlloc </identifier>
<symbol> ( </symbol>
<expressionList>
<expression>
<term>
<keyword> this </keyword>
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
<subroutineDec>
<keyword> method </keyword>
<keyword> void </keyword>
<identifier> draw </identifier>
<symbol> ( </symbol>
<parameterList>
</parameterList>
<symbol> ) </symbol>
<subroutineBody>
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
<identifier> size </identifier>
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
<subroutineDec>
<keyword> method </keyword>
<keyword> void </keyword>
<identifier> erase </identifier>
<symbol> ( </symbol>
<parameterList>
</parameterList>
<symbol> ) </symbol>
<subroutineBody>
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
<identifier> size </identifier>
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
<subroutineDec>
<keyword> method </keyword>
<keyword> void </keyword>
<identifier> incSize </identifier>
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
</term>
<symbol> &amp; </symbol>
<term>
<symbol> ( </symbol>
<expression>
<term>
<symbol> ( </symbol>
<expression>
<term>
<identifier> x </identifier>
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
<integerConstant> 510 </integerConstant>
</term>
</expression>
<symbol> ) </symbol>
</term>
</expression>
<symbol> ) </symbol>
<symbol> { </symbol>
<statements>
<doStatement>
<keyword> do </keyword>
<identifier> erase </identifier>
<symbol> ( </symbol>
<expressionList>
</expressionList>
<symbol> ) </symbol>
<symbol> ; </symbol>
</doStatement>
<letStatement>
<keyword> let </keyword>
<identifier> size </identifier>
<symbol> = </symbol>
<expression>
<term>
<identifier> size </identifier>
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
<identifier> draw </identifier>
<symbol> ( </symbol>
<expressionList>
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
<subroutineDec>
<keyword> method </keyword>
<keyword> void </keyword>
<identifier> decSize </identifier>
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
<identifier> size </identifier>
</term>
<symbol> &gt; </symbol>
<term>
<integerConstant> 2 </integerConstant>
</term>
</expression>
<symbol> ) </symbol>
<symbol> { </symbol>
<statements>
<doStatement>
<keyword> do </keyword>
<identifier> erase </identifier>
<symbol> ( </symbol>
<expressionList>
</expressionList>
<symbol> ) </symbol>
<symbol> ; </symbol>
</doStatement>
<letStatement>
<keyword> let </keyword>
<identifier> size </identifier>
<symbol> = </symbol>
<expression>
<term>
<identifier> size </identifier>
</term>
<symbol> - </symbol>
<term>
<integerConstant> 2 </integerConstant>
</term>
</expression>
<symbol> ; </symbol>
</letStatement>
<doStatement>
<keyword> do </keyword>
<identifier> draw </identifier>
<symbol> ( </symbol>
<expressionList>
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
<subroutineDec>
<keyword> method </keyword>
<keyword> void </keyword>
<identifier> moveUp </identifier>
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
<identifier> y </identifier>
</term>
<symbol> &gt; </symbol>
<term>
<integerConstant> 1 </integerConstant>
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
<letStatement>
<keyword> let </keyword>
<identifier> y </identifier>
<symbol> = </symbol>
<expression>
<term>
<identifier> y </identifier>
</term>
<symbol> - </symbol>
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
<subroutineDec>
<keyword> method </keyword>
<keyword> void </keyword>
<identifier> moveLeft </identifier>
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
<identifier> x </identifier>
</term>
<symbol> &gt; </symbol>
<term>
<integerConstant> 1 </integerConstant>
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
<symbol> ( </symbol>
<expression>
<term>
<identifier> x </identifier>
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
<identifier> size </identifier>
</term>
</expression>
</expressionList>
<symbol> ) </symbol>
<symbol> ; </symbol>
</doStatement>
<letStatement>
<keyword> let </keyword>
<identifier> x </identifier>
<symbol> = </symbol>
<expression>
<term>
<identifier> x </identifier>
</term>
<symbol> - </symbol>
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
<integerConstant> 1 </integerConstant>
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
<subroutineDec>
<keyword> method </keyword>
<keyword> void </keyword>
<identifier> moveRight </identifier>
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
<identifier> x </identifier>
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
<integerConstant> 510 </integerConstant>
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
<integerConstant> 1 </integerConstant>
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
<letStatement>
<keyword> let </keyword>
<identifier> x </identifier>
<symbol> = </symbol>
<expression>
<term>
<identifier> x </identifier>
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
<symbol> ( </symbol>
<expression>
<term>
<identifier> x </identifier>
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
<symbol> } </symbol>
</class>
        """)
        jack_mock_in_file = StringIO(jack_mock_class)
        mock_output_file = StringIO()

        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)
        comp_eng.compile_class()
        comp_eng.outfile.seek(0)

        compiled_lines = comp_eng.outfile.readlines()
        result_lines = io.StringIO(result_mock).readlines()

        self.assertEqual(result_lines[0], compiled_lines[0])

        count = 0
        for line in compiled_lines:
            self.assertEqual(result_lines[count], line)
            count = count + 1

    def test_compile_expression(self):
        jack_mock_class = """
        count < 100;
        """
        jack_mock_in_file = StringIO(jack_mock_class)
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)

        comp_eng.tokenizer.advance()
        comp_eng.compile_expression()

        comp_eng.outfile.seek(0)
        file_lines = comp_eng.outfile.readlines()
        self.assertEqual("<expression>\n", file_lines[0])
        self.assertEqual("<term>\n", file_lines[1])
        self.assertEqual("<identifier> count </identifier>\n", file_lines[2])
        self.assertEqual("</term>\n", file_lines[3])
        # self.assertEqual("<symbol> < </symbol>\n", file_lines[4])
        self.assertEqual("<symbol> &lt; </symbol>\n", file_lines[4])
        self.assertEqual("<term>\n", file_lines[5])
        self.assertEqual("<integerConstant> 100 </integerConstant>\n", file_lines[6])
        self.assertEqual("</term>\n", file_lines[7])
        self.assertEqual("</expression>\n", file_lines[8])

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

    def test_compile_let(self):
        jack_mock_class = """
        let game = game;
        """

        jack_mock_in_file = StringIO(jack_mock_class)
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)

        comp_eng.tokenizer.advance()
        comp_eng.compile_let()

        comp_eng.outfile.seek(0)
        count = 0
        file_lines = comp_eng.outfile.readlines()
        self.assertEqual("<letStatement>\n", file_lines[0])
        self.assertEqual("<keyword> let </keyword>\n", file_lines[1])
        self.assertEqual("<identifier> game </identifier>\n", file_lines[2])
        self.assertEqual("<symbol> = </symbol>\n", file_lines[3])
        self.assertEqual("<expression>\n", file_lines[4])
        self.assertEqual("<term>\n", file_lines[5])
        self.assertEqual("<identifier> game </identifier>\n", file_lines[6])
        self.assertEqual("</term>\n", file_lines[7])
        self.assertEqual("</expression>\n", file_lines[8])
        self.assertEqual("<symbol> ; </symbol>\n", file_lines[9])
        self.assertEqual("</letStatement>\n", file_lines[10])

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

    def test_compile_do(self):
        jack_mock_class = """
        do game.dispose(this, that);
        """

        jack_mock_in_file = StringIO(jack_mock_class)
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)

        comp_eng.tokenizer.advance()
        comp_eng.compile_do()

        comp_eng.outfile.seek(0)
        file_lines = comp_eng.outfile.readlines()
        self.assertEqual("<doStatement>\n", file_lines[0])
        self.assertEqual("<keyword> do </keyword>\n", file_lines[1])
        self.assertEqual("<identifier> game </identifier>\n", file_lines[2])
        self.assertEqual("<symbol> . </symbol>\n", file_lines[3])
        self.assertEqual("<identifier> dispose </identifier>\n", file_lines[4])
        self.assertEqual("<symbol> ( </symbol>\n", file_lines[5])
        self.assertEqual("<expressionList>\n", file_lines[6])
        self.assertEqual("<expression>\n", file_lines[7])
        self.assertEqual("<term>\n", file_lines[8])
        self.assertEqual("<keyword> this </keyword>\n", file_lines[9])
        self.assertEqual("</term>\n", file_lines[10])
        self.assertEqual("</expression>\n", file_lines[11])
        self.assertEqual("<symbol> , </symbol>\n", file_lines[12])
        self.assertEqual("<expression>\n", file_lines[13])
        self.assertEqual("<term>\n", file_lines[14])
        self.assertEqual("<identifier> that </identifier>\n", file_lines[15])
        self.assertEqual("</term>\n", file_lines[16])
        self.assertEqual("</expression>\n", file_lines[17])
        self.assertEqual("</expressionList>\n", file_lines[18])

    def test_compile_term(self):
        jack_mock_term = """
        (key = 0)
        """

    def test_compile_while(self):
        jack_mock_class = """
         while (key = 0) {
            let key = Keyboard.keyPressed();
            do moveSquare();
         }
        """

        jack_mock_in_file = StringIO(jack_mock_class)
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)

        comp_eng.tokenizer.advance()
        comp_eng.compile_while()

        comp_eng.outfile.seek(0)
        file_lines = comp_eng.outfile.readlines()
        self.assertEqual("<whileStatement>\n", file_lines[0])
        self.assertEqual("<keyword> while </keyword>\n", file_lines[1])
        self.assertEqual("<symbol> ( </symbol>\n", file_lines[2])
        self.assertEqual("<expression>\n", file_lines[3])
        self.assertEqual("<term>\n", file_lines[4])
        self.assertEqual("<identifier> key </identifier>\n", file_lines[5])
        self.assertEqual("</term>\n", file_lines[6])
        self.assertEqual("<symbol> = </symbol>\n", file_lines[7])
        self.assertEqual("<term>\n", file_lines[8])
        self.assertEqual("<integerConstant> 0 </integerConstant>\n", file_lines[9])
        self.assertEqual("</term>\n", file_lines[10])
        self.assertEqual("</expression>\n", file_lines[11])
        self.assertEqual("<symbol> ) </symbol>\n", file_lines[12])
        self.assertEqual("<symbol> { </symbol>\n", file_lines[13])
        self.assertEqual("<statements>\n", file_lines[14])
        self.assertEqual("<letStatement>\n", file_lines[15])
        self.assertEqual("<keyword> let </keyword>\n", file_lines[16])
        self.assertEqual("<identifier> key </identifier>\n", file_lines[17])
        self.assertEqual("<symbol> = </symbol>\n", file_lines[18])
        self.assertEqual("<expression>\n", file_lines[19])
        self.assertEqual("<term>\n", file_lines[20])
        self.assertEqual("<identifier> Keyboard </identifier>\n", file_lines[21])
        self.assertEqual("<symbol> . </symbol>\n", file_lines[22])
        self.assertEqual("<identifier> keyPressed </identifier>\n", file_lines[23])
        # self.assertEqual("<symbol> ( </symbol>\n", file_lines[24])
        # self.assertEqual("<symbol> ) </symbol>\n", file_lines[25])
        # self.assertEqual("</term>\n", file_lines[26])
        # self.assertEqual("</expression>\n", file_lines[27])
        # self.assertEqual("<symbol> ; </symbol>\n", file_lines[28])
        # self.assertEqual("</letStatement>\n", file_lines[29])
        # self.assertEqual("<doStatement>\n", file_lines[30])
        # self.assertEqual("<keyword> do </keyword>\n", file_lines[31])
        # self.assertEqual("<identifier> moveSquare </identifier>\n", file_lines[32])
        # self.assertEqual("<symbol> ( </symbol>\n", file_lines[33])
        # self.assertEqual("<expressionList>\n", file_lines[34])
        # self.assertEqual("</expressionList>\n", file_lines[35])
        # self.assertEqual("<symbol> ) </symbol>\n", file_lines[36])
        # self.assertEqual("<symbol> ; </symbol>\n", file_lines[37])
        # self.assertEqual("</doStatement>\n", file_lines[38])
        # self.assertEqual("</statements>\n", file_lines[39])
        # self.assertEqual("<symbol> } </symbol>\n", file_lines[40])
        # self.assertEqual("</whileStatement>\n", file_lines[41])

    def test_compile_subroutine(self):
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
            input_stream=jack_mock_in_file, output_stream=mock_output_file)

        while comp_eng.tokenizer.has_more_tokens():
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

        result_buffer = io.StringIO(result)
        result_lines = result_buffer.readlines()

        count = 0
        for line in result_lines:
            self.assertEqual(line, file_lines[count])
            count = count + 1

    def test_compile_parameter_list(self):
        jack_mock_class = """
        constructor Square new(int Ax, int Ay, int Asize) {
        """

        jack_mock_in_file = StringIO(jack_mock_class)
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)

        while comp_eng.tokenizer.currentToken != ")":
            comp_eng.tokenizer.advance()
            if comp_eng.tokenizer.currentToken == "(":
                comp_eng.compile_parameter_list()

        comp_eng.outfile.seek(0)
        file_lines = comp_eng.outfile.readlines()
        self.assertEqual("<parameterList>\n", file_lines[0])
        self.assertEqual("<keyword> int </keyword>\n", file_lines[1])
        self.assertEqual("<identifier> Ax </identifier>\n", file_lines[2])
        self.assertEqual("<symbol> , </symbol>\n", file_lines[3])
        self.assertEqual("<keyword> int </keyword>\n", file_lines[4])
        self.assertEqual("<identifier> Ay </identifier>\n", file_lines[5])
        self.assertEqual("<symbol> , </symbol>\n", file_lines[6])
        self.assertEqual("<keyword> int </keyword>\n", file_lines[7])
        self.assertEqual("<identifier> Asize </identifier>\n", file_lines[8])
        self.assertEqual("<parameterList>\n", file_lines[0])

        result = """
        <parameterList>
              <keyword> int </keyword>
              <identifier> Ax </identifier>
              <symbol> , </symbol>
              <keyword> int </keyword>
              <identifier> Ay </identifier>
              <symbol> , </symbol>
              <keyword> int </keyword>
              <identifier> Asize </identifier>
        </parameterList>
        """

    def test_compile_if(self):
        jack_mock_class = """
        if (direction = 1) {}
        """

        jack_mock_in_file = StringIO(jack_mock_class)
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)

        comp_eng.tokenizer.advance()
        comp_eng.compile_if()

        comp_eng.outfile.seek(0)
        file_lines = comp_eng.outfile.readlines()

        self.assertEqual("<ifStatement>\n", file_lines[0])
        self.assertEqual("<keyword> if </keyword>\n", file_lines[1])
        self.assertEqual("<symbol> ( </symbol>\n", file_lines[2])
        self.assertEqual("<expression>\n", file_lines[3])
        self.assertEqual("<term>\n", file_lines[4])
        self.assertEqual("<identifier> direction </identifier>\n", file_lines[5])
        self.assertEqual("</term>\n", file_lines[6])
        self.assertEqual("<symbol> = </symbol>\n", file_lines[7])
        self.assertEqual("<term>\n", file_lines[8])
        self.assertEqual("<integerConstant> 1 </integerConstant>\n", file_lines[9])
        self.assertEqual("</term>\n", file_lines[10])
        self.assertEqual("</expression>\n", file_lines[11])
        self.assertEqual("<symbol> ) </symbol>\n", file_lines[12])
        self.assertEqual("<symbol> { </symbol>\n", file_lines[13])
        self.assertEqual("<statements>\n", file_lines[14])

        result = """
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
              </statements>
          <symbol> } </symbol>
        </ifStatement>
        """

    def test_compile_var_declaration(self):
        jack_mock_class = """
        var int i, j;
        """

        jack_mock_in_file = StringIO(jack_mock_class)
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)

        comp_eng.tokenizer.advance()
        comp_eng.compile_var_declaration()

        comp_eng.outfile.seek(0)
        file_lines = comp_eng.outfile.readlines()

        self.assertEqual("<varDec>\n", file_lines[0])
        self.assertEqual("<keyword> var </keyword>\n", file_lines[1])
        self.assertEqual("<keyword> int </keyword>\n", file_lines[2])
        self.assertEqual("<identifier> i </identifier>\n", file_lines[3])
        self.assertEqual("<symbol> , </symbol>\n", file_lines[4])
        self.assertEqual("<identifier> j </identifier>\n", file_lines[5])
        self.assertEqual("<symbol> ; </symbol>\n", file_lines[6])
        self.assertEqual("</varDec>\n", file_lines[7])

        result = """
        <varDec>
          <keyword> var </keyword>
          <keyword> int </keyword>
          <identifier> i </identifier>
          <symbol> , </symbol>
          <identifier> j </identifier>
          <symbol> ; </symbol>
        </varDec>
        """

    def test_compile_return(self):
        jack_mock_class = """
        return this;
        """

        jack_mock_class2 = """
        return;
        """

        jack_mock_in_file = StringIO(jack_mock_class)
        mock_output_file = StringIO()
        comp_eng = CompilationEngine(
            input_stream=jack_mock_in_file, output_stream=mock_output_file)

        comp_eng.tokenizer.advance()
        comp_eng.compile_return()

        comp_eng.outfile.seek(0)
        file_lines = comp_eng.outfile.readlines()

        self.assertEqual("<returnStatement>\n", file_lines[0])
        self.assertEqual("<keyword> return </keyword>\n", file_lines[1])
        self.assertEqual("<expression>\n", file_lines[2])
        self.assertEqual("<term>\n", file_lines[3])
        self.assertEqual("<keyword> this </keyword>\n", file_lines[4])
        self.assertEqual("</term>\n", file_lines[5])
        self.assertEqual("</expression>\n", file_lines[6])
        self.assertEqual("<symbol> ; </symbol>\n", file_lines[7])
        self.assertEqual("</returnStatement>\n", file_lines[8])

        jack_mock_in_file2 = StringIO(jack_mock_class2)
        mock_output_file2 = StringIO()
        comp_eng2 = CompilationEngine(
            input_stream=jack_mock_in_file2, output_stream=mock_output_file2)
        comp_eng2.tokenizer.advance()
        comp_eng2.compile_return()
        comp_eng2.outfile.seek(0)
        file_lines = comp_eng2.outfile.readlines()

        self.assertEqual("<returnStatement>\n", file_lines[0])
        self.assertEqual("<keyword> return </keyword>\n", file_lines[1])
        self.assertEqual("<symbol> ; </symbol>\n", file_lines[2])
        self.assertEqual("</returnStatement>\n", file_lines[3])


def test_compile_statements():
    assert False


def test_compile_expression():
    assert False


def test_compile_expression_list():
    assert False
