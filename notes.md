# Unit 1.1 – boolean logic

## Boolean identities

#### _commutative laws_

(x AND y) = (y AND x)  
(x OR y) = (y OR x)

#### _associative laws_

(x AND (y AND z)) = ((x AND y) AND z)  
(x OR (y OR z)) = ((x OR y) OR z)

#### _distributive laws_

(x AND (y OR z)) = (x AND y) OR (x AND z)  
(x OR (y AND z)) = (x OR y) AND (x OR z)

#### _de Morgan laws_

NOT(x AND y) = NOT(x) AND NOT(y)
NOT(x OR y) = NOT(x) OR NOT(y)

## Boolean identity equivalence

each line is equivalent to the others

| law             | rule                                |
| --------------- | ----------------------------------- |
| De Morgan law   | NOT(NOT(x) AND NOT(x OR y))         |
| Associative law | NOT(NOT(x) AND (NOT(x) AND NOT(y))) |
| Idempotence     | NOT((NOT(x) AND NOT(x)) AND NOT(y)) |
| De Morgan       | NOT(NOT(x) OR NOT(NOT(y)))          |
| Double Negation | NOT(NOT(x) OR NOT(NOT(y)))          |
|                 | x or y                              |

# chapter 11

| RAM addresses | Usage                     |
| ------------- | ------------------------- |
| 0-15          | sixteen virtual registers |
| 16 - 255      | Static variables          |
| 256 - 2047    | Stack                     |
| 2048 - 16383  | Heap                      |
| 16384 - 24575 | Memory I/O                |
| 24575 - 32767 | Unused memory             |

| Register   | Name | Usage                     |
| ---------- | ---- | ------------------------- |
| RAM[0]     | SP   | Stack Pointer             |
| RAM[1]     | LCL  | local segment             |
| RAM[2]     | ARG  | current argument segment  |
| RAM[3]     | THIS | this segment              |
| RAM[4]     | THAT | that segment              |
| RAM[5-12]  | --   | temp segment              |
| RAM[13-15] | --   | general purpose registers |

## Handling Arrays

_how does THIS (RAM[3]) and that (RAM[4]) work?_

| -                    | this                                        | that                                       |
| -------------------- | ------------------------------------------- | ------------------------------------------ |
| VM Use:              | represents the values of the current object | represents the values of the current array |
| pointer base address | THIS                                        | THAT                                       |
| how to set           | pop pointer 0 (sets THIS)                   | pop pointer 1 (sets THAT)                  |

### array logic

_How to set `arr[2] = 17`?_

// pseudo code

```
push arr[2] // base address
push 2 // offset
add
pop pointer 1
push 17
pop that 0
```

_What about set `a[i] = b[j]`?_

```
push a
push i
add
push b
push j
add
pop pointer 1 // pop the result of b + j to that segment RAM[4]
push temp 0
pop that 0
```
