from io import TextIOBase
from string import Template
from enum import Enum


# class segments correspond directly to vm output code
class Segments(Enum):
    CONST = "constant"
    ARG = "arg"
    LOCAL = "local"
    STATIC = "static"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"


class VMWriter:
    def __init__(self, output_file_stream):
        """
        Creates a new file and prepares for writing

        :param output_file_stream:
        :return:
        """

        if isinstance(output_file_stream, TextIOBase):
            self._outfile = output_file_stream
        else:
            self._outfile = open(output_file_stream, mode="w+", encoding='utf-8')

    @property
    def outfile(self):
        return self._outfile

    @staticmethod
    def get_segment_from_kind(identifier_kind):
        if identifier_kind == "var" or identifier_kind == "field":
            return Segments.LOCAL.value
        if identifier_kind == "static":
            return Segments.STATIC.value
        if identifier_kind == "argument":
            return Segments.ARG.value

    @staticmethod
    def get_arithmetic_command(symbol):
        # :param arithmetic_command: ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT
        if symbol == "-":
            return "sub"
        if symbol == "+":
            return "add"
        if symbol == ">":
            return "gt"
        if symbol == "<":
            return "lt"
        if symbol == "&":
            return "and"
        if symbol == "|":
            return "or"
        if symbol == "~":
            return "not"
        if symbol == "*":
            return "Math.multiply 2"
        if symbol == "/":
            return "Math.divide 2"
        return None
        # TODO: add other arithmetic commands

    def write_push(self, segment, index):
        """
        Writes a VM push command

        :param segment: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP
        :param index: INT
        :return: None
        """
        command = Template("push $segment $index\n")
        command = command.substitute(segment=segment, index=index)
        self._outfile.write(command)

    def write_pop(self, segment, index):
        """
        Writes a VM pop command

        :param segment: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP
        :param index: INT
        :return: None
        """
        command = Template("pop $segment $index\n")
        command = command.substitute(segment=segment, index=index)
        self._outfile.write(command)

    def write_arithmetic(self, arithmetic_command):
        """
        Writes a VM arithmetic command

        :param arithmetic_command: ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT
        :return: None
        """
        command = Template("$command\n")
        command = command.substitute(command=arithmetic_command)
        self._outfile.write(command)

    def write_label(self, label):
        """
        Writes a VM label command

        :param label: String
        :return: None
        """
        label_command = Template("label $label_command\n")
        label_command = label_command.substitute(label_command=label)
        self._outfile.write(label_command)

    def write_goto(self, label):
        """
        Writes a VM goto command
        :param label: String
        :return: None
        """
        goto_command = Template("goto $label\n")
        goto_command = goto_command.substitute(label=label)
        self._outfile.write(goto_command)

    def write_if(self, label):
        """
        Writes a VM if-goto command
        :param label: String
        :return: None
        """
        if_goto_command = Template("if-goto $label\n")
        if_goto_command = if_goto_command.substitute(label=label)
        self._outfile.write(if_goto_command)

    def write_call(self, name, n_args):
        """
        Writes a VM call command
        :param name: String
        :param n_args: Int
        :return: None
        """
        call_command = Template("call $name $n_args\n")
        call_command = call_command.substitute(name=name, n_args=n_args)
        self._outfile.write(call_command)

    def write_function(self, name, n_locals):
        """
        Writes a VM function command
        :param name: String
        :param n_locals: Int
        :return: None
        """
        function_command = Template("function $name $n_locals\n")
        function_command = function_command.substitute(name=name, n_locals=n_locals)
        self._outfile.write(function_command)

    def write_return(self):
        """Writes VM return command"""
        self._outfile.write("return\n")

    def write_custom(self, custom):
        self._outfile.write(Template("$custom\n").substitute(custom=custom))

    def close(self):
        """Closes the output file"""
        self._outfile.close()
