# _31_ComputacionNeuronal.py
# Computacion Neuronal
# La neurona artificial es una simplificacion matematica de la neurona biologica.
# Recibe entradas, las pondera, suma y aplica una funcion de activacion.
#
# Modelo de McCulloch-Pitts (1943):
#   salida = f(suma(wi * xi) + bias)
# Donde f es la funcion de activacion.

import math

print("=" * 55)
print("  COMPUTACION NEURONAL — NEURONA ARTIFICIAL")
print("=" * 55)

# ---- Modelo de una neurona ----
def neurona(entradas, pesos, bias, activacion):
    suma = sum(w * x for w, x in zip(pesos, entradas)) + bias
    return activacion(suma), suma

# ---- Funciones de activacion ----
def escalon(z):    return 1 if z >= 0 else 0
def sigmoid(z):    return 1 / (1 + math.exp(-max(-500, min(500, z))))
def tanh(z):       return math.tanh(z)
def relu(z):       return max(0, z)
def lineal(z):     return z

activaciones = {
    "Escalon":  escalon,
    "Sigmoid":  sigmoid,
    "Tanh":     tanh,
    "ReLU":     relu,
    "Lineal":   lineal,
}

print("\nNeurona con 3 entradas:")
entradas = [0.5, -0.3, 0.8]
pesos    = [0.4,  0.7, -0.2]
bias     = 0.1

suma_ponderada = sum(w*x for w,x in zip(pesos, entradas)) + bias
print(f"  Entradas : {entradas}")
print(f"  Pesos    : {pesos}")
print(f"  Bias     : {bias}")
print(f"  Suma     : {suma_ponderada:.4f}")
print(f"\n  {'Activacion':<12} {'Salida'}")
print("  " + "-" * 22)
for nombre, fn in activaciones.items():
    sal, _ = neurona(entradas, pesos, bias, fn)
    print(f"  {nombre:<12} {sal:.6f}")

# ---- Neurona como compuerta logica AND ----
print("\nNeurona como compuerta AND (funcion escalon):")
pesos_and = [1, 1]; bias_and = -1.5
print(f"  {'x1':<4} {'x2':<4} {'suma':<8} {'salida'}")
print("  " + "-" * 24)
for x1, x2 in [(0,0),(0,1),(1,0),(1,1)]:
    sal, z = neurona([x1,x2], pesos_and, bias_and, escalon)
    print(f"  {x1:<4} {x2:<4} {z:<8.1f} {sal}")

print("\nLimitacion: una sola neurona solo puede aprender funciones linealmente separables.")
print("Para XOR se necesitan multiples capas (red multicapa).")
