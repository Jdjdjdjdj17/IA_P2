# _49_ReconocimientoDeEscritura.py
# Reconocimiento de Escritura (OCR — Optical Character Recognition)
# Identifica caracteres o palabras en imagenes de texto.
# Pipeline clasico:
#   1. Preprocesado (binarizacion, normalizacion)
#   2. Segmentacion de caracteres
#   3. Extraccion de caracteristicas
#   4. Clasificacion
#
# Aqui simulamos el reconocimiento de digitos con vectores de pixeles simplificados.

import math
import random

print("=" * 55)
print("  RECONOCIMIENTO DE ESCRITURA (OCR)")
print("=" * 55)

# ---- Representacion de digitos 5x3 en pixeles ----
# 1=tinta, 0=fondo
digitos = {
    "0": [[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1]],
    "1": [[0,1,0],[1,1,0],[0,1,0],[0,1,0],[1,1,1]],
    "2": [[1,1,1],[0,0,1],[1,1,1],[1,0,0],[1,1,1]],
    "3": [[1,1,1],[0,0,1],[0,1,1],[0,0,1],[1,1,1]],
    "4": [[1,0,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1]],
    "5": [[1,1,1],[1,0,0],[1,1,1],[0,0,1],[1,1,1]],
}

def aplanar(patron):
    return [p for fila in patron for p in fila]

def agregar_ruido(vec, prob=0.1):
    return [1-v if random.random()<prob else v for v in vec]

def distancia_hamming(a, b):
    return sum(1 for ai,bi in zip(a,b) if ai != bi)

def normalizar_img(img_ruidosa):
    """Binariza: >0.5 -> 1, sino -> 0"""
    return [1 if v >= 0.5 else 0 for v in img_ruidosa]

# ---- Base de datos de referencia ----
referencias = {dig: aplanar(patron) for dig, patron in digitos.items()}

# ---- Clasificador por distancia minima ----
def reconocer(muestra):
    muestra_norm = normalizar_img(muestra)
    distancias = {dig: distancia_hamming(muestra_norm, ref)
                  for dig, ref in referencias.items()}
    return min(distancias, key=distancias.get), distancias

def imprimir_digito(vec, ancho=3):
    for i in range(0, 15, ancho):
        fila = vec[i:i+ancho]
        print("    " + " ".join("█" if v > 0.5 else "·" for v in fila))

# ---- Evaluacion ----
print("\nBase de referencia (digitos limpios):")
for dig, ref in referencias.items():
    pixeles = sum(ref)
    print(f"  Digito '{dig}': {pixeles} pixeles activos, vector={ref}")

print("\nReconocimiento con ruido (prob_ruido=15%):")
random.seed(5)
correctos = 0
total = 0
for dig_real, patron in digitos.items():
    for _ in range(3):
        vec_original = aplanar(patron)
        vec_ruidoso  = agregar_ruido(vec_original, prob=0.15)
        pred, dists  = reconocer(vec_ruidoso)
        ok = pred == dig_real
        if ok: correctos += 1
        total += 1

print(f"  Precision: {correctos}/{total} = {correctos/total*100:.1f}%")

# Mostrar un ejemplo visual
print("\nEjemplo visual — digito '5' con ruido:")
vec_5_ruidoso = agregar_ruido(aplanar(digitos["5"]), prob=0.15)
imprimir_digito(vec_5_ruidoso)
pred, dists = reconocer(vec_5_ruidoso)
print(f"  Reconocido como: '{pred}'")
print(f"  Distancias: {dists}")

print("\nEn sistemas reales:")
print("  CNN entrenadas en MNIST (70,000 imagenes) alcanzan >99% de precision")
print("  Tesseract: motor OCR open-source para texto impreso")
print("  Desafios: escritura cursiva, variaciones de fuente, ruido, inclinacion")
