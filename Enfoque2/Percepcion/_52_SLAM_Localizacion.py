# _52_SLAM_Localizacion.py
# Localizacion y SLAM (Simultaneous Localization and Mapping)
# El robot necesita saber DOS cosas al mismo tiempo:
#   - DONDE esta (localizacion)
#   - COMO es el entorno (mapa)
# El problema es circular: para localizarse necesita el mapa,
# y para hacer el mapa necesita saber donde esta.
#
# SLAM resuelve ambos problemas simultaneamente.
# Localizacion Monte Carlo (Filtro de Particulas): cada particula es una hipotesis
# de la posicion del robot. Se actualiza con las observaciones del sensor.

import random
import math

print("=" * 55)
print("  SLAM Y LOCALIZACION MONTE CARLO")
print("=" * 55)

# ---- Entorno: cuadricula 10x10 con obstaculos ----
FILAS, COLS = 10, 10
mapa = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,1,1,0,0,0,1,1,0,0],
    [0,1,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,1,0,0,0,0,0],
    [0,0,0,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,1,0],
    [0,0,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
]   # 0=libre, 1=obstaculo

def libre(f, c):
    return 0 <= f < FILAS and 0 <= c < COLS and mapa[f][c] == 0

def sensor_distancia(f, c, direccion):
    """Simula un sensor de distancia en una direccion"""
    df, dc = direccion
    dist = 0
    nf, nc = f + df, c + dc
    while libre(nf, nc):
        dist += 1
        nf += df; nc += dc
        if dist > 9: break
    return dist

# ---- Localizacion Monte Carlo ----
N_particulas = 300

# Inicializar particulas en celdas libres
def init_particulas():
    particulas = []
    while len(particulas) < N_particulas:
        f = random.randint(0, FILAS-1)
        c = random.randint(0, COLS-1)
        if libre(f, c):
            particulas.append([f, c])
    return particulas

def mover_particulas(particulas, df, dc):
    """Mueve particulas con ruido"""
    nuevas = []
    for f, c in particulas:
        nf = f + df + random.choice([-1,0,0,0,1])
        nc = c + dc + random.choice([-1,0,0,0,1])
        if libre(nf, nc):
            nuevas.append([nf, nc])
        else:
            nuevas.append([f, c])
    return nuevas

def ponderar(particulas, observacion_real, direccion):
    """Peso basado en similitud de la observacion del sensor"""
    pesos = []
    for f, c in particulas:
        obs_part = sensor_distancia(f, c, direccion)
        diff = abs(obs_part - observacion_real)
        peso = math.exp(-diff**2 / 2.0)
        pesos.append(peso)
    return pesos

def remuestrear(particulas, pesos):
    total = sum(pesos)
    if total == 0:
        return particulas[:]
    pesos_norm = [p/total for p in pesos]
    return [list(p) for p in random.choices(particulas, weights=pesos_norm, k=N_particulas)]

def estimacion(particulas):
    f_est = sum(p[0] for p in particulas) / len(particulas)
    c_est = sum(p[1] for p in particulas) / len(particulas)
    return round(f_est,1), round(c_est,1)

# ---- Simulacion del robot ----
pos_real = [1, 0]   # posicion real del robot
particulas = init_particulas()
direccion_sensor = (0, 1)  # sensor mira a la derecha
movimientos = [(0,1),(0,1),(1,0),(1,0),(0,1)]

print(f"\nRobot en mapa {FILAS}x{COLS}")
print(f"Sensor: distancia a obstaculo en direccion {direccion_sensor}")
print(f"\n{'Paso':<6} {'Pos_real':<14} {'Estimacion':<14} {'Error'}")
print("-" * 45)

for paso, (df, dc) in enumerate(movimientos):
    # Mover robot
    nf, nc = pos_real[0]+df, pos_real[1]+dc
    if libre(nf, nc): pos_real = [nf, nc]

    # Observar
    obs_real = sensor_distancia(pos_real[0], pos_real[1], direccion_sensor)

    # Actualizar particulas
    particulas = mover_particulas(particulas, df, dc)
    pesos      = ponderar(particulas, obs_real, direccion_sensor)
    particulas = remuestrear(particulas, pesos)

    est = estimacion(particulas)
    error = math.sqrt((est[0]-pos_real[0])**2 + (est[1]-pos_real[1])**2)
    print(f"{paso+1:<6} ({pos_real[0]},{pos_real[1]}){'':6} ({est[0]},{est[1]}){'':6} {error:.2f}")

print(f"\nMapa del entorno (0=libre, 1=obstaculo):")
for f, fila in enumerate(mapa):
    linea = ""
    for c, v in enumerate(fila):
        if [f,c] == pos_real:
            linea += "R "
        else:
            linea += "█ " if v else "· "
    print(f"  {linea}")
print(f"  R = posicion final del robot")
print(f"\nSLAM completo: simultaneamente construye el mapa Y se localiza en el.")
print(f"Algoritmos SLAM populares: EKF-SLAM, FastSLAM, GraphSLAM, ORB-SLAM.")
