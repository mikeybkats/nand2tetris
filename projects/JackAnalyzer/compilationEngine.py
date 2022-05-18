from JackTokenizer import JackTokenizer
from TagTypes import Tag_Types
from TokenTypes import Token_Type, Keyword
import os


class CompilationEngine(self):
    def __init__(self, inputFileStream, outputFileStream):
        """ 
        Creates a new compilation engin with the givin input and output. The next routine called must be compileClass()
        """

        # make a jack tokenizer
        self._tokenizer = JackTokenizer(inputStreamOrFile=inputFileStream)
        # make the outfile
        self._outfile = open(inputFileStream, mode="w+", encoding='utf-8')

        pass

    def write_xml_tag(self, tagType):
        self._outfile.write("<" + tagType + ">")

    def write_xml_closing_tag(self, tagType):
        self._outfile.write("</" + tagType + ">\n")

    def compile_class(self):
        """Compiles a complete class"""
        while self._tokenizer.has_more_tokens():
            # get the token
            self._tokenizer.advance()

            if (self._tokenizer.token_type() == Token_Type.KEYWORD and
                    self._tokenizer.currentToken == "class"):
                self.write_xml_tag(Tag_Types.CLASS)
                self._outfile.write("\n")
                self.write_xml_tag(Tag_Types.KEYWORD)
                self._outfile.write(self._tokenizer.currentToken)
                self.write_xml_closing_tag(Tag_Types.KEYWORD)
                break

            if self._tokenizer.token_type() == Token_Type.IDENTIFIER:
                self.write_xml_tag(Tag_Types.IDENTIFIER)
                self._outfile.write(self._tokenizer.currentToken)
                self.write_xml_closing_tag(Tag_Types.IDENTIFIER)
                break

            if (
                self._tokenizer.token_type() == Token_Type.SYMBOL
                    and (self._tokenizer.currentToken == "{"
                         or self._tokenizer.currentToken == "}")
            ):
                self.write_xml_tag(Tag_Types.SYMBOL)
                self._outfile.write(self._tokenizer.currentToken)
                self.write_xml_closing_tag(Tag_Types.SYMBOL)
                break

            if (
                self._tokenizer.token_type() == Token_Type.KEYWORD and
                (
                    self._tokenizer.currentToken == Keyword.STATIC or
                    self._tokenizer.currentToken == Keyword.FIELD
                )
            ):
                self.compile_class_var_declaration()
                break

    def compile_class_var_declaration(self):
        """Compiles a static declaration or a field declaration"""
        pass

    def compile_subroutine(self):
        """Compiles a complete method, function, or constructor"""
        pass

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list, not including the enclosing "()"."""
        pass

    def compile_var_declaration(self):
        """Compiles var declaration"""
        pass

    def compile_statements(self):
        """Compiles a sequence of statements, not including the enclosing curly braces "{}". """
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
        pass

    def compile_term(self):
        """
        Compiles a term. This routine must distinguish between variables, arrays and objects and subroutine calls.
        This routine will require a look ahead token which will be one of '[', or '(', or '.'. Any other token is not part of the term
        """
        pass

    def compile_expression_list(self):
        """Compiles a possibly empty comma-seperated list of expressions"""
        pass
