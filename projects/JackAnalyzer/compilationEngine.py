
class CompilationEngine(self):
    def __init__(self, inputFileStream, outputFileStream):
        """ 
        Creates a new compilation engin with the givin input and output. The next routine called must be compileClass()
        """
        pass

    def compile_class(self):
        """Compiles a complete class"""
        pass

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
