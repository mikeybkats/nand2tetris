// sum1ToN.asm
// Computes RAM[1] = 1 + 2 + 3 + ... n
// Usage: Put number (n) in RAM[0]

// n = 0
// i = 1
// sum = 0
// 
// LOOP: 
//     if i < n goto STOP
//     sum = sum + i
//     i = i + 1
//     goto LOOP
// STOP:
//     R1 = sum

@R0
D=M
@n
D=M
@i
M=1
@sum
M=0

(LOOP)
@i
D=M
@n 
D=D-M
@STOP
D;JGT // if i > n goto STOP

@sum
D=M
@i
D=D+M
@sum
M=D
@i
M=M+1
@LOOP
0;JMP

(STOP)
@sum
D=M
@R1
M=D

(END)
@END
0;JMP