# _30_DeepLearning.py
# Aprendizaje Profundo (Deep Learning)
# Redes neuronales con multiples capas ocultas que aprenden representaciones
# jerarquicas de los datos. Cada capa extrae caracteristicas mas abstractas.
#
# Aqui implementamos una red neuronal multicapa (MLP) desde cero
# para clasificar el problema XOR (no linealmente separable).

import math
import random

print("=" * 55)
print("  DEEP LEARNING — RED MULTICAPA (MLP)")
print("=" * 55)

# ---- Funciones de activacion ----
def sigmoid(x):
    return 1 / (1 + math.exp(-max(-500, min(500, x))))

def sigmoid_deriv(s):  # s ya es sigmoid(x)
    return s * (1 - s)

def relu(x):
    return max(0, x)

def relu_deriv(x):
    return 1 if x > 0 else 0

# ---- Red: 2 entradas -> 4 neuronas ocultas -> 1 salida ----
# Para aprender XOR: (0,0)->0, (0,1)->1, (1,0)->1, (1,1)->0

random.seed(42)
def rand_w(): return random.gauss(0, 0.5)

# Pesos capa oculta (2 entradas + bias -> 4 neuronas)
W1 = [[rand_w() for _ in range(2)] for _ in range(4)]
b1 = [rand_w() for _ in range(4)]

# Pesos capa salida (4 neuronas + bias -> 1 salida)
W2 = [rand_w() for _ in range(4)]
b2 = rand_w()

lr = 0.5
datos = [([0,0], 0), ([0,1], 1), ([1,0], 1), ([1,1], 0)]

print(f"\nProblema XOR: (0,0)->0, (0,1)->1, (1,0)->1, (1,1)->0")
print(f"Arquitectura: 2 -> 4 (sigmoid) -> 1 (sigmoid)")
print(f"Learning rate: {lr}\n")
print(f"{'Epoca':<8} {'Loss MSE'}")
print("-" * 22)

for epoca in range(5001):
    total_loss = 0
    random.shuffle(datos)

    for x, y_real in datos:
        # ---- Forward ----
        h_pre = [sum(W1[j][i]*x[i] for i in range(2)) + b1[j] for j in range(4)]
        h     = [sigmoid(v) for v in h_pre]
        y_pre = sum(W2[j]*h[j] for j in range(4)) + b2
        y     = sigmoid(y_pre)
        total_loss += (y - y_real)**2

        # ---- Backward ----
        d_out = (y - y_real) * sigmoid_deriv(y)
        for j in range(4):
            d_h = d_out * W2[j] * sigmoid_deriv(h[j])
            for i in range(2):
                W1[j][i] -= lr * d_h * x[i]
            b1[j] -= lr * d_h
            W2[j]  -= lr * d_out * h[j]
        b2 -= lr * d_out

    if epoca % 1000 == 0:
        print(f"{epoca:<8} {total_loss/4:.6f}")

print(f"\nPredicciones finales:")
for x, y_real in datos:
    h     = [sigmoid(sum(W1[j][i]*x[i] for i in range(2)) + b1[j]) for j in range(4)]
    y_pre = sigmoid(sum(W2[j]*h[j] for j in range(4)) + b2)
    pred  = 1 if y_pre >= 0.5 else 0
    ok    = "✓" if pred == y_real else "✗"
    print(f"  XOR{x} = {y_real}  |  Red: {y_pre:.4f} -> {pred}  {ok}")
