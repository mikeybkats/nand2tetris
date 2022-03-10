# import test framework
import unittest
from parser import Parser
import sys
import os


class TestParser(unittest.TestCase):
    def test_constructor(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_parser_infile(self):
        cwd = os.getcwd() + "/projects/VMTranslator"
        parser = Parser(infile_path=cwd + "/testVM.vm",
                        outfile_path=cwd + "/testOutputVM.asm")
        self.assertEqual(parser.infile_path(), 'testVM.vm')


if __name__ == '__main__':
    unittest.main()
