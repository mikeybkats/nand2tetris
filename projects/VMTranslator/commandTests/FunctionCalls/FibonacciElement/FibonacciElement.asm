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
@4
D=A
@0
A=M
M=D
@0
M=M+1
@Main.fibonacci$ret.1.1
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
@Main.fibonacci
A;JMP
(Main.fibonacci$ret.1.1)
(WHILE)
@WHILE
0;JMP
(Main.fibonacci)
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
D=M-D
M=-1
@LT_051cfe0e3240487fbca83a50
D;JLT
@0
A=M-1
M=0
(LT_051cfe0e3240487fbca83a50)
@0
M=M-1
A=M
D=M
@Main.fibonacci$IF_TRUE
D;JNE
@Main.fibonacci$IF_FALSE
0;JMP
(Main.fibonacci$IF_TRUE)
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
D=M // set RAM[local] into D reg
@endframe_2 
M=D // store RAM[local] into RAM[endframe] 
@5
D=A
@endframe_2
A=M-D  // goto RAM[endframe] - 5
D=M    // set D to *(RAM[endframe] - 5)
@return_2 
M=D    // set RAM[retAddr] = to *(RAM[endframe] - 5)
@0
A=M-1 // goto the SP-1 addr
D=M   // set D reg to SP-1
@2
A=M   // set the location of ARG to D reg
M=D 
@2
D=M+1
@0
M=D
@endframe_2
A=M-1
D=M
@4
M=D
@2
D=A
@endframe_2
A=M-D
D=M
@3
M=D
@3
D=A
@endframe_2
A=M-D
D=M
@2
M=D
@4
D=A
@endframe_2
A=M-D
D=M
@1
M=D
@return_2
A=M
A;JMP
(Main.fibonacci$IF_FALSE)
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
@Main.fibonacci$ret.1.3
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
@Main.fibonacci
A;JMP
(Main.fibonacci$ret.1.3)
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
@Main.fibonacci$ret.1.4
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
@Main.fibonacci
A;JMP
(Main.fibonacci$ret.1.4)
@0
A=M-1
D=M
@0
M=M-1
A=M-1
M=D+M
@1 
D=M // set RAM[local] into D reg
@endframe_5 
M=D // store RAM[local] into RAM[endframe] 
@5
D=A
@endframe_5
A=M-D  // goto RAM[endframe] - 5
D=M    // set D to *(RAM[endframe] - 5)
@return_5 
M=D    // set RAM[retAddr] = to *(RAM[endframe] - 5)
@0
A=M-1 // goto the SP-1 addr
D=M   // set D reg to SP-1
@2
A=M   // set the location of ARG to D reg
M=D 
@2
D=M+1
@0
M=D
@endframe_5
A=M-1
D=M
@4
M=D
@2
D=A
@endframe_5
A=M-D
D=M
@3
M=D
@3
D=A
@endframe_5
A=M-D
D=M
@2
M=D
@4
D=A
@endframe_5
A=M-D
D=M
@1
M=D
@return_5
A=M
A;JMP
