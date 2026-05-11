# _48_ReconocimientoDeObjetos.py
# Reconocimiento de Objetos
# Tarea de identificar QUE objeto esta en una imagen y DONDE esta.
# Enfoques:
#   - Basado en caracteristicas: HOG, SIFT, ORB + clasificador
#   - Basado en redes neuronales: CNN, YOLO, R-CNN
#
# Aqui simulamos el pipeline clasico con descriptores simples y k-NN.

import math
import random

print("=" * 55)
print("  RECONOCIMIENTO DE OBJETOS")
print("=" * 55)

# ---- Descriptor HOG simplificado ----
# HOG (Histogram of Oriented Gradients):
# Divide la imagen en celdas, calcula histograma de orientaciones del gradiente.
# Aqui usamos una version muy simplificada en 1D.

def gradiente(region):
    """Calcula magnitud y orientacion del gradiente (simplificado)"""
    F, C = len(region), len(region[0])
    magnitudes = []
    orientaciones = []
    for i in range(1, F-1):
        for j in range(1, C-1):
            gx = region[i][j+1] - region[i][j-1]
            gy = region[i+1][j] - region[i-1][j]
            mag = math.sqrt(gx**2 + gy**2)
            ang = math.degrees(math.atan2(gy, gx)) % 180
            magnitudes.append(mag)
            orientaciones.append(ang)
    return magnitudes, orientaciones

def hog_descriptor(region, n_bins=9):
    """Histograma de gradientes orientados (simplificado)"""
    mags, angs = gradiente(region)
    hist = [0.0] * n_bins
    bin_size = 180 / n_bins
    for mag, ang in zip(mags, angs):
        bin_idx = int(ang / bin_size) % n_bins
        hist[bin_idx] += mag
    # Normalizar
    total = math.sqrt(sum(h**2 for h in hist)) + 1e-10
    return [h/total for h in hist]

def distancia_euclid(a, b):
    return math.sqrt(sum((ai-bi)**2 for ai,bi in zip(a,b)))

# ---- Dataset de entrenamiento (regiones simuladas) ----
random.seed(42)

def imagen_circulo():
    return [[0 if (i-3)**2+(j-3)**2 < 9 else 200
             for j in range(8)] for i in range(8)]

def imagen_cuadrado():
    return [[0 if 2<=i<=5 and 2<=j<=5 else 200
             for j in range(8)] for i in range(8)]

def agregar_ruido(img):
    return [[max(0,min(255, p + random.randint(-20,20)))
             for p in fila] for fila in img]

# Generar dataset
train = []
for _ in range(10):
    train.append((hog_descriptor(agregar_ruido(imagen_circulo())), "circulo"))
    train.append((hog_descriptor(agregar_ruido(imagen_cuadrado())), "cuadrado"))

# ---- Clasificar con k-NN (k=3) ----
def knn(descriptor, train, k=3):
    distancias = [(distancia_euclid(descriptor, d), clase) for d,clase in train]
    distancias.sort(key=lambda x: x[0])
    vecinos = distancias[:k]
    votos = {}
    for _, clase in vecinos:
        votos[clase] = votos.get(clase, 0) + 1
    return max(votos, key=votos.get)

# ---- Evaluar ----
print("\nPipeline: imagen -> HOG descriptor -> k-NN (k=3)")
print(f"\n{'Objeto real':<14} {'Prediccion':<14} {'Correcto'}")
print("-" * 38)

correctos = 0
test_objs = [("circulo",  imagen_circulo),
             ("cuadrado", imagen_cuadrado)] * 5

for nombre, fn in test_objs:
    img  = agregar_ruido(fn())
    desc = hog_descriptor(img)
    pred = knn(desc, train)
    ok   = pred == nombre
    if ok: correctos += 1
    print(f"{nombre:<14} {pred:<14} {'✓' if ok else '✗'}")

print(f"\nPrecision: {correctos}/{len(test_objs)} = {correctos/len(test_objs)*100:.0f}%")
print("\nEn sistemas reales:")
print("  HOG + SVM  : muy efectivo para deteccion de peatones (Dalal & Triggs 2005)")
print("  CNN (AlexNet, VGG, ResNet): aprenden sus propios descriptores automaticamente")
print("  YOLO / R-CNN: deteccion Y localizacion en tiempo real")
