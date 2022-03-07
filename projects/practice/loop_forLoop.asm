// for ( int i = 0; i < n; i++){
//     arr[i] = -1
// }

// arr=100
@100
D=A
@arr
M=D

// n = 10
@10
D=A
@n
M=D

// initialize i = 0
@i
M=0

(loop)
    // if (i == n ) goto end
    @i
    D=M
    @n
    D=D-M

    @END
    D;JEQ // jump if equal to
    
    // RAM[arr + i] = -1
    @arr
    D=M
    @i
    A=D+M
    M=-1

    // i++
    @i
    M=M+1

    @loop
    0;JMP

(end)

    @end
    0;JMP