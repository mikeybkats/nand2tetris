import unittest
import os
from tokenizer import JackTokenizer
from io import StringIO
from tokenTypes import TokenTypeTable, Token_Type


class TokenizerTest(unittest.TestCase):
    def test_hasMoreTokens(self):
        testFile = StringIO("""a test 


        file 
        
        hello             has more         

                     lines

        """)
        tokenizer = JackTokenizer(inputStreamOrFile=testFile)
        self.assertEqual(tokenizer.hasMoreTokens(), True)

        tokenizer.advance()
        self.assertEqual("a", tokenizer.currentToken)

        tokenizer.advance()
        self.assertEqual("test", tokenizer.currentToken)

        self.assertEqual(True, tokenizer.hasMoreTokens())

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

    def test_getNextToken(self):
        testString = """ 
        class Main {
            var String io;

            let io = "foo"
        }
        """
        testFile = StringIO(testString)
        tokenizer = JackTokenizer(inputStreamOrFile=testFile)

        firstWord = tokenizer.getNextToken(testFile)
        self.assertEqual(firstWord, "class")
        secondWord = tokenizer.getNextToken(testFile)
        self.assertEqual(secondWord, "Main")
        thirdWord = tokenizer.getNextToken(testFile)
        self.assertEqual(thirdWord, "{")
        fourthWord = tokenizer.getNextToken(testFile)
        self.assertEqual(fourthWord, "var")

        testString2 = """ 
        var String io;
        var int three;
        """
        testFile = StringIO(testString2)
        tokenizer = JackTokenizer(inputStreamOrFile=testFile)
        tokenizer.advance()
        tokenizer.advance()
        token = tokenizer.getNextToken(testFile)
        self.assertEqual("io", token)
        token = tokenizer.getNextToken(testFile)
        self.assertEqual(";", token)

        tokenizer.advance()
        tokenizer.advance()
        token = tokenizer.getNextToken(testFile)
        self.assertEqual("three", token)

        # test symbols
        testString = """ 
            var int x, y, z;
            var Boolean xgt;
            let xgt = x>z;
            let y = "\<foo";
        }
        """
        testFile = StringIO(testString)
        tokenizer = JackTokenizer(inputStreamOrFile=testFile)

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

    def test_tokenTable(self):
        tokenTable = TokenTypeTable()
        tokenType = tokenTable.getTokenType("55555")
        self.assertEqual(tokenType, Token_Type.INT_CONST)

        tokenType = tokenTable.getTokenType("\"my_string\"")
        self.assertEqual(tokenType, Token_Type.STRING_CONST)

        tokenType = tokenTable.getTokenType("'my_string'")
        self.assertEqual(tokenType, Token_Type.STRING_CONST)

        tokenType = tokenTable.getTokenType("let")
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
        self.assertEqual(Token_Type.KEYWORD, tokenizer.tokenType())

        # Main identifier
        tokenizer.advance()
        self.assertEqual(Token_Type.IDENTIFIER, tokenizer.tokenType())

        # {} token symbol
        tokenizer.advance()
        self.assertEqual(Token_Type.SYMBOL, tokenizer.tokenType())

        # ; semi colon
        token = tokenizer.currentToken
        while token != ";":
            tokenizer.advance()
            token = tokenizer.currentToken
        self.assertEqual(Token_Type.SYMBOL, tokenizer.tokenType())

        # identifier
        token = tokenizer.currentToken
        while token != "hello":
            tokenizer.advance()
            token = tokenizer.currentToken
        self.assertEqual(Token_Type.IDENTIFIER, tokenizer.tokenType())

        # string const
        token = tokenizer.currentToken
        while token != "\"foo\"":
            tokenizer.advance()
            token = tokenizer.currentToken
        self.assertEqual(Token_Type.STRING_CONST, tokenizer.tokenType())

        # int constant
        token = tokenizer.currentToken
        while token != "55412":
            tokenizer.advance()
            token = tokenizer.currentToken
        self.assertEqual(Token_Type.INT_CONST, tokenizer.tokenType())
