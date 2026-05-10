# _24_NaiveBayes.py
# Clasificador Naive Bayes
# Asume que todas las caracteristicas son condicionalmente independientes dado la clase.
# P(clase | x1,...,xn) proporcional a P(clase) * producto P(xi | clase)
#
# "Naive" porque la independencia condicional rara vez se cumple en la realidad,
# pero el clasificador funciona sorprendentemente bien en la practica.

print("=" * 55)
print("  NAIVE BAYES — CLASIFICADOR")
print("=" * 55)

# ---- Dataset: clasificar correos como spam o no-spam ----
# Caracteristicas: palabras presentes (1) o ausentes (0)
# [oferta, gratis, ganaste, amigo, reunion, proyecto]

datos_entrenamiento = [
    # [oferta, gratis, ganaste, amigo, reunion, proyecto], clase
    ([1, 1, 1, 0, 0, 0], "spam"),
    ([1, 1, 0, 0, 0, 0], "spam"),
    ([0, 1, 1, 0, 0, 0], "spam"),
    ([1, 0, 1, 0, 0, 0], "spam"),
    ([0, 0, 0, 1, 1, 1], "no_spam"),
    ([0, 0, 0, 1, 0, 1], "no_spam"),
    ([0, 0, 0, 0, 1, 1], "no_spam"),
    ([0, 0, 0, 1, 1, 0], "no_spam"),
]
palabras = ["oferta", "gratis", "ganaste", "amigo", "reunion", "proyecto"]
clases   = ["spam", "no_spam"]

# ---- Entrenamiento: estimar P(clase) y P(xi | clase) ----
# Suavizado de Laplace (+1) para evitar probabilidades cero
def entrenar(datos):
    conteos_clase = {c: 0 for c in clases}
    conteos_word  = {c: [0]*len(palabras) for c in clases}
    for x, clase in datos:
        conteos_clase[clase] += 1
        for i, val in enumerate(x):
            conteos_word[clase][i] += val

    n_total = len(datos)
    p_clase = {c: conteos_clase[c]/n_total for c in clases}
    p_word  = {}
    for c in clases:
        n_c = conteos_clase[c]
        p_word[c] = [(conteos_word[c][i]+1)/(n_c+2) for i in range(len(palabras))]
    return p_clase, p_word

p_clase, p_word = entrenar(datos_entrenamiento)
print("\nProbabilidades a priori:")
for c, p in p_clase.items():
    print(f"  P({c}) = {p:.3f}")

print("\nP(palabra=1 | clase) con suavizado Laplace:")
print(f"  {'Palabra':<12}", end="")
for c in clases: print(f"{c:>10}", end="")
print()
for i, pal in enumerate(palabras):
    print(f"  {pal:<12}", end="")
    for c in clases: print(f"{p_word[c][i]:>10.3f}", end="")
    print()

# ---- Clasificacion ----
import math
def clasificar(x):
    scores = {}
    for c in clases:
        log_p = math.log(p_clase[c])
        for i, val in enumerate(x):
            p = p_word[c][i] if val == 1 else (1 - p_word[c][i])
            log_p += math.log(p + 1e-10)
        scores[c] = log_p
    return max(scores, key=scores.get), scores

print("\nClasificacion de nuevos correos:")
nuevos = [
    ([1, 1, 1, 0, 0, 0], "spam"),
    ([0, 0, 0, 1, 1, 1], "no_spam"),
    ([1, 0, 0, 1, 0, 0], "?"),
]
for x, real in nuevos:
    pred, scores = clasificar(x)
    palabras_presentes = [palabras[i] for i,v in enumerate(x) if v==1]
    print(f"  Palabras: {palabras_presentes:<35} -> Prediccion: {pred:<10} Real: {real}")
