import sys
import os
from app_state import AppState
from file_handler import FileHandler
from vm_parser import VMParser
from app_state import AppState
from commands import CommandTable
from code_writer import CodeWriter


class VMTranslator:
    def __init__(self, infile_path, outfile_path):
        file_handler = FileHandler(infile_path, outfile_path)
        command_table = CommandTable()
        app_state = AppState(file_handler, command_table)

        self._parser = VMParser(app_state, command_table)
        self._codeWriter = CodeWriter(app_state, file_handler)

    def parseInput(self):
        if self._parser.has_more_commands():
            self._parser.advance()
            cur = self._parser.current_command()
            arg1 = self._parser.arg1()
            arg2 = self._parser.arg2()
            self._codeWriter.command_router(
                self._parser.command_type(), arg1, arg2)
        pass

    def writeOutput(self):
        pass


if __name__ == '__main__':
    outfile_path = 'output.asm'
    if len(sys.argv) == 3:
        outfile_path = sys.argv[2]

    VMTranslator(infile_path=sys.argv[1], outfile_path=outfile_path)
