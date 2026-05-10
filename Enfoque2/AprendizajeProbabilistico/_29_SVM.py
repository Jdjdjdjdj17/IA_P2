# _29_SVM.py
# Maquinas de Vectores Soporte (SVM — Support Vector Machine)
# Encuentra el hiperplano que MAXIMIZA el margen entre dos clases.
# Los "vectores soporte" son los puntos mas cercanos al hiperplano.
#
# Version lineal (sin nucleo): w*x + b = 0
# Con nucleo (kernel): permite separar datos no linealmente separables
# proyectandolos a un espacio de mayor dimension.
#
# Aqui implementamos un SVM lineal simple con gradiente descendente.

import random
import math

print("=" * 55)
print("  SVM — MAQUINAS DE VECTORES SOPORTE")
print("=" * 55)

# ---- Dataset linealmente separable: 2 clases en 2D ----
random.seed(5)
datos = []
for _ in range(30):
    x1 = random.uniform(0, 2); x2 = random.uniform(0, 2)
    datos.append(([x1, x2], 1))    # clase +1: cuadrante bajo-izquierdo
for _ in range(30):
    x1 = random.uniform(3, 5); x2 = random.uniform(3, 5)
    datos.append(([x1, x2], -1))   # clase -1: cuadrante alto-derecho
random.shuffle(datos)

# ---- SVM con gradiente descendente (Hinge Loss) ----
# Minimiza: (1/2)||w||^2 + C * suma max(0, 1 - y*(w*x+b))
# Gradiente:
#   Si y*(w*x+b) >= 1: dw = w,         db = 0
#   Si y*(w*x+b) <  1: dw = w - C*y*x, db = C*y

w  = [0.0, 0.0]
b  = 0.0
lr = 0.01
C  = 1.0
epochs = 200

print(f"\nDataset: 60 puntos, 2 clases")
print(f"Parametros: lr={lr}, C={C}, epochs={epochs}\n")

for ep in range(epochs):
    random.shuffle(datos)
    total_loss = 0
    for x, y in datos:
        score = sum(w[i]*x[i] for i in range(2)) + b
        hinge = max(0, 1 - y*score)
        total_loss += 0.5*sum(wi**2 for wi in w) + C*hinge

        if y*score < 1:  # dentro del margen o clasificado mal
            for i in range(2):
                w[i] = w[i]*(1-lr) + lr*C*y*x[i]
            b += lr*C*y
        else:            # clasificado correctamente fuera del margen
            for i in range(2):
                w[i] = w[i]*(1-lr)

    if ep % 50 == 49:
        print(f"  Epoch {ep+1}: Loss={total_loss:.4f}  w={[round(wi,3) for wi in w]}  b={b:.3f}")

# ---- Evaluacion ----
correctos = 0
for x, y in datos:
    pred = 1 if sum(w[i]*x[i] for i in range(2)) + b >= 0 else -1
    if pred == y: correctos += 1

print(f"\nResultado:")
print(f"  Hiperplano: {w[0]:.3f}*x1 + {w[1]:.3f}*x2 + {b:.3f} = 0")
print(f"  Precision en train: {correctos}/{len(datos)} = {correctos/len(datos)*100:.1f}%")
print(f"\nKernels comunes para datos no lineales:")
print(f"  - Lineal:      K(x,z) = x·z")
print(f"  - Polinomial:  K(x,z) = (x·z + 1)^d")
print(f"  - RBF/Gaussiano: K(x,z) = exp(-||x-z||^2 / 2sigma^2)  <- el mas usado")
