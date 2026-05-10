# _26_AgrupamientoNoSupervisado.py
# Agrupamiento No Supervisado (Clustering)
# El agente agrupa datos SIN etiquetas, solo por similitud.
# Algoritmos: k-Medias, DBSCAN, jerarquico, etc.
# Aqui implementamos k-Medias desde cero.

import random
import math

print("=" * 55)
print("  AGRUPAMIENTO NO SUPERVISADO — k-MEDIAS")
print("=" * 55)

# ---- Datos: puntos 2D de 3 grupos ----
random.seed(7)
def generar_grupo(cx, cy, n=15, ruido=0.8):
    return [(cx + random.gauss(0,ruido), cy + random.gauss(0,ruido)) for _ in range(n)]

datos = generar_grupo(1, 1) + generar_grupo(5, 5) + generar_grupo(1, 5)
k = 3

def distancia(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def asignar_clusters(datos, centroides):
    return [min(range(k), key=lambda i: distancia(p, centroides[i])) for p in datos]

def recalcular_centroides(datos, asignaciones):
    centroides = []
    for c in range(k):
        grupo = [datos[i] for i, a in enumerate(asignaciones) if a == c]
        if grupo:
            cx = sum(p[0] for p in grupo) / len(grupo)
            cy = sum(p[1] for p in grupo) / len(grupo)
            centroides.append((cx, cy))
        else:
            centroides.append(datos[random.randint(0, len(datos)-1)])
    return centroides

def inercia(datos, asignaciones, centroides):
    return sum(distancia(datos[i], centroides[asignaciones[i]])**2
               for i in range(len(datos)))

# ---- Inicializacion: centroides aleatorios ----
centroides = random.sample(datos, k)
print(f"\nDatos: {len(datos)} puntos en 3 grupos reales")
print(f"k = {k}, centroides iniciales:")
for i, c in enumerate(centroides):
    print(f"  C{i}: ({c[0]:.2f}, {c[1]:.2f})")

print(f"\n{'Iter':<6} {'Inercia':<12} {'Cambio_centroides'}")
print("-" * 38)

asignaciones_prev = None
for it in range(20):
    asignaciones = asignar_clusters(datos, centroides)
    nuevos_centroides = recalcular_centroides(datos, asignaciones)
    iner = inercia(datos, asignaciones, centroides)

    cambio = sum(distancia(centroides[i], nuevos_centroides[i]) for i in range(k))
    print(f"{it+1:<6} {iner:<12.4f} {cambio:.6f}")

    centroides = nuevos_centroides
    if cambio < 1e-6:
        print(f"  Convergio en iteracion {it+1}")
        break

print(f"\nCentroides finales:")
for i, c in enumerate(centroides):
    n_puntos = asignaciones.count(i)
    print(f"  Cluster {i}: ({c[0]:.3f}, {c[1]:.3f})  | {n_puntos} puntos")

print(f"\nConteo por cluster: {[asignaciones.count(i) for i in range(k)]}")
print(f"(Grupos reales: 15, 15, 15)")
