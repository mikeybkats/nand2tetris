@EQ
M=1
@0
A=M

@NEQ
M=-1
@0
A=M
@10
D=A
@0
A=M
M=D
@0
M=M+1
@10
D=A
@0
A=M
M=D
@0
M=M+1
@0
A=M-1
D=M
M=0
@0
M=M-1
A=M-1
D=M-D    
@EQ
D;JEQ
@NEQ
D;JMP
@11
D=A
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
M=0
@0
M=M-1
A=M-1
D=M-D    
@EQ
D;JEQ
@NEQ
D;JMP