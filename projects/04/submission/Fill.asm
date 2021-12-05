// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
@SCREEN 
D=A
@screenAddress // Starts at 16384
M=D

@24576
D=A
@screenMax
M=D

@KBD  // on or off
D=M
@END
D;JEQ

(KEYPRESS)
  @i
  M=0

  (LOOP)
    @screenAddress // must remain constant
    D=M  // 16384

    @i  
    A=D+M // A=16384+M - M starts at 0
          // Must stop when the value of i = 8192
    M=-1  // RAM[i]=-1
    
    @i
    M=M+1 // M=M+1 incrementing by 1

    @KBD  // on or off
    D=M
    @SCREENWHITE
    D;JEQ

  @screenAddress //16384
  D=M
  @i
  D=D+M   // 16384 + count
  @screenMax
  D=M-D // 24576 - count 
  @LOOP
  D;JGT

@KBD
D=M
@KEYPRESS
D;JGT

// for (i = screenAddress; i < screenMax; i++){
(SCREENWHITE)
@i
M=0

  (LOOPWHITE)
    @screenAddress // must remain constant
    D=M  // 16384
    @i  
    A=D+M // A=16384+M - M starts at 0
          // Must stop when the value of i = 8192
    M=0   //RAM[i]=0
    
    @i
    M=M+1 // M=M+1 incrementing by 1

    @KBD  // on or off
    D=M
    @KEYPRESS
    D;JGT

  @screenAddress
  D=M
  @i
  D=D+M
  @screenMax
  D=M-D
  @LOOPWHITE
  D;JGT

(END)
  @KBD  // on or off
  D=M
  @KEYPRESS
  D;JGT
@END
0;JMP