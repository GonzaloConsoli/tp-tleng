# TP TLeng

## Parte 2

### Gramática

La siguientes producciones corresponden a la gramática elegida. El símbolo distinguido es R y están escritas de modo tal que pueden utilizarse directamente en https://mdaines.github.io/grammophone para su análisis

```
R -> B .
R -> U .
R -> char .
R -> C .
R -> "(" R ")" .
R -> "(" ")" .
B -> R "|" R .
B -> R R .
U -> R "*" .
U -> R "+" .
U -> R "?" .
U -> R "{" n "}" .
U -> R "{" n "," m "}" .
C -> "[" X "]" .
C -> "/" "d" .
C -> "/" "w" .
X -> char .
X -> char "-" char .
X -> char X .
X -> char "-" char X .
```

Una breve explicación de cada una:

1. R -> B: Una expresión regular puede ser un operador binario
1. R -> U: Una expresión regular puede ser un operador unario
1. R -> char: Una expresión regular puede ser un caracter
1. R -> C: Una expresión regular puede ser una clase de caracteres
1. R -> "(" R ")" : Una expresión regular puede ser una expresión regular entre paréntesis
1. R -> "(" ")": Una expresión regular puede ser lambda entre paréntesis
1. B -> R "|" R: Un operador binario es la unión
1. B -> R R: Un operador binario es la concatenación
1. U -> R "\*": Un operador unario es la clausura de Kleene
1. U -> R "+": Un operador unario es la clausura positiva
1. U -> R "?": Un operador unario es el opcional
1. U -> R "{" n "}" : Un operador unario es el cuantificador simple
1. U -> R "{" n "," n "}": Un operador unario es el cuantificador doble
1. C -> "[" X "]": Una clase de caracteres comienza con [, termina con ] y posee un contenido X
1. C -> "/" "d": Una clase de caracteres especial es /d (deberia ser \d)
1. C -> "/" "w": Una clase de caracteres especial es /w (deberia ser \w)
1. X -> char: El contenido de una clase de caracteres puede ser un caracter
1. X -> char - char: El contenido de una clase de caracteres puede ser un rango de caracteres
1. X -> char X: El contenido de una clase de caracteres puede ser un caracter seguido de más contenido
1. X -> char - char X: El contenido de una clase de caracteres puede ser un rango de caracteres seguido de más contenido
