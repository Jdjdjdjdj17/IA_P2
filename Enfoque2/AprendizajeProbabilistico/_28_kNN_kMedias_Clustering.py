# _28_kNN_kMedias_Clustering.py
# k-NN, k-Medias y Clustering
# k-NN (k Vecinos mas Cercanos): clasificacion supervisada
#   Clasifica un punto nuevo segun la mayoria de sus k vecinos mas cercanos.
# k-Medias: ya implementado en _26 (clustering no supervisado)
# Aqui implementamos k-NN desde cero y comparamos ambos enfoques.

import math
import random

print("=" * 55)
print("  k-NN, k-MEDIAS Y CLUSTERING")
print("=" * 55)

# ---- Dataset: puntos 2D con 3 clases ----
random.seed(3)
def generar(cx, cy, clase, n=20):
    return [((cx+random.gauss(0,0.8), cy+random.gauss(0,0.8)), clase) for _ in range(n)]

datos = generar(1,1,"A") + generar(4,4,"B") + generar(1,4,"C")
random.shuffle(datos)

# Separar en train (80%) y test (20%)
corte = int(len(datos)*0.8)
train = datos[:corte]
test  = datos[corte:]

def distancia(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def knn(punto, train, k):
    """Clasifica 'punto' usando los k vecinos mas cercanos"""
    vecinos = sorted(train, key=lambda d: distancia(punto, d[0]))[:k]
    # Mayoria de votos
    votos = {}
    for _, clase in vecinos:
        votos[clase] = votos.get(clase, 0) + 1
    return max(votos, key=votos.get)

print(f"\nDataset: {len(datos)} puntos, clases A/B/C")
print(f"Train: {len(train)}  Test: {len(test)}\n")

print(f"Resultados k-NN para distintos valores de k:")
print(f"{'k':<5} {'Correctos':<12} {'Precision'}")
print("-" * 28)
for k in [1, 3, 5, 7, 9]:
    correctos = sum(1 for punto, clase_real in test
                    if knn(punto, train, k) == clase_real)
    print(f"{k:<5} {correctos}/{len(test):<10} {correctos/len(test)*100:.1f}%")

# ---- Clasificacion de un punto nuevo ----
nuevo = (2.5, 2.5)
print(f"\nPunto nuevo: {nuevo}")
for k in [1, 3, 5]:
    pred = knn(nuevo, train, k)
    print(f"  k={k} -> Clase predicha: {pred}")

# ---- Diferencia conceptual ----
print(f"\nDiferencia clave:")
print(f"  k-NN    : supervisado (necesita etiquetas), clasifica puntos nuevos")
print(f"  k-Medias: no supervisado (sin etiquetas), descubre grupos en los datos")
print(f"  Ambos usan distancia euclidiana como medida de similitud")
