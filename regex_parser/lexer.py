from ply.lex import lex
import sys

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
    'COMMA'
]

# Reglas para el analizador léxico

# Ignoramos espacios y tabulaciones
t_ignore = ' \t'

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


# Ignoramos saltos de línea y llevamos registro del número de línea actual
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Reconocimiento de tokens complejos
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_CHAR(t):
    r'[a-zA-Z0-9]'
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