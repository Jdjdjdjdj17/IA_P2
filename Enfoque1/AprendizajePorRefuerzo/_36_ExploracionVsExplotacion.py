# _36_ExploracionVsExplotacion.py
# Exploracion vs. Explotacion
# Uno de los dilemas centrales del aprendizaje por refuerzo:
#   - EXPLORAR: probar acciones nuevas para descubrir si son mejores
#   - EXPLOTAR: usar la mejor accion conocida hasta ahora
#
# Estrategias comunes:
#   1. Epsilon-Greedy: explora con probabilidad epsilon
#   2. Decaimiento de epsilon: epsilon disminuye con el tiempo
#   3. UCB (Upper Confidence Bound): favorece acciones poco exploradas

import random
import math

# ---- Problema del Bandido de K-brazos ----
# El agente elige entre K "maquinas tragamonedas" (acciones)
# Cada maquina tiene una recompensa promedio desconocida
K = 5
recompensas_reales = [1.5, 2.0, 3.5, 0.8, 2.8]  # El agente NO sabe estos valores

def jalar_maquina(k):
    """Simula jalar el brazo k con ruido gaussiano"""
    return recompensas_reales[k] + random.gauss(0, 1)

pasos = 1000

# ---- Estrategia 1: Epsilon-Greedy con epsilon fijo ----
def epsilon_greedy(epsilon):
    Q    = [0.0] * K
    N    = [0]   * K
    total_recompensa = 0
    for _ in range(pasos):
        if random.random() < epsilon:
            k = random.randint(0, K-1)  # explorar
        else:
            k = Q.index(max(Q))          # explotar
        r = jalar_maquina(k)
        N[k] += 1
        Q[k] += (r - Q[k]) / N[k]  # media incremental
        total_recompensa += r
    return total_recompensa / pasos, Q.index(max(Q))

# ---- Estrategia 2: UCB ----
def ucb():
    Q    = [0.0] * K
    N    = [0]   * K
    total_recompensa = 0
    for t in range(1, pasos+1):
        # Primero probar cada maquina al menos una vez
        if t <= K:
            k = t - 1
        else:
            ucb_vals = [Q[i] + math.sqrt(2 * math.log(t) / N[i]) for i in range(K)]
            k = ucb_vals.index(max(ucb_vals))
        r = jalar_maquina(k)
        N[k] += 1
        Q[k] += (r - Q[k]) / N[k]
        total_recompensa += r
    return total_recompensa / pasos, Q.index(max(Q))

print("=" * 50)
print("  EXPLORACION vs. EXPLOTACION")
print("  Problema del Bandido de K-brazos")
print("=" * 50)
print(f"\nMaquinas: {K}  |  Pasos: {pasos}")
print(f"Recompensas reales: {recompensas_reales}  (ocultas al agente)")
print(f"Mejor maquina real: {recompensas_reales.index(max(recompensas_reales))}")

for eps in [0.0, 0.1, 0.3]:
    promedio, mejor = epsilon_greedy(eps)
    nombre = "Greedy puro" if eps == 0.0 else f"ε-Greedy ε={eps}"
    print(f"\n{nombre}: recompensa promedio={promedio:.3f}  maquina elegida={mejor}")

promedio_ucb, mejor_ucb = ucb()
print(f"\nUCB:                recompensa promedio={promedio_ucb:.3f}  maquina elegida={mejor_ucb}")

print(f"\nConclusion:")
print(f"  - Con epsilon=0 (greedy puro) el agente puede quedarse atrapado en una maquina mala.")
print(f"  - Con epsilon mayor explora mas pero pierde algo de recompensa.")
print(f"  - UCB balancea automaticamente segun la incertidumbre de cada accion.")
