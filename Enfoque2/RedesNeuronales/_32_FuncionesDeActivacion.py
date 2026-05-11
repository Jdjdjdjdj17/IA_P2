# _32_FuncionesDeActivacion.py
# Funciones de Activacion
# Introducen no-linealidad a la red neuronal, permitiendole aprender
# patrones complejos que una combinacion lineal no podria capturar.
#
# Las mas comunes y sus caracteristicas:
#   Escalon   : clasica, no diferenciable (no sirve para backprop)
#   Sigmoid   : salida [0,1], problema de gradiente desvaneciente
#   Tanh      : salida [-1,1], centrada en 0, mejor que sigmoid
#   ReLU      : la mas usada en deep learning, rapida y efectiva
#   Leaky ReLU: corrige el problema de "neuronas muertas" de ReLU
#   Softmax   : para clasificacion multiclase (ultima capa)

import math

print("=" * 55)
print("  FUNCIONES DE ACTIVACION")
print("=" * 55)

def escalon(z):      return 1 if z >= 0 else 0
def sigmoid(z):      return 1 / (1 + math.exp(-max(-500, min(500, z))))
def tanh_fn(z):      return math.tanh(z)
def relu(z):         return max(0.0, z)
def leaky_relu(z, alpha=0.01): return z if z > 0 else alpha * z
def softmax(zs):
    mx = max(zs)
    exps = [math.exp(z - mx) for z in zs]
    total = sum(exps)
    return [e/total for e in exps]

# Derivadas (para backpropagacion)
def d_sigmoid(z):    s = sigmoid(z); return s*(1-s)
def d_tanh(z):       return 1 - math.tanh(z)**2
def d_relu(z):       return 1 if z > 0 else 0
def d_leaky(z, a=0.01): return 1 if z > 0 else a

print("\nComparacion en distintos valores de z:")
print(f"{'z':>6} {'Escalon':>9} {'Sigmoid':>9} {'Tanh':>9} {'ReLU':>9} {'LeakyReLU':>11}")
print("-" * 58)
for z in [-3, -1, -0.5, 0, 0.5, 1, 3]:
    print(f"{z:>6.1f} {escalon(z):>9.4f} {sigmoid(z):>9.4f} "
          f"{tanh_fn(z):>9.4f} {relu(z):>9.4f} {leaky_relu(z):>11.4f}")

print("\nDerivadas en distintos valores (importantes para backpropagacion):")
print(f"{'z':>6} {'d_sigmoid':>11} {'d_tanh':>9} {'d_relu':>9} {'d_leaky':>10}")
print("-" * 48)
for z in [-2, -0.5, 0, 0.5, 2]:
    print(f"{z:>6.1f} {d_sigmoid(z):>11.4f} {d_tanh(z):>9.4f} "
          f"{d_relu(z):>9.4f} {d_leaky(z):>10.4f}")

print("\nSoftmax para clasificacion multiclase (ej. 3 clases):")
logits = [2.0, 1.0, 0.1]
probs  = softmax(logits)
print(f"  Logits: {logits}")
print(f"  Probs : {[round(p,4) for p in probs]}  suma={sum(probs):.4f}")

print("\nResumen:")
print("  Sigmoid/Tanh : capas ocultas en redes pequenas")
print("  ReLU         : capas ocultas en deep learning (default)")
print("  Leaky ReLU   : cuando hay neuronas muertas con ReLU")
print("  Softmax      : ultima capa en clasificacion multiclase")
