# _45_Preprocesado_Filtros.py
# Preprocesado de Imagen: Filtros
# Antes de analizar una imagen se aplican filtros para:
#   - Reducir ruido (suavizado)
#   - Resaltar caracteristicas (nitidez, bordes)
#
# Una imagen es una matriz de pixeles con valores de intensidad [0, 255].
# Los filtros se aplican mediante CONVOLUCION: deslizar un kernel sobre la imagen.
# resultado[i][j] = suma de (kernel * region_imagen centrada en i,j)

print("=" * 55)
print("  PREPROCESADO DE IMAGEN — FILTROS")
print("=" * 55)

# ---- Imagen de ejemplo 6x6 (escala de grises) ----
imagen = [
    [ 10,  10,  10,  10,  10,  10],
    [ 10,  10,  10,  10,  10,  10],
    [ 10,  10, 200, 200,  10,  10],
    [ 10,  10, 200, 200,  10,  10],
    [ 10,  10,  10,  10,  10,  10],
    [ 10,  10,  10,  10,  10,  10],
]
F, C = len(imagen), len(imagen[0])

def convolucionar(img, kernel):
    """Aplica un kernel de convolucion a la imagen (sin padding)"""
    k = len(kernel)
    margen = k // 2
    resultado = [[0.0]*C for _ in range(F)]
    for i in range(margen, F-margen):
        for j in range(margen, C-margen):
            suma = 0
            for ki in range(k):
                for kj in range(k):
                    suma += kernel[ki][kj] * img[i-margen+ki][j-margen+kj]
            resultado[i][j] = round(suma, 2)
    return resultado

def imprimir_imagen(img, titulo):
    print(f"\n{titulo}:")
    for fila in img:
        print("  " + "  ".join(f"{v:6.1f}" for v in fila))

# ---- Filtro de suavizado (promedio) 3x3 ----
kernel_promedio = [
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9],
]

# ---- Filtro Gaussiano 3x3 ----
kernel_gauss = [
    [1/16, 2/16, 1/16],
    [2/16, 4/16, 2/16],
    [1/16, 2/16, 1/16],
]

# ---- Filtro de nitidez (sharpening) ----
kernel_nitidez = [
    [ 0, -1,  0],
    [-1,  5, -1],
    [ 0, -1,  0],
]

# ---- Filtro de deteccion de bordes (Laplaciano) ----
kernel_laplaciano = [
    [ 0,  1,  0],
    [ 1, -4,  1],
    [ 0,  1,  0],
]

imprimir_imagen(imagen, "Imagen original")
imprimir_imagen(convolucionar(imagen, kernel_promedio),  "Filtro Promedio 3x3 (suavizado)")
imprimir_imagen(convolucionar(imagen, kernel_gauss),     "Filtro Gaussiano 3x3 (suavizado con peso)")
imprimir_imagen(convolucionar(imagen, kernel_nitidez),   "Filtro Nitidez")
imprimir_imagen(convolucionar(imagen, kernel_laplaciano),"Filtro Laplaciano (bordes)")

print("""
Tipos de filtros:
  Paso-bajo (suavizado):  promedio, gaussiano -> elimina ruido de alta frecuencia
  Paso-alto (bordes):     laplaciano, sobel   -> resalta cambios bruscos
  Nitidez:                combinacion de la imagen original y paso-alto
""")
