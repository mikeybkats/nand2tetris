from commands import Commands
from textwrap import dedent
import uuid
from code_writer_dict import CodeWriterDict


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
            ('pointer0', '3'),  # push pointer 0/1 (this/that)
            ('pointer1', '4')  # push pointer 0/1 (this/that)
        ])
        self._assembly = CodeWriterDict()

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
        if command_type == Commands.C_LABEL:
            self.write_label(arg1)
        if command_type == Commands.C_IF:
            self.write_if(arg1)
        if command_type == Commands.C_GOTO:
            self.write_go_to(arg1)
        if command_type == Commands.C_FUNCTION:
            self.write_function(function_name=arg1, num_locals=arg2)
        if command_type == Commands.C_RETURN:
            self.write_return()

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
            return spFirstOp + spSecOp + self._assembly.get_assembly(command).format(neq_id, neq_id)
        if command == "gt":
            gt_id = uuid.uuid4()
            return spFirstOp + spSecOp + self._assembly.get_assembly(command).format(gt_id, gt_id)
        if command == "lt":
            lt_id = uuid.uuid4()
            return spFirstOp + spSecOp + self._assembly.get_assembly(command).format(lt_id, lt_id)
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

    def get_segment_index(self, index, segment):
        if segment == "pointer":
            return int(self.get_segment(
                segment + str(index)))
        else:
            return int(self.get_segment(segment))

    def get_push_assembly(self, command, segment, index):
        if segment != "static":
            segment_index = self.get_segment_index(index, segment)

        if segment == "constant":
            return self._assembly.get_assembly("push_" + segment).format(index, segment_index, segment_index)

        if segment == "static":
            # stored in global space!
            # static index in FOO.vm assembles to reference FOO.i -> @Foo.5 ect
            variableName = self._file_handler.infile_name() + "." + str(index)
            return self._assembly.get_assembly("push_" + segment).format(variableName)

        if segment == "temp":
            tempAddress = index + int(self._segments.get("temp"))
            return self._assembly.get_assembly("push_" + segment).format(tempAddress)

        if segment == "pointer":
            return self._assembly.get_assembly("push_" + segment).format(segment_index)

        else:
            return self._assembly.get_assembly("push_default").format(index, segment_index)

    def get_pop_assembly(self, command, segment, index):
        if segment != "static":
            segment_index = self.get_segment_index(index, segment)

        if segment == "static":
            variableName = self._file_handler.infile_name() + "." + str(index)
            return self._assembly.get_assembly("pop_" + segment).format(variableName)

        if segment == "temp":
            tempAddress = index + int(self._segments.get("temp"))
            return self._assembly.get_assembly("pop_" + segment).format(tempAddress)

        if segment == "pointer":
            return self._assembly.get_assembly("pop_" + segment).format(segment_index)

        return self._assembly.get_assembly("pop_default").format(index, segment_index, segment_index, index, segment_index)

    def write_push_pop(self, command, segment, index):
        '''
        Writes the assembly code that is the translation of the given command, where command is either C_PUSH or C_POP

        command:
            C_PUSH or C_POP
        segment:
            Str
        index: 
            int
        '''
        assembly = ""
        if self._app_state.current_command_type == Commands.C_PUSH:
            assembly = self.get_push_assembly(command, segment, index)

        if self._app_state.current_command_type == Commands.C_POP:
            assembly = self.get_pop_assembly(command, segment, index)

        self._file_handler.write_to_output_file(assembly)

    def write_init(self):
        '''
        Writes assembly code that effects the VM initialization, also called bootstrap code. This code must be placed at the beginning of the output file.
        '''
        self._file_handler.write_to_output_file(
            self._assembly.get_assembly("bootstrap"))
        pass

    def write_label(self, label):
        '''
        label: 
            string
        '''
        assembly = self._assembly.get_assembly("label").format(label)
        self._file_handler.write_to_output_file(assembly)
        pass

    def write_go_to(self, label):
        '''
        label: 
            string
        '''
        assembly = self._assembly.get_assembly("goto").format(label)
        self._file_handler.write_to_output_file(assembly)
        pass

    def write_if(self, label):
        '''
        label: 
            string
        '''
        assembly = self._assembly.get_assembly("if_goto").format(label)
        self._file_handler.write_to_output_file(assembly)
        pass

    def write_function(self, function_name, num_locals):
        '''
        function_name: 
            string

        num_locals:
            int
        '''
        functionSymbolb = repr(uuid.uuid1().hex)
        functionSymbol = function_name + "$" + functionSymbolb

        count = 0
        localAssembly = ""
        while (count < num_locals):
            localAssembly = localAssembly + \
                self.get_push_assembly(
                    command="push local {}".format(count), segment="local", index=count)
            count = count + 1

        assembly = dedent("""\
            ({})
            """).format(function_name) + localAssembly
        self._file_handler.write_to_output_file(assembly)
        pass

    def write_call(self, function_name, num_args):
        '''
        function_name: 
            string

        num_args:
            int
        '''
        # TODO: implement
        pass

    def write_return(self):
        # TODO: implement
        END_FRAME = "@{}\n".format(self.get_segment("local"))

        # store return address in temp var
        RET_ADDRESS = dedent("""\
            @5
            D=A
            {}
            D=M-D
            A=D
            """).format(END_FRAME)
        POINTER_ARG = dedent("""\
            @0
            A=M
            D=M
            @{}
            A=M
            M=D
            """).format(self.get_segment("argument"))
        # SP = ARG + 1
        SP = dedent("""\
            @{}
            D=M+1
            @0
            A=D
            """).format(self.get_segment("argument"))
        # THAT = END_FRAME - 1
        # THIS = END_FRAME - 2
        # ARG = END_FRAME - 3
        # LCL = END_FRAME - 4
        # GOTO RET_ADDRESS
        assembly = RET_ADDRESS
        self._file_handler.write_to_output_file(assembly)
        pass

    def close_write_output(self):
        self._file_handler.close_and_write()
