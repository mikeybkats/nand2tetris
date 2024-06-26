from JackTokenizer import JackTokenizer
from TokenTypes import Token_Type, GrammarLanguage, TerminalTypeTable, is_op
from io import TextIOBase
import html


class CompilationEngine:
    def __init__(self, input_stream, output_stream):
        """ 
        Creates a new compilation engine with the given input and output. The next routine called must be compileClass()
        """

        # make a jack tokenizer
        self._tokenizer = JackTokenizer(inputStreamOrFile=input_stream)
        # make the outfile
        if isinstance(output_stream, TextIOBase):
            self._outfile = output_stream
        else:
            self._outfile = open(output_stream, mode="w+", encoding='utf-8')

    @property
    def tokenizer(self):
        return self._tokenizer

    @property
    def outfile(self):
        return self._outfile

    def close_outfile(self):
        self._outfile.close()

    def write_xml_tag(self, tag_type):
        self._outfile.write("<" + tag_type + ">")

    def write_xml_tag_2(self, tag_type, tag_open):
        terminal_types = TerminalTypeTable()
        if terminal_types.is_terminal(tag_type):
            self.write_terminal_tag(tag_type)
        else:
            self.write_non_terminal_tag(tag_type, tag_open)

    def write_xml_closing_tag(self, tag_type):
        self._outfile.write("</" + tag_type + ">\n")

    def write_token(self):
        token = self._tokenizer.currentToken
        if is_op(token):
            token = html.escape(token)
        self._outfile.write(" " + token + " ")

    def write_non_terminal_tag(self, tag_type, closed):
        """Writes an open token tag: <tokenType>\n or </tokenType>\n"""
        if closed:
            self.write_xml_closing_tag(tag_type)
        else:
            self.write_xml_tag(tag_type)
            self._outfile.write("\n")

    def write_terminal_tag(self, token_type):
        """Writes a closed token tag: <tokenType> currentToken </tokenType>\n"""
        self.write_xml_tag(token_type)
        self.write_token()
        self.write_xml_closing_tag(token_type)

    def compile_class(self):
        """Compiles a complete class"""

        while self._tokenizer.has_more_tokens():
            self._tokenizer.advance()

            if self._tokenizer.currentToken == GrammarLanguage.CLASS.value:
                self.write_non_terminal_tag(GrammarLanguage.CLASS.value, False)
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                self._tokenizer.advance()
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())
                self._tokenizer.advance()
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

    def compile_class_var_declaration(self):
        """Compiles a static declaration or a field declaration"""
        if (self._tokenizer.currentToken == GrammarLanguage.STATIC.value or
                self._tokenizer.currentToken == GrammarLanguage.FIELD.value):

            self.write_xml_tag_2(GrammarLanguage.CLASS_VAR_DEC.value, False)
            self.write_terminal_tag(self._tokenizer.token_type().value.lower())

            while self._tokenizer.currentToken != ";":
                self._tokenizer.advance()
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())

            self.write_xml_closing_tag(GrammarLanguage.CLASS_VAR_DEC.value)

    def compile_subroutine(self):
        """Compiles a complete method, function, or constructor"""
        if (self._tokenizer.currentToken == GrammarLanguage.FUNCTION.value or
                self._tokenizer.currentToken == GrammarLanguage.METHOD.value or
                self._tokenizer.currentToken == GrammarLanguage.CONSTRUCTOR.value):
            self.write_xml_tag_2(GrammarLanguage.SUB_ROUTINE_DEC.value, False)
            self.write_terminal_tag(self._tokenizer.token_type().value.lower())

            while self._tokenizer.currentToken != "}":
                self._tokenizer.advance()

                if self._tokenizer.currentToken == "{":
                    self.write_xml_tag_2(GrammarLanguage.SUB_ROUTINE_BOD.value, False)

                if ((self._tokenizer.currentToken != GrammarLanguage.VAR.value and
                     self._tokenizer.currentToken != GrammarLanguage.INT.value and
                     self._tokenizer.currentToken != GrammarLanguage.DO.value and
                     self._tokenizer.currentToken != GrammarLanguage.IF.value and
                     self._tokenizer.currentToken != GrammarLanguage.LET.value) and
                        self._tokenizer.token_type().value.lower() == GrammarLanguage.KEYWORD.value or
                        self._tokenizer.token_type().value.lower() == GrammarLanguage.IDENTIFIER.value or
                        self._tokenizer.token_type().value.lower() == GrammarLanguage.SYMBOL.value):
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

                # compile parameter list
                if self._tokenizer.currentToken == "(":
                    self.compile_parameter_list()
                    # write the closing ')' symbol
                    self.write_terminal_tag(GrammarLanguage.SYMBOL.value)

            self.write_terminal_tag(self._tokenizer.token_type().value.lower())
            self.write_xml_closing_tag(GrammarLanguage.SUB_ROUTINE_BOD.value)
            self.write_xml_closing_tag(GrammarLanguage.SUB_ROUTINE_DEC.value)

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list, not including the enclosing "()"."""
        self.write_xml_tag_2(GrammarLanguage.PARAMETER_LIST.value, False)

        if self._tokenizer.currentToken == "(":
            self._tokenizer.advance()

        # ((type varName)(',' type varName)*)?
        while self._tokenizer.currentToken != ")":
            self.write_terminal_tag(self._tokenizer.token_type().value.lower())
            self._tokenizer.advance()

        self.write_xml_closing_tag(GrammarLanguage.PARAMETER_LIST.value)

    def compile_var_declaration(self):
        """
        Compiles var declaration

        var type varName (, varName)*;
        """
        self.write_xml_tag_2(GrammarLanguage.VAR_DEC.value, False)
        self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        while self._tokenizer.currentToken != ";":
            self._tokenizer.advance()
            self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        self.write_xml_closing_tag(GrammarLanguage.VAR_DEC.value)

    def compile_statements(self):
        """Compiles a sequence of statements, not including the
        enclosing curly braces "{}". Compiles if, let and while statements"""
        self.write_xml_tag_2(GrammarLanguage.STATEMENTS.value, False)

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
        self.write_xml_tag_2(GrammarLanguage.LET_STATEMENT.value, False)
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
        self.write_xml_tag_2(GrammarLanguage.DO_STATEMENT.value, False)
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
        self.write_xml_tag(GrammarLanguage.TERM.value)
        self.outfile.write("\n")

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

                while (self._tokenizer.currentToken != ";" and
                        self._tokenizer.currentToken != "{" and
                        self._tokenizer.currentToken != ")" and
                       self._tokenizer.currentToken != "]" and
                        self._tokenizer.currentToken != "="):
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

        if is_op(self._tokenizer.currentToken):
            self.write_terminal_tag(self._tokenizer.token_type().value.lower())
            self._tokenizer.advance()
            self.compile_term()

        self.write_xml_closing_tag(GrammarLanguage.TERM.value)

    def compile_expression_list(self):
        """Compiles a possibly empty comma-separated list of expressions"""
        self.write_xml_tag_2(GrammarLanguage.EXPRESSION_LIST.value, False)

        while self._tokenizer.currentToken != ";" and self._tokenizer.currentToken != ")":
            self._tokenizer.advance()
            if self._tokenizer.currentToken != ")":
                self.compile_expression()

            if self._tokenizer.currentToken == ",":
                self.write_terminal_tag(self._tokenizer.token_type().value.lower())

        self.write_non_terminal_tag(GrammarLanguage.EXPRESSION_LIST.value, True)
