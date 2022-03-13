from commands import Commands


class CodeWriter:
    def __init__(self, app_state, file_handler):
        '''
        Opens the output file/stream and gets ready to write into it
        '''
        self._file_handler = file_handler
        self._app_state = app_state
        self._filename = ""

    def filename(self, filename):
        '''
        Informs the code writer that the translation of a new VM file is started.

        Arg1:
            Str
        '''
        self._filename = filename
        pass

    def command_router(self, command_type, arg1, arg2):
        # determine the type of command and then runs the appropriate write operation
        # push static 10
        if command_type == Commands.C_PUSH:
            self.write_push_pop(command, arg1, arg2)

    def write_arithmetic(self, command):
        '''
        Writes the assembly code that is the translation of the given arithmetic

        Arg1:
            C_ARITHMETIC command
        '''
        pass

    def get_push_pop_assembly(self, command, segment, index):
        segments = dict([
            # constant always points to stack pointer current location
            ('constant', '0'),
            ('local', '24575')
        ])
        segment = segments.get(segment)
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
        segmentValue = "@" + index + "\nD=A\n"
        stackBase = "@{}\nA=M\nM=D\n@{}\nM=M+1\n".format(
            segment, segment)
        self._file_handler.outfile().truncate()
        self._file_handler.write_to_output_file(segmentValue + stackBase)

        pass

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
        assembly = self.get_push_pop_assembly(command, arg1, arg2)
