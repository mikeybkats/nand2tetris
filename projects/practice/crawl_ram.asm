// set RAM[0] to the number ram units to crawl from 1 to X
@R0 // limit 
D=M

@count
M=0
D=A

// RAM[i] = -1
@count
A=M+1
M=-1

@count
M=M+1

@R0
D=M+1
@count
D=D-M

@4
D;JGT

(END)
@END
0;JMP

