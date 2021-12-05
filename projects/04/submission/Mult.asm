// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// int a
// int b
// int c = 0
// 
// for(i=0; i<b; i++){
//   c = a+c
// }
// 
// i    a   b   c
// 0    4   5   4
// 1            8
// 2            12
// 3            16
// 4            20

@i
M=0
@R2
M=0

@R0
D=M
@END
D;JEQ

@R1
D=M
@END
D;JEQ

(LOOP)
  @R0
  D=M
  @R2
  M=M+D // calculate result 
  @i
  M=M+1 // @16 count 

  @R1
  D=M
  @i
  D=D-M // if @16 - R1 is greater than zero loop

@LOOP
D;JGT

(END)
@END
0;JMP
