// int a
// int b
// int result = 0
// for(let i = 0; i < a; i++){
//     result = b + result
// }


// a = value of RAM[0]
@0
D=M
@a
M=D

// b = value of RAM[1]
@1
D=M
@a
M=D

// i = 0
@i
M=0

(LOOP) 
//  calc the result
    @a
    D=M
    @result
    M=D+M

// increment the counter
    @i
    D=M
    M=D+1

// test to see if the limit has been reached
    @i 
    D=M
    @a 
    D=D-M
    @LOOP
    D;JLT


(END)
@END
0;JMP