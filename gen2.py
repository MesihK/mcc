#ast = ('fun', 'int', 'main', ('comp_stm', ('stm_lst', ('stmt', ('decli', 'int', 'i', 1)), ('asign', 'i', ('binop', '+', ('binop', '/',('binop', '*', 3, 5), 2), ('id', 'i'))))))
#ast = ('fun', 'int', 'main', (('decli', 'int', 'i', 1), ('asign', 'i', ('binop', '+', ('binop', '/', ('binop', '*', 3, 5), 2), ('id', 'i')))))
#ast = ('decli', 'int', 'i', ('binop', '+', 3, 5))
#ast = ('decli', 'int', 'i', ('binop', '+', 3, ('binop', '*', 5, 2)))
#ast = ('unit', ('decli', 'int', 'a'), ('decli', 'int', 'i', ('binop', '+', 3, ('binop', '*', 5, 2))))
ast = ('unit', ('unit', ('decli', 'int', 'a'), ('decli', 'int', 'i', ('binop', '+', 3, ('binop', '*', 5, 2)))), ('fun', 'int', 'main', ('asign', 'a', ('binop', '*', 3, 2))))




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
variables = {} 
print(ast)
print('parse ast')

def parse_ast(ast):
    ret = ""
    if type(ast[0]) == tuple:
        for inst in ast:
            ret = ret + parse_ast(inst)
        return ret
    if ast[0] == 'unit':
        v_e1 = ast[1]
        v_e2 = ast[2]
        ins1 = list()
        ins2 = list()
        if type(v_e1) == tuple:
            v_e1, ins1 = parse_ast(v_e1)
        if type(v_e2) == tuple:
            v_e2, ins2 = parse_ast(v_e2)
        return (v_e1,v_e2), ins1+ins2

    if ast[0] == 'fun':
        print('fun')
        f_type = ast[1]
        f_name = ast[2]
        f_stm = ast[3]
        ins = list()
        ins.append(f_name+':')
        r, insf = parse_ast(f_stm)
        functions[f_name] = r, ins+insf 
        return None, list()
    elif ast[0] == 'decli':
        inse = list()
        v_type = ast[1]
        v_name = ast[2]
        if len(ast) > 3:
            print('integer decleration with exp')
            v_exp = ast[3]
            if type(v_exp) == tuple:
                re, inse = parse_ast(v_exp)
                inse.append('sw $'+re+','+v_name)
                dealloc_reg(re)
            else:
                r1 = alloc_reg()
                inse.append('li $'+r1+','+v_exp)
                inse.append('sw $'+r1+','+v_name)
                dealloc_reg(r1)
        else:
            print('integer decleration ')
        variables[v_name] = (v_type, '0') 
        return None, inse
    elif ast[0] == 'asign':
        print('var asign')
        v_name = ast[1]
        v_exp = ast[2]
        ins = list()
        if type(v_exp) == tuple:
            v_exp, ins = parse_ast(v_exp)
        return v_exp, ins

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
    return ret;


i=0
v, ins = parse_ast(ast)
print(v, ins)
asm = open('out.asm', "w+")
for line in ins:
    print(line, file=asm)

print(variables)
print(functions)
