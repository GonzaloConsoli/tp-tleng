from ply.yacc import yacc
from regex import Union, Concat, Star, Plus, Lambda

precedence = (
        # ('left', 'IF', 'THEN', 'ELSE'),
        # ('left', 'PLUS', 'MINUS'),
        # ('left', 'TIMES'),
        # ('right', 'EQUALS', 'LESS_THAN', 'GREATER_THAN'),
        # ('right', 'AND'),
        # ('right', 'OR'),
        # ('right', 'TO'),
        # ('left', 'NOT', 'UMINUS')
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
    regex : regex regex
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

def parse_and_print(string):
    startingValues = {}

    try:
        parse_result = parser.parse(string)
        evaluationResult = parse_result.evaluate(startingValues)
        print(str(evaluationResult))
    except Exception:
        print("Error during parsin.")