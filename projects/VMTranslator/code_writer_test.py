import unittest
import os
import sys
from code_writer import CodeWriter
from app_state import AppState
from file_handler import FileHandler
from commands import Commands, CommandTable
from vm_parser import VMParser

command_table = CommandTable()
cwd = os.getcwd() + "/projects/VMTranslator"
outfile_path = cwd + "/commandTests/testFile_DO_NOT_EDIT.asm"
file_handler = FileHandler(infile_path=cwd + "/commandTests/testFile_DO_NOT_EDIT.vm",
                           outfile_path=outfile_path)
app_state = AppState(file_handler, command_table)
parser = VMParser(app_state, command_table)
code_writer = CodeWriter(app_state, file_handler)


class CodeWriterTest(unittest.TestCase):
    def test_constructor(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_set_filename(self):
        # code_writer.set_filename("fooBar.asm")
        pass

    def test_get_segment(self):
        segmentValue = code_writer.get_segment("constant")
        self.assertEqual(segmentValue, '0')

    def test_get_push_pop_assembly(self):
        parser.advance()
        arg1 = parser.arg1()
        arg2 = parser.arg2()
        command = app_state.current_command
        assembly = code_writer.get_push_pop_assembly(command, arg1, arg2)
        self.assertEqual("@10\nD=A\n@0\nA=M\nM=D\n@0\nM=M+1\n", assembly)


if __name__ == '__main__':
    unittest.main()
