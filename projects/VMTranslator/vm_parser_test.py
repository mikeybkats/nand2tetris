import unittest
from vm_parser import VMParser
from app_state import AppState
from file_handler import FileHandler
from commands import Commands, CommandTable
import sys
import os

cwd = os.getcwd() + "/projects/VMTranslator"

file_handler = FileHandler(infile_path=cwd + "/testVM.vm",
                           outfile_path=cwd + "/testOutputVM.asm")
command_table = CommandTable()
app_state = AppState(file_handler, command_table)
parser = VMParser(app_state, command_table)


class TestParser(unittest.TestCase):
    def test_constructor(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_parser_has_more_commands(self):
        parser.state().infile.seek(0, 0)
        self.assertEqual(parser.has_more_commands(), True)
        parser.state().infile.seek(0, 2)
        self.assertEqual(parser.has_more_commands(), False)

    def test_remove_comments(self):
        word = parser.remove_comments(
            "push local 10 // pushes value to local memory")
        self.assertEqual(word, "push local 10")
        word2 = parser.remove_comments(
            "              push local 10                 // pushes value to local memory")
        self.assertEqual(word2, "push local 10")

    def test_state(self):
        self.assertIsNotNone(parser.state)

    def test_current_command(self):
        parser.state().infile.seek(0, 0)
        parser.advance()
        command = parser.current_command
        self.assertEqual(command, "push constant 10")

    def test_advance(self):
        parser.state().infile.seek(0, 0)
        parser.advance()
        word = parser.state().current_command
        self.assertEqual(word, "push constant 10")

        parser.advance()
        word = parser.state().current_command
        self.assertEqual(word, "push constant 5")

        parser.advance()
        word = parser.state().current_command
        self.assertEqual(word, "add")
        self.assertEqual(parser.has_more_commands(), True)

    def test_while_has_more_commands(self):
        count = 0
        while parser.has_more_commands():
            parser.advance()
            count = count + 1
        self.assertEqual(count, 13)

    def test_arg1(self):
        parser.state().infile.seek(0, 0)
        parser.advance()
        arg1 = parser.arg1()
        self.assertEqual(arg1, "constant")

    def test_arg2(self):
        parser.state().infile.seek(0, 0)
        parser.advance()
        arg2 = parser.arg2()
        self.assertEqual(arg2, 10)

    def test_command_type(self):
        parser.state().infile.seek(0, 0)
        parser.advance()
        commandType = parser.command_type()
        self.assertEqual(commandType, Commands.C_PUSH)

        parser.advance()
        commandType = parser.command_type()
        self.assertEqual(commandType, Commands.C_PUSH)

        parser.advance()
        commandType = parser.command_type()
        self.assertEqual(commandType, Commands.C_ARITHMETIC)


if __name__ == '__main__':
    unittest.main()
