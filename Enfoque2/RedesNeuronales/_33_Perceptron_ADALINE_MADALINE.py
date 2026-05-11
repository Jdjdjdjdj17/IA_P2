# _33_Perceptron_ADALINE_MADALINE.py
# Perceptron, ADALINE y MADALINE
#
# PERCEPTRON (Rosenblatt, 1958):
#   Aprende con funcion escalon. Converge si los datos son linealmente separables.
#   Regla: w = w + lr * (y_real - y_pred) * x
#
# ADALINE (Widrow-Hoff, 1960):
#   Usa salida lineal para el aprendizaje (LMS/Least Mean Squares).
#   Regla: w = w + lr * (y_real - z) * x   (z = suma ponderada, antes de activacion)
#
# MADALINE: red de multiples ADALINE con una capa de decision.

import random
import math

print("=" * 55)
print("  PERCEPTRON, ADALINE Y MADALINE")
print("=" * 55)

# ---- Dataset: clasificacion lineal (OR logico) ----
datos = [([0,0], -1), ([0,1], 1), ([1,0], 1), ([1,1], 1)]

def dot(w, x, b):
    return sum(wi*xi for wi,xi in zip(w,x)) + b

# ==========================================
# PERCEPTRON
# ==========================================
print("\n--- PERCEPTRON ---")
w, b, lr = [0.0, 0.0], 0.0, 0.3
for epoca in range(20):
    errores = 0
    for x, y in datos:
        z    = dot(w, x, b)
        pred = 1 if z >= 0 else -1
        if pred != y:
            errores += 1
            for i in range(len(w)):
                w[i] += lr * y * x[i]
            b += lr * y
    if errores == 0:
        print(f"  Convergio en epoca {epoca+1}")
        break

print(f"  Pesos finales: w={[round(wi,3) for wi in w]}, b={b:.3f}")
print(f"  Predicciones:")
for x, y in datos:
    pred = 1 if dot(w, x, b) >= 0 else -1
    print(f"    {x} -> pred={pred}, real={y}  {'✓' if pred==y else '✗'}")

# ==========================================
# ADALINE (salida lineal para aprendizaje)
# ==========================================
print("\n--- ADALINE ---")
w2, b2, lr2 = [0.0, 0.0], 0.0, 0.1
for epoca in range(100):
    mse = 0
    for x, y in datos:
        z     = dot(w2, x, b2)          # salida lineal (antes de activacion)
        error = y - z
        mse  += error**2
        for i in range(len(w2)):
            w2[i] += lr2 * error * x[i]
        b2 += lr2 * error
    if epoca % 20 == 19:
        print(f"  Epoca {epoca+1}: MSE={mse/4:.6f}")

print(f"  Pesos finales: w={[round(wi,3) for wi in w2]}, b={b2:.3f}")
print(f"  Predicciones:")
for x, y in datos:
    z    = dot(w2, x, b2)
    pred = 1 if z >= 0 else -1
    print(f"    {x} -> z={z:.3f} pred={pred}, real={y}  {'✓' if pred==y else '✗'}")

# ==========================================
# MADALINE (concepto)
# ==========================================
print("\n--- MADALINE (descripcion) ---")
print("  Multiples ADALINE en la capa oculta + capa de decision.")
print("  Puede resolver problemas no linealmente separables (como XOR).")
print("  Regla de aprendizaje MRI: solo cambia los pesos de la neurona oculta")
print("  cuya salida esta mas cerca de 0 (la mas 'indecisa').")
print("  Antecedente directo del Perceptron Multicapa moderno.")
