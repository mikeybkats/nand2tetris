@1
D=A
@2
A=D+M
D=M
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M // get the topmost value from the stack
@4
M=D // insert the value into this/that
@0
D=A
@0
A=M
M=D
@0
M=M+1
@0 // get the index
D=A
@4 // set the destination at this/that (will change this back later) 
M=M+D
@0
A=M-1 // go to SP
D=M // set D reg to RAM[SP]
@4 // go to this/that
A=M
M=D // set RAM[THIS/THAT] to RAM[SP]
@0
D=A // set this/that back to what it was originally
@4
M=M-D
@1
D=A
@0
A=M
M=D
@0
M=M+1
@1 // get the index
D=A
@4 // set the destination at this/that (will change this back later) 
M=M+D
@0
A=M-1 // go to SP
D=M // set D reg to RAM[SP]
@4 // go to this/that
A=M
M=D // set RAM[THIS/THAT] to RAM[SP]
@1
D=A // set this/that back to what it was originally
@4
M=M-D
@0
D=A
@2
A=D+M
D=M
@0
A=M
M=D
@0
M=M+1
@2
D=A
@0
A=M
M=D
@0
M=M+1
@0
A=M-1
D=M
@0
M=M-1
A=M-1
M=M-D
@0 // get the index
D=A
@2 // set the destination at this/that (will change this back later) 
M=M+D
@0
A=M-1 // go to SP
D=M // set D reg to RAM[SP]
@2 // go to this/that
A=M
M=D // set RAM[THIS/THAT] to RAM[SP]
@0
D=A // set this/that back to what it was originally
@2
M=M-D
(MAIN_LOOP_START)
@0
D=A
@2
A=D+M
D=M
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M
@COMPUTE_ELEMENT
D;JNE
@END_PROGRAM
0;JMP
(COMPUTE_ELEMENT)
@0
D=A
@4
A=D+M
D=M
@0
A=M
M=D
@0
M=M+1
@1
D=A
@4
A=D+M
D=M
@0
A=M
M=D
@0
M=M+1
@0
A=M-1
D=M
@0
M=M-1
A=M-1
M=D+M
@2 // get the index
D=A
@4 // set the destination at this/that (will change this back later) 
M=M+D
@0
A=M-1 // go to SP
D=M // set D reg to RAM[SP]
@4 // go to this/that
A=M
M=D // set RAM[THIS/THAT] to RAM[SP]
@2
D=A // set this/that back to what it was originally
@4
M=M-D
@4 
D=M // take the value of this or that
@0
A=M
M=D // push it ontop of the stack
@0
M=M+1
@1
D=A
@0
A=M
M=D
@0
M=M+1
@0
A=M-1
D=M
@0
M=M-1
A=M-1
M=D+M
@0
M=M-1
A=M
D=M // get the topmost value from the stack
@4
M=D // insert the value into this/that
@0
D=A
@2
A=D+M
D=M
@0
A=M
M=D
@0
M=M+1
@1
D=A
@0
A=M
M=D
@0
M=M+1
@0
A=M-1
D=M
@0
M=M-1
A=M-1
M=M-D
@0 // get the index
D=A
@2 // set the destination at this/that (will change this back later) 
M=M+D
@0
A=M-1 // go to SP
D=M // set D reg to RAM[SP]
@2 // go to this/that
A=M
M=D // set RAM[THIS/THAT] to RAM[SP]
@0
D=A // set this/that back to what it was originally
@2
M=M-D
@MAIN_LOOP_START
0;JMP
(END_PROGRAM)
