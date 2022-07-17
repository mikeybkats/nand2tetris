from JackTokenizer import JackTokenizer
from TokenTypes import Token_Type, GrammarLanguage, TerminalTypeTable, is_op
from io import TextIOBase
from VMWriter import VMWriter
from SymbolTable import SymbolTable
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

    def compile_subroutine(self):
        """Compiles a complete method, function, or constructor"""
        if self.is_subroutine():
            self._symbol_table.start_subroutine()
            self.reset_table_obj()

            # write the first subroutine entry
            self._symbol_table.define(
                i_name="this",
                i_type=self._class_name,
                i_kind="argument"
            )

            self.write_xml_tag_smart(GrammarLanguage.SUB_ROUTINE_DEC.value, False)
            self.write_terminal_tag(self._tokenizer.token_type().value.lower())

            count = 0
            while count != 3:
                # count 0 write the first label in the signature method / function / constructor
                # count 1 write the return type in the signature
                # count 2 write the name of the method / function / constructor
                self.write_xml_tag_smart(self._tokenizer.token_type().value.lower(), True)
                self._tokenizer.advance()
                count = count + 1

            while self._tokenizer.currentToken != ")":
                # compile parameter list
                if self._tokenizer.currentToken == "(":
                    self.compile_parameter_list()
                    # write the closing ')' symbol
                    self.write_terminal_tag(GrammarLanguage.SYMBOL.value)

            while self.not_end_of_routine():
                self._tokenizer.advance()

                if self._tokenizer.currentToken == "{":
                    self.write_xml_tag_smart(GrammarLanguage.SUB_ROUTINE_BOD.value, False)

                # is the method / subroutine signature (first line before subroutine body)
                # if self.is_subroutine_identifier_signature():
                #     self.write_terminal_tag(self._tokenizer.token_type().value.lower())

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

        self._table_obj["kind"] = "local"

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

        while self._tokenizer.currentToken != ";":
            self._tokenizer.advance()

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

        self.write_terminal_tag(self._tokenizer.token_type().value.lower())
        self.write_xml_closing_tag(GrammarLanguage.RETURN_STATEMENT.value)

    def compile_expression(self):
        """Compiles an expression - expression grammar: term (op term) """
        self.write_non_terminal_tag(GrammarLanguage.EXPRESSION.value, False)

        if self._tokenizer.currentToken == "=":
            self._tokenizer.advance()

        expression = True

        if is_op(self._tokenizer.currentToken):
            self.compile_term()
            self._tokenizer.advance()
            expression = False

        while expression:
            if self._tokenizer.currentToken == "(":
                self.compile_term()
            if is_op(self._tokenizer.currentToken):
                self.write_terminal_tag(GrammarLanguage.SYMBOL.value)
            elif self._tokenizer.token_type() != Token_Type.SYMBOL:
                self.compile_term()

            self._tokenizer.advance()

            if (self._tokenizer.currentToken == ";" or
                    self._tokenizer.currentToken == ")" or
                    self._tokenizer.currentToken == "]" or
                    self._tokenizer.currentToken == ","):
                expression = False

        self.write_non_terminal_tag(GrammarLanguage.EXPRESSION.value, True)

    def compile_term(self):
        """
        term: varName | constant
        Compiles a term. This routine must distinguish between variables, arrays and objects and subroutine calls.
        This routine will require a look ahead token which will be one of
        '[', or '(', or '.'. Any other token is not part of the term
        """
        self.write_xml_tag_open(GrammarLanguage.TERM.value)
        if self._write_xml:
            self._outfile.write("\n")

        if self._tokenizer.currentToken == "(":
            self.write_terminal_tag(self._tokenizer.token_type().value.lower())
            self._tokenizer.advance()
            self.compile_expression()
            self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        if self._tokenizer.token_type() == Token_Type.INT_CONST:
            self.write_terminal_tag(GrammarLanguage.INT_CONSTANT.value)

        if self._tokenizer.token_type() == Token_Type.KEYWORD:
            self.write_terminal_tag(GrammarLanguage.KEYWORD.value)

        if self._tokenizer.token_type() == Token_Type.IDENTIFIER:
            self.write_terminal_tag(GrammarLanguage.IDENTIFIER.value)

            if (self._tokenizer.look_ahead() == "." or
                self._tokenizer.look_ahead() == "[" or
                    self._tokenizer.look_ahead() == "("):

                while is_object_or_array(self._tokenizer.currentToken):
                    self._tokenizer.advance()

                    if self._tokenizer.currentToken == ".":
                        self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                        self._tokenizer.advance()
                        self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                        self._tokenizer.advance()

                        if self._tokenizer.currentToken == "(":
                            self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                            self.compile_expression_list()
                            self.write_terminal_tag(self._tokenizer.token_type().value.lower())

                    if self._tokenizer.currentToken == "[":
                        self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                        self._tokenizer.advance()
                        self.compile_expression()
                        self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        if self._tokenizer.token_type() == Token_Type.STRING_CONST:
            self._tokenizer.currentToken = self._tokenizer.currentToken.strip("\"")
            self.write_terminal_tag(GrammarLanguage.STRING_CONST.value)

            # write string constant
            # for each character
            # self._vm_writer.write_push()

        if is_op(self._tokenizer.currentToken):
            self.write_terminal_tag(self._tokenizer.token_type().value.lower())
            self._tokenizer.advance()
            self.compile_term()

        self.write_xml_closing_tag(GrammarLanguage.TERM.value)

    def compile_expression_list(self):
        """Compiles a possibly empty comma-separated list of expressions"""
        self.write_xml_tag_smart(GrammarLanguage.EXPRESSION_LIST.value, False)

        while self._tokenizer.currentToken != ";" and self._tokenizer.currentToken != ")":
            self._tokenizer.advance()
            if self._tokenizer.currentToken != ")":
                self.compile_expression()

            if self._tokenizer.currentToken == ",":
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        self.write_non_terminal_tag(GrammarLanguage.EXPRESSION_LIST.value, True)
