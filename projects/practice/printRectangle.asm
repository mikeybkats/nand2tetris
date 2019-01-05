// Program: Rectangle.asm
// Draws a filled Rectangle at the screens top left corner
// The rectangles width is 16 pixels, and its height is RAM[0]  
// Usage: put a non-negative number (rectangle's height) in RAM[0]

// for (i=0; i<n; i++) {
//   // draw 16 black pixels at the
//   // beginning of row i
// }

// addr = SCREEN
// n = RAM[0]
// i = 0
// 
// LOOP:
//   if i > n goto END
//   RAM[addr] = -1 // 1111 1111 1111 1111
//   // advances to the next row
//   addr = addr + 32
//   i = i + 1
//   goto LOOP
// 
// END: 
//   goto END

  @SCREEN
  D=A
  @addr // addr = 16384 (screens base address)
  M=D

  @0
  D=M
  @n
  M=D // n = RAM[0]

  @i
  M=0

(VERTICALLOOP)
  @i
  D=M // RAM[0]
  @n
  D=D-M
  @END
  D;JGT 

  @addr
  A=M   // A=value of @addr or A=RAM[addr]
  M=-1

  @32
  D=A
  @addr
  M=M+D

  @i
  M=M+1 // Increments the loop

  @VERTICALLOOP
  0; JMP

(END)
  @END
  0;JMP









