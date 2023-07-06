from ply.yacc import yacc
from regex import Union, Concat, Star, Plus, Lambda, Char
from .lexer import tokens

precedence = (
        ('left', 'UNION'),
        ('left', 'CONCAT'),
        ('nonassoc', 'KLEENE', 'POSITIVE', 'QUESTION', 'CB_OPEN')
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
    p[0] = Star(p[1])

def p_positive_regex(p):
    '''
    regex : regex POSITIVE
    '''
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
    '''
    p[0] = Char(p[1])

def p_content_range(p):
    '''
    content : CHAR MINUS CHAR
    '''
    chars = []
    for i in range(ord(p[1]), ord(p[3])+1):
        chars.append(chr(i))

    current = Lambda()
    for char in chars:
        current = Union(current, Char(char))

    p[0] = current

def p_content_char_append(p):
    '''
    content : CHAR content
    '''
    p[0] = Union(p[1], p[2])

def p_content_range_append(p):
    '''
    content : CHAR MINUS CHAR content
    '''
    p[0] = Union(p[1], p[4])

# def p_special_classes(p):
#     '''
#     regex : BACKSLASH CHAR
#     '''
#     breakpoint()
#     char = p[2]
#     if char == 'd':
#         p[0] = '[0-9]'
#     elif char == 'w':
#         p[0] = '[a-zA-Z0-9_]'
#     else:
#         p[0] = Concat(Char('\\'), Char(char))



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
    return parser.parse(string)

def parse_and_print(string):
    startingValues = {}

    try:
        parse_result = parse(string)
        evaluationResult = parse_result.evaluate(startingValues)
        print(str(evaluationResult))
    except Exception:
        print("Error during parsin.")