# Registro de cambios

**Versión actual**: 4

## Versión 4
* Se modificó la función principal del programa `tlengrep.py` para que solo
  no omita los espacios en blanco de cada línea del archivo de entrada
  (pasando el parámetro `\n` a los llamados a `line.strip`)
* Se agregaron tests para la funcionalidad de parsing de expresiones regulares.
  En detalle:
    * Se agregó el programa `test_parser.py` para ejecutar los test de parsing.
    * Se agregó el archivo `tests/parser.py` que define los casos de test de
      parsing.
    * Se agregaron líneas al archivo `tests/input/strings.txt` para tener más
      entradas de prueba.
    * Se modificaron los resultados esperados de algunos de los tests existentes
      (`/tests/regex/output`) para reflejar las nuevas cadenas de prueba:
      `r09.txt`, `r14.txt`, `r16.txt`, `r17.txt`, `r20.txt`.
    * Se agregó un nuevo caso de test para el motor de expresions regulares:
      `/tests/regex/modules/r33.py`.
    * Se agregó un archivo auxiliar `tests/utils.py` con funciones auxiliares
      para los tests.
* Se agregó compatibilidad con Python >= 3.9. Para esto, se hicieron algunos
  cambios menores en el módulo `automata/afnd.py`, reemplazando el uso de
  `StrEnum` por `Enum` y el operador de tipos `|` por `typing.Union`.
* Se eliminó un parámetro inútil del método `mark_initial_state` de la clase
  abstracta `AF`.

## Versión 3
* Se corrigió un problema en los tests que los hacía fallar espuriamente en
  Windows debido a la diferencia de convención para los finales de línea.

## Versión 2
* Se corrigió un bug en el método `normalize_states` de la clase abstracta `AF`
  que generaba problemas cuando los nuevos nombres de los estados coincidían
  con nombres de estados existentes
* Se renombró el método privado `_print_transitions` de la clase abstracta `AF`
  y sus subclases a `_transitions_to_str`, para reflejar mejor su funcionalidad
  y evitar confusiones.
