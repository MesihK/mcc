import sys
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

asm = open(sys.argv[1], "w")
stack_pointer = 0
registers = {
    'at':0, 'v0':0, 'v1':0,
    'a0':0, 'a1':0, 'a2':0, 'a3':0,
    't0':0, 't2':0, 't3':0, 't4':0, 't5':0, 't6':0, 't7':0,
    's0':0, 's1':0, 's1':0, 's1':0, 's1':0, 's1':0, 's1':0,
    't8':0, 't9':0, 't10':0, 'k0':0, 'k1':0,
    'gp':0, 'sp':0, 'fp':0, 'ra':0
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

#t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

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
#    ('left', '^'),
#    ('left', '|'),
#    ('left', '&'),
    ('left', '+', '-'),
    ('left', '*', '/'),
#    ('right', '~'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}

def p_statement_if_def(p):
    'statement : IF "(" expression ")" statement '
    print('if definition', p[3], p[5])

def p_statement_if_else_def(p):
    'statement : IF "(" expression ")" statement ELSE statement '
    print('if else definition', p[3], p[5], p[7])

def p_statement_arr_def(p):
    'statement : INT ID "[" NUMBER "]" "=" "{" expression_list "}" ";"'
    print('array definition', p[2], p[4], p[8])

def p_statement_def(p):
    '''statement : INT ID "=" expression ";"
                 | INT ID ";"'''
    print('variable definition of:', p[2], len(p))
    global stack_pointer
    stack_pointer = stack_pointer + 4
    s = stack_pointer
    if len(p) < 6:
        print('sw', '$zero,', str(s)+'($sp)', file=asm)
    else:
        if is_reg(p[4]):
            print('sw', '$'+p[4]+',', str(s)+'($sp)', file=asm)
            dealloc_reg(p[4])
        else:
            r1 = alloc_reg()
            print('li', '$'+r1+',', p[4], file=asm)
            print('sw', '$'+r1+',', str(s)+'($sp)', file=asm)
            dealloc_reg(r1)
    names[p[2]] = s

def p_statement_assign(p):
    'statement : ID "=" expression ";"'
    print('variable assign:', p[1])
    if p[1] not in names : raise Exception(p[1]+' is not defined')
    s = names[p[1]]
    if is_reg(p[3]):
        print('sw', '$'+p[3], ',', str(s)+'($sp)', file=asm)
        dealloc_reg(p[3])
    else:
        r1 = alloc_reg()
        print('li', '$'+r1, ',', p[3], file=asm)
        print('sw', '$'+r1, ',', str(s)+'($sp)', file=asm)
        dealloc_reg(r1)
    names[p[1]] = s

def p_expression_list(p):
    '''expression_list : expression ',' expression 
                       | expression_list ',' expression 
                       | expression_list ',' expression_list '''
    p[0] = str(p[1])+','+str(p[3])

def p_statement_expr(p):
    '''statement : expression ";"
                 | compound_statement'''
    print(p[1])


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    #print('calculate ' , p[0] , '=' , p[1] , p[2] , p[3])
    r1 = alloc_reg()
    if is_reg(p[1]): r2 = p[1]
    else :
        r2 = alloc_reg()
        print('li', '$'+r2, ',',  p[1], file=asm)

    if is_reg(p[3]): r3 = p[3]
    else :
        r3 = alloc_reg()
        print('li', '$'+r3, ',',  p[3], file=asm)

    if p[2] == '+':
        print('add', '$'+r1, ',', '$'+r2, ',', '$'+r3, file=asm)
    elif p[2] == '-':
        print('sub', '$'+r1, ',', '$'+r2, ',', '$'+r3, file=asm)
    elif p[2] == '*':
        print('mul', '$'+r1, ',', '$'+r2, ',', '$'+r3, file=asm)
    elif p[2] == '/':
        print('div', '$'+r1, ',', '$'+r2, ',', '$'+r3, file=asm)

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
    print('array access', p[1], p[3])


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_name(p):
    "expression : ID"
    try:
        s = names[p[1]]
        r1 = alloc_reg()
        print('lw', '$'+r1, str(s)+'($sp)', file=asm)
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

print('.data', file=asm)
print('.text', file=asm)
while 1:
    try:
        s = raw_input('calc > ')
        print('#'+s, file=asm)
    except EOFError:
        break
    except KeyboardInterrupt:
        break
    if not s:
        continue
    yacc.parse(s)

print('#Variable List:', file=asm)
for var in names:
    print('#'+var, 'is at:', names[var], file=asm)

