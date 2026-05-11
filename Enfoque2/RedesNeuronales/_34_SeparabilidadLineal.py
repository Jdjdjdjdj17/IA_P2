# _34_SeparabilidadLineal.py
# Separabilidad Lineal
# Un problema es linealmente separable si existe un hiperplano que separa
# perfectamente las dos clases en el espacio de caracteristicas.
#
# El Perceptron SOLO converge si el problema es linealmente separable.
# XOR es el ejemplo clasico de NO separabilidad lineal.

import math

print("=" * 55)
print("  SEPARABILIDAD LINEAL")
print("=" * 55)

# ---- Verificar separabilidad lineal con Perceptron ----
def entrenar_perceptron(datos, max_epocas=100):
    w, b = [0.0]*len(datos[0][0]), 0.0
    lr   = 0.3
    for ep in range(max_epocas):
        errores = 0
        for x, y in datos:
            z    = sum(wi*xi for wi,xi in zip(w,x)) + b
            pred = 1 if z >= 0 else -1
            if pred != y:
                errores += 1
                for i in range(len(w)):
                    w[i] += lr * y * x[i]
                b += lr * y
        if errores == 0:
            return True, ep+1, w, b
    return False, max_epocas, w, b

# ---- Problemas linealmente separables ----
print("\nProblemas 2D:")
problemas = {
    "AND": [([0,0],-1),([0,1],-1),([1,0],-1),([1,1], 1)],
    "OR":  [([0,0],-1),([0,1], 1),([1,0], 1),([1,1], 1)],
    "NOT": [([0,]   , 1),([1,], -1)],
    "XOR": [([0,0],-1),([0,1], 1),([1,0], 1),([1,1],-1)],
    "XNOR":[([0,0], 1),([0,1],-1),([1,0],-1),([1,1], 1)],
}

print(f"  {'Problema':<10} {'Separable':<12} {'Epocas':<10} {'Pesos finales'}")
print("  " + "-" * 55)
for nombre, datos in problemas.items():
    sep, epocas, w, b = entrenar_perceptron(datos)
    estado = "SI" if sep else "NO"
    print(f"  {nombre:<10} {estado:<12} {epocas:<10} w={[round(x,2) for x in w]} b={round(b,2)}")

print("""
Explicacion geometrica:
  - AND/OR/NOT: existe una linea que separa + de - -> SEPARABLE
  - XOR/XNOR:  no existe ninguna linea que los separe -> NO SEPARABLE

  AND:           OR:            XOR:
  . .            . +            . +
  . +            + +            + .
  separable      separable      NO separable (necesita curva)

Solucion para no separables:
  1. Transformar el espacio de caracteristicas (kernel trick en SVM)
  2. Usar redes multicapa con capas ocultas (Perceptron Multicapa)
""")
