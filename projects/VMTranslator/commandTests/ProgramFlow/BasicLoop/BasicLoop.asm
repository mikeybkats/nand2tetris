@0
D=A
@0
A=M
M=D
@0
M=M+1
@0 // get the index
D=A
@1 // set the destination at this/that (will change this back later) 
M=M+D
@0  // goto topmost value on stack 
M=M-1
A=M 
D=M // set D reg to RAM[SP-1]
@1 // go to this/that
A=M
M=D // set RAM[THIS/THAT] to RAM[SP]
@0
D=A // set this/that back to what it was originally
@1
M=M-D
(LOOP_START)
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
D=A
@1
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
@0 // get the index
D=A
@1 // set the destination at this/that (will change this back later) 
M=M+D
@0  // goto topmost value on stack 
M=M-1
A=M 
D=M // set D reg to RAM[SP-1]
@1 // go to this/that
A=M
M=D // set RAM[THIS/THAT] to RAM[SP]
@0
D=A // set this/that back to what it was originally
@1
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
@0  // goto topmost value on stack 
M=M-1
A=M 
D=M // set D reg to RAM[SP-1]
@2 // go to this/that
A=M
M=D // set RAM[THIS/THAT] to RAM[SP]
@0
D=A // set this/that back to what it was originally
@2
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
@0
M=M-1
A=M
D=M
@LOOP_START
D;JNE
@0
D=A
@1
A=D+M
D=M
@0
A=M
M=D
@0
M=M+1
