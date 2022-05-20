import unittest
import io
from io import StringIO
from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer


jackMockClass = """ 
    class Main {
        var String io;
        let io = "foo"
    }
"""
jackMockInFile = StringIO(jackMockClass)
mockOutputFile = StringIO()


class CompilationEngineTest(unittest.TestCase):
    def test_init(self):
        compEng = CompilationEngine(
            inputFileStream=jackMockInFile, outputFileStream=mockOutputFile)

        # test retrieval of outfile
        outfile = compEng.outfile
        self.assertIs(outfile, mockOutputFile)

        # test if tokenizer was created
        tokenizer = compEng.tokenizer
        self.assertIsInstance(tokenizer, JackTokenizer)

    def test_compile_class(self):
        compEng = CompilationEngine(
            inputFileStream=jackMockInFile, outputFileStream=mockOutputFile)

        compEng.compile_class()
        # compEng.outfile.close()

        count = 0
        with compEng.outfile as file:
            for line in file:
                if count == 0:
                    self.assertEqual(line[count], "<class>")
                if count == 1:
                    self.assertEqual(line[count], "<identifier>")
                if count == 2:
                    self.assertEqual(line[count], "Main")
                if count == 2:
                    self.assertEqual(line[count], "<identifier>")
                count = count + 1
