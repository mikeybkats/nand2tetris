@R0
D=M
@n    // n = RAM[16]
M=D   // n = R0
@i    // i = RAM[17]
M=1   // i = 1
@sum  // sum = RAM[18]
M=0   // sum = 0

(loop)
  @i
  D=M   // D = RAM[17] 
  @n    
  D=D-M // D = RAM[17] - RAM[16] 
  @STOP
  D; JGT  // if i > n jump to stop


