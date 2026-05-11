# _37_MapasKohonen.py
# Mapas Autoorganizados de Kohonen (SOM — Self-Organizing Map)
# Red neuronal NO supervisada que aprende a proyectar datos de alta dimension
# en una cuadricula 2D, preservando la topologia (vecinos en datos -> vecinos en mapa).
#
# Algoritmo:
#   1. Para cada dato, encontrar la neurona ganadora (BMU: Best Matching Unit)
#   2. Actualizar BMU y sus vecinas hacia el dato
#   3. Reducir la tasa de aprendizaje y el radio de vecindad con el tiempo

import random
import math

print("=" * 55)
print("  MAPAS AUTOORGANIZADOS DE KOHONEN (SOM)")
print("=" * 55)

# ---- SOM 4x4 para datos 3D (colores RGB) ----
FILAS, COLS = 4, 4
DIM = 3   # dimension de los datos (R, G, B)
random.seed(7)

# Inicializar pesos aleatorios [0,1]
pesos = [[[random.random() for _ in range(DIM)]
          for _ in range(COLS)]
         for _ in range(FILAS)]

# Datos: colores RGB normalizados [0,1]
datos = [
    [1.0, 0.0, 0.0],  # rojo
    [0.0, 1.0, 0.0],  # verde
    [0.0, 0.0, 1.0],  # azul
    [1.0, 1.0, 0.0],  # amarillo
    [1.0, 0.0, 1.0],  # magenta
    [0.0, 1.0, 1.0],  # cyan
    [1.0, 1.0, 1.0],  # blanco
    [0.0, 0.0, 0.0],  # negro
    [0.5, 0.5, 0.5],  # gris
    [1.0, 0.5, 0.0],  # naranja
]

def distancia_euclid(a, b):
    return math.sqrt(sum((ai-bi)**2 for ai,bi in zip(a,b)))

def bmu(dato, pesos):
    """Mejor neurona ganadora"""
    mejor = (0, 0); mejor_d = float('inf')
    for f in range(FILAS):
        for c in range(COLS):
            d = distancia_euclid(dato, pesos[f][c])
            if d < mejor_d:
                mejor_d = d; mejor = (f, c)
    return mejor

def vecindad(bmu_fc, f, c, radio):
    """Funcion gaussiana de vecindad"""
    dist2 = (bmu_fc[0]-f)**2 + (bmu_fc[1]-c)**2
    return math.exp(-dist2 / (2*radio**2))

# ---- Entrenamiento ----
n_epocas    = 500
lr0         = 0.5
radio0      = max(FILAS, COLS) / 2

print(f"\nSOM {FILAS}x{COLS}, datos RGB, {n_epocas} epocas")
print(f"lr0={lr0}, radio0={radio0:.1f}\n")

for ep in range(n_epocas):
    lr    = lr0    * math.exp(-ep / n_epocas)
    radio = radio0 * math.exp(-ep / n_epocas)
    dato  = random.choice(datos)
    b     = bmu(dato, pesos)

    for f in range(FILAS):
        for c in range(COLS):
            h = vecindad(b, f, c, max(radio, 0.5))
            for d in range(DIM):
                pesos[f][c][d] += lr * h * (dato[d] - pesos[f][c][d])

# ---- Mostrar mapa: asignar cada posicion al color mas cercano ----
nombres_colores = {
    (1,0,0):"rojo",(0,1,0):"verde",(0,0,1):"azul",
    (1,1,0):"amarillo",(1,0,1):"magenta",(0,1,1):"cyan",
    (1,1,1):"blanco",(0,0,0):"negro",(0.5,0.5,0.5):"gris",(1,0.5,0):"naranja"
}

print("Mapa SOM entrenado (color mas cercano a cada neurona):")
for f in range(FILAS):
    fila = ""
    for c in range(COLS):
        mejor_d = float('inf'); mejor_nombre = "?"
        for dato in datos:
            d = distancia_euclid(dato, pesos[f][c])
            if d < mejor_d:
                mejor_d = d
                mejor_nombre = next((v for k,v in nombres_colores.items()
                                    if distancia_euclid(dato,list(k))<0.01), "?")
        fila += f"{mejor_nombre:<11}"
    print(f"  {fila}")

print("\nColores similares deberian quedar en posiciones cercanas del mapa.")
