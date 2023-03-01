from JackTokenizer import JackTokenizer
from TokenTypes import Token_Type, GrammarLanguage, TerminalTypeTable, is_op, is_prefix_operator
from io import TextIOBase
from VMWriter import VMWriter, Segments, get_math_lib_args
from SymbolTable import SymbolTable, is_standard_lib
from string import Template
import html


def is_object_or_array(current_token):
    if (current_token != ";" and
            current_token != "{" and
            current_token != ")" and
            current_token != "]" and
            current_token != "="):
        return True
    return False


class CompilationEngine:
    """The name of the class being compiled"""
    _class_name = ""

    """The current expression being processed"""
    _exp = ""

    """Expression list count. The count of the number of arguments passed to a function or method"""
    _expression_list_count = 0

    _var_declaration_count = 0

    _if_statement_count = 0
    _else_statement_count = 0

    # _array_object = ""

    _while_expression_count = 0

    _calling_function = ""

    # current method can be "function" | "constructor" | "method"
    _current_method_type = ""
    _current_method_name = ""
    _current_method_return_type = ""

    # current line keyword "let" | "do" | "if"
    _current_line_keyword = ""

    def __init__(self, input_stream, output_stream):
        """
        Creates a new compilation engine with the given input and output. The next routine called must be compileClass()

        :param input_stream:
        :param output_stream:
        :param write_xml:
            boolean - if true Compilation engine will output xml
        """

        # make a jack tokenizer
        self._tokenizer = JackTokenizer(inputStreamOrFile=input_stream)
        self._write_xml = False
        # make the outfile
        # if write_xml:
        #     if isinstance(output_stream, TextIOBase):
        #         self._outfile = output_stream
        #     else:
        #         self._outfile = open(output_stream, mode="w+", encoding='utf-8')

        # make VMWriter
        self._vm_writer = VMWriter(output_stream)

        # make SymbolTable
        self._symbol_table = SymbolTable()
        self._table_obj = {"name": "", "type": "", "kind": ""}

    @property
    def tokenizer(self):
        return self._tokenizer

    @property
    def outfile(self):
        return self._outfile

    def close_outfile(self):
        if not self._write_xml:
            self._vm_writer.close()
        else:
            self._outfile.close()

    def write_xml_tag_open(self, tag_type):
        if self._write_xml:
            self._outfile.write("<" + tag_type + ">")

    def write_xml_tag_smart(self, tag_type, tag_open):
        if self._write_xml:
            terminal_types = TerminalTypeTable()
            if terminal_types.is_terminal(tag_type):
                self.write_terminal_tag(tag_type)
            else:
                self.write_non_terminal_tag(tag_type, tag_open)

    def write_xml_closing_tag(self, tag_type):
        if self._write_xml:
            self._outfile.write("</" + tag_type + ">\n")

    def write_token(self):
        if self._write_xml:
            token = self._tokenizer.currentToken
            if is_op(token):
                token = html.escape(token)
            self._outfile.write(" " + token + " ")

    def write_non_terminal_tag(self, tag_type, closed):
        """Writes an open token tag: <tokenType>\n or </tokenType>\n"""
        if self._write_xml:
            if closed:
                self.write_xml_closing_tag(tag_type)
            else:
                self.write_xml_tag_open(tag_type)
                self._outfile.write("\n")

    def write_terminal_tag(self, token_type):
        """Writes a closed token tag: <tokenType> currentToken </tokenType>\n"""
        if self._write_xml:
            self.write_xml_tag_open(token_type)
            self.write_token()
            self.write_xml_closing_tag(token_type)

    def write_temp_table_object(self, token_type):
        if token_type == GrammarLanguage.KEYWORD.value.lower():
            self._table_obj["type"] = self._tokenizer.currentToken
        if token_type == GrammarLanguage.IDENTIFIER.value.lower():
            self._table_obj["name"] = self._tokenizer.currentToken

    def write_table_object_definition(self):
        self._symbol_table.define(
            i_name=self._table_obj["name"],
            i_type=self._table_obj["type"],
            i_kind=self._table_obj["kind"]
        )

    def reset_table_obj(self):
        self._table_obj = {"name": "", "type": "", "kind": ""}

    def compile_class(self):
        """Compiles a complete class"""
        self._symbol_table.start_class()
        self.reset_table_obj()

        while self._tokenizer.has_more_tokens():
            self._tokenizer.advance()

            if self._tokenizer.currentToken == GrammarLanguage.CLASS.value:
                # write class tag
                self.write_non_terminal_tag(GrammarLanguage.CLASS.value, False)

                # write class keyword
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                self._tokenizer.advance()

                # write the class name
                self._class_name = self._tokenizer.currentToken
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                self._tokenizer.advance()

                # write the opening curly brace
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())

            if (self._tokenizer.currentToken == GrammarLanguage.VAR.value or
                    self._tokenizer.currentToken == GrammarLanguage.STATIC.value or
                    self._tokenizer.currentToken == GrammarLanguage.FIELD.value):
                self.compile_class_var_declaration()

            if self.is_subroutine():
                self._current_method_type = self._tokenizer.currentToken
                self.compile_subroutine()

    def is_subroutine(self):
        if (self._tokenizer.currentToken == GrammarLanguage.FUNCTION.value or
                self._tokenizer.currentToken == GrammarLanguage.METHOD.value or
                self._tokenizer.currentToken == GrammarLanguage.CONSTRUCTOR.value):
            return True
        return False

    def not_end_of_routine(self):
        if self._tokenizer.currentToken != "}":
            return True
        return False

    def is_subroutine_identifier_signature(self):
        if ((self._tokenizer.currentToken != GrammarLanguage.VAR.value and
             self._tokenizer.currentToken != GrammarLanguage.INT.value and
             self._tokenizer.currentToken != GrammarLanguage.DO.value and
             self._tokenizer.currentToken != GrammarLanguage.IF.value and
             self._tokenizer.currentToken != GrammarLanguage.LET.value) and
                self._tokenizer.token_type().value.lower() == GrammarLanguage.KEYWORD.value or
                self._tokenizer.token_type().value.lower() == GrammarLanguage.IDENTIFIER.value or
                self._tokenizer.token_type().value.lower() == GrammarLanguage.SYMBOL.value):
            return True
        return False

    def write_function_name(self):
        # write the function name after the number of local vars has been counted
        self._var_declaration_count = self._symbol_table.var_count("var")
        self._vm_writer.write_function(name=self._class_name + "." + self._current_method_name, n_locals=self._var_declaration_count)

        if self._current_method_type == "constructor":
            self._vm_writer.write_push(segment="constant", index=self._symbol_table.var_table_count("class"))
            self._vm_writer.write_custom("call Memory.alloc 1")
            self._vm_writer.write_pop("pointer", 0)

    def is_statement(self):
        return (self._tokenizer.currentToken == GrammarLanguage.LET.value or
                self._tokenizer.currentToken == GrammarLanguage.DO.value or
                self._tokenizer.currentToken == GrammarLanguage.IF.value or
                self._tokenizer.currentToken == GrammarLanguage.WHILE.value or
                self._tokenizer.currentToken == GrammarLanguage.RETURN.value)

    def compile_subroutine(self):
        """Compiles a complete method, function, or constructor"""
        subroutine_name_written = False
        self._if_statement_count = 0
        self._while_expression_count = 0

        self._symbol_table.start_subroutine()
        self.reset_table_obj()

        if self._current_method_type == GrammarLanguage.METHOD.value:
            self._symbol_table.define(
                i_name="this",
                i_type=self._class_name,
                i_kind="argument"
            )

        count = 0
        while count != 3:
            if count == 1:
                self._current_method_return_type = self._tokenizer.currentToken
            if count == 2:
                self._current_method_name = self._tokenizer.currentToken

            self._tokenizer.advance()
            count = count + 1

        if self._tokenizer.currentToken == "(":
            self.compile_parameter_list()

        while self.not_end_of_routine():
            self._tokenizer.advance()

            if self._tokenizer.currentToken == "{":
                self._tokenizer.advance()

            # compile declarations
            if self._tokenizer.currentToken == GrammarLanguage.VAR.value:
                self.compile_var_declaration()

            # compile statements
            if self.is_statement():
                # compile subroutine name
                if not subroutine_name_written:
                    self.write_function_name()
                    subroutine_name_written = True

                if self._current_method_type == GrammarLanguage.METHOD.value:
                    self._vm_writer.write_push(segment="argument", index=0)
                    self._vm_writer.write_pop(segment="pointer", index=0)

                self.compile_statements()

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list, not including the enclosing "()"."""
        self._table_obj["kind"] = "argument"

        if self._tokenizer.currentToken == "(":
            self._tokenizer.advance()

        parameter_count = 0
        # ((type varName)(',' type varName)*)?
        while self._tokenizer.currentToken != ")":
            next_token = self._tokenizer.look_ahead()

            if (not self._tokenizer.currentToken == "," and
                    not next_token == ","
                    and self._tokenizer.get_token_type(next_token) == "identifier"):
                # then it must be the parameter type
                self._table_obj["type"] = self._tokenizer.currentToken

            elif self._tokenizer.token_type().value.lower() == "identifier":
                self._table_obj["name"] = self._tokenizer.currentToken
                self.write_table_object_definition()

                parameter_count = parameter_count + 1

            self._tokenizer.advance()

        return parameter_count

    def compile_class_var_declaration(self):
        """Compiles a static declaration or a field declaration"""

        if (self._tokenizer.currentToken == GrammarLanguage.STATIC.value or
                self._tokenizer.currentToken == GrammarLanguage.FIELD.value):

            self._table_obj["kind"] = self._tokenizer.currentToken

            count = 0
            while self._tokenizer.currentToken != ";":
                self._tokenizer.advance()
                count = count + 1

                if count == 1:
                    self._table_obj["type"] = self._tokenizer.currentToken

                if count == 2:
                    self._table_obj["name"] = self._tokenizer.currentToken

                if self._tokenizer.currentToken == "," or self._tokenizer.currentToken == ";":
                    count = 1
                    self.write_table_object_definition()

            self.write_xml_closing_tag(GrammarLanguage.CLASS_VAR_DEC.value)

    def compile_var_declaration(self):
        """
        Compiles var declaration

        var type varName (, varName)*;
        """
        self.write_temp_table_object(self._tokenizer.token_type().value.lower())
        self._table_obj["kind"] = "var"

        count = 0
        while self._tokenizer.currentToken != ";":
            self._tokenizer.advance()
            count = count + 1

            if count == 1:
                self._table_obj["type"] = self._tokenizer.currentToken

            if count == 2:
                self._table_obj["name"] = self._tokenizer.currentToken

            if self._tokenizer.currentToken == "," or self._tokenizer.currentToken == ";":
                count = 1
                self.write_table_object_definition()
                self._var_declaration_count = self._var_declaration_count + 1

        # self.write_xml_closing_tag(GrammarLanguage.VAR_DEC.value)

    def compile_statements(self):
        """Compiles a sequence of statements, not including the
        enclosing curly braces "{}". Compiles if, let and while statements"""
        while self.is_statement():
            if self._tokenizer.currentToken == GrammarLanguage.LET.value:
                self.compile_let()
            if self._tokenizer.currentToken == GrammarLanguage.DO.value:
                self.compile_do()
            if self._tokenizer.currentToken == GrammarLanguage.IF.value:
                self.compile_if()
            if self._tokenizer.currentToken == GrammarLanguage.WHILE.value:
                self.compile_while()
            if self._tokenizer.currentToken == GrammarLanguage.RETURN.value:
                self.compile_return()

            self._tokenizer.advance()

    def compile_array_addition(self, array_expression):
        is_array = self._symbol_table.type_of(array_expression) == "Array"
        if not is_array:
            self.compile_expression("]")
        else:
            self._tokenizer.advance()
            self._tokenizer.advance()
            has_child_array = self._symbol_table.type_of(self._tokenizer.currentToken) == "Array"

            self.compile_array_addition(self._tokenizer.currentToken)

            if has_child_array:
                self._vm_writer.write_pop(segment="pointer", index=1)
                self._vm_writer.write_push(segment="that", index=0)

                segment = self._vm_writer.get_segment_from_kind(self._symbol_table.kind_of(array_expression))
                index = self._symbol_table.index_of(array_expression)

                self._vm_writer.write_push(segment, index)
            else:
                segment = self._vm_writer.get_segment_from_kind(self._symbol_table.kind_of(array_expression))
                index = self._symbol_table.index_of(array_expression)

                self._vm_writer.write_push(segment, index)

            self._vm_writer.write_arithmetic(arithmetic_command="add")

    def write_array_closure(self):
        self._vm_writer.write_pop("temp", 0)
        self._vm_writer.write_pop("pointer", 1)
        self._vm_writer.write_push("temp", 0)
        self._vm_writer.write_pop("that", 0)

    def compile_let(self):
        """Compiles a let statement"""
        self._current_line_keyword = GrammarLanguage.LET.value
        destination_array_object = False

        count = 0
        while self._tokenizer.currentToken != ";":
            self._tokenizer.advance()
            count = count + 1

            if count == 1:
                assignment_destination = self._tokenizer.currentToken

            if self.tokenizer.look_ahead() == "[":
                destination_array_object = True
                self.compile_array_addition(self._tokenizer.currentToken)

            if self.tokenizer.currentToken == "=":
                while self._tokenizer.currentToken != ";":
                    self.compile_expression()

                segment = self._vm_writer.get_segment_from_kind(self._symbol_table.kind_of(assignment_destination))
                index = self._symbol_table.index_of(assignment_destination)

            if self.tokenizer.currentToken == ";" and not destination_array_object:
                self._vm_writer.write_pop(segment=segment, index=index)

        if destination_array_object:
            self.write_array_closure()

    def get_segment_from_current_token(self):
        return self._vm_writer.get_segment_from_kind(self._symbol_table.kind_of(self._tokenizer.currentToken))

    def compile_do(self):
        """Compiles a do statement"""
        self._current_line_keyword = GrammarLanguage.DO.value

        self._tokenizer.advance()
        calling_function_type = self.get_type_of_calling_function()

        if self._symbol_table.is_var(self._tokenizer.currentToken):
            index = self._symbol_table.index_of(self._tokenizer.currentToken)
            segment = self.get_segment_from_current_token()
            self._vm_writer.write_push(segment=segment, index=index)

        is_calling_method = False
        calling_local_object_method = self._symbol_table.is_var(self._tokenizer.currentToken)
        if self._tokenizer.currentToken[0].islower() and not self._tokenizer.look_ahead() == ".":
            is_calling_method = True

        while self._tokenizer.currentToken != ";":
            self._tokenizer.advance()

            calling_function_type = self.build_stack_methods(calling_function_type)

            if self._tokenizer.currentToken == "(":
                self.write_terminal_tag(GrammarLanguage.SYMBOL.value.lower())
                self.compile_expression_list()

            self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        if calling_function_type:
            if is_calling_method:
                self._expression_list_count = self._expression_list_count or 1

                # if calling a method then push a reference to the class - pointer 0
                self._vm_writer.write_push(segment="pointer", index=0)
                self._vm_writer.write_call(self._class_name + "." + calling_function_type, self._expression_list_count)
            else:
                if calling_local_object_method:
                    self._expression_list_count = self._expression_list_count + 1
                self._vm_writer.write_call(calling_function_type, self._expression_list_count)
            self._vm_writer.write_pop(segment="temp", index=0)

    def compile_while(self):
        """Compiles a while statement"""

        local_while_expression_count = self._while_expression_count

        while self._tokenizer.currentToken != "}":
            self._tokenizer.advance()

            if self._tokenizer.currentToken == "(":
                self._vm_writer.write_label(label="WHILE_EXP" + str(local_while_expression_count))

                self._while_expression_count = local_while_expression_count + 1

                self._tokenizer.advance()
                self.compile_expression()

                self._vm_writer.write_arithmetic("not")

                self._vm_writer.write_if(label="WHILE_END" + str(local_while_expression_count))

            if self._tokenizer.currentToken == "{":
                self._tokenizer.advance()
                self.compile_statements()

        self._vm_writer.write_goto(label="WHILE_EXP" + str(local_while_expression_count))
        self._vm_writer.write_label(label="WHILE_END" + str(local_while_expression_count))

    def compile_if(self):
        """Compiles if statement"""
        self._current_line_keyword == GrammarLanguage.IF.value

        self._tokenizer.advance()

        if self._tokenizer.currentToken == "(":
            self._tokenizer.advance()
            self.compile_expression(")")
            self._tokenizer.advance()

        this_if_statement_count = 0
        while self._tokenizer.currentToken != "}":

            if self._tokenizer.currentToken == "{":
                # Write if-goto IF_TRUE
                self._vm_writer.write_if(label="IF_TRUE" + str(self._if_statement_count))

                # Write goto IF_FALSE
                self._vm_writer.write_goto(label="IF_FALSE" + str(self._if_statement_count))

                # Write label IF_TRUE
                self._vm_writer.write_label(label="IF_TRUE" + str(self._if_statement_count))

                this_if_statement_count = self._if_statement_count
                self._if_statement_count = self._if_statement_count + 1

                self._tokenizer.advance()
                self.compile_statements()

                break

            self._tokenizer.advance()

        if self._tokenizer.look_ahead() == GrammarLanguage.ELSE.value:
            self._vm_writer.write_goto(label="IF_END" + str(this_if_statement_count))
            self._vm_writer.write_label(label="IF_FALSE" + str(this_if_statement_count))
            self._tokenizer.advance()
            self.compile_else(this_if_statement_count)
        else:
            # Write label IF_FALSE
            self._vm_writer.write_label(label="IF_FALSE" + str(this_if_statement_count))

    def compile_else(self, count):
        while self._tokenizer.currentToken != "}":
            if self._tokenizer.currentToken == "{":
                self._tokenizer.advance()
                self.compile_statements()
                self._vm_writer.write_label(label="IF_END" + str(count))
                break

            self._else_statement_count = self._else_statement_count + 1
            self._tokenizer.advance()

    def compile_return(self):
        """Compiles a return statement"""
        self._current_line_keyword = GrammarLanguage.RETURN.value
        self._tokenizer.advance()

        if self._tokenizer.currentToken != ";":
            self.compile_expression()

        if (self._current_method_type != GrammarLanguage.CONSTRUCTOR.value and
                self._current_method_return_type == "void"):
            self._vm_writer.write_push(segment="constant", index=0)
        # else:
        #     self._vm_writer.write_push(segment="pointer", index=0)

        self._vm_writer.write_return()

    def write_arithmetic_vm(self, operator):
        arithmetic_command = VMWriter.get_arithmetic_command(operator)
        if is_standard_lib(arithmetic_command):
            self._vm_writer.write_call(arithmetic_command, get_math_lib_args(arithmetic_command))
        else:
            self._vm_writer.write_arithmetic(arithmetic_command)

    def write_arithmetic_negation_vm(self, operator):
        if operator == "-":
            self._vm_writer.write_arithmetic("neg")
        if operator == "~":
            self._vm_writer.write_arithmetic("not")

    def compile_expression_operator(self):
        cur_operator = self._tokenizer.currentToken

        # a prefix operator is - or ~
        if is_prefix_operator(cur_operator):
            self._tokenizer.advance()
            self.compile_term()
            self.write_arithmetic_negation_vm(cur_operator)
            # self.write_arithmetic_vm(cur_operator)
            self._tokenizer.advance()
        else:
            self.write_arithmetic_vm(cur_operator)
            self._tokenizer.advance()
            self.compile_term()
            self._tokenizer.advance()

    def expression_ended(self):
        return (self._tokenizer.currentToken == ";" or
                self._tokenizer.currentToken == ")" or
                self._tokenizer.currentToken == "]" or
                self._tokenizer.currentToken == ",")

    def get_type_of_grammar_language(self):
        """returns the type of the symbol of the current token
        :returns "array" | "object" | "function" | "integer"
        """
        cur_token = self._tokenizer.currentToken
        if self._symbol_table.is_var(cur_token):
            if self._symbol_table.type_of(cur_token) == "Array":
                return GrammarLanguage.ARRAY.value
            if self._symbol_table.type_of(cur_token) != "Array" and self._symbol_table.type_of(cur_token).isupper():
                return GrammarLanguage.OBJECT.value
            if self._symbol_table.type_of(cur_token) == "int":
                return GrammarLanguage.INT.value
        else:
            None

    def compile_expression(self, until=False):
        """Compiles an expression - expression grammar: term (op term) """
        expression = True
        if self._tokenizer.currentToken == "=":
            self._tokenizer.advance()

        if is_op(self._tokenizer.currentToken):
            self.compile_expression_operator()
            expression = False

        while expression:
            if self._tokenizer.currentToken == "(":
                self._tokenizer.advance()
                self.compile_expression(until=")")
                self._tokenizer.advance()

            if is_op(self._tokenizer.currentToken):
                cur_operator = self._tokenizer.currentToken
                self._tokenizer.advance()

                if self._tokenizer.currentToken != ";":
                    self.compile_term()

                self.write_arithmetic_vm(cur_operator)

            elif self._tokenizer.token_type() != Token_Type.SYMBOL:
                self.compile_term()

            self._tokenizer.advance()

            if until:
                if self._tokenizer.currentToken == until:
                    expression = False
            elif self.expression_ended():
                expression = False

    def compile_term_write_function_call(self):
        # is function call or arithmetic priority
        if self._tokenizer.currentToken == "(":
            # TODO: verify this is the correct logic
            # while self._tokenizer.currentToken == "(":
            self._tokenizer.advance()
            self.compile_expression(")")

    def compile_term_write_int_constant(self):
        # code_write if exp.is_numeric then write_push int constant
        if self._tokenizer.token_type() == Token_Type.INT_CONST.value or self._tokenizer.currentToken.isnumeric():
            self._vm_writer.write_push(segment=Segments.CONST.value, index=self._tokenizer.currentToken)

    def write_constructor(self):
        pass

    def get_type_of_calling_function(self):
        # get the type of the calling function and save it in a variable
        return self._symbol_table.type_of(self._tokenizer.currentToken) or self._tokenizer.currentToken

    def build_stack_methods(self, calling_function):
        # push each argument to the stack
        if self._tokenizer.currentToken == ".":
            calling_function = calling_function + self._tokenizer.currentToken
            self._tokenizer.advance()

            calling_function = calling_function + self._tokenizer.currentToken
            self._tokenizer.advance()

            if self._tokenizer.currentToken == "(":
                self.compile_expression_list()

        return calling_function

    def compile_term_write_objects_arrays_calls(self):
        is_method = False
        is_array = False

        calling_function_type = self.get_type_of_calling_function()
        if self._tokenizer.currentToken[0].islower() and not self._symbol_table.is_var(self._tokenizer.currentToken):
            is_method = True

        if self._tokenizer.look_ahead() == "[":
            is_array = True
            self.compile_array_addition(self._tokenizer.currentToken)

            self._vm_writer.write_pop("pointer", 1)
            self._vm_writer.write_push("that", 0)

        # write objects and arrays
        while is_object_or_array(self._tokenizer.currentToken):
            self._tokenizer.advance()
            calling_function_type = self.build_stack_methods(calling_function_type)

        if is_method:
            self._expression_list_count = self._expression_list_count + 1

        if not is_array:
            self._calling_function = calling_function_type
            self._vm_writer.write_call(self._calling_function, self._expression_list_count)

    def compile_term_write_arrays(self):
        if self._tokenizer.token_type() == Token_Type.IDENTIFIER:
            # is function call array or object
            if (self._tokenizer.look_ahead() == "." or
                    self._tokenizer.look_ahead() == "[" or
                    self._tokenizer.look_ahead() == "("):
                self.compile_term_write_objects_arrays_calls()

    def compile_term_write_boolean(self):
        if self._tokenizer.token_type() == Token_Type.KEYWORD:
            if self._tokenizer.currentToken == "true":
                self._vm_writer.write_push("constant", 1)
                self._vm_writer.write_arithmetic("neg")
            if self._tokenizer.currentToken == "false" or self._tokenizer.currentToken == "null":
                self._vm_writer.write_push("constant", 0)
            if self._tokenizer.currentToken == "this" and self._current_line_keyword == "do":
                self._vm_writer.write_push(segment="pointer", index=0)

    def compile_term_write_variables(self):
        # changed from .is_var to .kind_of
        if self._symbol_table.is_var(self._tokenizer.currentToken):
            kind = self._symbol_table.kind_of(self._tokenizer.currentToken)
            segment = VMWriter.get_segment_from_kind(kind)
            index = self._symbol_table.index_of(self._tokenizer.currentToken)

            self._vm_writer.write_push(segment=segment, index=index)

    def compile_term_write_operators(self):
        if is_op(self._tokenizer.currentToken):
            arithmetic_command = VMWriter.get_arithmetic_command(self._tokenizer.currentToken)
            self._vm_writer.write_arithmetic(arithmetic_command)
            self.write_arithmetic_vm(self._tokenizer.currentToken)

            self._tokenizer.advance()

            self.compile_term()

    def compile_term_write_string_constant(self):
        if self._tokenizer.token_type() == Token_Type.STRING_CONST:
            self._tokenizer.currentToken = self._tokenizer.currentToken.strip("\"")
            self.write_terminal_tag(GrammarLanguage.STRING_CONST.value)

            self._vm_writer.write_push("constant", len(self.tokenizer.currentToken))
            self._vm_writer.write_call("String.new", 1)

            for char in self._tokenizer.currentToken:
                self._vm_writer.write_push("constant", ord(char))
                self._vm_writer.write_call("String.appendChar", 2)

    def compile_term(self):
        """
        term: varName | constant
        Compiles a term. This routine must distinguish between variables, arrays and objects and subroutine calls.
        This routine will require a look ahead token which will be one of
        '[', or '(', or '.'. Any other token is not part of the term
        """
        self.compile_term_write_int_constant()

        self.compile_term_write_function_call()

        # write vm for variables
        self.compile_term_write_boolean()
        self.compile_term_write_arrays()
        self.compile_term_write_variables()

        self.compile_term_write_string_constant()
        self.compile_term_write_operators()

    def compile_expression_list(self):
        """Compiles a possibly empty comma-separated list of expressions"""
        self._expression_list_count = 0
        while self._tokenizer.currentToken != ";" and self._tokenizer.currentToken != ")":
            self._tokenizer.advance()

            if self._tokenizer.currentToken != ")":
                self._expression_list_count = self._expression_list_count + 1
                self.compile_expression()

            # if self._tokenizer.currentToken == ",":
            #     self.write_terminal_tag(self._tokenizer.token_type().value.lower())
