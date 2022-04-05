from commands import Commands
from textwrap import dedent
import uuid


class CodeWriter:
    def __init__(self, app_state, file_handler):
        '''
        Opens the output file/stream and gets ready to write into it
        '''
        self._file_handler = file_handler
        self._app_state = app_state
        self._filename = ""
        self._segments = dict([
            # pop takes whatever the sp is pointing at and puts it at the target memory segment
            # push pushes the target to the location of the sp
            # # pop this 5
            # constant always points to stack pointer current location
            ('constant', '0'),  # RAM[0] SP stack pointer
            ('local', '1'),  # RAM[1] LCL local segment pointer
            ('argument', '2'),  # RAM[2] ARG argument segment pointer
            ('this', '3'),  # RAM[3] THIS segment pointer
            ('that', '4'),  # RAM[4] THAT segment pointer
            # ('static', 'x'),  #
            ('temp', '5'),  # RAM[5 - 12]
            ('pointer', "xxx")  # Arbitrary rule of the game can only be 0 or 1
            # push pointer 0/1 (this/that)
            # pop pointer 0/1 (this/that)
            # pointer 0 should result in accessing this
            # pointer 1 should result in accessing that
        ])

    def get_segment(self, segment_name):
        return self._segments.get(segment_name)

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
        if command_type == Commands.C_PUSH or command_type == Commands.C_POP:
            self.write_push_pop(command, arg1, arg2)
        if command_type == Commands.C_ARITHMETIC:
            self.write_arithmetic(command)

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
            neq_id = uuid.uuid4()
            return spFirstOp + spSecOp + dedent("""\
                D=M-D    
                M=-1
                @NE_{}
                D;JNE
                @0
                A=M-1
                M=1
                (NE_{})
                """).format(neq_id, neq_id)
        if command == "gt":
            le_id = uuid.uuid4()
            return spFirstOp + spSecOp + dedent("""\
                D=M-D
                M=-1
                @LE_{}
                D;JLE
                @0
                A=M-1
                M=1
                (LE_{})
                """).format(le_id, le_id)
        if command == "lt":
            gt_id = uuid.uuid4()
            return spFirstOp + spSecOp + dedent("""\
                D=M-D
                M=-1
                @GT_{}
                D;JGE
                @0
                A=M-1
                M=1
                (GT_{})
                """).format(gt_id, gt_id)
        if command == "and":
            # 16 bitwise and
            return spFirstOp + spSecOp + "M=D&M\n"
        if command == "or":
            # 16 bitwise or
            return spFirstOp + spSecOp + "M=D|M\n"
        if command == "not":
            return spFirstOp + "M=!D\n"

    def write_arithmetic(self, command):
        '''
        Writes the assembly code that is the translation of the given arithmetic

        Arg1:
            C_ARITHMETIC command
        '''
        c_arithmetic_assembly = self.get_arithmetic_assembly(command.lower())
        self._file_handler.write_to_output_file(c_arithmetic_assembly)
        pass

    def get_push_pop_assembly(self, command, segment, index):
        if segment != "static":
            segment_index = int(self.get_segment(segment))
        if self._app_state.current_command_type == Commands.C_PUSH:
            if segment == "constant":
                return "@{}\nD=A\n@{}\nA=M\nM=D\n@{}\nM=M+1\n".format(index, segment_index, segment_index)
            if segment == "local" or segment == "argument" or segment == "this" or segment == "that":
                return "@{}\nD=A\n@{}\nA=D+M\nD=M\n@0\nA=M\nM=D\n".format(index, segment_index)
            if segment == "static":
                # stored in global space!
                # TODO static index in FOO.vm assembles to reference FOO.i
                # @Foo.5 ect
                variableName = self._file_handler.infile_name() + "." + str(index)
                return dedent("""\
                @{}
                D=M
                @0
                A=M
                M=D
                @0
                M=M+1
                """).format(variableName)
        if self._app_state.current_command_type == Commands.C_POP:
            if segment == "static":
                variableName = self._file_handler.infile_name() + "." + str(index)
                return dedent("""\
                @0
                A=M-1
                D=M
                @{}
                M=D
                @0
                M=M-1
                A=M
                M=0
                """).format(variableName)

            return "@{}\nD=A\n@{}\nM=M+D\n@0\nM=M-1\nA=M\nD=M\nM=0\n@{}\nA=M\nM=D\n@{}\nD=A\n@{}\nM=M-D\n".format(index, segment_index, segment_index, index, segment_index)

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
        print(command)
        self._file_handler.write_to_output_file(assembly)

    def close_write_output(self):
        self._file_handler.close_and_write()
