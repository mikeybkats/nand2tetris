from io import TextIOBase

class VMWriter:
    def __int__(self, output_file_stream):
        """
        Creates a new file and prepares for writing

        :param output_file_stream:
        :return:
        """

        if isinstance(output_file_stream, TextIOBase):
            self._outfile = output_file_stream
        else:
            self._outfile = open(output_file_stream, mode="w+", encoding='utf-8')

    def write_push(self, segment, index):
        """
        Writes a VM push command

        :param segment: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP
        :param index: INT
        :return: None
        """

    def write_pop(self, segment, index):
        """
        Writes a VM pop command

        :param segment: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP
        :param index: INT
        :return: None
        """

    def write_arithmetic(self, command):
        """
        Writes a VM arithmetic command

        :param command: ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT
        :return: None
        """

    def write_label(self, label):
        """
        Writes a VM label command

        :param label: String
        :return: None
        """

    def write_goto(self, label):
        """
        Writes a VM goto command
        :param label: String
        :return: None
        """

    def write_if(self, label):
        """
        Writes a VM if-goto command
        :param label: String
        :return: None
        """

    def write_call(self, name, n_args):
        """
        Writes a VM call command
        :param name: String
        :param n_args: Int
        :return: None
        """

    def write_function(self, name, n_locals):
        """
        Writes a VM function command
        :param name: String
        :param n_locals: Int
        :return: None
        """

    def write_return(self):
        """Writes VM return command"""

    def close(self):
        """Closes the output file"""
