import unittest
import os
from JackTokenizer import JackTokenizer
from io import StringIO
from TokenTypes import TokenTypeTable, Token_Type
from textwrap import dedent

class TokenizerTest(unittest.TestCase):
    def test_look_ahead(self):
        jack_mock_class = """
        let side = box.x
        """

        jack_mock_in_file = StringIO(jack_mock_class)
        tokenizer = JackTokenizer(
            inputStreamOrFile=jack_mock_in_file)

        self.assertEqual("let", tokenizer.look_ahead())

        tokenizer.advance()
        self.assertEqual("let", tokenizer.currentToken)
        tokenizer.advance()
        self.assertEqual("side", tokenizer.currentToken)
        tokenizer.advance()
        self.assertEqual("=", tokenizer.currentToken)
        tokenizer.advance()
        self.assertEqual("box", tokenizer.currentToken)
        self.assertEqual(".", tokenizer.look_ahead())

    def test_has_more_tokens(self):
        testFile = StringIO("""
        a test 


        file 
        
        hello             has more         

                     lines

        """)
        tokenizer = JackTokenizer(inputStreamOrFile=testFile)
        self.assertEqual(tokenizer.has_more_tokens(), True)

        tokenizer.advance()
        self.assertEqual("a", tokenizer.currentToken)

        tokenizer.advance()
        self.assertEqual("test", tokenizer.currentToken)

        self.assertEqual(True, tokenizer.has_more_tokens())

        tokenizer.advance()
        self.assertEqual("file", tokenizer.currentToken)

        tokenizer.advance()
        self.assertEqual("hello", tokenizer.currentToken)

        tokenizer.advance()
        self.assertEqual("has", tokenizer.currentToken)

        tokenizer.advance()
        self.assertEqual("more", tokenizer.currentToken)

        tokenizer.advance()
        self.assertEqual("lines", tokenizer.currentToken)

        while tokenizer.has_more_tokens():
            tokenizer.advance()
        self.assertEqual(False, tokenizer.has_more_tokens())

    def test_get_next_token(self):
        # test quotation marks
        test_string_comments = "nonsense * = \"this is a string constant\""
        test_file = StringIO(test_string_comments)
        tokenizer = JackTokenizer(inputStreamOrFile=test_file)

        self.assertEqual(test_string_comments, tokenizer.infile.read())
        tokenizer.infile.seek(0)

        tokenizer.get_next_token(tokenizer.infile)
        token = tokenizer.get_next_token(tokenizer.infile)
        self.assertEqual("*", token)

        token = tokenizer.get_next_token(tokenizer.infile)
        self.assertEqual("=", token)

        token = tokenizer.get_next_token(tokenizer.infile)
        self.assertEqual("this is a string constant", token)

        # test_string = """
        # class Main {
        #     var String io;
        #
        #     let io = "foo"
        # }
        # """
        # test_file = StringIO(test_string)
        # tokenizer = JackTokenizer(inputStreamOrFile=test_file)
        #
        # first_word = tokenizer.get_next_token(test_file)
        # self.assertEqual(first_word, "class")
        # second_word = tokenizer.get_next_token(test_file)
        # self.assertEqual(second_word, "Main")
        # third_word = tokenizer.get_next_token(test_file)
        # self.assertEqual(third_word, "{")
        # fourth_word = tokenizer.get_next_token(test_file)
        # self.assertEqual(fourth_word, "var")
        #
        # test_string2 = """
        # var String io;
        # var int three;
        # """
        # test_file = StringIO(test_string2)
        # tokenizer = JackTokenizer(inputStreamOrFile=test_file)
        # tokenizer.advance()
        # tokenizer.advance()
        # token = tokenizer.get_next_token(test_file)
        # self.assertEqual("io", token)
        # token = tokenizer.get_next_token(test_file)
        # self.assertEqual(";", token)
        #
        # tokenizer.advance()
        # tokenizer.advance()
        # token = tokenizer.get_next_token(test_file)
        # self.assertEqual("three", token)
        #
        # # test symbols
        # test_string = """
        #     var int x, y, z;
        #     var Boolean xgt;
        #     let xgt = x>z;
        #     let y = "\<foo";
        # }
        # """
        # test_file = StringIO(test_string)
        # tokenizer = JackTokenizer(inputStreamOrFile=test_file)
        #
        # # test if it can get commas
        # tokenizer.advance()
        # tokenizer.advance()
        # tokenizer.advance()
        # tokenizer.advance()
        # token = tokenizer.currentToken
        # self.assertEqual(token, ",")
        # tokenizer.advance()
        # tokenizer.advance()
        # token = tokenizer.currentToken
        # self.assertEqual(token, ",")
        #
        # # test if it can get symbols sandwiched between letters
        # while token != "=":
        #     tokenizer.advance()
        #     token = tokenizer.currentToken
        # tokenizer.advance()
        # tokenizer.advance()
        # token = tokenizer.currentToken
        # self.assertEqual(token, ">")
        #
        # # test comments
        # test_string_comments = """
        #     var int x; // x is used for blah
        #     var Boolean xgt; // another comment
        # }
        # """
        # test_file = StringIO(test_string_comments)
        # tokenizer = JackTokenizer(inputStreamOrFile=test_file)
        #
        # tokenizer.advance()
        # tokenizer.advance()
        # tokenizer.advance()
        # tokenizer.advance()
        # tokenizer.advance()
        # self.assertEqual(Token_Type.SYMBOL, tokenizer.token_type())
        # self.assertNotEqual("/", tokenizer.currentToken)
        #


    def test_strip_comments(self):
        mock_comment = dedent("""\
                          // This file is part of www.nand2tetris.org
                          // and the book "The Elements of Computing Systems"
                          // by Nisan and Schocken, MIT Press.
                          // File name: projects/10/Square/SquareGame.jack
                          
                          // (same as projects/09/Square/SquareGame.jack)
                          
                          /**
                          * Implements the Square Dance game.
                          * This simple game allows the user to move a black square around
                          * the screen, and change the square's size during the movement.
                          * When the game starts, a square of 30 by 30 pixels is shown at the
                          * top-left corner of the screen. The user controls the square as follows.
                          * The 4 arrow keys are used to move the square up, down, left, and right.
                          * The 'z' and 'x' keys are used, respectively, to decrement and increment
                          * the square's size. The 'q' key is used to quit the game.
                          */
                          
                          int foo = arg1; // this is a comment
                          """)
        mock_input = StringIO(mock_comment)
        mock_output = "int foo = arg1;"

        tokenizer = JackTokenizer(inputStreamOrFile=mock_input)
        result = tokenizer.strip_comments_from_infile()

        self.assertEqual(mock_output, result.getvalue())

    def test_advance(self):
        testString = """ 
        class Main {
            var String io;

            let io = "foo"
        }
        """
        testFile = StringIO(testString)
        tokenizer = JackTokenizer(inputStreamOrFile=testFile)

        token = tokenizer.currentToken
        self.assertEqual("", token)

        tokenizer.advance()
        token = tokenizer.currentToken
        self.assertEqual("class", token)

        tokenizer.advance()
        tokenizer.advance()
        tokenizer.advance()
        tokenizer.advance()
        token = tokenizer.currentToken
        self.assertEqual("String", token)

        test_string2 = """ 
        baz.bar
        foo[1]
        """
        test_file2 = StringIO(test_string2)
        tokenizer = JackTokenizer(inputStreamOrFile=test_file2)

        tokenizer.advance()
        tokenizer.advance()
        token = tokenizer.currentToken
        self.assertEqual(".", token)

        tokenizer.advance()
        tokenizer.advance()
        tokenizer.advance()
        token = tokenizer.currentToken
        self.assertEqual("[", token)

        tokenizer.advance()
        token = tokenizer.currentToken
        self.assertEqual("1", token)

    def test_tokenTable(self):
        tokenTable = TokenTypeTable()
        tokenType = tokenTable.get_token_type("55555")
        self.assertEqual(tokenType, Token_Type.INT_CONST)

        tokenType = tokenTable.get_token_type("\"my_string\"")
        self.assertEqual(tokenType, Token_Type.STRING_CONST)

        tokenType = tokenTable.get_token_type("'my_string'")
        self.assertEqual(tokenType, Token_Type.STRING_CONST)

        tokenType = tokenTable.get_token_type("let")
        self.assertEqual(tokenType, Token_Type.KEYWORD)

    def test_tokenType(self):
        testString = """
        class Main {
            var String io;
            var int number;

            method hello(){
                let io = "foo";
                let number = 55412;
            }
        }
        """
        testFile = StringIO(testString)
        tokenizer = JackTokenizer(inputStreamOrFile=testFile)

        # class token keyward
        tokenizer.advance()
        self.assertEqual(Token_Type.KEYWORD, tokenizer.token_type())

        # Main identifier
        tokenizer.advance()
        self.assertEqual(Token_Type.IDENTIFIER, tokenizer.token_type())

        # {} token symbol
        tokenizer.advance()
        self.assertEqual(Token_Type.SYMBOL, tokenizer.token_type())

        # ; semi colon
        token = tokenizer.currentToken
        while token != ";":
            tokenizer.advance()
            token = tokenizer.currentToken
        self.assertEqual(Token_Type.SYMBOL, tokenizer.token_type())

        # identifier
        token = tokenizer.currentToken
        while token != "hello":
            tokenizer.advance()
            token = tokenizer.currentToken
        self.assertEqual(Token_Type.IDENTIFIER, tokenizer.token_type())

        # string const
        token = tokenizer.currentToken
        while token != "\"foo\"":
            tokenizer.advance()
            token = tokenizer.currentToken
        self.assertEqual(Token_Type.STRING_CONST, tokenizer.token_type())

        # int constant
        token = tokenizer.currentToken
        while token != "55412":
            tokenizer.advance()
            token = tokenizer.currentToken
        self.assertEqual(Token_Type.INT_CONST, tokenizer.token_type())

    def test_token_type(self):
        test_string = """
        boop 100
        """
        test_file = StringIO(test_string)
        tokenizer = JackTokenizer(inputStreamOrFile=test_file)
        tokenizer.advance()
        token_type = tokenizer.token_type()
        self.assertEqual(token_type, Token_Type.IDENTIFIER)

        tokenizer.advance()
        token_type = tokenizer.token_type()
        self.assertEqual(token_type, Token_Type.INT_CONST)
