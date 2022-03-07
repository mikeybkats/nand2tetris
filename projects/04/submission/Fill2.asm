// Application turns the screen black with no control
// 256 rows
// 512 pixels per row
// each ram location targets 16 pixels 
// screen starts at RAM[16384]
// 16384 + 8192 = 24576 (end of screen in ram)

@SCREEN // @16384
D=A
@screenStart // @16
M=D            // @16 = 16384

@24576
D=A
@screenEnd
M=D

(LOOP)
    @screenStart
    A=M
    M=-1
    
    @screenStart
    M=M+1

    @screenEnd
    D=M
    @screenStart
    D=D-M

    @LOOP
    D;JGT

(END)
    @END
    0;JMP