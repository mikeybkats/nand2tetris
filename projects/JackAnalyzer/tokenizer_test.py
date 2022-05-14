import unittest
import os
from tokenizer import JackTokenizer
from io import StringIO

tokenizer = JackTokenizer(
    inputStreamOrFile=os.getcwd() + '/JackAnalyzer/testFiles/simple.jack')


class TokenizerTest(unittest.TestCase):
    def test_constructor(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_hasMoreTokens(self):
        self.assertEqual(tokenizer.hasMoreTokens(), True)

    def test_getNextToken(self):
        testString = "here are some tokens"
        testFile = StringIO(testString)

        firstWord = tokenizer.getNextToken(testFile)
        self.assertEqual(firstWord, "here")
        secondWord = tokenizer.getNextToken(testFile)
        self.assertEqual(secondWord, "are")
        thirdWord = tokenizer.getNextToken(testFile)
        self.assertEqual(thirdWord, "some")
        fourthWord = tokenizer.getNextToken(testFile)
        self.assertEqual(fourthWord, "tokens")
