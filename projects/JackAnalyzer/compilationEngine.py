from JackTokenizer import JackTokenizer
from TagTypes import Tag_Types
from TokenTypes import Token_Type, GrammarLanguage, TerminalTypeTable
from io import TextIOBase


class CompilationEngine:
    def __init__(self, input_stream, output_stream):
        """ 
        Creates a new compilation engin with the givin input and output. The next routine called must be compileClass()
        """

        # make a jack tokenizer
        self._tokenizer = JackTokenizer(inputStreamOrFile=input_stream)
        # make the outfile
        if isinstance(output_stream, TextIOBase):
            self._outfile = output_stream
        else:
            self._outfile = open(input_stream, mode="w+", encoding='utf-8')

    @property
    def tokenizer(self):
        return self._tokenizer

    @property
    def outfile(self):
        return self._outfile

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
        self._outfile.write(" " + self._tokenizer.currentToken + " ")

    # TODO: implement this write_non_terminal_tag so that write_xml_tag does not need more qualifying lines of code
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
            # get the token
            self._tokenizer.advance()

            # if keyword and word == class
            if (self._tokenizer.token_type() == GrammarLanguage.KEYWORD.value and
                    self._tokenizer.currentToken == "class"):
                self.write_xml_tag_2(GrammarLanguage.CLASS.value, True)

            # if identifier
            if self._tokenizer.token_type() == GrammarLanguage.IDENTIFIER.value:
                self.write_terminal_tag(GrammarLanguage.IDENTIFIER.value)
                break

            if (self._tokenizer.token_type() == GrammarLanguage.SYMBOL.value and
                    self._tokenizer.currentToken == "{"):
                self.write_terminal_tag(GrammarLanguage.SYMBOL.value)
                break

            # TODO: compile all statements
            # now compile all the class elements
            # self.compile_class_var_declaration()

            if (self._tokenizer.token_type() == GrammarLanguage.SYMBOL.value and
                    self._tokenizer.currentToken == "}"):
                self.write_terminal_tag(GrammarLanguage.SYMBOL.value)
                break

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

                self.write_terminal_tag(self._tokenizer.token_type().value.lower())

                if self._tokenizer.currentToken == "(":
                    self.write_xml_tag_2(GrammarLanguage.PARAMETER_LIST.value, False)

                    # ((type varName)(',' type varName)*)?
                    while self._tokenizer.currentToken != ")":
                        self._tokenizer.advance()

                        if self._tokenizer.currentToken == ",":
                            self.write_terminal_tag(self._tokenizer.token_type().value.lower())

                        if self._tokenizer.currentToken == ")":
                            self.write_xml_closing_tag(GrammarLanguage.PARAMETER_LIST.value)

                        if self._tokenizer.currentToken != ",":
                            self.compile_term()



    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list, not including the enclosing "()"."""
        pass

    def compile_var_declaration(self):
        """Compiles var declaration"""
        pass

    def compile_statements(self):
        """Compiles a sequence of statements, not including the
        enclosing curly braces "{}". Compiles if, let and while statements"""
        pass

    def compile_do(self):
        """Compiles a do statement"""
        pass

    def compile_let(self):
        """Compiles a let statement"""
        pass

    def compile_while(self):
        """Compiles a while statement"""

    def compile_return(self):
        """Compiles a return statement"""
        pass

    def compile_if(self):
        """Compiles if statement"""
        pass

    def compile_expression(self):
        """Compiles an expressions"""

    def compile_term(self):
        """
        term: varName | constant
        Compiles a term. This routine must distinguish between variables, arrays and objects and subroutine calls.
        This routine will require a look ahead token which will be one of
        '[', or '(', or '.'. Any other token is not part of the term
        """

        if self._tokenizer.token_type() == Token_Type.SYMBOL:
            self.write_xml_tag(GrammarLanguage.SYMBOL.value)
            self.write_token()
            self.write_xml_closing_tag(GrammarLanguage.SYMBOL.value)
            return

        self.write_xml_tag(GrammarLanguage.TERM.value)
        self.outfile.write("\n")

        if self._tokenizer.token_type() == Token_Type.INT_CONST:
            self.write_xml_tag(GrammarLanguage.INT_CONSTANT.value)

        if self._tokenizer.token_type() == Token_Type.IDENTIFIER:
            self.write_xml_tag(GrammarLanguage.IDENTIFIER.value)

        # TODO: update outfile.write here so it can distinguish between the different kinds of term tokens
        # but for now it just writes the current token
        self.write_token()

        if self._tokenizer.token_type() == Token_Type.IDENTIFIER:
            self.write_xml_closing_tag(GrammarLanguage.IDENTIFIER.value)

        if self._tokenizer.token_type() == Token_Type.INT_CONST:
            self.write_xml_closing_tag(GrammarLanguage.INT_CONSTANT.value)

        self.write_xml_closing_tag(GrammarLanguage.TERM.value)

    def compile_expression_list(self):
        """Compiles a possibly empty comma-separated list of expressions"""
        pass
