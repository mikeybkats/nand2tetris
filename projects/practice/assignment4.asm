// while any key is pressed make screen black
// while no key is pressed make the screen white
// 
// screenAddress = SCREEN 
// screenMax = 24576
// 
// keyPress = bool
// 
// while (keyPress){
//   for (i = screenAddress; i < screenMax; i++){
//      RAM[i] = -1
//   }
// }
// 
// for (i = screenAddress; i < screenMax; i++){
//   RAM[i] = 0
// }
// 
// while (0 == 0){
//   // look for keyPress
//   // if keyPress run keyPressLoop
// }

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
