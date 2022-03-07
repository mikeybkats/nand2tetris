# this import is not working
from projects.VMTranslator.parser import Parser

# import test framework
import unittest


class TestParser(unittest.TestCase):
    def test_constructor(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_parser_infile(self):
        parser = Parser(infile_path="helloVM.vm",
                        outfile_path="helloVM.asm")
        self.assertEqual(parser.infile(), 'helloVM.vm')


if __name__ == '__main__':
    unittest.main()
