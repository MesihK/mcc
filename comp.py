import sys
import gen2
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

c = open(sys.argv[1], "r")

# Reserved words
reserved = (
    'AUTO', 'BREAK', 'CASE', 'CHAR', 'CONST', 'CONTINUE', 'DEFAULT', 'DO', 'DOUBLE',
    'ELSE', 'ENUM', 'EXTERN', 'FLOAT', 'FOR', 'GOTO', 'IF', 'INT', 'LONG', 'REGISTER',
    'RETURN', 'SHORT', 'SIGNED', 'SIZEOF', 'STATIC', 'STRUCT', 'SWITCH', 'TYPEDEF',
    'UNION', 'UNSIGNED', 'VOID', 'VOLATILE', 'WHILE', 'ASM', 'PRINTSTR',
)

tokens = reserved + (
    'ID', 'NUMBER', 'SCONST',

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

# String literal
t_SCONST = r'\"([^\\\n]|(\\.))*?\"'

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
def p_file(p):
    '''file : unit
            | file unit'''
    if len(p) >= 3:
        p[0] = ('unit', p[1], p[2])
    else:
        p[0] = p[1]

def p_unit(p):
    '''unit : fun_def
            | decleration ";" '''
    p[0] = p[1]

def p_statement_fun_def(p):
    '''fun_def : decleration_specifier ID "(" ")" compound_statement
               | decleration_specifier ID "(" decleration_list ")" compound_statement'''
    if len(p) >= 7:
        p[0] = ('fun', p[1], p[2], p[4], p[6])
    else:
        p[0] = ('fun', p[1], p[2], p[5])

def p_statement_expr(p):
    '''statement : expression ";"
                 | decleration ";"
                 | compound_statement'''
    p[0] = p[1]

def p_statement_fun_call(p):
    '''expression : ID "(" ")"
                  | ID "(" expression_list ")" '''
    if len(p) > 4:
        p[0] = ('call', p[1], p[3])
    else:
        p[0] = ('call', p[1])

def p_statement_asm_call(p):
    '''expression : ASM "(" SCONST ")"'''
    p[0] = (p[1], p[3])


def p_statement_str_call(p):
    '''expression : PRINTSTR "(" SCONST ")"'''
    p[0] = (p[1], p[3])


def p_decleration_specifier (p):
    '''decleration_specifier : VOID
                             | INT
                             | CHAR'''
    p[0] = p[1]

def p_statement_return(p):
    'statement : RETURN expression ";" '
    p[0] = ('ret', p[2])

def p_statement_while_def(p):
    'statement : WHILE "(" expression ")" statement '
    p[0] = ('while', p[3], p[5])

def p_statement_if_def(p):
    'statement : IF "(" expression ")" statement '
    p[0] = ('if', p[3], p[5])


def p_statement_if_else_def(p):
    'statement : IF "(" expression ")" statement ELSE statement '
    p[0] = ('ifelse', p[3], p[5], p[7])

def p_statement_arr_def(p):
    '''decleration : decleration_specifier ID "[" NUMBER "]" "=" "{" expression_list "}"
                   | decleration_specifier ID "[" NUMBER "]" '''
    if len(p) <= 7:
        p[0] = ('arrdeciz', p[1], p[2], p[4])
    else:
        p[0] = ('arrdeci', p[1], p[2], p[4], p[8])

def p_statement_def(p):
    '''decleration : decleration_specifier ID "=" expression
                   | decleration_specifier ID '''
    if len(p) >= 5:
        p[0] = ('decli', p[1], p[2], p[4])
    else:
        p[0] = ('decli', p[1], p[2])

def p_statement_assign(p):
    'statement : ID "=" expression ";"'
    p[0] = ('asign', p[1], p[3])

def p_expression_list(p):
    '''expression_list : expression 
                       | expression_list ',' expression'''
    if len(p) >= 3:
        p[0] = (p[1],  p[3])
    else:
        p[0] = p[1]

def p_decleration_list(p):
    '''decleration_list : decleration
                        | decleration_list ',' decleration'''
    if len(p) >= 3:
        p[0] = (p[1],  p[3])
    else:
        p[0] = p[1]

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    p[0] = ('binop', p[2], p[1], p[3])


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = ('uminus', p[2])

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expression_arr_name(p):
    "expression : ID '[' expression ']'"
    p[0] = ('arrid', p[1], p[3])

def p_expression_arr_asign(p):
    "expression : ID '[' expression ']' '=' expression"
    p[0] = ('arrasign', p[1], p[3], p[6])

def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_name(p):
    "expression : ID"
    p[0] = ('id', p[1])

def p_cond_exp(p):
    '''expression : eq_exp'''
    p[0] = p[1]

def p_eq_exp(p):
    '''eq_exp : expression EQ expression
              | expression NE expression
              | expression LOR expression
              | expression LAND expression
              | expression '<' expression
              | expression '>' expression
              | expression GE expression
              | expression LE expression'''
    p[0] = ('cond', p[2], p[1], p[3])

def p_compound_statement(p):
    '''compound_statement : "{" statement_list "}"
                          | "{" "}"'''
    if len(p) >= 4:
        p[0] = p[2]


def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) >= 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()

ast = yacc.parse(c.read())
fast = open('ast', 'w')
print(ast, file=fast)
asm = open(sys.argv[2], 'w+')
print('# Generated from: ' + sys.argv[1], file=asm)
gen2.parse(ast, asm)

