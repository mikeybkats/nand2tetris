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
