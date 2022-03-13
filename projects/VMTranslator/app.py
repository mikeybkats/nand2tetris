import sys
import os
from app_state import AppState
from file_handler import FileHandler
from vm_parser import VMParser
from app_state import AppState
from commands import CommandTable, Commands
from code_writer import CodeWriter


class VMTranslator:
    def __init__(self, infile_path, outfile_path):
        file_handler = FileHandler(infile_path, outfile_path)
        command_table = CommandTable()
        self._app_state = AppState(file_handler, command_table)

        self._parser = VMParser(self._app_state, command_table)
        self._codeWriter = CodeWriter(self._app_state, file_handler)

    def parseInput(self):
        while self._parser.has_more_commands():
            self._parser.advance()
            arg1 = self._parser.arg1()
            arg2 = ""
            if self._app_state.current_command_type == Commands.C_PUSH or self._app_state.current_command_type == Commands.C_POP or self._app_state.current_command_type == Commands.C_FUNCTION or self._app_state.current_command_type == Commands.C_CALL:
                arg2 = self._parser.arg2()
            if self._parser.current_command and arg1:
                self._codeWriter.command_router(
                    self._parser.current_command, arg1, arg2)

    def writeOutput(self):
        self._codeWriter.close_write_output()


if __name__ == '__main__':
    outfile_path = 'output.asm'
    if len(sys.argv) == 3:
        outfile_path = sys.argv[2]

    vmTrans = VMTranslator(infile_path=sys.argv[1], outfile_path=outfile_path)
    vmTrans.parseInput()
    vmTrans.writeOutput()
