@R0
D=M

// red 
@R8
D;JGT // if R0>0 goto 8
//

@R1
M=0 // RAM[1] = 0
@10
0;JMP // end program inft loop

// red
@R1
M=1
//

@10
0;JMP