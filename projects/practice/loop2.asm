// int count;
// for (int i = 0; i < length; i++){
//     count = i;
// }

@R0
D=M // sets D register to value of A register 0

@length
M=D
D=M

@i
M=0

@count
M=0

(LOOP)
    @length
    D=M
    @i
    M=M+1
    D=M
    @count
    M=D

@length
D=M
@i
D=D-M
@END
D;JEQ 

@LOOP
D;JGT

(END)
    @END
    0;JMP


