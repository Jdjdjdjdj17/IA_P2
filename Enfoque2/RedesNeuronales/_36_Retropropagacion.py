# _36_Retropropagacion.py
# Retropropagacion del Error (Backpropagation)
# Algoritmo para calcular el gradiente del error respecto a cada peso de la red.
# Usa la regla de la cadena del calculo diferencial para propagar el error
# desde la salida hacia la entrada, capa por capa.
#
# Pasos:
#   1. Forward: calcular salidas de cada capa
#   2. Calcular error en la salida
#   3. Backward: propagar el error hacia atras actualizando pesos

import math
import random

print("=" * 55)
print("  RETROPROPAGACION DEL ERROR (BACKPROPAGATION)")
print("=" * 55)

def sigmoid(z):      return 1/(1+math.exp(-max(-500,min(500,z))))
def d_sigmoid(s):    return s*(1-s)   # s ya es sigmoid(z)

# ---- Red 2->2->1 para aprender XOR ----
random.seed(42)
def rw(): return random.gauss(0, 0.5)

# Capa oculta: 2 neuronas
W1 = [[rw(),rw()],[rw(),rw()]]
b1 = [rw(), rw()]
# Capa salida: 1 neurona
W2 = [rw(), rw()]
b2 = rw()

lr   = 0.5
datos = [([0,0],0),([0,1],1),([1,0],1),([1,1],0)]

def forward(x):
    # Capa oculta
    z1 = [W1[j][0]*x[0]+W1[j][1]*x[1]+b1[j] for j in range(2)]
    h  = [sigmoid(z) for z in z1]
    # Capa salida
    z2 = W2[0]*h[0]+W2[1]*h[1]+b2
    y  = sigmoid(z2)
    return h, z1, y, z2

def backward_y_actualizar(x, y_real, h, z1, y, z2):
    global W1, b1, W2, b2

    # ---- Gradiente en la salida ----
    d_out = (y - y_real) * d_sigmoid(y)   # dL/dz2

    # ---- Actualizar W2, b2 ----
    for j in range(2):
        W2[j] -= lr * d_out * h[j]
    b2 -= lr * d_out

    # ---- Gradiente en la capa oculta ----
    for j in range(2):
        d_h = d_out * W2[j] * d_sigmoid(h[j])   # dL/dz1[j]
        # Actualizar W1[j], b1[j]
        W1[j][0] -= lr * d_h * x[0]
        W1[j][1] -= lr * d_h * x[1]
        b1[j]    -= lr * d_h

print(f"\nEntrenando XOR con red 2->2->1, lr={lr}\n")
print(f"{'Epoca':<8} {'Loss MSE':<12} {'Preds'}")
print("-" * 45)

for ep in range(10001):
    random.shuffle(datos)
    mse = 0
    for x, y_real in datos:
        h, z1, y_pred, z2 = forward(x)
        mse += (y_pred - y_real)**2
        backward_y_actualizar(x, y_real, h, z1, y_pred, z2)

    if ep % 2000 == 0:
        preds = []
        for x, _ in sorted(datos):
            _, _, y_pred, _ = forward(x)
            preds.append(f"{round(y_pred,3)}")
        print(f"{ep:<8} {mse/4:<12.6f} {preds}")

print(f"\nPredicciones finales:")
for x, y_real in sorted(datos):
    _, _, y_pred, _ = forward(x)
    pred = 1 if y_pred >= 0.5 else 0
    print(f"  XOR{x}={y_real}  red={y_pred:.4f} -> {pred}  {'✓' if pred==y_real else '✗'}")
