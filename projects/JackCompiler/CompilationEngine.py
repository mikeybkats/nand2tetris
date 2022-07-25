from JackTokenizer import JackTokenizer
from TokenTypes import Token_Type, GrammarLanguage, TerminalTypeTable, is_op
from io import TextIOBase
from VMWriter import VMWriter, Segments, get_math_lib_args
from SymbolTable import SymbolTable, is_standard_lib
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

    def __init__(self, input_stream, output_stream, write_xml):
        """
        Creates a new compilation engine with the given input and output. The next routine called must be compileClass()

        :param input_stream:
        :param output_stream:
        :param write_xml:
            boolean - if true Compilation engine will output xml
        """

        # make a jack tokenizer
        self._tokenizer = JackTokenizer(inputStreamOrFile=input_stream)
        self._write_xml = write_xml

        # make the outfile
        if write_xml:
            if isinstance(output_stream, TextIOBase):
                self._outfile = output_stream
            else:
                self._outfile = open(output_stream, mode="w+", encoding='utf-8')

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
        else:
            if token_type == GrammarLanguage.KEYWORD.value:
                self._table_obj["type"] = self._tokenizer.currentToken
            if token_type == GrammarLanguage.IDENTIFIER.value:
                self._table_obj["name"] = self._tokenizer.currentToken

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

            if (self._tokenizer.currentToken == GrammarLanguage.METHOD.value or
                self._tokenizer.currentToken == GrammarLanguage.CONSTRUCTOR.value or
                    self._tokenizer.currentToken == GrammarLanguage.FUNCTION.value):
                self.compile_subroutine()

        self.write_terminal_tag(self._tokenizer.token_type().value.lower())
        self.write_non_terminal_tag(GrammarLanguage.CLASS.value, True)

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

    def is_method(self):
        if self._tokenizer.currentToken == GrammarLanguage.METHOD:
            return True
        else:
            return False

    def compile_subroutine(self):
        """Compiles a complete method, function, or constructor"""
        if self.is_subroutine():
            self._symbol_table.start_subroutine()
            self.reset_table_obj()

            # write the first subroutine entry
            if not self.is_method():
                self._symbol_table.define(
                    i_name="this",
                    i_type=self._class_name,
                    i_kind="argument"
                )
                self._vm_writer.write_push(segment="argument", index=0)
                self._vm_writer.write_pop(segment="pointer", index=0)

            self.write_xml_tag_smart(GrammarLanguage.SUB_ROUTINE_DEC.value, False)
            # self.write_terminal_tag(self._tokenizer.token_type().value.lower())

            count = 0
            while count != 3:
                # count 0 write the first label in the signature method / function / constructor
                # count 1 write the return type in the signature
                # count 2 write the name of the method / function / constructor
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                self._tokenizer.advance()
                count = count + 1

            # while self._tokenizer.currentToken != ")":
            #     # compile parameter list
            if self._tokenizer.currentToken == "(":
                # write the opening '(' symbol
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                self.compile_parameter_list()
                # write the closing ')' symbol
                self.write_terminal_tag(GrammarLanguage.SYMBOL.value)

            while self.not_end_of_routine():
                self._tokenizer.advance()

                if self._tokenizer.currentToken == "{":
                    self.write_xml_tag_smart(GrammarLanguage.SUB_ROUTINE_BOD.value, False)
                    self.write_terminal_tag(self._tokenizer.token_type().value.lower())

                # compile declarations
                if (self._tokenizer.currentToken == GrammarLanguage.VAR.value or
                        self._tokenizer.currentToken == GrammarLanguage.INT.value):
                    self.compile_var_declaration()

                # compile statements
                if (self._tokenizer.currentToken == GrammarLanguage.LET.value or
                    self._tokenizer.currentToken == GrammarLanguage.DO.value or
                        self._tokenizer.currentToken == GrammarLanguage.IF.value):
                    self.compile_statements()

            self.write_terminal_tag(self._tokenizer.token_type().value.lower())
            self.write_xml_closing_tag(GrammarLanguage.SUB_ROUTINE_BOD.value)
            self.write_xml_closing_tag(GrammarLanguage.SUB_ROUTINE_DEC.value)

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list, not including the enclosing "()"."""
        self.write_xml_tag_smart(GrammarLanguage.PARAMETER_LIST.value, False)
        self._table_obj["kind"] = "argument"

        if self._tokenizer.currentToken == "(":
            self._tokenizer.advance()

        # ((type varName)(',' type varName)*)?
        while self._tokenizer.currentToken != ")":
            # self._symbol_table.define(i_name=)
            next_token = self._tokenizer.look_ahead()
            if (not self._tokenizer.currentToken == "," and
                    not next_token == ","
                    and self._tokenizer.get_token_type(next_token) == "identifier"):
                # then it must be the parameter type
                self._table_obj["type"] = self._tokenizer.currentToken
            elif self._tokenizer.token_type().value.lower() == "identifier":
                self._table_obj["name"] = self._tokenizer.currentToken
                self._symbol_table.define(
                    i_name=self._table_obj["name"],
                    i_kind=self._table_obj["kind"],
                    i_type=self._table_obj["type"]
                )

            self.write_terminal_tag(self._tokenizer.token_type().value.lower())
            self._tokenizer.advance()

        self.write_xml_closing_tag(GrammarLanguage.PARAMETER_LIST.value)

    def compile_class_var_declaration(self):
        """Compiles a static declaration or a field declaration"""

        if (self._tokenizer.currentToken == GrammarLanguage.STATIC.value or
                self._tokenizer.currentToken == GrammarLanguage.FIELD.value):

            self.write_xml_tag_smart(GrammarLanguage.CLASS_VAR_DEC.value, False)
            self.write_terminal_tag(self._tokenizer.token_type().value.lower())

            self._table_obj["kind"] = self._tokenizer.currentToken

            while self._tokenizer.currentToken != ";":
                self._tokenizer.advance()
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())

                if self._tokenizer.currentToken == "," or self._tokenizer.currentToken == ";":
                    self._symbol_table.define(
                        i_name=self._table_obj["name"],
                        i_type=self._table_obj["type"],
                        i_kind=self._table_obj["kind"]
                    )

            self.write_xml_closing_tag(GrammarLanguage.CLASS_VAR_DEC.value)

    def compile_var_declaration(self):
        """
        Compiles var declaration

        var type varName (, varName)*;
        """
        self.write_xml_tag_smart(GrammarLanguage.VAR_DEC.value, False)
        self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        self._table_obj["kind"] = "var"

        while self._tokenizer.currentToken != ";":
            self._tokenizer.advance()
            self.write_terminal_tag(self._tokenizer.token_type().value.lower())

            if self._tokenizer.currentToken == "," or self._tokenizer.currentToken == ";":
                self._symbol_table.define(
                    i_name=self._table_obj["name"],
                    i_type=self._table_obj["type"],
                    i_kind=self._table_obj["kind"]
                )

        self.write_xml_closing_tag(GrammarLanguage.VAR_DEC.value)

    def compile_statements(self):
        """Compiles a sequence of statements, not including the
        enclosing curly braces "{}". Compiles if, let and while statements"""
        self.write_xml_tag_smart(GrammarLanguage.STATEMENTS.value, False)

        while (self._tokenizer.currentToken == GrammarLanguage.DO.value or
                self._tokenizer.currentToken == GrammarLanguage.RETURN.value or
               self._tokenizer.currentToken == GrammarLanguage.WHILE.value or
               self._tokenizer.currentToken == GrammarLanguage.LET.value or
               self._tokenizer.currentToken == GrammarLanguage.IF.value):

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

        self.write_xml_closing_tag(GrammarLanguage.STATEMENTS.value)

    def compile_let(self):
        """Compiles a let statement"""
        self.write_xml_tag_smart(GrammarLanguage.LET_STATEMENT.value, False)
        self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        count = 0
        while self._tokenizer.currentToken != ";":
            self._tokenizer.advance()
            count = count + 1

            if count == 1:
                assignment_destination = self._tokenizer.currentToken

            if self.tokenizer.look_ahead() == "[":
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                self.tokenizer.advance()
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                self.compile_expression()
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                self.tokenizer.advance()

            if self.tokenizer.currentToken == "=":
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                self.compile_expression()
                break

            self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        segment = self._vm_writer.get_segment_from_kind(self._symbol_table.kind_of(assignment_destination))
        index = self._symbol_table.index_of(assignment_destination)
        self._vm_writer.write_pop(segment=segment, index=index)

        self.write_terminal_tag(self._tokenizer.token_type().value.lower())
        self.write_xml_closing_tag(GrammarLanguage.LET_STATEMENT.value)

    def compile_do(self):
        """Compiles a do statement"""
        self.write_xml_tag_smart(GrammarLanguage.DO_STATEMENT.value, False)
        self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        while self._tokenizer.currentToken != ";":
            self._tokenizer.advance()

            if self._tokenizer.currentToken == "(":
                self.write_terminal_tag(GrammarLanguage.SYMBOL.value.lower())
                self.compile_expression_list()

            self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        # self.write_terminal_tag(self._tokenizer.token_type().value.lower())
        self.write_xml_closing_tag(GrammarLanguage.DO_STATEMENT.value)

    def compile_while(self):
        """Compiles a while statement"""
        self.write_non_terminal_tag(GrammarLanguage.WHILE_STATEMENT.value, False)
        self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        while self._tokenizer.currentToken != "}":
            self._tokenizer.advance()

            if self._tokenizer.currentToken == "(":
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                self._tokenizer.advance()
                self.compile_expression()
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())

            if self._tokenizer.currentToken == "{":
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                self._tokenizer.advance()
                self.compile_statements()
                # self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        self.write_terminal_tag(self._tokenizer.token_type().value.lower())
        self.write_xml_closing_tag(GrammarLanguage.WHILE_STATEMENT.value)

    def compile_if(self):
        """Compiles if statement"""
        self.write_non_terminal_tag(GrammarLanguage.IF_STATEMENT.value, False)
        self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        self._tokenizer.advance()

        if self._tokenizer.currentToken == "(":
            self.write_terminal_tag(self._tokenizer.token_type().value.lower())
            self._tokenizer.advance()
            self.compile_expression()
            self.write_terminal_tag(self._tokenizer.token_type().value.lower())
            self._tokenizer.advance()

        while self._tokenizer.currentToken != "}":

            if self._tokenizer.currentToken == "{":
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                self._tokenizer.advance()
                self.compile_statements()
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                break

            self._tokenizer.advance()

        if self._tokenizer.look_ahead() == GrammarLanguage.ELSE.value:
            self._tokenizer.advance()
            self.compile_else()

        self.write_non_terminal_tag(GrammarLanguage.IF_STATEMENT.value, True)

    def compile_else(self):
        self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        while self._tokenizer.currentToken != "}":
            if self._tokenizer.currentToken == "{":
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                self._tokenizer.advance()
                self.compile_statements()
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                break

            self._tokenizer.advance()

    def compile_return(self):
        """Compiles a return statement"""
        self.write_non_terminal_tag(GrammarLanguage.RETURN_STATEMENT.value, False)
        self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        self._tokenizer.advance()
        if self._tokenizer.currentToken != ";":
            self.compile_expression()

        self._vm_writer.write_return()
        self.write_terminal_tag(self._tokenizer.token_type().value.lower())
        self.write_xml_closing_tag(GrammarLanguage.RETURN_STATEMENT.value)

    @property
    def exp(self):
        return self._exp

    def build_exp(self):
        self._exp = self._exp + self._tokenizer.currentToken

    def write_arithmetic_vm(self, operator):
        arithmetic_command = VMWriter.get_arithmetic_command(operator)
        if is_standard_lib(arithmetic_command):
            self._vm_writer.write_call(arithmetic_command, get_math_lib_args(arithmetic_command))
        else:
            self._vm_writer.write_arithmetic(arithmetic_command)

    def compile_expression(self):
        """Compiles an expression - expression grammar: term (op term) """
        expression = True

        self.write_non_terminal_tag(GrammarLanguage.EXPRESSION.value, False)

        if self._tokenizer.currentToken == "=":
            self._tokenizer.advance()

        if is_op(self._tokenizer.currentToken):
            cur_operator = self._tokenizer.currentToken

            self.write_arithmetic_vm(cur_operator)
            # arithmetic_command = VMWriter.get_arithmetic_command(cur_operator)
            # self._vm_writer.write_arithmetic(arithmetic_command)

            self.build_exp()
            self._tokenizer.advance()

            self.compile_term()

            self._tokenizer.advance()
            expression = False

        while expression:
            if self._tokenizer.currentToken == "(":
                self.compile_term()
            if is_op(self._tokenizer.currentToken):
                self.write_terminal_tag(GrammarLanguage.SYMBOL.value)

                cur_operator = self._tokenizer.currentToken
                self.build_exp()
                self._tokenizer.advance()

                if self._tokenizer.currentToken != ";":
                    self.compile_term()

                # arithmetic_command = VMWriter.get_arithmetic_command(cur_operator)
                # self._vm_writer.write_arithmetic(arithmetic_command)
                self.write_arithmetic_vm(cur_operator)

            elif self._tokenizer.token_type() != Token_Type.SYMBOL:
                self.compile_term()

            if self._tokenizer.currentToken != ";":
                self.build_exp()

            self._tokenizer.advance()

            if (self._tokenizer.currentToken == ";" or
                    self._tokenizer.currentToken == ")" or
                    self._tokenizer.currentToken == "]" or
                    self._tokenizer.currentToken == ","):
                expression = False

        self.write_non_terminal_tag(GrammarLanguage.EXPRESSION.value, True)

    def compile_term_write_opening_tag(self):
        self.write_xml_tag_open(GrammarLanguage.TERM.value)
        if self._write_xml:
            self._outfile.write("\n")

    def compile_term_write_function_call(self):
        # is function call or arithmetic priority
        if self._tokenizer.currentToken == "(":
            self.write_terminal_tag(self._tokenizer.token_type().value.lower())
            self.build_exp()
            self._tokenizer.advance()

            self.compile_expression()
            self.write_terminal_tag(self._tokenizer.token_type().value.lower())

    def compile_term_write_int_constant(self):
        # code_write if exp.is_numeric then write_push int constant
        if self._tokenizer.token_type() == Token_Type.INT_CONST:
            self.write_terminal_tag(GrammarLanguage.INT_CONSTANT.value)

            self._vm_writer.write_push(segment=Segments.CONST.value, index=self._tokenizer.currentToken)

    def write_constructor(self):
        pass

    def compile_term_write_objects_and_arrays(self):
        # get the name of the calling function and save it in a variable
        type_of = self._symbol_table.type_of(self._tokenizer.currentToken) or self._tokenizer.currentToken
        calling_function = type_of
        is_method = False
        if self._tokenizer.currentToken[0].islower():
            is_method = True

        # write objects and arrays
        while is_object_or_array(self._tokenizer.currentToken):
            # build exp
            self.build_exp()
            self._tokenizer.advance()

            # push each argument to the stack
            if self._tokenizer.currentToken == ".":
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                # build exp
                self.build_exp()
                calling_function = calling_function + self._tokenizer.currentToken
                self._tokenizer.advance()

                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                # build exp
                self.build_exp()
                calling_function = calling_function + self._tokenizer.currentToken
                self._tokenizer.advance()

                if self._tokenizer.currentToken == "(":
                    self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                    self.compile_expression_list()
                    self.write_terminal_tag(self._tokenizer.token_type().value.lower())

            if self._tokenizer.currentToken == "[":
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                # build exp
                self.build_exp()
                self._tokenizer.advance()

                self.compile_expression()
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
        # push calling function to the stack
        if calling_function:
            if is_method:
                self._expression_list_count = self._expression_list_count + 1
            self._vm_writer.write_call(calling_function, self._expression_list_count)

    def compile_term_write_keywords_and_identifiers(self):
        if self._tokenizer.token_type() == Token_Type.KEYWORD:
            self.write_terminal_tag(GrammarLanguage.KEYWORD.value)
            if self._tokenizer.currentToken == "true":
                self._vm_writer.write_push("constant", 1)
                self._vm_writer.write_arithmetic("neg")
            if self._tokenizer.currentToken == "false" or self._tokenizer.currentToken == "null":
                self._vm_writer.write_push("constant", 0)
        if self._tokenizer.token_type() == Token_Type.IDENTIFIER:
            self.write_terminal_tag(GrammarLanguage.IDENTIFIER.value)

            # code_write if exp.is_var then write_push(exp)
            if self._symbol_table.is_var(self._tokenizer.currentToken):
                kind = self._symbol_table.kind_of(self._tokenizer.currentToken)
                segment = VMWriter.get_segment_from_kind(kind)
                index = self._symbol_table.index_of(self._tokenizer.currentToken)

                self._vm_writer.write_push(segment=segment, index=index)

            # is function call array or object
            if (self._tokenizer.look_ahead() == "." or
                    self._tokenizer.look_ahead() == "[" or
                    self._tokenizer.look_ahead() == "("):
                self.compile_term_write_objects_and_arrays()

    def compile_term_write_operators(self):
        if is_op(self._tokenizer.currentToken):
            self.write_terminal_tag(self._tokenizer.token_type().value.lower())

            # arithmetic_command = VMWriter.get_arithmetic_command(self._tokenizer.currentToken)
            # self._vm_writer.write_arithmetic(arithmetic_command)
            self.write_arithmetic_vm(self._tokenizer.currentToken)

            # build exp
            self.build_exp()
            self._tokenizer.advance()

            self.compile_term()

    def compile_term(self):
        """
        term: varName | constant
        Compiles a term. This routine must distinguish between variables, arrays and objects and subroutine calls.
        This routine will require a look ahead token which will be one of
        '[', or '(', or '.'. Any other token is not part of the term
        """
        self.compile_term_write_opening_tag()
        self.compile_term_write_function_call()
        self.compile_term_write_int_constant()
        self.compile_term_write_keywords_and_identifiers()

        if self._tokenizer.token_type() == Token_Type.STRING_CONST:
            self._tokenizer.currentToken = self._tokenizer.currentToken.strip("\"")
            self.write_terminal_tag(GrammarLanguage.STRING_CONST.value)

        self.compile_term_write_operators()

        self.write_xml_closing_tag(GrammarLanguage.TERM.value)

    def compile_expression_list(self):
        """Compiles a possibly empty comma-separated list of expressions"""
        self.write_xml_tag_smart(GrammarLanguage.EXPRESSION_LIST.value, False)

        self._expression_list_count = 0
        while self._tokenizer.currentToken != ";" and self._tokenizer.currentToken != ")":
            self.build_exp()
            self._tokenizer.advance()

            if self._tokenizer.currentToken != ")":
                self._expression_list_count = self._expression_list_count + 1
                self.compile_expression()

            if self._tokenizer.currentToken == ",":
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        self.write_non_terminal_tag(GrammarLanguage.EXPRESSION_LIST.value, True)
