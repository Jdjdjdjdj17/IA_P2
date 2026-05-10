# _21_FiltradoDeParticulas.py
# Filtrado de Particulas (Particle Filter)
# Metodo aproximado para modelos no lineales o no gaussianos.
# Representa la distribucion del estado con un conjunto de PARTICULAS (muestras).
# Cada particula es una hipotesis del estado actual con un peso asociado.
#
# Pasos: Prediccion -> Ponderacion -> Remuestreo

import random
import math

print("=" * 55)
print("  FILTRADO DE PARTICULAS")
print("=" * 55)

# ---- Modelo: seguimiento de posicion 1D no lineal ----
# Transicion: x_t = x_{t-1} + 1 + ruido
# Observacion: z_t = x_t + ruido_sensor

N_particulas = 200
ruido_proc   = 0.5
ruido_sensor = 1.5

def transicion(x):
    return x + 1.0 + random.gauss(0, ruido_proc)

def verosimilitud(z, x):
    """P(z | x) — gaussiana"""
    diff = z - x
    return math.exp(-0.5*(diff/ruido_sensor)**2) / (ruido_sensor*math.sqrt(2*math.pi))

def remuestrear(particulas, pesos):
    """Remuestreo por ruleta (importancia)"""
    total = sum(pesos)
    pesos_norm = [p/total for p in pesos]
    return random.choices(particulas, weights=pesos_norm, k=N_particulas)

# Inicializar particulas uniformemente
particulas = [random.uniform(-2, 2) for _ in range(N_particulas)]

# Posicion real y observaciones
pos_real = 0.0
print(f"\n{'t':<4} {'Pos_real':<12} {'Obs':<10} {'Estimacion':<14} {'Error'}")
print("-" * 50)

for t in range(1, 8):
    pos_real += 1.0 + random.gauss(0, ruido_proc)
    z = pos_real + random.gauss(0, ruido_sensor)

    # ---- Prediccion: propagar particulas ----
    particulas = [transicion(p) for p in particulas]

    # ---- Ponderacion: calcular peso de cada particula ----
    pesos = [verosimilitud(z, p) for p in particulas]

    # ---- Estimacion: media ponderada ----
    total   = sum(pesos)
    estimacion = sum(p*w for p,w in zip(particulas,pesos)) / total

    error = abs(estimacion - pos_real)
    print(f"{t:<4} {pos_real:<12.3f} {z:<10.3f} {estimacion:<14.3f} {error:.3f}")

    # ---- Remuestreo ----
    particulas = remuestrear(particulas, pesos)

print(f"\nVentaja sobre Kalman:")
print(f"  - No asume linealidad ni gaussianidad")
print(f"  - Funciona con cualquier modelo de transicion/observacion")
print(f"  - Mas particulas = mayor precision, mayor costo computacional")
