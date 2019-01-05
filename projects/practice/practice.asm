// adds up two numbers
// M is the ram 
// D is the registorM
// The Hack machine language recognizes three 16-bit registers:*/
//• D: used to store data*/
//• A: used to store data / address the memory*/
//• M: represents the currently addressed memory register: M = RAM[A]*/

@0 
D=M // D = RAM[0]

@1
//D=D+M // RAM[1] = RAM[0] + RAM[1]
D=M

@2 // RAM[2] = 
M=D

@3
D=M

@4
M=D

