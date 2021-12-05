// set RAM[0] to the number ram units to crawl from 1 to X
@R0 // limit 
D=M

@count
M=A
D=A 

(LOOP)
    @count
    M=M+1 // RAM[16] = count+1
    D=M
    A=M // access ram at M 
    M=-1 // set ram at M to -1

    // count - 16 - RAM[0] 
    @count
    D=D-A
    @R0
    D=D-M
        @END
        D;JEQ

@LOOP
D;JGT

(END)
0;JMP

