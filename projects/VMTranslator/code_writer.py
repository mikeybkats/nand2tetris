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
        self._file_handler.write_to_output_file(
            self.get_arithmetic_assembly_header())

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

    def get_arithmetic_assembly_header(self):
        return dedent("""\
            @EQ
            M=1
            @0
            A=M

            @NEQ
            M=-1
            @0
            A=M
            """)

    def get_arithmetic_assembly(self, command):
        # stores value of RAM[SP-1] in D register
        spFirstOp = "@0\nA=M-1\nD=M\nM=0\n"
        # sets value of RAM[0] to (RAM[0]-1) and targets 1 minus the stack pointer
        spSecOp = "@0\nM=M-1\nA=M-1\n"
        if command == "add":
            return spFirstOp + spSecOp + "M=D+M\n"
        if command == "sub":
            return spFirstOp + spSecOp + "M=M-D\n"
        if command == "neg":
            return spFirstOp + "M=M-D\n"
        if command == "eq":
            # get the first value into D Register
            # get the second value
            # @0\nA=M\nM=1\n@0\nM=M-1\n
            # D=M-D
            # @0
            # 0;JEQ
            # M=-1
            return spFirstOp + spSecOp + dedent("""\
                D=M-D    
                @EQ
                D;JEQ
                @NEQ
                D;JMP
                """)

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
        # pushes to the top of the stack
        if self._app_state.current_command_type == Commands.C_PUSH:
            return "@{}\nD=A\n@{}\nA=M\nM=D\n@{}\nM=M+1\n".format(index, segment, segment)
        else:
            # get the address of the pop destination segments are described above in constructor
            return None

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
