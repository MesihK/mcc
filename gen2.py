ast = ('unit', ('unit', ('unit', ('decli', 'int', 'i', 0), ('fun', 'int', 'main', ((('decli', 'int', 'a', ('binop', '*', ('id', 'i'), 3)), ('decli', 'int', 'b', 4)), ('asign', 'i', ('binop', '+', ('id', 'a'), ('id', 'b')))))), ('fun', 'int', 'test', (('decli', 'int', 'c'), ('decli', 'int', 'd')))), ('fun', 'int', 't2', ('asign', 'i', 3)))



#TODO
# *OK - function call
# *OK - conditional expressions
# *OK - if
# *OK - if - else
# *OK - while
# *OK - local variables
# *OK - gloabal variables
# arrays
# char variable
# function recursion
# function arguments
# function return
# asm("add $t0, $t1, $t2")

registers = {
    #'at':0, 'v0':0, 'v1':0,
    #'a0':0, 'a1':0, 'a2':0, 'a3':0,
    't0':0, 't1':0, 't2':0, 't3':0, 't4':0, 't5':0, 't6':0, 't7':0,
    's0':0, 's1':0, 's2':0, 's3':0, 's4':0, 's5':0, 's6':0, 's7':0,
    't8':0, 't9':0, 't10':0,
    #'k0':0, 'k1':0,
    #'gp':0, 'sp':0, 'fp':0, 'ra':0
}


def alloc_reg():
    for reg in registers:
        if(registers[reg] == 0):
            registers[reg] = 1
            return reg

def dealloc_reg(r):
    if registers[r] != 1: print('register', r, 'is not allocated!')
    registers[r] = 0

def is_reg(r):
    if r in registers:
        return True
    else:
        return False

lbl_cnt = 0
def gen_lbl():
    global lbl_cnt
    lbl_cnt = lbl_cnt + 1
    return 'lbl'+str(lbl_cnt)

def gen_condop(op, p1, p2):
    lbl_exit = gen_lbl()
    ins = list()
    if is_reg(p1): r2 = p1
    else :
        r2 = alloc_reg()
        ins.append('li $'+r2+','+str(p1))

    if is_reg(p2): r3 = p2
    else :
        r3 = alloc_reg()
        ins.append('li $'+r3+','+str(p2))

    if op == '==':
        ins.append('bne $'+r2+', $'+r3+', '+lbl_exit)
    elif op == '!=':
        ins.append('beq $'+r2+', $'+r3+', '+lbl_exit)
    elif op == '<':
        ins.append('bge $'+r2+', $'+r3+', '+lbl_exit)
    elif op == '>':
        ins.append('ble $'+r2+', $'+r3+', '+lbl_exit)
    elif op == '<=':
        ins.append('bgt $'+r2+', $'+r3+', '+lbl_exit)
    elif op == '>=':
        ins.append('ble $'+r2+', $'+r3+', '+lbl_exit)

    dealloc_reg(r2)
    dealloc_reg(r3)
    return lbl_exit, ins

def gen_binop(op, p1, p2):
    ins = list()
    r1 = alloc_reg()
    if is_reg(p1): r2 = p1
    else :
        r2 = alloc_reg()
        ins.append('li $'+r2+','+str(p1))

    if is_reg(p2): r3 = p2
    else :
        r3 = alloc_reg()
        ins.append('li $'+r3+','+str(p2))

    if op == '+':
        ins.append('add $'+r1+', $'+r2+', $'+r3)
    elif op == '-':
        ins.append('sub $'+r1+', $'+r2+', $'+r3)
    elif op == '*':
        ins.append('mul $'+r1+', $'+r2+', $'+r3)
    elif op == '/':
        ins.append('div $'+r1+', $'+r2+', $'+r3)

    dealloc_reg(r2)
    dealloc_reg(r3)

    return (r1, ins)

functions = {}
g_variables = {} 
l_variables = {} 
print(ast)
print('parse ast')

global_var = True
global_fun_name = ''

def get_stack_num(f_name, v_name):
    stack = 0
    for var in l_variables[f_name]:
        if v_name in var: break
        stack += 1
    return ((stack+1)*4)

def parse_ast(ast):
    global global_var
    global global_fun_name
    if type(ast[0]) == tuple:
        r = list()
        ins = list()
        for inst in ast:
            ri, insi = parse_ast(inst)
            #r = (r,  ri)
            ins = ins + insi
        return None, ins
    if ast[0] == 'unit':
        global_var = True
        v_e1 = ast[1]
        v_e2 = ast[2]
        ins1 = list()
        ins2 = list()
        if type(v_e1) == tuple:
            v_e1, ins1 = parse_ast(v_e1)
        if type(v_e2) == tuple:
            v_e2, ins2 = parse_ast(v_e2)
        return None, ins1+ins2

    if ast[0] == 'fun':
        global_var = False
        print('fun')
        f_type = ast[1]
        f_name = ast[2]
        global_fun_name = f_name
        f_stm = ast[3]
        ins = list()
        ins.append(f_name+':')
        r, insf = parse_ast(f_stm)
        #compute total stack area needed
        tot_var = 1
        if f_name in l_variables:
            for var in l_variables[f_name]:
                tot_var += 1
        #allocate stack
        ins.append('addi $sp, $sp, -'+str(tot_var*4))
        #save ra
        ins.append('sw $ra, 0($sp)')
        #load ra
        insf.append('lw $ra, 0($sp)')
        #deallocate ra
        insf.append('addi $sp, $sp, '+str(tot_var*4))
        if f_name is not 'main':
            insf.append('jr $ra')
        else:
            insf.append('li $v0 10 #prgoram finished call terminate')
            insf.append('syscall')
        functions[f_name] = r, ins+insf 
        return None, list()

    if ast[0] == 'call':
        f_name = ast[1]
        print('funtcion call', f_name)
        ins = list()
        ins.append('jal ' + f_name)
        return None, ins

    if ast[0] == 'cond':
        v_op = ast[1]
        v_e1 = ast[2]
        v_e2 = ast[3]
        ins1 = list()
        ins2 = list()
        if type(v_e1) == tuple:
            v_e1, ins1 = parse_ast(v_e1)
        if type(v_e2) == tuple:
            v_e2, ins2 = parse_ast(v_e2)

        lbl, ins = gen_condop(v_op, v_e1, v_e2)
        return lbl, ins1+ins2+ins

    if ast[0] == 'if':
        if_exp = ast[1]
        if_stmt = ast[2]
        
        ins = list()
        ins_e = list()
        ins_s = list()
        if type(if_exp) == tuple:
            lbl, ins_e = parse_ast(if_exp)
        if type(if_stmt) == tuple:
            r, ins_s = parse_ast(if_stmt)

        ins = ins_e + ins_s
        ins.append(lbl+':')
        return None, ins

    if ast[0] == 'ifelse':
        if_exp = ast[1]
        if_stmt = ast[2]
        else_stmt = ast[3]
        
        ins = list()
        ins_e = list()
        ins_s = list()
        ins_else = list()
        if type(if_exp) == tuple:
            lbl, ins_e = parse_ast(if_exp)
        if type(if_stmt) == tuple:
            r, ins_s = parse_ast(if_stmt)
        if type(else_stmt) == tuple:
            r, ins_else = parse_ast(else_stmt)

        ins = ins_e + ins_s
        ins.append(lbl+':')
        ins = ins + ins_else
        return None, ins

    if ast[0] == 'while':
        w_exp = ast[1]
        w_stmt = ast[2]
        
        ins = list()
        ins_e = list()
        ins_s = list()
        if type(w_exp) == tuple:
            lbl_exit, ins_e = parse_ast(w_exp)
        if type(w_stmt) == tuple:
            r, ins_s = parse_ast(w_stmt)

        lbl_start = gen_lbl()
        ins.append(lbl_start+':')
        ins = ins + ins_e + ins_s
        ins.append('j '+lbl_start)
        ins.append(lbl_exit+':')
        return None, ins

    elif ast[0] == 'decli':
        inse = list()
        v_type = ast[1]
        v_name = ast[2]
        stack = 0
        if global_var:
            g_variables[v_name] = (v_type, '0') 
        else:
            if global_fun_name not in l_variables:
                l_variables[global_fun_name] = ({v_name: (v_type, 1)})
            else:
                l_variables[global_fun_name] = ((l_variables[global_fun_name]),({v_name: (v_type, 1)}))
            stack  = get_stack_num(global_fun_name, v_name)
        if len(ast) > 3:
            print('integer decleration with exp',global_fun_name,  global_var)
            v_exp = ast[3]
            if type(v_exp) == tuple:
                re, inse = parse_ast(v_exp)
                if global_var:
                    inse.append('sw $'+re+','+v_name)
                else:
                    inse.append('sw $'+re+', '+str(stack)+'($sp)')
                dealloc_reg(re)
            else:
                r1 = alloc_reg()
                if global_var:
                    inse.append('li $'+r1+','+str(v_exp))
                    inse.append('sw $'+r1+','+v_name)
                else:
                    inse.append('li $'+r1+','+str(v_exp))
                    inse.append('sw $'+r1+', '+str(stack)+'($sp)')
                dealloc_reg(r1)
        else:
            print('integer decleration ',global_fun_name,  global_var)
            if not global_var:
                inse.append('sw $zero, '+str(stack)+'($sp)')
        return None, inse
    elif ast[0] == 'arrdec':
        inse = list()
        v_type = ast[1]
        v_name = ast[2]
        v_num = ast[3]
        stack = 0
        dec = '0'
        for i in range(int(v_num)-1):
                dec += ', 0'
        if global_var:
            g_variables[v_name] = (v_type, dec) 
        else:
            if global_fun_name not in l_variables:
                l_variables[global_fun_name] = ({v_name: (v_type, v_num)})
            else:
                l_variables[global_fun_name] = ((l_variables[global_fun_name]),({v_name: (v_type, v_num)}))
            stack  = get_stack_num(global_fun_name, v_name)
        if len(ast) > 4:
            print('arr decleration with exp',global_fun_name,  global_var)
            v_exp = ast[4]
            if type(v_exp) == tuple:
                re, inse = parse_ast(v_exp)
                if global_var:
                    inse.append('sw $'+re+','+v_name)
                else:
                    inse.append('sw $'+re+', '+str(stack)+'($sp)')
                dealloc_reg(re)
            else:
                r1 = alloc_reg()
                if global_var:
                    inse.append('li $'+r1+','+str(v_exp))
                    inse.append('sw $'+r1+','+v_name)
                else:
                    inse.append('li $'+r1+','+str(v_exp))
                    inse.append('sw $'+r1+', '+str(stack)+'($sp)')
                dealloc_reg(r1)
        else:
            print('integer decleration ',global_fun_name,  global_var)
            if not global_var:
                inse.append('sw $zero, '+str(stack)+'($sp)')
        return None, inse

    elif ast[0] == 'asign':
        print('var asign')
        v_name = ast[1]
        v_exp = ast[2]
        ins = list()
        stack = 0
        if not v_name in g_variables:
            stack = get_stack_num(global_fun_name, v_name)
        if type(v_exp) == tuple:
            v_exp, ins = parse_ast(v_exp)
            if v_name in g_variables:
                ins.append('sw $'+v_exp+', '+v_name)
            else:
                ins.append('sw $'+v_exp+', '+str(stack)+'($sp)')
            dealloc_reg(v_exp)
        else:
            r1 = alloc_reg()
            if v_name in g_variables:
                ins.append('li $'+r1+','+str(v_exp))
                ins.append('sw $'+r1+','+v_name)
            else:
                ins.append('li $'+r1+','+str(v_exp))
                ins.append('sw $'+r1+', '+str(stack)+'($sp)')
            dealloc_reg(r1)
        return None, ins

    elif ast[0] == 'binop':
        print('binop')
        v_op = ast[1]
        v_e1 = ast[2]
        v_e2 = ast[3]
        ins1 = list()
        ins2 = list()
        if type(v_e1) == tuple:
            v_e1, ins1 = parse_ast(v_e1)
        if type(v_e2) == tuple:
            v_e2, ins2 = parse_ast(v_e2)

        r, ins = gen_binop(v_op, v_e1, v_e2)
        return r, ins1+ins2+ins

    elif ast[0] == 'id':
        print('var access')
        v_name = ast[1]
        r1 = alloc_reg()
        ins = list()
        if v_name in g_variables:
            ins.append('lw $'+r1+','+v_name)
        else:
            stack = get_stack_num(global_fun_name, v_name)
            ins.append('lw $'+r1+', '+str(stack)+'($sp)')
        return r1, ins
    return ret;


ins = list()
v, ins = parse_ast(ast)

i=0
ins.insert(i, '.data')
i = i+1
for var in g_variables:
    ins.insert(i, var+': .word ' + g_variables[var][1])
    i = i+1

ins.insert(i, '.text')
ins.append('')
i = i+1

if 'main' in functions:
    for line in functions['main'][1]:
        ins.append(line)
    ins.append('')

for f in functions:
    if f == 'main': continue
    for line in functions[f][1]:
        ins.append(line)
    ins.append('')

print(v, ins)
asm = open('out.asm', "w+")
for line in ins:
    print(line, file=asm)

print('global variables:')
print(g_variables)
print('local variables:')
print(l_variables)
print(functions)

