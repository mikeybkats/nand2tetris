# this import is not working
from projects.seven.VMTranslator import Parser

# import test framework
import unittest


class TestParser(unittest.TestCase):
    def test_constructor(self):
        self.assertEqual('foo'.upper(), 'FOO')
        # self.parser = Parser(infile_path="helloVM.vm",
        #                      outfile_path="helloVM.asm")

    # def test_parser_infile(self):
    #     self.assertEqual(self.parser.infile(), 'helloVM.vm')


if __name__ == '__main__':
    unittest.main()
