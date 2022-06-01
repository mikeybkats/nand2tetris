import unittest
import os
from JackTokenizer import JackTokenizer
from io import StringIO
from TokenTypes import TokenTypeTable, Token_Type


class TokenizerTest(unittest.TestCase):
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
        test_string = """ 
        class Main {
            var String io;

            let io = "foo"
        }
        """
        test_file = StringIO(test_string)
        tokenizer = JackTokenizer(inputStreamOrFile=test_file)

        first_word = tokenizer.get_next_token(test_file)
        self.assertEqual(first_word, "class")
        second_word = tokenizer.get_next_token(test_file)
        self.assertEqual(second_word, "Main")
        third_word = tokenizer.get_next_token(test_file)
        self.assertEqual(third_word, "{")
        fourth_word = tokenizer.get_next_token(test_file)
        self.assertEqual(fourth_word, "var")

        test_string2 = """ 
        var String io;
        var int three;
        """
        test_file = StringIO(test_string2)
        tokenizer = JackTokenizer(inputStreamOrFile=test_file)
        tokenizer.advance()
        tokenizer.advance()
        token = tokenizer.get_next_token(test_file)
        self.assertEqual("io", token)
        token = tokenizer.get_next_token(test_file)
        self.assertEqual(";", token)

        tokenizer.advance()
        tokenizer.advance()
        token = tokenizer.get_next_token(test_file)
        self.assertEqual("three", token)

        # test symbols
        test_string = """ 
            var int x, y, z;
            var Boolean xgt;
            let xgt = x>z;
            let y = "\<foo";
        }
        """
        test_file = StringIO(test_string)
        tokenizer = JackTokenizer(inputStreamOrFile=test_file)

        # test if it can get commas
        tokenizer.advance()
        tokenizer.advance()
        tokenizer.advance()
        tokenizer.advance()
        token = tokenizer.currentToken
        self.assertEqual(token, ",")
        tokenizer.advance()
        tokenizer.advance()
        token = tokenizer.currentToken
        self.assertEqual(token, ",")

        # test if it can get symbols sandwiched between letters
        while token != "=":
            tokenizer.advance()
            token = tokenizer.currentToken
        tokenizer.advance()
        tokenizer.advance()
        token = tokenizer.currentToken
        self.assertEqual(token, ">")

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