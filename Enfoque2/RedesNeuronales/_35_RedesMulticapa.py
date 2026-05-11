# _35_RedesMulticapa.py
# Redes Multicapa (MLP — Multilayer Perceptron)
# Resuelve el problema de separabilidad lineal agregando capas ocultas.
# Arquitectura: Capa entrada -> Capas ocultas -> Capa salida
#
# El aprendizaje se hace con Retropropagacion (ver _36).
# Aqui mostramos la arquitectura y el paso forward en detalle.

import math
import random

print("=" * 55)
print("  REDES MULTICAPA (MLP)")
print("=" * 55)

def sigmoid(z): return 1 / (1 + math.exp(-max(-500, min(500, z))))

# ---- Arquitectura: 2 -> 3 -> 2 -> 1 (3 capas) ----
# Para clasificar puntos en 4 regiones (problema mas complejo que XOR)

class CapaDensa:
    def __init__(self, n_entrada, n_salida):
        random.seed(0)
        self.W = [[random.gauss(0, 0.5) for _ in range(n_entrada)] for _ in range(n_salida)]
        self.b = [0.0] * n_salida

    def forward(self, x):
        self.entrada = x
        self.z = [sum(self.W[j][i]*x[i] for i in range(len(x))) + self.b[j]
                  for j in range(len(self.b))]
        self.salida = [sigmoid(z) for z in self.z]
        return self.salida

# ---- Construir la red ----
capas = [
    CapaDensa(2, 4),   # capa oculta 1: 2 entradas -> 4 neuronas
    CapaDensa(4, 3),   # capa oculta 2: 4 neuronas -> 3 neuronas
    CapaDensa(3, 1),   # capa salida  : 3 neuronas -> 1 salida
]

def forward_red(x):
    activacion = x
    print(f"  Entrada: {[round(v,4) for v in activacion]}")
    for i, capa in enumerate(capas):
        activacion = capa.forward(activacion)
        print(f"  Capa {i+1} ({len(capa.b)} neuronas): {[round(v,4) for v in activacion]}")
    return activacion

print("\nArquitectura: 2 -> 4 -> 3 -> 1")
print("Activacion: Sigmoid en todas las capas\n")

# Paso forward con algunos puntos de ejemplo
ejemplos = [[0.1, 0.2], [0.9, 0.8], [0.5, 0.5]]
for x in ejemplos:
    print(f"Ejemplo {x}:")
    salida = forward_red(x)
    print(f"  Prediccion: {salida[0]:.4f}\n")

# ---- Parametros totales ----
total_params = 0
dims = [2, 4, 3, 1]
print("Parametros de la red:")
for i in range(len(dims)-1):
    params = dims[i]*dims[i+1] + dims[i+1]  # pesos + bias
    total_params += params
    print(f"  Capa {i+1}: {dims[i]}x{dims[i+1]} pesos + {dims[i+1]} bias = {params} params")
print(f"  Total: {total_params} parametros entrenables")

print("\nCapacidad de representacion:")
print("  1 capa oculta  : puede aproximar cualquier funcion continua (teorema universal)")
print("  Mas capas      : aprende representaciones jerarquicas mas eficientemente")
print("  Mas neuronas   : mas capacidad, mas riesgo de sobreajuste")
