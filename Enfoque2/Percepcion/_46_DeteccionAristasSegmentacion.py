# _46_DeteccionAristasSegmentacion.py
# Deteccion de Aristas y Segmentacion
#
# DETECCION DE ARISTAS: identifica bordes en la imagen donde hay
# cambios bruscos de intensidad. Algoritmos: Sobel, Canny.
# Una arista = gradiente de alta magnitud.
#
# SEGMENTACION: divide la imagen en regiones con propiedades similares.
# Algoritmos: umbralizado, crecimiento de regiones, watershed.

import math

print("=" * 55)
print("  DETECCION DE ARISTAS Y SEGMENTACION")
print("=" * 55)

# ---- Imagen de ejemplo 8x8 ----
imagen = [
    [10, 10, 10, 10,200,200,200,200],
    [10, 10, 10, 10,200,200,200,200],
    [10, 10, 10, 10,200,200,200,200],
    [10, 10, 10, 10,200,200,200,200],
    [10, 10, 10, 10,200,200,200,200],
    [10, 10, 10, 10,200,200,200,200],
    [10, 10, 10, 10,200,200,200,200],
    [10, 10, 10, 10,200,200,200,200],
]
F, C = len(imagen), len(imagen[0])

# ---- Operador Sobel ----
# Gx detecta bordes verticales, Gy horizontales
Gx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
Gy = [[-1,-2,-1], [ 0, 0, 0], [ 1, 2, 1]]

def sobel(img):
    resultado = [[0]*C for _ in range(F)]
    for i in range(1, F-1):
        for j in range(1, C-1):
            gx = sum(Gx[ki][kj]*img[i-1+ki][j-1+kj] for ki in range(3) for kj in range(3))
            gy = sum(Gy[ki][kj]*img[i-1+ki][j-1+kj] for ki in range(3) for kj in range(3))
            resultado[i][j] = int(math.sqrt(gx**2 + gy**2))
    return resultado

def umbralizar(img, umbral):
    return [[255 if img[i][j] >= umbral else 0 for j in range(C)] for i in range(F)]

bordes = sobel(imagen)
print("\nMagnitud del gradiente Sobel:")
for fila in bordes:
    print("  " + " ".join(f"{v:4}" for v in fila))

umbral = 100
bordes_bin = umbralizar(bordes, umbral)
print(f"\nBordes binarizados (umbral={umbral}):")
for fila in bordes_bin:
    print("  " + " ".join("█" if v > 0 else "·" for v in fila))

# ---- Segmentacion por umbralizado global ----
print("\n--- SEGMENTACION POR UMBRALIZADO ---")
umbral_seg = 100
segmentada = [[1 if imagen[i][j] > umbral_seg else 0 for j in range(C)] for i in range(F)]
print(f"Umbral de segmentacion: {umbral_seg}")
print("Segmentacion (0=fondo, 1=objeto):")
for fila in segmentada:
    print("  " + " ".join("█" if v else "·" for v in fila))

# ---- Crecimiento de regiones ----
print("\n--- CRECIMIENTO DE REGIONES ---")
def crecer_region(img, semilla, tolerancia=50):
    f0, c0 = semilla
    val_semilla = img[f0][c0]
    visitado = [[False]*C for _ in range(F)]
    region = []
    cola = [semilla]
    visitado[f0][c0] = True
    while cola:
        f, c = cola.pop(0)
        region.append((f, c))
        for df, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nf, nc = f+df, c+dc
            if 0<=nf<F and 0<=nc<C and not visitado[nf][nc]:
                if abs(img[nf][nc] - val_semilla) <= tolerancia:
                    visitado[nf][nc] = True
                    cola.append((nf, nc))
    return region

region_oscura  = crecer_region(imagen, (0, 0), tolerancia=50)
region_clara   = crecer_region(imagen, (0, 7), tolerancia=50)
print(f"Region desde (0,0) val={imagen[0][0]}: {len(region_oscura)} pixeles")
print(f"Region desde (0,7) val={imagen[0][7]}: {len(region_clara)} pixeles")
print(f"Total pixeles: {F*C} = {len(region_oscura)} + {len(region_clara)}")
