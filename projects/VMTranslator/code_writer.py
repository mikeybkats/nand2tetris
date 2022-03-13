from commands import Commands
from textwrap import dedent


class CodeWriter:
    def __init__(self, app_state, file_handler):
        '''
        Opens the output file/stream and gets ready to write into it
        '''
        self._file_handler = file_handler
        self._app_state = app_state
        self._filename = ""
        self._segments = dict([
            # constant always points to stack pointer current location
            ('constant', '0'),  # RAM[0] stack pointer
            ('local', '1'),  # RAM[1] local segment pointer
            ('argument', '2'),  # RAM[2] argument segment pointer
            ('this', '3'),  # RAM[3] this segment pointer
            ('that', '4'),  # RAM[4] that segment pointer
        ])

    def filename(self, filename):
        '''
        Informs the code writer that the translation of a new VM file is started.

        Arg1:
            Str
        '''
        self._filename = filename
        pass

    def command_router(self, command, arg1, arg2=""):
        # determine the type of command and then runs the appropriate write operation
        # push static 10
        command_type = self._app_state.current_command_type
        if command_type == Commands.C_PUSH:
            self.write_push_pop(command, arg1, arg2)
        if command_type == Commands.C_ARITHMETIC:
            self.write_arithmetic(command)

    def get_arithmetic_assembly(self, command):
        if command == "add":
            return dedent("""\
            @0
            A=M-1
            D=M
            M=0
            @0
            M=M-1
            A=M-1
            M=D+M
            """)
        return ""

    def write_arithmetic(self, command):
        '''
        Writes the assembly code that is the translation of the given arithmetic

        Arg1:
            C_ARITHMETIC command
        '''
        c_arithmetic_assembly = self.get_arithmetic_assembly(command)
        self._file_handler.write_to_output_file(c_arithmetic_assembly)
        pass

    def get_push_pop_assembly(self, command, segment, index):
        segment = self._segments.get(segment)
        # pushOrPopOp = "+" if command == "push" else "-"

        # push segment index
        # set d reg to index
        # @index
        # D=A
        # goto the address of stack pointer @0 is the stack pointer address
        # @0
        # A=M
        # set value of ram address to d reg
        # M=D
        # increment the stack pointer
        # @0
        # D=D+1
        return "@{}\nD=A\n@{}\nA=M\nM=D\n@{}\nM=M+1\n".format(index, segment, segment)

    def write_push_pop(self, command, segment, index):
        '''
        Writes the assembly code that is the translation of the given command, where command is either C_PUSH or C_POP

        Arg1:
            C_PUSH or C_POP

        Arg2:
            Str

        Arg3: 
            int
        '''
        # self._file_handler.outfile.truncate()
        assembly = self.get_push_pop_assembly(command, segment, index)
        self._file_handler.write_to_output_file(assembly)

    def close_write_output(self):
        self._file_handler.close_and_write()
