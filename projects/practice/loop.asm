// Program: loop.asm  
// uses the input of RAM[0] as the number of times it loops 
// verify that it loops that number of times by counting up from zero into RAM[16]
// while count is not equal to R0 add one

(ADDONE)
  @R0
  D=M
  @count  // RAM[16]
  M=M+1   // RAM[16] = RAM[16] + 1

D=D-M

@END
D;JEQ   // jump to end if RAM[0] - RAM[16] === 0

@ADDONE
D;JNE  // jump to addone if RAM[0] - RAM[16] !== 0 

(END)
  @END
  0;JMP
  
