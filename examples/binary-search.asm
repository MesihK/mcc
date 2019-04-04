# Generated from: binary-search.c
# Generated at: 2019-04-04 12:43:54.357163
.data
lbl8: .asciiz "Element is not present in array"
lbl9: .asciiz "Element is at:"
arr: .word 2, 3, 4, 10, 40
n: .word 0
.text
li $t0,5
sw $t0,n

main:
addi $sp, $sp, -12
sw $ra, 0($sp)
li $t2,10
sw $t2, 4($sp)
lw $t2,n
subi $t2, $t2, 1
lw $t3, 4($sp)
li $a0 0
add $a1 $zero, $t2
add $a2 $zero, $t3
jal binarySearch
sw $v0, 8($sp)
lw $t4, 8($sp)
li $t5,-1
bne $t4, $t5, lbl7
la $a0, lbl8
li $v0, 4
syscall
j lbl6
lbl7:
la $a0, lbl9
li $v0, 4
syscall
lw $t4, 8($sp)
add $a0 $zero, $t4
jal print_int
lbl6:
li $v0, 0
lw $ra, 0($sp)
addi $sp, $sp, 12
lw $ra, 0($sp)
addi $sp, $sp, 12
li $v0 10 #prgoram finished call terminate
syscall

binarySearch:
addi $sp, $sp, -20
sw $ra, 0($sp)
sw $zero, 4($sp)
sw $zero, 8($sp)
sw $zero, 12($sp)
sw $a0, 4($sp)
sw $a1, 8($sp)
sw $a2, 12($sp)
lbl5:
lw $t0, 4($sp)
lw $t1, 8($sp)
bgt $t0, $t1, lbl1
lw $t0, 4($sp)
lw $t1, 8($sp)
lw $t2, 4($sp)
sub $t3, $t1, $t2
li $t2,2
div $t1, $t3, $t2
add $t2, $t0, $t1
sw $t2, 16($sp)
la $t0, arr
lw $t1, 16($sp)
add $t1, $t1, $t1
add $t1, $t1, $t1
add $t1, $t0, $t1
lw $t1, ($t1)
lw $t2, 12($sp)
bne $t1, $t2, lbl2
lw $t1, 16($sp)
add $v0, $zero, $t1
lw $ra, 0($sp)
addi $sp, $sp, 20
jr $ra
lbl2:
la $t1, arr
lw $t2, 16($sp)
add $t2, $t2, $t2
add $t2, $t2, $t2
add $t2, $t1, $t2
lw $t2, ($t2)
lw $t3, 12($sp)
bge $t2, $t3, lbl4
lw $t2, 16($sp)
addi $t2, $t2, 1
sw $t2, 4($sp)
j lbl3
lbl4:
lw $t2, 16($sp)
subi $t2, $t2, 1
sw $t2, 8($sp)
lbl3:
j lbl5
lbl1:
li $v0, -1
lw $ra, 0($sp)
addi $sp, $sp, 20
jr $ra
lw $ra, 0($sp)
addi $sp, $sp, 20
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

