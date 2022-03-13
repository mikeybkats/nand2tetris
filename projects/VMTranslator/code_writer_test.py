import unittest
import os
import sys
from code_writer import CodeWriter
from app_state import AppState
from file_handler import FileHandler
from commands import CommandTable

cwd = os.getcwd() + "/projects/VMTranslator"
outfile_path = cwd + "/testOutputVM.asm"
file_handler = FileHandler(infile_path=cwd + "/testVM.vm",
                           outfile_path=outfile_path)
app_state = AppState(file_handler, CommandTable())
code_writer = CodeWriter(app_state, file_handler)


class CodeWriterTest(unittest.TestCase):
    def test_constructor(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_set_filename(self):
        # code_writer.set_filename("fooBar.asm")
        pass

    def test_get_push_pop_assembly(self):
        # file_handler.outfile.truncate()
        assembly = code_writer.get_push_pop_assembly("push", "constant", "10")
        self.assertEqual("@10\nD=A\n@0\nA=M\nM=D\n@0\nM=M+1\n", assembly)

    def test_write_push_pop(self):
        code_writer.write_push_pop("push", "constant", "10")
        file_handler.outfile.close()
        file_contents = open(outfile_path, mode='r').read()
        self.assertMultiLineEqual(
            "@10\nD=A\n@0\nA=M\nM=D\n@0\nM=M+1\n", file_contents)


if __name__ == '__main__':
    unittest.main()
