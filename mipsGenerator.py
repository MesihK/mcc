import datetime
#TODO
# *OK - function call
# *OK - conditional expressions
# *OK - if
# *OK - if - else
# *OK - while
# *OK - local variables
# *OK - gloabal variables
# *OK - arrays
# *OK - function arguments
# *OK - function return
# *OK - binop and or nor xor nand xnor
# *OK - print by syscall
# *OK - function recursion
# *OK - asm("add $t0, $t1, $t2")
# *OK - char variable
# *OK - for loop
# *OK - continue
# *OK - break
# *OK - do while loop
# switch - case
# *OK - pointers
# pointer increment
# *p = arr; expression. direct access to address of array
# documentation
# *OK - example programs

registers = {
    #'at':0, 'v0':0, 'v1':0,
    #'a0':0, 'a1':0, 'a2':0, 'a3':0,
    't0':0, 't1':0, 't2':0, 't3':0, 't4':0, 't5':0, 't6':0, 't7':0,
    's0':0, 's1':0, 's2':0, 's3':0, 's4':0, 's5':0, 's6':0, 's7':0,
    't8':0, 't9':0,
    'k0':0, 'k1':0,
    #'gp':0, 'sp':0, 'fp':0, 'ra':0
}
all_registers = {
    'at':0, 'v0':0, 'v1':0,
    'a0':0, 'a1':0, 'a2':0, 'a3':0,
    't0':0, 't1':0, 't2':0, 't3':0, 't4':0, 't5':0, 't6':0, 't7':0,
    's0':0, 's1':0, 's2':0, 's3':0, 's4':0, 's5':0, 's6':0, 's7':0,
    't8':0, 't9':0,
    'k0':0, 'k1':0,
    'gp':0, 'sp':0, 'fp':0, 'ra':0
}


def alloc_reg():
    for reg in registers:
        if(registers[reg] == 0):
            registers[reg] = 1
            return reg
    raise Exception('Not enough register')

def dealloc_reg(r):
    if r not in registers:
        if r not in all_registers:
            raise Exception(r+' is not register!')
    else:
        registers[r] = 0

def is_reg(r):
    if r in all_registers:
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
        ins.append('blt $'+r2+', $'+r3+', '+lbl_exit)

    dealloc_reg(r2)
    dealloc_reg(r3)
    return lbl_exit, ins

def gen_binop(op, p1, p2):
    ins = list()
    if op != '*' and op != '/':
        if is_reg(p1) and not is_reg(p2):
            if op == '+':
                ins.append('addi $'+p1+', $'+p1+', '+str(p2))
            elif op == '-':
                ins.append('subi $'+p1+', $'+p1+', '+str(p2))
            elif op == '&':
                ins.append('andi $'+p1+', $'+p1+', '+str(p2))
            elif op == '|':
                ins.append('ori $'+p1+', $'+p1+', '+str(p2))
            elif op == '^':
                ins.append('xori $'+p1+', $'+p1+', '+str(p2))
            return p1, ins
        if not is_reg(p1) and is_reg(p2):
            if op == '+':
                ins.append('addi $'+p2+', $'+p2+', '+str(p1))
            elif op == '-':
                ins.append('subi $'+p2+', $'+p2+', -'+str(p1))
            elif op == '&':
                ins.append('andi $'+p2+', $'+p2+', '+str(p1))
            elif op == '|':
                ins.append('ori $'+p2+', $'+p2+', '+str(p1))
            elif op == '^':
                ins.append('xori $'+p2+', $'+p2+', '+str(p1))
            return p2, ins

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
    elif op == '&':
        ins.append('and $'+r1+', $'+r2+', $'+r3)
    elif op == '|':
        ins.append('or $'+r1+', $'+r2+', $'+r3)
    elif op == '^':
        ins.append('xor $'+r1+', $'+r2+', $'+r3)

    dealloc_reg(r2)
    dealloc_reg(r3)

    return (r1, ins)

functions = {}
g_variables = {} 
l_variables = {} 
s_variables = {}

global_var = True
global_fun_name = ''

def get_stack_num(f_name, v_name):
    stack = 0
    for var in l_variables[f_name]:
        if v_name == var: break
        stack += l_variables[f_name][var][1]
    return ((stack+1)*4)

def parse_ast(ast):
    global global_var
    global global_fun_name

    if type(ast) == int:
        return ast, list()

    elif type(ast) == str:
        if ast == 'continue':
            ins = list()
            ins.append('j START')
            return None, ins

        if ast == 'break':
            ins = list()
            ins.append('j END')
            return None, ins

        if ast == 'ret':
            ins = list()
            ins.append('lw $ra, 0($sp)')
            ins.append('addi $sp, $sp, STACK')
            if global_fun_name != 'main':
                ins.append('jr $ra')
            return None, ins

    if type(ast[0]) == int:
        r, ins = parse_ast(ast[1])
        return (ast[0],r), ins
    elif type(ast[0]) == tuple:
        r = None 
        ins = list()
        for inst in ast:
            ri, insi = parse_ast(inst)
            if ri is not None:
                if r == None:
                    r = ri
                else:
                    r = (r,  ri)
            ins = ins + insi
        return r, ins
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
        f_type = ast[1].strip()
        f_name = ast[2].strip()
        global_fun_name = f_name
        has_arg = False
        if len(ast) > 4:
            has_arg = True
            f_arg = ast[3]
            f_stm = ast[4]
        else:
            f_stm = ast[3]
        ins = list()
        ins.append(f_name+':')
        insa = list()
        arg_cnt = 0
        if has_arg:
            r, insa = parse_ast(f_arg)
            if f_name in l_variables:
                for var in l_variables[f_name]:
                    arg_cnt += l_variables[f_name][var][1]
            if arg_cnt > 8:
                print('To many argumnets in function: '+f_name)
        r, insf = parse_ast(f_stm)
        #compute total stack area needed
        tot_var = 1
        if f_name in l_variables:
            for var in l_variables[f_name]:
                tot_var += l_variables[f_name][var][1]

        for index, item in enumerate(insf):
            insf[index] = item.replace('STACK', str(tot_var*4))
        #allocate stack
        ins.append('addi $sp, $sp, -'+str(tot_var*4))
        #save ra
        ins.append('sw $ra, 0($sp)')
        #load arguments
        if has_arg:
            for i in range(arg_cnt):
                insa.append('sw $a'+str(i)+', '+str(4+i*4)+'($sp)')
        #load ra
        insf.append('lw $ra, 0($sp)')
        #deallocate ra
        insf.append('addi $sp, $sp, '+str(tot_var*4))
        if f_name != 'main':
            insf.append('jr $ra')
        else:
            insf.append('li $v0 10 #prgoram finished call terminate')
            insf.append('syscall')
        functions[f_name] = r, ins+insa+insf
        return None, list()

    if ast[0] == 'call':
        f_name = ast[1]
        ins = list()

        if len(ast) > 2:
            f_arg = ast[2]
            r, ins = parse_ast(f_arg)
            arg_list = str(r).replace("'",'').replace(' ','').replace('(','').replace(')','').split(',')
            arg_cnt = 0;
            for a in arg_list:
                if is_reg(a):
                    ins.append('add $a'+str(arg_cnt)+' $zero, $'+a)
                else:
                    ins.append('li $a'+str(arg_cnt)+' '+a)
                arg_cnt += 1

        ins.append('jal ' + f_name)
        return 'v0', ins

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
        lbl_e = gen_lbl()
        if type(if_exp) == tuple:
            lbl, ins_e = parse_ast(if_exp)
        r, ins_s = parse_ast(if_stmt)
        ins_s.append('j '+lbl_e)
        r, ins_else = parse_ast(else_stmt)

        ins = ins_e + ins_s
        ins.append(lbl+':')
        ins = ins + ins_else
        ins.append(lbl_e+':')
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
        for index, item in enumerate(ins_s):
            ins_s[index] = ins_s[index].replace('START', lbl_start)
            ins_s[index] = ins_s[index].replace('END', lbl_exit)
        ins = ins + ins_e + ins_s
        ins.append('j '+lbl_start)
        ins.append(lbl_exit+':')
        return None, ins

    if ast[0] == 'dowhile':
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
        for index, item in enumerate(ins_s):
            ins_s[index] = ins_s[index].replace('START', lbl_start)
            ins_s[index] = ins_s[index].replace('END', lbl_exit)
        ins = ins + ins_s + ins_e
        ins.append('j '+lbl_start)
        ins.append(lbl_exit+':')
        return None, ins

    if ast[0] == 'for':
        v_exp1 = ast[1]
        v_exp2 = ast[2]
        v_exp3 = ast[3]
        v_stmt = ast[4]

        ins = list()
        ins_e1 = list()
        ins_e2 = list()
        ins_e3 = list()
        ins_s = list()
        if type(v_exp1) == tuple:
            r, ins_e1 = parse_ast(v_exp1)
        if type(v_exp2) == tuple:
            lbl_exit, ins_e2 = parse_ast(v_exp2)
        if type(v_exp3) == tuple:
            r, ins_e3 = parse_ast(v_exp3)
        if type(v_stmt) == tuple:
            r, ins_s = parse_ast(v_stmt)
        ins = ins_e1
        lbl_start = gen_lbl()
        ins.append(lbl_start+':')
        for index, item in enumerate(ins_s):
            ins_s[index] = ins_s[index].replace('START', lbl_start)
            ins_s[index] = ins_s[index].replace('END', lbl_exit)
        ins = ins+ins_e2+ins_s+ins_e3
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
                l_variables[global_fun_name] = {v_name: (v_type, 1)}
            else:
                l_variables[global_fun_name][v_name] = (v_type, 1)
            stack  = get_stack_num(global_fun_name, v_name)
        if len(ast) > 3:
            v_exp = ast[3]
            if type(v_exp) == tuple:
                re, inse = parse_ast(v_exp)
                v_exp = re
            if is_reg(v_exp):
                if global_var:
                    inse.append('sw $'+v_exp+','+v_name)
                else:
                    inse.append('sw $'+v_exp+', '+str(stack)+'($sp)')
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
            if not global_var:
                inse.append('sw $zero, '+str(stack)+'($sp)')
        return None, inse
    elif ast[0] == 'arrdeciz':
        inse = list()
        v_type = ast[1]
        v_name = ast[2]
        v_num = ast[3]
        stack = 0
        if global_var:
            dec = '0'
            for i in range(int(v_num)-1):
                    dec += ', 0'
            g_variables[v_name] = (v_type, dec) 
        else:
            if global_fun_name not in l_variables:
                l_variables[global_fun_name] = {v_name: (v_type, v_num)}
            else:
                l_variables[global_fun_name][v_name] = (v_type, v_num)
            stack  = get_stack_num(global_fun_name, v_name)
        if not global_var:
            for i in range(int(v_num)):
                inse.append('sw $zero, '+str(stack+i*4)+'($sp)')
        return None, inse
    elif ast[0] == 'arrdeci':
        inse = list()
        v_type = ast[1]
        v_name = ast[2]
        v_num = ast[3]
        v_list = ast[4]
        stack = 0
        if global_var:
            g_variables[v_name] = (v_type, str(v_list).replace('(','').replace(')','')) 
        else:
            if global_fun_name not in l_variables:
                l_variables[global_fun_name] = {v_name: (v_type, v_num)}
            else:
                l_variables[global_fun_name][v_name] = (v_type, v_num)
            stack  = get_stack_num(global_fun_name, v_name)
        if not global_var:
            i = 0
            r, ins = parse_ast(v_list)
            exp_list = str(r).replace("'",'').replace(' ','').replace('(','').replace(')','').split(',')
            for exp in exp_list:
                try:
                    e = int(exp)
                    r1 = alloc_reg()
                    ins.append('li $'+r1+','+str(e))
                    ins.append('sw $'+r1+', '+str(stack+i*4)+'($sp)')
                    dealloc_reg(r1)
                except ValueError as ex:
                    r = exp
                    ins.append('sw $'+r+', '+str(stack+i*4)+'($sp)')
                    dealloc_reg(r)
                i += 1
            inse += ins
        return None, inse

    elif ast[0] == 'asign':
        v_name = ast[1]
        v_exp = ast[2]
        ins = list()
        stack = 0
        if not v_name in g_variables:
            stack = get_stack_num(global_fun_name, v_name)
        if type(v_exp) == tuple:
            v_exp, ins = parse_ast(v_exp)
            if type(v_exp) == int:
                r1  = alloc_reg()
                ins.append('li $'+r1+','+str(v_exp))
                v_exp = r1
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

    elif ast[0] == 'arrasign':
        v_name = ast[1]
        v_ind = ast[2]
        v_exp = ast[3]
        ins = list()
        insi = list()
        inse = list()
        stack = 0
        if not v_name in g_variables:
            stack = get_stack_num(global_fun_name, v_name)
            sp = 'sp'
        else:
            sp = alloc_reg()
            ins.append('la $'+sp+', '+v_name)

        if type(v_ind) == tuple:
            v_ind, insi = parse_ast(v_ind)

        #example global array access
        #la $t3, list         # put address of list into $t3
        #li $t2, 6            # put the index into $t2
        #add $t2, $t2, $t2    # double the index
        #add $t2, $t2, $t2    # double the index again (now 4x)
        #add $t1, $t2, $t3    # combine the two components of the address
        #lw $t4, 0($t1)       # get the value from the array cell

        if not is_reg(v_ind):
            r_ind = alloc_reg()
            insi.append('li $'+r_ind+','+str(v_ind))#add index of array
            v_ind = r_ind
        insi.append('add $'+v_ind+', $'+v_ind+', $'+v_ind)# double the index
        insi.append('add $'+v_ind+', $'+v_ind+', $'+v_ind)# double the index
        insi.append('add $'+v_ind+', $'+sp+', $'+v_ind)#add stack pointer
        if not v_name in g_variables:
            insi.append('addi $'+v_ind+', $'+v_ind+','+str(stack))#add index of array

        if type(v_exp) == tuple:
            v_exp, inse = parse_ast(v_exp)
        else:
            r_exp = alloc_reg()
            insi.append('li $'+r_exp+','+str(v_exp))#add index of array
            v_exp = r_exp
        inse.append('sw $'+v_exp+', ($'+v_ind+')')

        dealloc_reg(v_ind)
        dealloc_reg(v_exp)

        ins += insi + inse

        return None, ins

    elif ast[0] == 'arrid':
        v_name = ast[1]
        v_ind = ast[2]
        ins = list()
        stack = 0
        if not v_name in g_variables:
            stack = get_stack_num(global_fun_name, v_name)
            sp = 'sp'
        else:
            sp = alloc_reg()
            ins.append('la $'+sp+', '+v_name)

        if type(v_ind) == tuple:
            v_ind, insi = parse_ast(v_ind)
            ins += insi

        if not is_reg(v_ind):
            r_ind = alloc_reg()
            ins.append('li $'+r_ind+','+str(v_ind))#add index of array
            v_ind = r_ind
        ins.append('add $'+v_ind+', $'+v_ind+', $'+v_ind)# double the index
        ins.append('add $'+v_ind+', $'+v_ind+', $'+v_ind)# double the index
        ins.append('add $'+v_ind+', $'+sp+', $'+v_ind)#add stack pointer
        if not v_name in g_variables:
            ins.append('addi $'+v_ind+', $'+v_ind+','+str(stack))#add index of array

        ins.append('lw $'+v_ind+', ($'+v_ind+')')
        return v_ind, ins

    elif ast[0] == 'ret':
        v_exp = ast[1]
        ins = list()
        if type(v_exp) == tuple:
            v_exp, ins = parse_ast(v_exp)
        if type(v_exp) == str:
            ins.append('add $v0, $zero, $'+v_exp)
            dealloc_reg(v_exp)
        elif type(v_exp) == int:
            ins.append('li $v0, '+str(v_exp))
        ins.append('lw $ra, 0($sp)')
        ins.append('addi $sp, $sp, STACK')
        if global_fun_name != 'main':
            ins.append('jr $ra')
        return 'v0', ins

    elif ast[0] == 'id':
        #TODO if id is array return it's address
        v_name = ast[1]
        ins = list()
        r1 = alloc_reg()
        if v_name in g_variables:
            ins.append('lw $'+r1+','+v_name)
        else:
            stack = get_stack_num(global_fun_name, v_name)
            ins.append('lw $'+r1+', '+str(stack)+'($sp)')
        return r1, ins

    elif ast[0] == 'char':
        if "'" not in ast[1]:
            raise Exception('char type error:'+ast[1])
        return ord(ast[1].replace("'",'')), list()

    elif ast[0] == 'binop':
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
        v_name = ast[1]
        r1 = alloc_reg()
        ins = list()
        if v_name in g_variables:
            ins.append('lw $'+r1+','+v_name)
        else:
            stack = get_stack_num(global_fun_name, v_name)
            ins.append('lw $'+r1+', '+str(stack)+'($sp)')
        return r1, ins
    elif ast[0] == 'asm':
        ins = list()
        ins.append(ast[1].replace('"',''))
        return None, ins

    elif ast[0] == 'printstr':
        lbl = gen_lbl()
        s_variables[lbl] = ast[1]
        ins = list()
        ins.append('la $a0, '+lbl)
        ins.append('li $v0, 4')
        ins.append('syscall')
        return None, ins

    elif ast[0] == 'uminus':
        v_exp = ast[1]
        ins = list()
        if type(v_exp) == tuple:
            v_exp, ins = parse_ast(v_exp)
        if type(v_exp) == int:
            v_exp = -v_exp
        elif is_reg(v_exp):
            ins.append('sub $'+v_exp+', $zero, $'+v_exp)
        return v_exp, ins

    elif ast[0] == 'not':
        v_exp = ast[1]
        ins = list()
        if type(v_exp) == tuple:
            v_exp, ins = parse_ast(v_exp)
        if type(v_exp) == int:
            v_exp = ~v_exp
        elif is_reg(v_exp):
            ins.append('not $'+v_exp+', $'+v_exp)
        return v_exp, ins

    elif ast[0] == 'address':
        v_name = ast[1]
        ins = list()
        r1 = alloc_reg()
        if v_name in g_variables:
            ins.append('la $'+r1+','+v_name)
        else:
            stack = get_stack_num(global_fun_name, v_name)
            ins.append('addi $'+r1+', $sp, '+str(stack))
        return r1, ins
    elif ast[0] == 'arraddress':
        v_name = ast[1]
        v_ind = ast[2]
        ins = list()
        stack = 0
        if not v_name in g_variables:
            stack = get_stack_num(global_fun_name, v_name)
            sp = 'sp'
        else:
            sp = alloc_reg()
            ins.append('la $'+sp+', '+v_name)

        if type(v_ind) == tuple:
            v_ind, insi = parse_ast(v_ind)
            ins += insi

        if not is_reg(v_ind):
            r_ind = alloc_reg()
            ins.append('li $'+r_ind+','+str(v_ind))#add index of array
            v_ind = r_ind
        ins.append('add $'+v_ind+', $'+v_ind+', $'+v_ind)# double the index
        ins.append('add $'+v_ind+', $'+v_ind+', $'+v_ind)# double the index
        ins.append('add $'+v_ind+', $'+sp+', $'+v_ind)#add stack pointer
        if not v_name in g_variables:
            ins.append('addi $'+v_ind+', $'+v_ind+','+str(stack))#add index of array

        return v_ind, ins

    elif ast[0] == 'paccess':
        v_name = ast[1]
        ins = list()
        r1 = alloc_reg()
        if v_name in g_variables:
            ins.append('lw $'+r1+','+v_name)
            ins.append('lw $'+r1+', ($'+r1+')')
        else:
            stack = get_stack_num(global_fun_name, v_name)
            ins.append('lw $'+r1+', '+str(stack)+'($sp)')
            ins.append('lw $'+r1+', ($'+r1+')')
        return r1, ins

    elif ast[0] == 'pasign':
        v_name = ast[1]
        v_exp = ast[2]
        ins = list()
        stack = 0
        if not v_name in g_variables:
            stack = get_stack_num(global_fun_name, v_name)
        if type(v_exp) == tuple:
            v_exp, ins = parse_ast(v_exp)
            if type(v_exp) == int:
                r1  = alloc_reg()
                ins.append('li $'+r1+','+str(v_exp))
                v_exp = r1
            if v_name in g_variables:
                r2  = alloc_reg()
                ins.append('lw $'+r2+','+v_name)
                ins.append('sw $'+v_exp+', ($'+r2+')')
                dealloc_reg(r2)
            else:
                r2  = alloc_reg()
                ins.append('lw $'+r2+', '+str(stack)+'($sp)')
                ins.append('sw $'+v_exp+', ($'+r2+')')
                dealloc_reg(r2)
            dealloc_reg(v_exp)
        else:
            r1 = alloc_reg()
            if v_name in g_variables:
                r2  = alloc_reg()
                ins.append('li $'+r1+','+str(v_exp))
                ins.append('lw $'+r2+','+v_name)
                ins.append('sw $'+r1+', ($'+r2+')')
                dealloc_reg(r2)
            else:
                r2  = alloc_reg()
                ins.append('li $'+r1+','+str(v_exp))
                ins.append('lw $'+r2+', '+str(stack)+'($sp)')
                ins.append('sw $'+r1+', ($'+r2+')')
                dealloc_reg(r2)
            dealloc_reg(r1)
        return None, ins

    raise Exception('Unknown AST:', ast)

def parse(ast, asm):
    ins = list()
    v, ins = parse_ast(ast)


    i=0
    ins.insert(i, '.data')
    i = i+1

    for var in s_variables:
        ins.insert(i, var+': .asciiz ' + s_variables[var])
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

    asm.write('# Generated at: '+str(datetime.datetime.now())+'\n')
    for line in ins:
        asm.write(line+'\n')
