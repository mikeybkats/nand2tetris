@SCREEN
D=A
@screenAddress // @16
M=D

@i  // @17
M=0 

@j // @18
M=0

@KBD
D=M
@keyPress
M=D

(KEYLOOP)
@KBD
D=M
@keyPress
M=D

@KEYLOOP
D;JEQ

(LOOPBLACK)
    @keyPress
    D=M
    @KEYLOOP
    D;JEQ

    @i
    D=M // set i = 0

    @screenAddress
    A=M+D  // set screenAddress location to its present value + the value of i
    M=-1   // blacken the pixels of the present location

    @8192 // screen size is 8k 
    D=A   // set the D register to ram address (the value we need to shift over on the screen)

    @i
    M=M+1 // get the value from @17 and add one for incrementing our loop
    D=D-M // D = 32 - i

@LOOPBLACK
D; JGT // if D > 0 jump

@keyPress
D=M
@KEYLOOP
D;JEQ

(END)
@END
0;JMP
