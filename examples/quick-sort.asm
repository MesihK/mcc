# Generated from: quick-sort.c
# Generated at: 2019-04-04 12:44:01.576688
.data
lbl6: .asciiz " "
lbl8: .asciiz "\n"
lbl9: .asciiz "Sorted array: "
arr: .word 10, 7, 8, 9, 1, 5
n: .word 0
.text
li $t0,6
sw $t0,n

main:
addi $sp, $sp, -4
sw $ra, 0($sp)
lw $k0,n
subi $k0, $k0, 1
li $a0 0
add $a1 $zero, $k0
jal quickSort
la $a0, lbl9
li $v0, 4
syscall
jal printArray
li $v0, 0
lw $ra, 0($sp)
addi $sp, $sp, 4
lw $ra, 0($sp)
addi $sp, $sp, 4
li $v0 10 #prgoram finished call terminate
syscall

swap:
addi $sp, $sp, -16
sw $ra, 0($sp)
sw $zero, 4($sp)
sw $zero, 8($sp)
sw $a0, 4($sp)
sw $a1, 8($sp)
lw $t0, 4($sp)
lw $t0, ($t0)
sw $t0, 12($sp)
lw $t0, 8($sp)
lw $t0, ($t0)
lw $t1, 4($sp)
sw $t0, ($t1)
lw $t0, 12($sp)
lw $t1, 8($sp)
sw $t0, ($t1)
lw $ra, 0($sp)
addi $sp, $sp, 16
jr $ra

partition:
addi $sp, $sp, -24
sw $ra, 0($sp)
sw $zero, 4($sp)
sw $zero, 8($sp)
sw $a0, 4($sp)
sw $a1, 8($sp)
la $t0, arr
lw $t1, 8($sp)
add $t1, $t1, $t1
add $t1, $t1, $t1
add $t1, $t0, $t1
lw $t1, ($t1)
sw $t1, 12($sp)
lw $t1, 4($sp)
subi $t1, $t1, 1
sw $t1, 16($sp)
li $t1,0
sw $t1, 20($sp)
lw $t1, 4($sp)
sw $t1, 20($sp)
lbl3:
lw $t1, 20($sp)
lw $t2, 8($sp)
subi $t2, $t2, 1
bgt $t1, $t2, lbl1
la $t1, arr
lw $t2, 20($sp)
add $t2, $t2, $t2
add $t2, $t2, $t2
add $t2, $t1, $t2
lw $t2, ($t2)
lw $t3, 12($sp)
bgt $t2, $t3, lbl2
lw $t2, 16($sp)
addi $t2, $t2, 1
sw $t2, 16($sp)
la $t2, arr
lw $t3, 16($sp)
add $t3, $t3, $t3
add $t3, $t3, $t3
add $t3, $t2, $t3
la $t4, arr
lw $t5, 20($sp)
add $t5, $t5, $t5
add $t5, $t5, $t5
add $t5, $t4, $t5
add $a0 $zero, $t3
add $a1 $zero, $t5
jal swap
lbl2:
lw $t1, 20($sp)
addi $t1, $t1, 1
sw $t1, 20($sp)
j lbl3
lbl1:
la $t6, arr
lw $t7, 16($sp)
addi $t7, $t7, 1
add $t7, $t7, $t7
add $t7, $t7, $t7
add $t7, $t6, $t7
la $s0, arr
lw $s1, 8($sp)
add $s1, $s1, $s1
add $s1, $s1, $s1
add $s1, $s0, $s1
add $a0 $zero, $t7
add $a1 $zero, $s1
jal swap
lw $s2, 16($sp)
addi $s2, $s2, 1
add $v0, $zero, $s2
lw $ra, 0($sp)
addi $sp, $sp, 24
jr $ra
lw $ra, 0($sp)
addi $sp, $sp, 24
jr $ra

quickSort:
addi $sp, $sp, -16
sw $ra, 0($sp)
sw $zero, 4($sp)
sw $zero, 8($sp)
sw $a0, 4($sp)
sw $a1, 8($sp)
lw $s2, 4($sp)
lw $s3, 8($sp)
bge $s2, $s3, lbl4
li $s2,0
sw $s2, 12($sp)
lw $s2, 4($sp)
lw $s3, 8($sp)
add $a0 $zero, $s2
add $a1 $zero, $s3
jal partition
sw $v0, 12($sp)
lw $s4, 4($sp)
lw $s5, 12($sp)
subi $s5, $s5, 1
add $a0 $zero, $s4
add $a1 $zero, $s5
jal quickSort
lw $s6, 12($sp)
addi $s6, $s6, 1
lw $s7, 8($sp)
add $a0 $zero, $s6
add $a1 $zero, $s7
jal quickSort
lbl4:
lw $ra, 0($sp)
addi $sp, $sp, 16
jr $ra

printArray:
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $zero, 4($sp)
li $t8,0
sw $t8, 4($sp)
lbl7:
lw $t8, 4($sp)
lw $t9,n
bge $t8, $t9, lbl5
la $t8, arr
lw $t9, 4($sp)
add $t9, $t9, $t9
add $t9, $t9, $t9
add $t9, $t8, $t9
lw $t9, ($t9)
add $a0 $zero, $t9
jal print_int
la $a0, lbl6
li $v0, 4
syscall
lw $t8, 4($sp)
addi $t8, $t8, 1
sw $t8, 4($sp)
j lbl7
lbl5:
la $a0, lbl8
li $v0, 4
syscall
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra

print_char:
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $zero, 4($sp)
sw $a0, 4($sp)
li $v0 11
syscall
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra

print_int:
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $zero, 4($sp)
sw $a0, 4($sp)
li $v0 1
syscall
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra

read_char:
addi $sp, $sp, -4
sw $ra, 0($sp)
li $v0 12
syscall
lw $ra, 0($sp)
addi $sp, $sp, 4
jr $ra

read_int:
addi $sp, $sp, -4
sw $ra, 0($sp)
li $v0 5
syscall
lw $ra, 0($sp)
addi $sp, $sp, 4
jr $ra

