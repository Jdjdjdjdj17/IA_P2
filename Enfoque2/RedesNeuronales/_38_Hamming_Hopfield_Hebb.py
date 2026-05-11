# _38_Hamming_Hopfield_Hebb.py
# Hamming, Hopfield y Regla de Hebb
#
# REGLA DE HEBB (1949): "Las neuronas que se activan juntas, se conectan."
#   w_ij += x_i * x_j   (aprendizaje hebbiano)
#
# RED DE HOPFIELD: red recurrente totalmente conectada que funciona como
#   memoria asociativa. Almacena patrones y los recupera aunque esten
#   incompletos o con ruido. Usa la regla de Hebb para aprender.
#
# RED DE HAMMING: clasifica patrones segun la distancia de Hamming
#   (numero de bits diferentes) al patron mas similar.

import random
import math

print("=" * 55)
print("  HEBB, HOPFIELD Y HAMMING")
print("=" * 55)

# ============================================================
# REGLA DE HEBB — aprendizaje hebbiano simple
# ============================================================
print("\n--- REGLA DE HEBB ---")
N = 4  # neuronas
patrones = [
    [1, 1,-1,-1],
    [-1,-1, 1, 1],
]
W = [[0.0]*N for _ in range(N)]
for p in patrones:
    for i in range(N):
        for j in range(N):
            if i != j:
                W[i][j] += p[i]*p[j] / N

print(f"Patrones almacenados: {patrones}")
print(f"Matriz de pesos Hebb:")
for fila in W:
    print(f"  {[round(w,2) for w in fila]}")

# ============================================================
# RED DE HOPFIELD — memoria asociativa
# ============================================================
print("\n--- RED DE HOPFIELD ---")

def actualizar_hopfield(estado, W, N):
    nuevo = estado[:]
    for i in range(N):
        s = sum(W[i][j]*estado[j] for j in range(N))
        nuevo[i] = 1 if s >= 0 else -1
    return nuevo

def energia(estado, W, N):
    return -0.5 * sum(W[i][j]*estado[i]*estado[j]
                      for i in range(N) for j in range(N))

# Recuperar patron con ruido
patron_ruidoso = [1, 1, 1, -1]   # correcto seria [1,1,-1,-1]
print(f"Patron almacenado: {patrones[0]}")
print(f"Patron con ruido : {patron_ruidoso}")

estado = patron_ruidoso[:]
for it in range(10):
    nuevo = actualizar_hopfield(estado, W, N)
    e = energia(estado, W, N)
    print(f"  Iter {it}: {estado}  E={e:.3f}")
    if nuevo == estado:
        print(f"  Convergio en iter {it}")
        break
    estado = nuevo

print(f"Patron recuperado: {estado}")
print(f"Patron original  : {patrones[0]}  {'✓' if estado==patrones[0] else '✗'}")

# ============================================================
# RED DE HAMMING — distancia de Hamming
# ============================================================
print("\n--- RED DE HAMMING ---")

def distancia_hamming(a, b):
    return sum(1 for ai, bi in zip(a,b) if ai != bi)

patrones_hamming = [
    [1,0,1,0,1],
    [0,1,0,1,0],
    [1,1,0,0,1],
]
consulta = [1,0,1,1,1]   # patron con 1 bit diferente al primero

print(f"Patrones: {patrones_hamming}")
print(f"Consulta: {consulta}")
print(f"\nDistancias de Hamming:")
mejor_d = float('inf'); mejor_p = None
for i, p in enumerate(patrones_hamming):
    d = distancia_hamming(consulta, p)
    print(f"  P{i}: {p}  ->  d={d}")
    if d < mejor_d:
        mejor_d = d; mejor_p = i

print(f"\nClasificado como: Patron {mejor_p} (d={mejor_d})")
