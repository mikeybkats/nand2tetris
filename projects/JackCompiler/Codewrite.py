from TokenTypes import GrammarLanguage, is_op


class Codewrite:
    def __int__(self, vm_writer):
        self._vm_writer = vm_writer

    def is_exp_op_exp(self, exp):
        return False

    def is_op_exp(self, exp):
        return False

    def get_exp_1(self, exp):
        pass

    def get_exp_2(self, exp):
        pass

    def get_op(self, exp):
        pass

    def get_function_name(self, exp_func):
        pass

    def get_exp_args(self, exp):
        pass

    def code_write(self, exp):
        if exp.isnumeric():
            self._vm_writer.write_push(exp)
        if self._symbol_table.kind_of(exp) == GrammarLanguage.VAR.value.lower():
            self._vm_writer.write_push(exp)
        if self.is_exp_op_exp(exp):
            exp1 = self.get_exp_1(exp)
            exp2 = self.get_exp_2(exp)
            op = self.get_op(exp)
            self.codewrite(exp1)
            self.codewrite(exp2)
            self._vm_writer.write_custom(op)
        if self.is_op_exp(exp):
            self.codewrite(exp)
            op = self.get_op(exp)
            self._vm_writer.write_custom(op)
        if self.exp_is_function(exp):
            exp_args = self.get_exp_args(exp)
            name = self.get_function_name(exp)
            n_args = len(exp_args)

            for exp_arg in exp_args:
                self.codewrite(exp_arg)
            self._vm_writer.write_call(n_args=n_args, name=name)

