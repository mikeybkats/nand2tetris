# import test framework
import unittest
from parser import Parser
import sys
import os

cwd = os.getcwd() + "/projects/VMTranslator"
parser = Parser(infile_path=cwd + "/testVM.vm",
                outfile_path=cwd + "/testOutputVM.asm")


class TestParser(unittest.TestCase):
    def test_constructor(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_parser_infile(self):
        self.assertEqual(parser.infile_path(), 'testVM.vm')

    def test_parser_has_more_commands(self):
        parser.state().infile().seek(0, 0)
        self.assertEqual(parser.has_more_commands(), True)
        parser.state().infile().seek(0, 2)
        self.assertEqual(parser.has_more_commands(), False)

    def test_remove_comments(self):
        word = parser.remove_comments(
            "push local 10 // pushes value to local memory")
        self.assertEqual(word, "push local 10")

    def test_state(self):
        self.assertIsNotNone(parser.state)

    def test_current_command(self):
        parser.advance()
        command = parser.current_command()
        self.assertEqual(command, "push local 10")

    def test_advance(self):
        parser.advance()
        word = parser.state().current_command
        self.assertEqual(word, "push local 10")

        parser.advance()
        word = parser.state().current_command
        self.assertEqual(word, "push local 5")

        parser.advance()
        word = parser.state().current_command
        self.assertEqual(word, "add")
        self.assertEqual(parser.has_more_commands(), False)


if __name__ == '__main__':
    unittest.main()
