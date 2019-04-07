# Generated from: hanoi.c
# Generated at: 2019-04-07 11:38:23.390561
.data
lbl2: .asciiz "\n Move disk 1 from rod: "
lbl3: .asciiz " to rod: "
lbl4: .asciiz "\n Move disk: "
lbl5: .asciiz " from rod: "
lbl6: .asciiz " to rod: "
.text

main:
addi $sp, $sp, -8
sw $ra, 0($sp)
li $t0,4
sw $t0, 4($sp)
lw $t0, 4($sp)
add $a0 $zero, $t0
li $a1 65
li $a2 67
li $a3 66
jal towerOfHanoi
li $v0, 0
lw $ra, 0($sp)
addi $sp, $sp, 8
lw $ra, 0($sp)
addi $sp, $sp, 8
li $v0 10 #prgoram finished call terminate
syscall

towerOfHanoi:
addi $sp, $sp, -20
sw $ra, 0($sp)
sw $zero, 4($sp)
sw $zero, 8($sp)
sw $zero, 12($sp)
sw $zero, 16($sp)
sw $a0, 4($sp)
sw $a1, 8($sp)
sw $a2, 12($sp)
sw $a3, 16($sp)
lw $t0, 4($sp)
li $t1,1
bne $t0, $t1, lbl1
la $a0, lbl2
li $v0, 4
syscall
lw $t0, 8($sp)
add $a0 $zero, $t0
jal print_char
la $a0, lbl3
li $v0, 4
syscall
lw $t0, 12($sp)
add $a0 $zero, $t0
jal print_char
lw $ra, 0($sp)
addi $sp, $sp, 20
jr $ra
lbl1:
lw $t0, 4($sp)
subi $t0, $t0, 1
lw $t1, 8($sp)
lw $t2, 16($sp)
lw $t3, 12($sp)
add $a0 $zero, $t0
add $a1 $zero, $t1
add $a2 $zero, $t2
add $a3 $zero, $t3
jal towerOfHanoi
la $a0, lbl4
li $v0, 4
syscall
lw $t0, 4($sp)
add $a0 $zero, $t0
jal print_int
la $a0, lbl5
li $v0, 4
syscall
lw $t0, 8($sp)
add $a0 $zero, $t0
jal print_char
la $a0, lbl6
li $v0, 4
syscall
lw $t0, 12($sp)
add $a0 $zero, $t0
jal print_char
lw $t0, 4($sp)
subi $t0, $t0, 1
lw $t1, 16($sp)
lw $t2, 12($sp)
lw $t3, 8($sp)
add $a0 $zero, $t0
add $a1 $zero, $t1
add $a2 $zero, $t2
add $a3 $zero, $t3
jal towerOfHanoi
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

