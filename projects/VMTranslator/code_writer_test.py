import unittest
import os
from code_writer import CodeWriter
from app_state import AppState
from file_handler import FileHandler
from commands import CommandTable

cwd = os.getcwd() + "/projects/VMTranslator"
file_handler = FileHandler(infile_path=cwd + "/testVM.vm",
                           outfile_path=cwd + "/testOutputVM.asm")
app_state = AppState(file_handler, CommandTable())
code_writer = CodeWriter(app_state, file_handler)


class CodeWriterTest(unittest.TestCase):
    def test_constructor(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_set_filename(self):
        # code_writer.set_filename("fooBar.asm")
        pass

    def test_get_push_pop_assembly(self):
        code_writer.get_push_pop_assembly("push", "constant", "10")


if __name__ == '__main__':
    unittest.main()
