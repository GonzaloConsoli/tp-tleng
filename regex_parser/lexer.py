from ply.lex import lex
import sys
import re

__all__ = ["lexer", "tokens", "tokenize"]


# Lista de tokens reconocibles por el lexer
tokens = [
    'CHAR', 
    'P_OPEN',
    'P_CLOSE',
    'UNION',
    'KLEENE',
    'POSITIVE',
    'QUESTION',
    'CB_OPEN',
    'CB_CLOSE',
    'NUM',
    'SB_OPEN',
    'SB_CLOSE',
    'BACKSLASH',
    'MINUS',
    'COMMA',
    'SIMPLE_QUANTIFIER',
    'DOUBLE_QUANTIFIER'
]

# Reglas para el analizador léxico

# Regexes para reconocer tokens simples
t_P_OPEN = r'\('
t_P_CLOSE = r'\)'
t_UNION = r'\|'
t_KLEENE = r'\*'
t_POSITIVE = r'\+'
t_QUESTION = r'\?'
t_CB_OPEN = r'\{'
t_CB_CLOSE = r'\}'
t_SB_OPEN = r'\['
t_SB_CLOSE = r'\]'
t_BACKSLASH = r'\\'
t_MINUS = r'\-'
t_COMMA = r','


# Reconocimiento de tokens complejos
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_SIMPLE_QUANTIFIER(t):
    r'{\d+}'
    t.value = int(re.findall('\d+', t.value)[0])
    return t

def t_DOUBLE_QUANTIFIER(t):
    r'{\d+,\d+}'
    t.value = re.findall('\d+', t.value)
    return t



def t_CHAR(t):
    r'[a-zA-Z0-9\s_]'
    t.value = str(t.value)
    return t


# Manejo básico de errores: omitimos caracteres extraños
def t_error(t):
    print(
        f'Ignoring illegal character {t.value[0]!r} at position {t.lexpos}', file=sys.stderr)
    t.lexer.skip(1)


# Construimos el lexer
lexer = lex()


# Aplicamos el lexer e imprimimos una lista de tokens
def tokenize_and_print(string):
    lexer.input(string)
    print(list(map(lambda token: (token.type, token.value), lexer)))