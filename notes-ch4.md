## instructions 
### A instruction 
"The A-instruction is used to set the A register to a 15-bit value" - Book page 64

@value // A = value where value is either a constant or a symbol

### C instruction  
dest = comp; jump

**comp** = 0, 1, -1, D, A, !D, !A, -D, -A, D+1, A+1, D-1, A-1, D+A, D-A, A-D, D&A, D|A
M, !M, -M, M+1, M-1, D+M, D-M, M-D, D&M, D|M

**dest** = null, M, D, MD, A, AM, AD, AMD  

**jump** = null, JGT, JEQ, JGE, JLT, JNE, JLE, JMP  

JGT - jump greater than.  
JEQ - jump equal to.  
JGE - jump greater or equal to.  
JLT - jump less than.  
JNE - jump not equal to.  
JLE - jump less than or equal to.   
JMP - jump!  

### working with registers  
D: data register  
A: address / data register  
M: currently selected memory register // M = RAM[A] 

### how do i set the register? 
we can't do it directly. so this won't work:  
``` D = 10 ```

you have to set it indirectly:

```
@10 		// selects the address 10  
D = A 		// the D register equals A (the constant 10) 
```

it makes more sense to think of it like  D = A = @10  
you can't say `D = @10	// No Wrong!`   

### what about incrementing the register?

``` 
// D++	
D = D + 1
```

### setting the data to memory? 
```
// D = RAM[17]	
@17			// select the register		
D = M		//	set D to the value of the register  

// RAM[17] = D 	
@17 		// select the register 	
M = D 		// set the Ram to the value of the register  

// RAM[17] = 0	
@17  
M = 0

// RAM[17] = 10 	
@10  
D = A	// this actually acquires the constant 10. so D = 10
@17 	// this addresses the register 17
M = D 

// RAM[5] = 15
@15
D = A
@R5			// 	this addresses the register 5 and we can add an R to denote this
M = D 	

```

you can't say something like `M = 10` because you can't just use constants like this in machine code	

```
// RAM[3] = RAM[5]
@3  
D = M	
@5	
M = D

```

### Use Trace Tables 
Trace tables help you keep track of changes in the variables when designing a program

| Iterations    | 0   | 1    | 2   | 3   | ...  |
| ------------- |:---:| ----:| ---:| ---:| ---: |
| RAM[0]        | 3   |      |     |     |      |
| n             | 3   |      |     |     |      |
| i             | 1   | 2    | 3   | 4   | ...  |   
| sum           | 0   | 1    | 2   | 6   | ...  |

### Assigning directly to the A instruction  
you can make basic arithmetic operations and assign directly to the a register. here is an example of a loop:  

```
// for (i = 0; i < 100; i++){ 
//		arr[i] = -1 
//	}

// suppose that arr = 100 and n = 10

// arr = 100 
	@100 
	D=A 	// A is 100
	M=D 	// RAM[100] is 100

// n = 10 
	@10 
	D=A 	// A is 10
	M=D 	// RAM[10] is 10

// initialize i = 0 
	@i 		// first variable is always register 16
	M=0 	// RAM[16] = 0

// if (i == n) go to END
(LOOP)
	@i 		
	D=M 	// M is i (the second variable is register 17)
	@n 		// n is 17
	D=D-M 	// M is n. D is itself minus n
	@END
	D; JEQ	// if equal to 0 jump to end

// RAM[arr + i] = -1
	@arr
	D=M 	// arr = 100
	@i 		
	A=D+M 	// arr + i
	M=-1

// i++
	@i
	M=M+1

	@LOOP
	0; JMP  
	
(END) 
	@END
	0;JMP	
	
```  

### Built in symbols  
virtual registers:  

```
// let RAM[5] = 7
@7
D=A
@5
M=D
```

better style:

``` 
// let RAM[5] = 7 
@7  
D=A 

@R5  
M=D 
```  

### Terminating a program. 
create an infinite loop at the last memory location. 

```
@6  
0; JMP
```