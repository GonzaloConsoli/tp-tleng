from ply.yacc import yacc
from regex import Union, Concat, Star, Plus, Lambda, Char, Empty
from .lexer import tokens

precedence = (
        ('left', 'UNION'),
        ('left', 'CONCAT'),
        ('nonassoc', 'KLEENE', 'POSITIVE', 'QUESTION', 'CB_OPEN'),
        ('nonassoc','CHAR', 
        'P_OPEN',
        'P_CLOSE',
        'CB_CLOSE',
        'NUM',
        'SB_OPEN',
        'SB_CLOSE',
        'BACKSLASH',
        'MINUS',
        'COMMA')
)

__all__ = ["parser", "parse_and_print"]


# Definimos una función para cada producción de la gramática
def p_union_regex(p):
    '''
    regex : regex UNION regex
    '''
    p[0] = Union(p[1], p[3])

def p_concat_regex(p):
    '''
    regex : regex regex %prec CONCAT
    '''
    p[0] = Concat(p[1], p[2])


def p_kleene_regex(p):
    '''
    regex :  regex KLEENE
    '''
    if isinstance(p[1], Star): raise SyntaxError
    p[0] = Star(p[1])

def p_positive_regex(p):
    '''
    regex : regex POSITIVE
    '''
    if isinstance(p[1], Plus): raise SyntaxError
    p[0] = Plus(p[1])

def p_optional_regex(p):
    '''
    regex : regex QUESTION
    '''
    p[0] = Union(p[1], Lambda())

def p_simple_quantifier(p):
    '''
    regex : regex CB_OPEN NUM CB_CLOSE
    '''
    base = p[1]
    appearances = p[3]
    current = Lambda()
    while (appearances > 0):
        current = Concat(current, base)
        appearances = appearances - 1;
    p[0] = current

def p_double_quantifier(p):
    '''
    regex : regex CB_OPEN NUM COMMA NUM CB_CLOSE
    '''
    base = p[1]
    min = p[3]
    max = p[5]
    current = Lambda()
    for i in range(0, max):
        if i < min:
            current = Concat(current, base)
        else:
            current = Union(current, Concat(current, base))
    p[0] = current

def p_char(p):
    '''
    regex : CHAR
    '''
    p[0] = Char(p[1])

def p_num(p):
    '''
    regex : NUM
    '''
    p[0] = Char(str(p[1]))

def p_parenthesis_regex(p):
    '''
    regex : P_OPEN regex P_CLOSE
    '''
    p[0] = p[2]

def p_parenthesis_lambda(p):
    '''
    regex : P_OPEN P_CLOSE
    '''
    p[0] = Lambda()

def p_class(p):
    '''
    regex : SB_OPEN content SB_CLOSE
    '''
    p[0] = p[2]

def p_content_char(p):
    '''
    content : CHAR
    content : MINUS
    content : CB_OPEN
    '''
    p[0] = Char(p[1])

def p_content_char_append(p):
    '''
    content : CHAR content
    '''
    p[0] = Union(Char(p[1]), p[2])

def p_content_num_append(p):
    '''
    content : NUM content
    '''
    p[0] = Union(Char(str(p[1])), p[2])

def p_content_num(p):
    '''
    content : NUM
    '''
    p[0] = Char(str(p[1]))

def p_content_range(p):
    '''
    content : CHAR MINUS CHAR
    '''
    if ord(p[3]) < ord(p[1]): raise SyntaxError

    chars = []
    for i in range(ord(p[1]), ord(p[3])+1):
        chars.append(chr(i))

    current = Empty()
    for char in chars:
        current = Union(current, Char(char))

    p[0] = current

def p_content_range_append(p):
    '''
    content : CHAR MINUS CHAR content
    '''
    if ord(p[3]) < ord(p[1]): raise SyntaxError

    chars = []
    for i in range(ord(p[1]), ord(p[3])+1):
        chars.append(chr(i))

    current = Empty()
    for char in chars:
        current = Union(current, Char(char))

    p[0] = Union(current, p[4])

def p_num_content_range(p):
    '''
    content : NUM MINUS NUM
    '''
    if p[3] < p[1]: raise SyntaxError

    chars = []
    for i in range(p[1], p[3]+1):
        chars.append(str(i))

    current = Empty()
    for char in chars:
        current = Union(current, Char(char))

    p[0] = current

def p_num_content_range_append(p):
    '''
    content : NUM MINUS NUM content
    '''
    chars = []
    for i in range(p[1], p[3]+1):
        chars.append(str(i))

    current = Empty()
    for char in chars:
        current = Union(current, Char(char))

    p[0] = Union(current, p[4])

def p_special_classes(p):
    '''
    regex : BACKSLASH CHAR
    '''
    char = p[2]
    if char == 'd':
        current = Empty()
        for i in range(0, 10):
            current = Union(current, Char(str(i)))
        p[0] = current
    elif char == 'w':
        current = Char('_')
        for i in range(ord('a'), ord('z')+1):
            current = Union(current, Char(chr(i)))
        for i in range(ord('A'), ord('Z')+1):
            current = Union(current, Char(chr(i)))
        for i in range(0, 10):
            current = Union(current, Char(str(i)))
        p[0] = current
    else:
        p[0] = Concat(Char('\\'), Char(char))

def p_popen(p):
    '''
    regex : BACKSLASH P_OPEN
    '''
    p[0] = Char('(')

def p_pclose(p):
    '''
    regex : BACKSLASH P_CLOSE
    '''
    p[0] = Char(')')

def p_union(p):
    '''
    regex : BACKSLASH UNION
    '''
    p[0] = Char('|')

def p_kleene(p):
    '''
    regex : BACKSLASH KLEENE
    content : BACKSLASH KLEENE
    '''
    p[0] = Char('*')

def p_positive(p):
    '''
    regex : BACKSLASH POSITIVE
    content : BACKSLASH POSITIVE
    '''
    p[0] = Char('+')


def p_question(p):
    '''
    regex : BACKSLASH QUESTION
    '''
    p[0] = Char('?')

def p_cbopen(p):
    '''
    regex : CB_OPEN
    regex : BACKSLASH CB_OPEN
    '''
    p[0] = Char('{')

def p_cbclose(p):
    '''
    regex : CB_CLOSE
    regex : BACKSLASH CB_CLOSE
    '''
    p[0] = Char('}')

def p_sbopen(p):
    '''
    regex : BACKSLASH SB_OPEN
    content : BACKSLASH SB_OPEN
    '''
    p[0] = Char('[')

def p_sbclose(p):
    '''
    regex : BACKSLASH SB_CLOSE
    '''
    p[0] = Char(']')

def p_backslash(p):
    '''
    regex : BACKSLASH BACKSLASH
    '''
    p[0] = Char('\\')

def p_minus(p):
    '''
    regex : MINUS
    '''
    p[0] = Char('-')

def p_comma(p):
    '''
    regex : BACKSLASH COMMA
    '''
    p[0] = Char(',')

def p_empty_class(p):
    '''
    regex : SB_OPEN SB_CLOSE
    '''
    p[0] = Empty()

# Manejo de errores
def p_error(p):
    if p:
        raise ParseError(
            f'Unexpected token {p.value!r} at position {p.lexpos}')
    else:
        raise ParseError(f'Unexpected end of expression')


class ParseError(Exception):
    pass


parser = yacc()

def parse(string):
    if string == '': return Lambda()
    return parser.parse(string)

def parse_and_print(string):
    startingValues = {}

    try:
        parse_result = parse(string)
        evaluationResult = parse_result.evaluate(startingValues)
        print(str(evaluationResult))
    except Exception:
        print("Error during parsin.")