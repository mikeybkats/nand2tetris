from commands import Commands
from textwrap import dedent
import uuid
from code_writer_dict import CodeWriterDict


class CodeWriter:
    function_name = ""
    call_count = 0
    has_sys_init = False

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
            ('temp0', '5'),  # RAM[5 - 12]
            ('temp1', '6'),  # RAM[5 - 12]
            ('temp2', '7'),  # RAM[5 - 12]
            ('temp3', '8'),  # RAM[5 - 12]
            ('temp4', '9'),  # RAM[5 - 12]
            ('temp5', '10'),  # RAM[5 - 12]
            ('temp6', '11'),  # RAM[5 - 12]
            ('temp7', '12'),  # RAM[5 - 12]
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
        if command_type == Commands.C_CALL:
            self.write_call(function_name=arg1, num_args=arg2)

    def get_arithmetic_assembly(self, command):
        # stores value of RAM[SP-1] in D register
        spFirstOp = "@0\nA=M-1\nD=M\n"
        # sets value of RAM[0] to (RAM[0]-1) and targets 1 minus the stack pointer
        spSecOp = "@0\nM=M-1\nA=M-1\n"
        if command == "add":
            return spFirstOp + spSecOp + "M=D+M\n"
        if command == "sub":
            return spFirstOp + spSecOp + "M=M-D\n"
        if command == "neg":
            return spFirstOp + "M=M-D\n"
        if command == "eq":
            neq_id = uuid.uuid4().hex[0:-8:1]
            return spFirstOp + spSecOp + self._assembly.get_assembly(command).format(neq_id, neq_id)
        if command == "gt":
            gt_id = uuid.uuid4().hex[0:-8:1]
            return spFirstOp + spSecOp + self._assembly.get_assembly(command).format(gt_id, gt_id)
        if command == "lt":
            lt_id = uuid.uuid4().hex[0:-8:1]
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
        if segment == "temp":
            return int(self.get_segment(segment + str(index)))
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
            tempAddress = int(self.get_segment("temp" + str(index)))
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
            # tempAddress = index + int(self._segments.get("temp"))
            tempAddress = int(self.get_segment("temp" + str(index)))
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
        self.write_call("Sys.init", 0)

    def write_label(self, label):
        '''
        label: 
            string
        '''
        if self.function_name and self.function_name != "Sys.init":
            label = self.function_name + "$" + label
        assembly = self._assembly.get_assembly("label").format(label)
        self._file_handler.write_to_output_file(assembly)

    def write_go_to(self, label):
        '''
        label: 
            string
        '''
        if self.function_name and self.function_name != "Sys.init":
            label = self.function_name + "$" + label
        assembly = self._assembly.get_assembly("goto").format(label)
        self._file_handler.write_to_output_file(assembly)

    def write_if(self, label):
        '''
        label: 
            string
        '''
        if self.function_name and self.function_name != "Sys.init":
            label = self.function_name + "$" + label
        assembly = self._assembly.get_assembly("if_goto").format(label)
        self._file_handler.write_to_output_file(assembly)

    def write_function(self, function_name, num_locals):
        '''
        function_name: 
            string

        num_locals:
            int
        '''
        self.function_name = function_name
        if function_name == "Sys.init":
            self.has_sys_init = True
        count = 0
        assembly = ""
        while (count < num_locals):
            assembly = assembly + dedent("""\
                @0
                A=M
                M=0
                @0
                M=M+1
                """)
            count = count + 1

        assembly = "({})\n".format(function_name) + assembly
        self._file_handler.write_to_output_file(assembly)

    def write_call(self, function_name, num_args):
        '''
        function_name: 
            string

        num_args:
            int
        '''
        return_address = function_name + "$ret." + \
            str(num_args) + "." + str(self.call_count)

        PUSH_RETURN_ADDR = self._assembly.get_assembly(
            "push_return_addr").format(return_address)
        PUSH_LCL = self._assembly.get_assembly(
            "push_segment").format(self.get_segment("local"))
        PUSH_ARG = self._assembly.get_assembly(
            "push_segment").format(self.get_segment("argument"))
        PUSH_THIS = self._assembly.get_assembly(
            "push_segment").format(self.get_segment("this"))
        PUSH_THAT = self._assembly.get_assembly(
            "push_segment").format(self.get_segment("that"))

        # ARG = SP - nArgs - 5
        arg_memory = self.get_segment("argument")
        ARG = dedent("""\
            @0  // put SP in RAM[ARG]
            D=M
            @{}
            M=D

            @{} // get num of args 
            D=A
            @{} // subtract number of arguments from RAM[ARG]
            M=M-D

            @5 // subtract 5 (number of saved stack items) from RAM[ARG]
            D=A
            @{}
            M=M-D
            """).format(arg_memory, num_args, arg_memory, arg_memory)

        # set local to value of SP
        LCL = "@0\nD=M\n@{}\nM=D\n".format(self.get_segment("local"))

        # remember A jumps around the RAM (runtime env)
        # jmp jumps around the ROM (program)
        GOTO_FUNCTION = dedent("""\
            @{}
            A;JMP
            """).format(function_name)

        RETURN_LABEL = "({})\n".format(return_address)

        assembly = PUSH_RETURN_ADDR + PUSH_LCL + PUSH_ARG + \
            PUSH_THIS + PUSH_THAT + ARG + LCL + \
            GOTO_FUNCTION + RETURN_LABEL
        self._file_handler.write_to_output_file(assembly)

        self.call_count = self.call_count + 1

    def write_return(self):

        # if not self.has_sys_init:
        #     return

        endframe = "endframe_" + str(self.call_count)
        SET_END_FRAME = dedent("""\
            @{} 
            D=M // set RAM[local] into D reg
            @{} 
            M=D // store RAM[local] into RAM[endframe] 
            """).format(self.get_segment("local"), endframe)

        # pointer of endframe - 5
        # put return address in temp variable
        retAddr = "return_" + str(self.call_count)

        self.call_count = self.call_count + 1

        RET = dedent("""\
            @5
            D=A
            @{}
            A=M-D  // goto RAM[endframe] - 5
            D=M    // set D to *(RAM[endframe] - 5)
            @{} 
            M=D    // set RAM[retAddr] = to *(RAM[endframe] - 5)
            """).format(endframe, retAddr)

        # *ARG = pop() reposition the return value (last value on current stack) for the caller (put it on arg)
        POINTER_ARG_POP = dedent("""\
            @0
            A=M-1 // goto the SP-1 addr
            D=M   // set D reg to SP-1
            @{}
            A=M   // set the location of ARG to D reg
            M=D 
            """).format(self.get_segment("argument"))

        # SP = ARG + 1
        SP = dedent("""\
            @{}
            D=M+1
            @0
            M=D
            """).format(self.get_segment("argument"))

        # THAT = *(END_FRAME - 1)
        THAT = dedent("""\
            @{}
            A=M-1
            D=M
            @{}
            M=D
            """).format(endframe, self.get_segment("that"))

        # THIS = *(END_FRAME - 2)
        THIS = dedent("""\
            @2
            D=A
            @{}
            A=M-D
            D=M
            @{}
            M=D
            """).format(endframe, self.get_segment("this"))

        # ARG = *(END_FRAME - 3)
        ARG = dedent("""\
            @3
            D=A
            @{}
            A=M-D
            D=M
            @{}
            M=D
            """).format(endframe, self.get_segment("argument"))

        # LCL = *(END_FRAME - 4)
        LCL = dedent("""\
            @4
            D=A
            @{}
            A=M-D
            D=M
            @{}
            M=D
            """).format(endframe, self.get_segment("local"))

        # jump to return address in callers code
        JMP_RET = dedent("""\
            @{}
            A=M
            A;JMP
            """).format(retAddr)

        assembly = SET_END_FRAME + RET + POINTER_ARG_POP + SP + \
            THAT + THIS + ARG + LCL + JMP_RET

        self._file_handler.write_to_output_file(assembly)

    def close_write_output(self):
        self._file_handler.close_and_write()
