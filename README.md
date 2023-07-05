# TP TLeng

## Parte 2

### Gramática

La siguientes producciones corresponden a la gramática elegida. El símbolo distinguido es R y están escritas de modo tal que pueden utilizarse directamente en https://mdaines.github.io/grammophone para su análisis

```
R -> R "|" R .
R -> R R .
R -> R "*" .
R -> R "+" .
R -> R "?" .
R -> R "{" num "}" .
R -> R "{" num "," num "}" .
R -> char .
R -> "(" R ")" .
R -> "(" ")" .
R -> C .
C -> "[" X "]" .
C -> "/" "char" .
X -> char .
X -> char "-" char .
X -> char X .
X -> char "-" char X .
```

Una breve explicación de cada una:

1. R -> R "|" R: Una expresión regular puede ser una union
1. R -> R R : Una expresión regular puede ser una concatenación
1. R -> R "\*": Una expresión regular puede ser la clausura de Kleene
1. R -> R "+": Una expresión regular puede ser la clausura positiva
1. R -> R "?": Una expresión regular puede ser el opcional
1. R -> R "{" num "}" : Una expresión regular puede ser el cuantificador simple
1. R -> R "{" num "," num "}": Una expresión regular puede ser el cuantificador doble
1. R -> char: Una expresión regular puede ser un caracter
1. R -> "(" R ")" : Una expresión regular puede ser una expresión regular entre paréntesis
1. R -> "(" ")": Una expresión regular puede ser lambda entre paréntesis
1. R -> C: Una expresión regular puede ser una clase de caracteres
1. C -> "[" X "]": Una clase de caracteres comienza con [, termina con ] y posee un contenido X
1. C -> "/" "char": Una clase de caracteres especial es /d y otra /w (deberian ser \d y \w)
1. X -> char: El contenido de una clase de caracteres puede ser un caracter
1. X -> char - char: El contenido de una clase de caracteres puede ser un rango de caracteres
1. X -> char X: El contenido de una clase de caracteres puede ser un caracter seguido de más contenido
1. X -> char - char X: El contenido de una clase de caracteres puede ser un rango de caracteres seguido de más contenido
