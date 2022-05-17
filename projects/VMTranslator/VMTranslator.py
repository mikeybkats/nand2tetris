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
        command_table = CommandTable()

        if os.path.isdir(infile_path):
            self._fileList = os.listdir(infile_path)
            self._file_handler = FileHandler(
                infile_path + "/" + self._fileList[0], outfile_path)
        else:
            self._file_handler = FileHandler(infile_path, outfile_path)
            self._file_handler.open_input_file()

        self._app_state = AppState(self._file_handler, command_table)
        self._parser = VMParser(self._app_state, command_table)
        self._codeWriter = CodeWriter(self._app_state, self._file_handler)

    def writeFileInit(self):
        self._codeWriter.write_init()

    def parseFileInput(self):
        while self._parser.has_more_commands():
            self._parser.advance()
            arg1 = self._parser.arg1()
            arg2 = ""
            if (self._app_state.current_command_type == Commands.C_PUSH or
                self._app_state.current_command_type == Commands.C_POP or
                self._app_state.current_command_type == Commands.C_FUNCTION or
                self._app_state.current_command_type == Commands.C_CALL
                ):
                arg2 = self._parser.arg2()
            if self._parser.current_command:
                self._codeWriter.command_router(
                    self._parser.current_command, arg1, arg2)

    def parseDirectoryInput(self, infile_path):
        hasFiles = False
        for fileName in self._fileList:
            if fileName == "Sys.vm":
                hasFiles = True
                new_infile_path = infile_path + "/" + fileName
                self._file_handler.infile_path = new_infile_path
                self._file_handler.open_input_file()
                self.writeFileInit()
                vmTrans.parseFileInput()
                self._fileList.remove("Sys.vm")
        for fileName in self._fileList:
            if fileName.endswith(".vm"):
                hasFiles = True
                new_infile_path = infile_path + "/" + fileName
                self._file_handler.infile_path = new_infile_path
                self._file_handler.open_input_file()

                vmTrans.parseFileInput()

        if hasFiles:
            vmTrans.writeOutput()
        else:
            print("No input at given location.")

    def writeOutput(self):
        self._codeWriter.close_write_output()


if __name__ == '__main__':
    infile_path = sys.argv[1]
    outfile_path = "Sys.asm"

    # if an outfile name is designated
    if len(sys.argv) == 3:
        outfile_path = os.path.realpath(infile_path) + "/" + sys.argv[2]
    else:
        # if the path is a directory
        if os.path.isdir(infile_path):
            outfile_path = infile_path + "/" + \
                os.path.basename(os.path.normpath(infile_path)) + ".asm"
        else:
            outfile_path = infile_path.replace(".vm", ".asm")

    vmTrans = VMTranslator(infile_path=infile_path, outfile_path=outfile_path)

    if os.path.isdir(infile_path):
        vmTrans.parseDirectoryInput(infile_path)
    else:
        vmTrans.parseFileInput()
        vmTrans.writeOutput()
