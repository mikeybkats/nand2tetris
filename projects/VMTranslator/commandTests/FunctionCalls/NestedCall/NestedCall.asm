@256
D=A
@0
M=D
@Sys.init$ret.0.0
D=A
@0
A=M
M=D
@0
M=M+1
@1
D=M
@0
A=M
M=D
@0
M=M+1
@2
D=M
@0
A=M
M=D
@0
M=M+1
@3
D=M
@0
A=M
M=D
@0
M=M+1
@4
D=M
@0
A=M
M=D
@0
M=M+1
@0  // put SP in RAM[ARG]
D=M
@2
M=D

@0 // get num of args 
D=A
@2 // subtract number of arguments from RAM[ARG]
M=M-D

@5 // subtract 5 (number of saved stack items) from RAM[ARG]
D=A
@2
M=M-D
@0
D=M
@1
M=D
@Sys.init
A;JMP
(Sys.init$ret.0.0)
(Sys.init)
@4000
D=A
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M // get the topmost value from the stack
@3
M=D // insert the value into this/that
@5000
D=A
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
@Sys.main$ret.0.0
D=A
@0
A=M
M=D
@0
M=M+1
@1
D=M
@0
A=M
M=D
@0
M=M+1
@2
D=M
@0
A=M
M=D
@0
M=M+1
@3
D=M
@0
A=M
M=D
@0
M=M+1
@4
D=M
@0
A=M
M=D
@0
M=M+1
@0  // put SP in RAM[ARG]
D=M
@2
M=D

@0 // get num of args 
D=A
@2 // subtract number of arguments from RAM[ARG]
M=M-D

@5 // subtract 5 (number of saved stack items) from RAM[ARG]
D=A
@2
M=M-D
@0
D=M
@1
M=D
@Sys.main
A;JMP
(Sys.main$ret.0.0)
@0
M=M-1
A=M
D=M
// M=0
@6
M=D
(LOOP)
@LOOP
0;JMP
(Sys.main)
@0
A=M
M=0
@0
M=M+1
@0
A=M
M=0
@0
M=M+1
@0
A=M
M=0
@0
M=M+1
@0
A=M
M=0
@0
M=M+1
@0
A=M
M=0
@0
M=M+1
@4001
D=A
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M // get the topmost value from the stack
@3
M=D // insert the value into this/that
@5001
D=A
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
@200
D=A
@0
A=M
M=D
@0
M=M+1
@1 // get the index
D=A
@1 // set the destination at this/that (will change this back later) 
M=M+D
@0  // goto topmost value on stack 
A=M-1 
D=M // set D reg to RAM[SP-1]
@1 // go to this/that
A=M
M=D // set RAM[THIS/THAT] to RAM[SP]
@1
D=A // set this/that back to what it was originally
@1
M=M-D
@40
D=A
@0
A=M
M=D
@0
M=M+1
@2 // get the index
D=A
@1 // set the destination at this/that (will change this back later) 
M=M+D
@0  // goto topmost value on stack 
A=M-1 
D=M // set D reg to RAM[SP-1]
@1 // go to this/that
A=M
M=D // set RAM[THIS/THAT] to RAM[SP]
@2
D=A // set this/that back to what it was originally
@1
M=M-D
@6
D=A
@0
A=M
M=D
@0
M=M+1
@3 // get the index
D=A
@1 // set the destination at this/that (will change this back later) 
M=M+D
@0  // goto topmost value on stack 
A=M-1 
D=M // set D reg to RAM[SP-1]
@1 // go to this/that
A=M
M=D // set RAM[THIS/THAT] to RAM[SP]
@3
D=A // set this/that back to what it was originally
@1
M=M-D
@123
D=A
@0
A=M
M=D
@0
M=M+1
@Sys.add12$ret.1.0
D=A
@0
A=M
M=D
@0
M=M+1
@1
D=M
@0
A=M
M=D
@0
M=M+1
@2
D=M
@0
A=M
M=D
@0
M=M+1
@3
D=M
@0
A=M
M=D
@0
M=M+1
@4
D=M
@0
A=M
M=D
@0
M=M+1
@0  // put SP in RAM[ARG]
D=M
@2
M=D

@1 // get num of args 
D=A
@2 // subtract number of arguments from RAM[ARG]
M=M-D

@5 // subtract 5 (number of saved stack items) from RAM[ARG]
D=A
@2
M=M-D
@0
D=M
@1
M=D
@Sys.add12
A;JMP
(Sys.add12$ret.1.0)
@0
M=M-1
A=M
D=M
// M=0
@5
M=D
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
@1
D=A
@1
A=D+M
D=M
@0
A=M
M=D
@0
M=M+1
@2
D=A
@1
A=D+M
D=M
@0
A=M
M=D
@0
M=M+1
@3
D=A
@1
A=D+M
D=M
@0
A=M
M=D
@0
M=M+1
@4
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
@0
A=M-1
D=M
@0
M=M-1
A=M-1
M=D+M
@0
A=M-1
D=M
@0
M=M-1
A=M-1
M=D+M
@0
A=M-1
D=M
@0
M=M-1
A=M-1
M=D+M
@1
D=M
@endframe_0
M=D
@5
D=A
@endframe_0
A=M-D  // goto RAM[endframe] - 5
D=M    // set D to *(RAM[endframe] - 5)
@return_0 
M=D    // set RAM[retAddr] = to *(RAM[endframe] - 5)
@0
A=M-1
D=M
@2
A=M
M=D
@2
D=M+1
@0
M=D
@endframe_0
A=M-1
D=M
@4
M=D
@2
D=A
@endframe_0
A=M-D
D=M
@3
M=D
@3
D=A
@endframe_0
A=M-D
D=M
@2
M=D
@4
D=A
@endframe_0
A=M-D
D=M
@1
M=D
@return_0
A=M
A;JMP
(Sys.add12)
@4002
D=A
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M // get the topmost value from the stack
@3
M=D // insert the value into this/that
@5002
D=A
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
@2
A=D+M
D=M
@0
A=M
M=D
@0
M=M+1
@12
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
@1
D=M
@endframe_1
M=D
@5
D=A
@endframe_1
A=M-D  // goto RAM[endframe] - 5
D=M    // set D to *(RAM[endframe] - 5)
@return_1 
M=D    // set RAM[retAddr] = to *(RAM[endframe] - 5)
@0
A=M-1
D=M
@2
A=M
M=D
@2
D=M+1
@0
M=D
@endframe_1
A=M-1
D=M
@4
M=D
@2
D=A
@endframe_1
A=M-D
D=M
@3
M=D
@3
D=A
@endframe_1
A=M-D
D=M
@2
M=D
@4
D=A
@endframe_1
A=M-D
D=M
@1
M=D
@return_1
A=M
A;JMP
