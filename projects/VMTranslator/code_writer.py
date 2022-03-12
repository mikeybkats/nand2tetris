class CodeWriter:
    def __init__(self, app_state, file_handler):
        '''Opens the output file/stream and gets ready to write into it'''
        self._file_handler = file_handler
        self._app_state = app_state

    def set_filename(self, filename):
        '''
        Informs the code writer that the translation of a new VM file is started.

        Arg1:
            Str
        '''
        self._file_handler.outfile_path(filename)

    def write_arithmetic(self, command):
        '''
        Writes the assembly code that is the translation of the given arithmetic

        Arg1:
            Commands
        '''
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
