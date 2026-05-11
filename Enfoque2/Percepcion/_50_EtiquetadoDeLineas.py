# _50_EtiquetadoDeLineas.py
# Etiquetado de Lineas (Line Labeling)
# Tecnica de vision por computador para interpretar imagenes de objetos polihedricos.
# A cada segmento de linea en la imagen se le asigna una etiqueta que indica
# su tipo en la escena 3D:
#   +  : arista convexa (doblez hacia afuera)
#   -  : arista concava (doblez hacia adentro)
#   -> : arista de contorno (borde del objeto)
#
# Algoritmo de Waltz: propaga restricciones hasta encontrar una interpretacion valida.

print("=" * 55)
print("  ETIQUETADO DE LINEAS (LINE LABELING)")
print("=" * 55)

# ---- Uniones validas (Waltz) para objetos polihedricos ----
# Cada union es una lista de etiquetas validas para las lineas que convergen en ella.
# Notacion: L=linea, etiquetas {'+','-','>','<'}
#
# Tipos de uniones:
#   Arrow (Y): 3 lineas, una de ellas es el "cuerpo"
#   Fork (Y):  3 lineas que se separan
#   T:         una linea es tapada por otra
#   L:         2 lineas

print("\nTipos de etiquetas para aristas:")
etiquetas_descrip = {
    "+":  "Arista convexa  (doblez hacia afuera, visible desde frente)",
    "-":  "Arista concava  (doblez hacia adentro, grieta o esquina interior)",
    ">":  "Contorno derecho (borde exterior del objeto, ocluye fondo)",
    "<":  "Contorno izquierdo (borde exterior, direccion opuesta)",
}
for etiq, desc in etiquetas_descrip.items():
    print(f"  [{etiq}] {desc}")

# ---- Restricciones de junctions (Huffman-Clowes) ----
# Para cada tipo de junction, lista de combinaciones validas de etiquetas
junctions_validos = {
    "FORK_Y": [
        ("+", "+", "+"),
        ("-", "-", "-"),
        ("+", "-", "-"),
        ("-", "+", "+"),
    ],
    "ARROW_Y": [
        ("+", ">", "<"),
        ("+", "<", ">"),
        ("-", ">", "<"),
    ],
    "T": [
        (">", "+", "-"),
        (">", "-", "+"),
        ("<", "+", "-"),
    ],
    "L": [
        (">", "<"),
        ("+", ">"),
        ("-", "<"),
        (">", "+"),
        ("<", "-"),
    ],
}

print("\nCombinaciones validas por tipo de union (Huffman-Clowes):")
for tipo, combis in junctions_validos.items():
    print(f"\n  Junction {tipo}:")
    for combi in combis:
        print(f"    {combi}")

# ---- Ejemplo: cubo simple ----
print("\n--- Ejemplo: interpretacion de esquina de cubo ---")
print("  La esquina frontal-superior-izquierda de un cubo es un FORK_Y")
print("  En una imagen 2D, 3 lineas convergen en ese punto.")
print()

escena = "cubo_esquina_frontal"
junction_tipo = "FORK_Y"
interpretaciones = junctions_validos[junction_tipo]

print(f"  Escena: {escena}")
print(f"  Tipo de junction: {junction_tipo}")
print(f"  Interpretaciones validas:")
for i, interp in enumerate(interpretaciones):
    print(f"    {i+1}. Linea1={interp[0]}  Linea2={interp[1]}  Linea3={interp[2]}")

print("""
Algoritmo de Waltz (propagacion de restricciones):
  1. Asignar todas las etiquetas posibles a cada linea
  2. Para cada junction, eliminar combinaciones invalidas
  3. Propagar: si una linea pierde etiquetas, re-revisar sus junctions vecinos
  4. Repetir hasta convergencia -> quedan solo las interpretaciones consistentes
  
  Si quedan 0 interpretaciones: la imagen es imposible (figura de Escher)
  Si queda 1: interpretacion unica
  Si quedan varias: ambiguedad perceptual
""")
