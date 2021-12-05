@R10
D=A
@R0
M=D

@R0
M=D // RAM[20] = 10
D=D+1 // RAM[11] = 11

@R4
D;JGT // JUMP To A register if greater than 0 