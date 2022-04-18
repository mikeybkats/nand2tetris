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
@6
D=A
@0
A=M
M=D
@0
M=M+1
@8
D=A
@0
A=M
M=D
@0
M=M+1
@Class1.set$ret.2.1
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

@2 // get num of args 
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
@Class1.set
A;JMP
(Class1.set$ret.2.1)
@0
M=M-1
A=M
D=M
// M=0
@5
M=D
@23
D=A
@0
A=M
M=D
@0
M=M+1
@15
D=A
@0
A=M
M=D
@0
M=M+1
@Class2.set$ret.2.2
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

@2 // get num of args 
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
@Class2.set
A;JMP
(Class2.set$ret.2.2)
@0
M=M-1
A=M
D=M
// M=0
@5
M=D
@Class1.get$ret.0.3
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
@Class1.get
A;JMP
(Class1.get$ret.0.3)
@Class2.get$ret.0.4
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
@Class2.get
A;JMP
(Class2.get$ret.0.4)
(WHILE)
@WHILE
0;JMP
(Class1.set)
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
A=M-1
D=M
@Class1.vm.0
M=D
@0
M=M-1
// A=M
// M=0
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
A=M-1
D=M
@Class1.vm.1
M=D
@0
M=M-1
// A=M
// M=0
@0
D=A
@0
A=M
M=D
@0
M=M+1
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
(Class1.get)
@Class1.vm.0
D=M
@0
A=M
M=D
@0
M=M+1
@Class1.vm.1
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
M=M-D
@1 
D=M // set RAM[local] into D reg
@endframe_6 
M=D // store RAM[local] into RAM[endframe] 
@5
D=A
@endframe_6
A=M-D  // goto RAM[endframe] - 5
D=M    // set D to *(RAM[endframe] - 5)
@return_6 
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
@endframe_6
A=M-1
D=M
@4
M=D
@2
D=A
@endframe_6
A=M-D
D=M
@3
M=D
@3
D=A
@endframe_6
A=M-D
D=M
@2
M=D
@4
D=A
@endframe_6
A=M-D
D=M
@1
M=D
@return_6
A=M
A;JMP
(Class2.set)
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
A=M-1
D=M
@Class2.vm.0
M=D
@0
M=M-1
// A=M
// M=0
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
A=M-1
D=M
@Class2.vm.1
M=D
@0
M=M-1
// A=M
// M=0
@0
D=A
@0
A=M
M=D
@0
M=M+1
@1 
D=M // set RAM[local] into D reg
@endframe_7 
M=D // store RAM[local] into RAM[endframe] 
@5
D=A
@endframe_7
A=M-D  // goto RAM[endframe] - 5
D=M    // set D to *(RAM[endframe] - 5)
@return_7 
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
@endframe_7
A=M-1
D=M
@4
M=D
@2
D=A
@endframe_7
A=M-D
D=M
@3
M=D
@3
D=A
@endframe_7
A=M-D
D=M
@2
M=D
@4
D=A
@endframe_7
A=M-D
D=M
@1
M=D
@return_7
A=M
A;JMP
(Class2.get)
@Class2.vm.0
D=M
@0
A=M
M=D
@0
M=M+1
@Class2.vm.1
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
M=M-D
@1 
D=M // set RAM[local] into D reg
@endframe_8 
M=D // store RAM[local] into RAM[endframe] 
@5
D=A
@endframe_8
A=M-D  // goto RAM[endframe] - 5
D=M    // set D to *(RAM[endframe] - 5)
@return_8 
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
@endframe_8
A=M-1
D=M
@4
M=D
@2
D=A
@endframe_8
A=M-D
D=M
@3
M=D
@3
D=A
@endframe_8
A=M-D
D=M
@2
M=D
@4
D=A
@endframe_8
A=M-D
D=M
@1
M=D
@return_8
A=M
A;JMP
