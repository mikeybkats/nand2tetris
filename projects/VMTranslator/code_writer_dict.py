from textwrap import dedent


class CodeWriterDict:
    def __init__(self):
        self._assembly = dict([
            ("eq", dedent("""\
                D=M-D
                M=-1
                @EQ_{}
                D;JEQ
                // @0
                // A=M-1
                // M=0
                (EQ_{})
                """)
             ),
            ("gt", dedent("""\
                D=M-D
                M=-1
                @GT_{}
                D;JGT
                // @0
                // A=M-1
                // M=0
                (GT_{})
                """)
             ),
            ("lt", dedent("""\
                D=M-D
                M=-1
                @LT_{}
                D;JLT
                // @0
                // A=M-1
                // M=0
                (LT_{})
                """)
             ),
            ("push_constant", dedent("""\
                @{}
                D=A
                @{}
                A=M
                M=D
                @{}
                M=M+1
            """)
             ),
            ("push_static", dedent("""\
                @{}
                D=M
                @0
                A=M
                M=D
                @0
                M=M+1
            """)
             ),
            ("push_temp", dedent("""\
                @{}
                D=M
                @0
                A=M
                M=D
                @0
                M=M+1
            """)
             ),
            ("push_pointer", dedent("""\
                @{} 
                D=M // take the value of this or that
                @0
                A=M
                M=D // push it ontop of the stack
                @0
                M=M+1
            """)
             ),
            ("push_default", dedent("""\
                @{}
                D=A
                @{}
                A=D+M
                D=M
                @0
                A=M
                M=D
                @0
                M=M+1
            """)
             ),
            ("pop_static", dedent("""\
                @0
                A=M-1
                D=M
                @{}
                M=D
                @0
                M=M-1
                // A=M
                // M=0
            """)
             ),
            ("pop_temp", dedent("""\
                @0
                M=M-1
                A=M
                D=M
                // M=0
                @{}
                M=D
            """)
             ),
            # popping the pointer means putting it onto this/that RAM[3/4]
            ("pop_pointer", dedent("""\
                @0
                M=M-1
                A=M
                D=M // get the topmost value from the stack
                @{}
                M=D // insert the value into this/that
            """)
             ),
            # popping takes one below the stack pointer
            ("pop_default", dedent("""\
                @{} // get the index
                D=A
                @{} // set the destination at this/that (will change this back later) 
                M=M+D
                @0
                A=M-1 // go to SP
                D=M // set D reg to RAM[SP]
                @{} // go to this/that
                A=M
                M=D // set RAM[THIS/THAT] to RAM[SP]
                @{}
                D=A // set this/that back to what it was originally
                @{}
                M=M-D
            """)
             ),
            ("bootstrap", "@256\nD=A\n@0\nM=D\n"),
            ("label", "({})\n"),
            ("goto", "@{}\n0;JMP\n"),
            ("if_goto", dedent("""\
                @0
                M=M-1
                A=M
                D=M
                @{}
                D;JNE
            """)
             ),
            ("push_segment", dedent("""\
                @{}
                D=M
                @0
                A=M
                M=D
                @0
                M=M+1
            """)),
        ])

    def get_assembly(self, command):
        return self._assembly.get(command)
