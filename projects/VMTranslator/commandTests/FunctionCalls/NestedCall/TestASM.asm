@5 // return address
D=A

@myLabel // puts label in 16
M=D // push return address to label
@0
M=M+1
@myLabel // jumps to 16
0;JMP
@0
M=1
@0
M=M+1
(label)
@0
M=1
@0
M=M+1
