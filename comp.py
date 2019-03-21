import sys
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

c = open(sys.argv[1], "r")
asm = open(sys.argv[2], "w+")
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

def dealloc_last_reg():
    for reg in reversed(list(registers.keys())):
        if(registers[reg] == 1):
            registers[reg] = 0
def dealloc_reg(r):
    if registers[r] != 1: print('register', r, 'is not allocated!', file=asm)
    registers[r] = 0

def is_reg(r):
    if r in registers:
        return True
    else:
        return False

# Reserved words
reserved = (
    'AUTO', 'BREAK', 'CASE', 'CHAR', 'CONST', 'CONTINUE', 'DEFAULT', 'DO', 'DOUBLE',
    'ELSE', 'ENUM', 'EXTERN', 'FLOAT', 'FOR', 'GOTO', 'IF', 'INT', 'LONG', 'REGISTER',
    'RETURN', 'SHORT', 'SIGNED', 'SIZEOF', 'STATIC', 'STRUCT', 'SWITCH', 'TYPEDEF',
    'UNION', 'UNSIGNED', 'VOID', 'VOLATILE', 'WHILE',
)

tokens = reserved + (
    'ID', 'NUMBER', 

    # Operators (<<,>>, ||, &&, <=, >=, ==, !=)
    'LSHIFT', 'RSHIFT',
    'LOR', 'LAND',
    'LE', 'GE', 'EQ', 'NE',
)

literals = ['=', '+', '-', '*', '/', '&', '|', '^', '~', '(', ')', '{', '}',
            '[', ']', ';', ',', '!', '<', '>']

# Tokens

# Operators
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_LOR = r'\|\|'
t_LAND = r'&&'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r


def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value, "ID")
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}
variables = {}

def p_statement_if_def(p):
    'statement : IF "(" expression ")" statement '
    print('if definition', p[3], p[5])

def p_statement_if_else_def(p):
    'statement : IF "(" expression ")" statement ELSE statement '
    print('if else definition', p[3], p[5], p[7])

def p_statement_arr_def(p):
    '''statement : INT ID "[" NUMBER "]" "=" "{" expression_list "}" ";"
                 | INT ID "[" NUMBER "]" ";" '''
    #TODO if exists split p[8] by ',' 
    if len(p) <= 7:
        #definition without initialization
        #initialize with zeros;
        def_str = '0'
        for i in range(1,int(p[4])):
                def_str = def_str + ', '
                def_str = def_str + '0'

        variables[p[2]] = def_str
    else:
        #definition with initialization
        exps = p[8].strip().split(',')
        if len(exps) != int(p[4]): raise Exception("array initialization error")
        def_str = ""
        i = 0
        for exp in exps:
            #if there is a reg in expression list than implement asm code
            if is_reg(exp):
                def_str = def_str + '0'
                r1 = alloc_reg()
                r2 = alloc_reg()
                print('la', '$'+r1+',', p[2], file=asm)# put address of list into $r1
                print('li', '$'+r2+',', str(i), file=asm)# put the index into $r2
                print('add', '$'+r2+',', '$'+r2+',', '$'+r2, file=asm)# double the index
                print('add', '$'+r2+',', '$'+r2+',', '$'+r2, file=asm)# double the index again 4x
                print('add', '$'+r2+',', '$'+r2+',', '$'+r1, file=asm)# combine to get address
                print('sw', '$'+exp+',', '0($'+r2+')', file=asm)#store the value of reg to array
                dealloc_reg(r1)
                dealloc_reg(r2)
                dealloc_reg(exp)
            else:
                def_str = def_str + exp
            if exp != exps[-1]:
                def_str = def_str + ", "
            i = i + 1

        variables[p[2]] = def_str

def p_statement_def(p):
    '''statement : INT ID "=" expression ";"
                 | INT ID ";"'''
    #print('variable definition of:', p[2], len(p))
    variables[p[2]] = "0"
    if len(p) >= 6:
        if is_reg(p[4]):
            print('sw', '$'+p[4]+',', p[2], file=asm)
            dealloc_reg(p[4])
        else:
            r1 = alloc_reg()
            print('li', '$'+r1+',', p[4], file=asm)
            print('sw', '$'+r1+',', p[2], file=asm)
            dealloc_reg(r1)

def p_statement_assign(p):
    'statement : ID "=" expression ";"'
    #print('variable assign:', p[1])
    if p[1] not in variables : raise Exception(p[1]+' is not defined')
    if is_reg(p[3]):
        print('sw', '$'+p[3]+',', p[1], file=asm)
        dealloc_reg(p[3])
    else:
        r1 = alloc_reg()
        print('li', '$'+r1+',', p[3], file=asm)
        print('sw', '$'+r1+',', p[1], file=asm)
        dealloc_reg(r1)

def p_expression_list(p):
    '''expression_list : expression ',' expression 
                       | expression_list ',' expression 
                       | expression_list ',' expression_list '''
    p[0] = str(p[1])+','+str(p[3])

def p_statement_expr(p):
    '''statement : expression ";"
                 | compound_statement'''
    #print(p[1])
    pass


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    r1 = alloc_reg()
    if is_reg(p[1]): r2 = p[1]
    else :
        r2 = alloc_reg()
        print('li', '$'+r2+',',  p[1], file=asm)

    if is_reg(p[3]): r3 = p[3]
    else :
        r3 = alloc_reg()
        print('li', '$'+r3+',',  p[3], file=asm)

    if p[2] == '+':
        print('add', '$'+r1+',', '$'+r2+',', '$'+r3, file=asm)
    elif p[2] == '-':
        print('sub', '$'+r1+',', '$'+r2+',', '$'+r3, file=asm)
    elif p[2] == '*':
        print('mul', '$'+r1+',', '$'+r2+',', '$'+r3, file=asm)
    elif p[2] == '/':
        print('div', '$'+r1+',', '$'+r2+',', '$'+r3, file=asm)

    p[0] = r1
    dealloc_reg(r2)
    dealloc_reg(r3)


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    if is_reg(p[2]):
        print('sub ', '$'+p[2]+',',  '$zero,', '$'+p[2], file=asm)
        p[0] = p[2]
    else:
        p[0] = -p[2]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expression_arr_name(p):
    "expression : ID '[' expression ']'"
    #print('array access', p[1], p[3])
    r1 = alloc_reg()
    r2 = alloc_reg()
    print('la', '$'+r2+',', p[1], file=asm)# put address of list into $r1
    if is_reg(p[3]):
        r3 = p[3]
    else:
        r3 = alloc_reg()
        print('li', '$'+r3+',', str(p[3]), file=asm)# put the index into $r2
    print('add', '$'+r3+',', '$'+r3+',', '$'+r3, file=asm)# double the index
    print('add', '$'+r3+',', '$'+r3+',', '$'+r3, file=asm)# double the index again 4x
    print('add', '$'+r3+',', '$'+r3+',', '$'+r2, file=asm)# combine to get address
    print('lw', '$'+r1+',', '0($'+r3+')', file=asm)#load array val to the reg 
    dealloc_reg(r2)
    dealloc_reg(r3)
    p[0] = r1;

def p_expression_arr_asign(p):
    "expression : ID '[' expression ']' '=' expression"
    #print('array asign', p[1], p[3], p[6])
    r2 = alloc_reg()
    print('la', '$'+r2+',', p[1], file=asm)# put address of list into $r1
    if is_reg(p[3]):
        r3 = p[3]
    else:
        r3 = alloc_reg()
        print('li', '$'+r3+',', str(p[3]), file=asm)# put the index into $r2
    print('add', '$'+r3+',', '$'+r3+',', '$'+r3, file=asm)# double the index
    print('add', '$'+r3+',', '$'+r3+',', '$'+r3, file=asm)# double the index again 4x
    print('add', '$'+r3+',', '$'+r3+',', '$'+r2, file=asm)# combine to get address
    if is_reg(p[6]):
        r1 = p[6]
    else:
        r1 = alloc_reg()
        print('li', '$'+r1+',', str(p[6]), file=asm)# put the index into $r2
    print('sw', '$'+r1+',', '0($'+r3+')', file=asm)#store the value of reg to array
    dealloc_reg(r1)
    dealloc_reg(r2)
    dealloc_reg(r3)


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_name(p):
    "expression : ID"
    try:
        r1 = alloc_reg()
        print('lw', '$'+r1+',', p[1], file=asm)
        p[0] = r1
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_cond_exp(p):
    '''expression : eq_exp'''
    print('cond', p[1])
    p[0] = p[1]

def p_eq_exp(p):
    '''eq_exp : expression EQ expression
              | expression NE expression
              | expression LOR expression
              | expression LAND expression
              | expression GE expression
              | expression LE expression'''
    print('cond eq', p[1], p[2], p[3])
    p[0] = 0

#-----------------------------------------------------------------------
def p_compound_statement(p):
    '''compound_statement : "{" statement_list "}"
                          | "{" "}"'''
    print('p_compound_statement')
    pass


def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    print('statement_list')
    pass

#-----------------------------------------------------------------------

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()

c_lines = c.readlines();
for line in c_lines:
    asm.write('#'+line)
    yacc.parse(line)

asm.seek(0,0); #goto begining
data = asm.read()
asm.seek(0,0); #goto begining
print('.data', file=asm)
for var in variables:
    print(var+':', '.word', variables[var], file=asm)
print('.text', file=asm)
asm.write(data)
