# Generated from: recursion.c
# Generated at: 2019-04-04 12:44:06.958328
.data
.text

main:
addi $sp, $sp, -8
sw $ra, 0($sp)
li $t1,5
sw $t1, 4($sp)
lw $t1, 4($sp)
add $a0 $zero, $t1
jal topla
add $a0 $zero, $v0
jal print_int
lw $ra, 0($sp)
addi $sp, $sp, 8
li $v0 10 #prgoram finished call terminate
syscall

topla:
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $zero, 4($sp)
sw $a0, 4($sp)
lw $t0, 4($sp)
li $t1,0
bgt $t0, $t1, lbl2
li $v0, 0
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
j lbl1
lbl2:
lw $t0, 4($sp)
subi $t0, $t0, 1
add $a0 $zero, $t0
jal topla
lw $t1, 4($sp)
add $t2, $v0, $t1
add $v0, $zero, $t2
lw $ra, 0($sp)
addi $sp, $sp, 8
jr $ra
lbl1:
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

