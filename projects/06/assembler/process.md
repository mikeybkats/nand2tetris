## initialization

- construct an empty symbol table
- add the predefined symbols to the table

## first pass

- scan the entire program
- for each 'instruction' of the form (xxx):
	- add the pair (xxx, address) and the instruction to the table where address is the number of the instruction

## second pass

- set _n_ to 16
- scan the program
	- for each instruction:
		- if the instruction is @symbol look up the symbol in the table
			- if found, use the value to complete the instruction translation
			- if not found, add the symbol _n_ to the table
			- use n to complete the instruction translation
			- n++
		- if the instruction is a C instruction, translate it
		- write translated instruction to output file