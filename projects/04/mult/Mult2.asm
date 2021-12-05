@R0
M=0
@R1
M=0
@R2
M=0
@i
M=0

(LOOP)
    // get value of R0
    @R0
    // set D to RAM[0]
    D=M
    // get value of R3
    @R3
    // set RAM[3] = D
    M=M+D

    // get value of R1
    @R1
    // set value of R1 - 1
    D=D-1

    @END
    D;JEQ

@LOOP
D;JGT

(END)
@END
0;JMP