from ply import lex

# states = (
#     ("CA", "exclusive"),
#     # ("tagf", "exclusive")
# )

tokens = (
    'FUNC',
    'DFUNC',
    'BLOCOA',
    'BLOCOF',
    'DVAR',
    'VAR',
    'WHILE',
    'FOR',
    'IF',
    'COMNTS',
    'COMNTSM',
    'VIRGULA',
    'PVIRGULA',
    'ATRIBUICAO'
)

def t_COMNTS(t):
    r'//.*'

def t_COMNTSM(t):
    r'/\*[^\t]*?\*/'

def t_BLOCOA(t):
    r'{'
    return t

def t_BLOCOF(t):
    r'}'
    return t

def t_WHILE(t):
    r'while[^{]*'
    return t

def t_FOR(t):
    r'for[^{]*'
    return t

def t_IF(t):
    r'if[^{]*'
    return t

def t_PVIRGULA(t):
    r';'
    return t

def t_VIRGULA(t):
    r','
    return t

def t_DFUNC(t):
    r'(function|program)[ ]+[A-Za-z_]+([ ]*\(.*\))?'
    return t

def t_FUNC(t):
    r'[A-Za-z_]+([ ]*\(.*\))'
    return t

def t_DVAR(t):
    r'[A-Za-z_]+[ ]+[A-Za-z_]+(\[.*\])?'
    return t

def t_VAR(t):
    r'[A-Za-z_]+(\[.*\])?'
    return t

def t_ATRIBUICAO(t):
    r'=[ ]*({.*})?[^;,]*'
    return t



t_ANY_ignore = ' \t\n'



def t_ANY_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

# lexer.variables = list()

lexer.input("""
/* max.p: calcula o maior inteiro duma lista desordenada
-- 2023-03-20 
-- by jcr
*/

int i = 10, a[10] = {1,2,3,4,5,6,7,8,9,10};

// Programa principal
program myMax{
  int max = a[0];
  for i in [1..9]{
    if max < a[i] {
      max = a[i];
    }
  }
  print(max);
}
""")

while tok := lexer.token():
    print(tok)

# print(lexer.variables)