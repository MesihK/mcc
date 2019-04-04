# Generated from: merge-sort.c
# Generated at: 2019-04-04 12:43:47.920545
.data
lbl16: .asciiz " "
lbl18: .asciiz "\n"
lbl19: .asciiz "Given array is \n"
lbl20: .asciiz "\nSorted array is \n"
arr: .word 12, 11, 13, 5, 6, 7
arr_size: .word 0
.text
li $t0,6
sw $t0,arr_size

main:
addi $sp, $sp, -4
sw $ra, 0($sp)
la $a0, lbl19
li $v0, 4
syscall
jal printArray
lw $s7,arr_size
subi $s7, $s7, 1
li $a0 0
add $a1 $zero, $s7
jal mergeSort
la $a0, lbl20
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

merge:
addi $sp, $sp, -116
sw $ra, 0($sp)
sw $zero, 4($sp)
sw $zero, 8($sp)
sw $zero, 12($sp)
sw $a0, 4($sp)
sw $a1, 8($sp)
sw $a2, 12($sp)
sw $zero, 16($sp)
sw $zero, 20($sp)
sw $zero, 24($sp)
lw $t0, 8($sp)
lw $t1, 4($sp)
sub $t2, $t0, $t1
addi $t2, $t2, 1
sw $t2, 28($sp)
lw $t0, 12($sp)
lw $t1, 8($sp)
sub $t2, $t0, $t1
sw $t2, 32($sp)
sw $zero, 36($sp)
sw $zero, 40($sp)
sw $zero, 44($sp)
sw $zero, 48($sp)
sw $zero, 52($sp)
sw $zero, 56($sp)
sw $zero, 60($sp)
sw $zero, 64($sp)
sw $zero, 68($sp)
sw $zero, 72($sp)
sw $zero, 76($sp)
sw $zero, 80($sp)
sw $zero, 84($sp)
sw $zero, 88($sp)
sw $zero, 92($sp)
sw $zero, 96($sp)
sw $zero, 100($sp)
sw $zero, 104($sp)
sw $zero, 108($sp)
sw $zero, 112($sp)
li $t0,0
sw $t0, 16($sp)
lbl2:
lw $t0, 16($sp)
lw $t1, 28($sp)
bge $t0, $t1, lbl1
lw $t0, 16($sp)
add $t0, $t0, $t0
add $t0, $t0, $t0
add $t0, $sp, $t0
addi $t0, $t0,36
la $t1, arr
lw $t2, 4($sp)
lw $t3, 16($sp)
add $t4, $t2, $t3
add $t4, $t4, $t4
add $t4, $t4, $t4
add $t4, $t1, $t4
lw $t4, ($t4)
sw $t4, ($t0)
lw $t0, 16($sp)
addi $t0, $t0, 1
sw $t0, 16($sp)
j lbl2
lbl1:
li $t0,0
sw $t0, 20($sp)
lbl4:
lw $t0, 20($sp)
lw $t2, 32($sp)
bge $t0, $t2, lbl3
lw $t0, 20($sp)
add $t0, $t0, $t0
add $t0, $t0, $t0
add $t0, $sp, $t0
addi $t0, $t0,76
la $t2, arr
lw $t3, 8($sp)
addi $t3, $t3, 1
lw $t4, 20($sp)
add $t5, $t3, $t4
add $t5, $t5, $t5
add $t5, $t5, $t5
add $t5, $t2, $t5
lw $t5, ($t5)
sw $t5, ($t0)
lw $t0, 20($sp)
addi $t0, $t0, 1
sw $t0, 20($sp)
j lbl4
lbl3:
li $t0,0
sw $t0, 16($sp)
li $t0,0
sw $t0, 20($sp)
lw $t0, 4($sp)
sw $t0, 24($sp)
lbl9:
lw $t0, 16($sp)
lw $t3, 28($sp)
bge $t0, $t3, lbl5
lw $t0, 20($sp)
lw $t3, 32($sp)
blt $t0, $t3, lbl6
j lbl5
lbl6:
lw $t0, 16($sp)
add $t0, $t0, $t0
add $t0, $t0, $t0
add $t0, $sp, $t0
addi $t0, $t0,36
lw $t0, ($t0)
lw $t3, 20($sp)
add $t3, $t3, $t3
add $t3, $t3, $t3
add $t3, $sp, $t3
addi $t3, $t3,76
lw $t3, ($t3)
bgt $t0, $t3, lbl8
la $t0, arr
lw $t3, 24($sp)
add $t3, $t3, $t3
add $t3, $t3, $t3
add $t3, $t0, $t3
lw $t4, 16($sp)
add $t4, $t4, $t4
add $t4, $t4, $t4
add $t4, $sp, $t4
addi $t4, $t4,36
lw $t4, ($t4)
sw $t4, ($t3)
lw $t3, 16($sp)
addi $t3, $t3, 1
sw $t3, 16($sp)
j lbl7
lbl8:
la $t3, arr
lw $t4, 24($sp)
add $t4, $t4, $t4
add $t4, $t4, $t4
add $t4, $t3, $t4
lw $t5, 20($sp)
add $t5, $t5, $t5
add $t5, $t5, $t5
add $t5, $sp, $t5
addi $t5, $t5,76
lw $t5, ($t5)
sw $t5, ($t4)
lw $t4, 20($sp)
addi $t4, $t4, 1
sw $t4, 20($sp)
lbl7:
lw $t4, 24($sp)
addi $t4, $t4, 1
sw $t4, 24($sp)
j lbl9
lbl5:
lbl11:
lw $t4, 16($sp)
lw $t5, 28($sp)
bge $t4, $t5, lbl10
la $t4, arr
lw $t5, 24($sp)
add $t5, $t5, $t5
add $t5, $t5, $t5
add $t5, $t4, $t5
lw $t6, 16($sp)
add $t6, $t6, $t6
add $t6, $t6, $t6
add $t6, $sp, $t6
addi $t6, $t6,36
lw $t6, ($t6)
sw $t6, ($t5)
lw $t5, 16($sp)
addi $t5, $t5, 1
sw $t5, 16($sp)
lw $t5, 24($sp)
addi $t5, $t5, 1
sw $t5, 24($sp)
j lbl11
lbl10:
lbl13:
lw $t5, 20($sp)
lw $t6, 32($sp)
bge $t5, $t6, lbl12
la $t5, arr
lw $t6, 24($sp)
add $t6, $t6, $t6
add $t6, $t6, $t6
add $t6, $t5, $t6
lw $t7, 20($sp)
add $t7, $t7, $t7
add $t7, $t7, $t7
add $t7, $sp, $t7
addi $t7, $t7,76
lw $t7, ($t7)
sw $t7, ($t6)
lw $t6, 20($sp)
addi $t6, $t6, 1
sw $t6, 20($sp)
lw $t6, 24($sp)
addi $t6, $t6, 1
sw $t6, 24($sp)
j lbl13
lbl12:
lw $ra, 0($sp)
addi $sp, $sp, 116
jr $ra

mergeSort:
addi $sp, $sp, -16
sw $ra, 0($sp)
sw $zero, 4($sp)
sw $zero, 8($sp)
sw $a0, 4($sp)
sw $a1, 8($sp)
lw $t6, 4($sp)
lw $t7, 8($sp)
bge $t6, $t7, lbl14
lw $t6, 4($sp)
lw $t7, 8($sp)
lw $s0, 4($sp)
sub $s1, $t7, $s0
li $s0,2
div $t7, $s1, $s0
add $s0, $t6, $t7
sw $s0, 12($sp)
lw $t6, 4($sp)
lw $t7, 12($sp)
add $a0 $zero, $t6
add $a1 $zero, $t7
jal mergeSort
lw $s0, 12($sp)
addi $s0, $s0, 1
lw $s1, 8($sp)
add $a0 $zero, $s0
add $a1 $zero, $s1
jal mergeSort
lw $s2, 4($sp)
lw $s3, 12($sp)
lw $s4, 8($sp)
add $a0 $zero, $s2
add $a1 $zero, $s3
add $a2 $zero, $s4
jal merge
lbl14:
lw $ra, 0($sp)
addi $sp, $sp, 16
jr $ra

printArray:
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $zero, 4($sp)
li $s5,0
sw $s5, 4($sp)
lbl17:
lw $s5, 4($sp)
lw $s6,arr_size
bge $s5, $s6, lbl15
la $s5, arr
lw $s6, 4($sp)
add $s6, $s6, $s6
add $s6, $s6, $s6
add $s6, $s5, $s6
lw $s6, ($s6)
add $a0 $zero, $s6
jal print_int
la $a0, lbl16
li $v0, 4
syscall
lw $s5, 4($sp)
addi $s5, $s5, 1
sw $s5, 4($sp)
j lbl17
lbl15:
la $a0, lbl18
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

