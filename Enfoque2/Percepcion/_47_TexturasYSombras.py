# _47_TexturasYSombras.py
# Texturas y Sombras
#
# TEXTURAS: patrones repetitivos en una region de la imagen.
# Se describen con estadisticas de la imagen: media, varianza, energia, contraste.
# Matriz GLCM (Gray-Level Co-occurrence Matrix): cuenta pares de pixeles
# con ciertas intensidades en una direccion dada.
#
# SOMBRAS: regiones oscuras causadas por oclusiones de luz.
# La deteccion de sombras es importante para separar objeto de sombra
# en vision por computador.

import math
from collections import defaultdict

print("=" * 55)
print("  TEXTURAS Y SOMBRAS")
print("=" * 55)

# ---- Dos regiones con texturas distintas ----
# Region uniforme (baja textura)
region_lisa = [
    [100, 102, 101, 100],
    [101, 100, 102, 101],
    [100, 101, 100, 102],
    [102, 100, 101, 100],
]

# Region rugosa (alta textura)
region_rugosa = [
    [20, 200,  20, 200],
    [200,  20, 200,  20],
    [20, 200,  20, 200],
    [200,  20, 200,  20],
]

def estadisticas(region):
    pixeles = [p for fila in region for p in fila]
    n   = len(pixeles)
    mu  = sum(pixeles) / n
    var = sum((p-mu)**2 for p in pixeles) / n
    return mu, math.sqrt(var)

def energia_textura(region):
    """Energia: sum(p^2) normalizado — alta en imagenes uniformes"""
    pixeles = [p/255 for fila in region for p in fila]
    return sum(p**2 for p in pixeles) / len(pixeles)

def contraste_glcm(region):
    """Contraste basado en diferencias entre pixeles adyacentes horizontales"""
    contraste = 0
    pares = 0
    F, C = len(region), len(region[0])
    for i in range(F):
        for j in range(C-1):
            contraste += (region[i][j] - region[i][j+1])**2
            pares += 1
    return contraste / pares if pares > 0 else 0

print("\n--- ANALISIS DE TEXTURAS ---")
for nombre, region in [("Lisa (baja textura)", region_lisa),
                        ("Rugosa (alta textura)", region_rugosa)]:
    mu, sigma = estadisticas(region)
    energia   = energia_textura(region)
    contraste = contraste_glcm(region)
    print(f"\n{nombre}:")
    print(f"  Media    : {mu:.2f}")
    print(f"  Std dev  : {sigma:.2f}   <- baja=uniforme, alta=variable")
    print(f"  Energia  : {energia:.4f} <- alta=uniforme, baja=variada")
    print(f"  Contraste: {contraste:.2f} <- bajo=suave, alto=rugoso")

# ---- Deteccion de sombras ----
print("\n--- DETECCION DE SOMBRAS ---")
print("Modelo simplificado: sombras son regiones oscuras con baja saturacion")

def detectar_sombra(intensidad, umbral_oscuro=80):
    """Un pixel es sombra si es oscuro (baja intensidad)"""
    return intensidad < umbral_oscuro

imagen_con_sombra = [
    [200, 200, 200, 180,  50,  40,  60, 200],
    [200, 200, 180,  55,  45,  50, 200, 200],
    [200, 180,  60,  50,  45, 200, 200, 200],
    [200, 200, 200,  48,  52, 200, 200, 200],
]

print("\nImagen (valor de intensidad):")
for fila in imagen_con_sombra:
    print("  " + " ".join(f"{v:4}" for v in fila))

print("\nMascara de sombras (S=sombra, ·=iluminado):")
for fila in imagen_con_sombra:
    print("  " + " ".join("S" if detectar_sombra(v) else "·" for v in fila))

print("\nUsos de la deteccion de sombras:")
print("  - Robotica: evitar confundir sombra con obstaculo")
print("  - Vision: recuperar la geometria 3D del objeto real sin la sombra")
print("  - Reconocimiento: las sombras pueden degradar la precision del clasificador")
