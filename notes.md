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
