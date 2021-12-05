(LOOP)
    @R0
    D=M

    @count // RAM[16]
    M=M+1

    D=D-M
@END
    D;JEQ

@LOOP
    D;JGT

(END)
    @END
    0;JMP