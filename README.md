# A Toy Mips C Compiler

MCC is a toy C compiler written using `ply` https://github.com/dabeaz/ply 
MCC generates Mips assembly code that can be run with `Mars4.5` http://courses.missouristate.edu/kenvollmar/mars/download.htm 

Usage: `mcc code.c output.asm`
It can be run with Python 2 or Python 3.
Tested with: 
* Python 3.7.3
* Python 2.7.16

It consist of 2 python source code. 
First one is `mcc`. Mcc is lexer and parser that is written by ply. 
It generates abstract syntax tree of given C code.
Second one is `mipsGenerator.py`. 
This code parses abstract syntax tree and generates assembly code.

This project is written for CSE531 at Gebze Technical University.

## Features

Here is list of supported futures:

- [x] Global - Local variables 
- [x] Int - Char variables
- [x] Array decleration
- [x] While loops
- [x] Do - While loops
- [x] For loops
- [x] Binary operations ( +, -, *, /, &, |, ^, -, ~ )
- [x] If, if - else statements
- [x] Function definitions
- [x] Function arguments
- [x] return statement
- [x] continue, break statement
- [x] asm("asm op") 
- [x] printstr("some string") 
- [x] conditional operations ( ==, !=, >=, <=, >, < )
- [ ] Group of conditional operations ( 3 == 2 | 3 !=5 )

## Test Framework

There is a basic test system for evaluating correctnes of assembly output.
Some input output functionality is supported over both misp side and gcc side:
```
#include<stdio.h>
void printstr(char *str){ printf("%s", str); }
void print_int(int i){ printf("%d",i); }
void print_char(char c){ printf("%c",c); }
char read_char(){ char c; scanf("%c",&c); return c; }
int read_int(){ int i; scanf("%d",&i); return i; }
```

mips side:
```
void print_char(char a){ asm("li $v0 11"); asm("syscall"); }
void print_int(int a){ asm("li $v0 1"); asm("syscall"); }
int read_char(){ asm("li $v0 12"); asm("syscall"); }
int read_int(){ asm("li $v0 5"); asm("syscall"); }
```

some basic test codes:
* arr-dec.c
* arr-op.c
* arr-print.c
* binary-search.c
* binop2.c
* binop.c
* char.c
* conditions.c
* cont-break.c
* for.c
* functions.c
* if.c
* if-else.c
* int-dec.c
* merge-sort.c
* recursion.c
* return.c
* while.c

whic is compiled using both `gcc` and `mcc` and output compared between two

Test can be run with using `tests/test.sh`.
Please change `Mars4.5` location inside script.


