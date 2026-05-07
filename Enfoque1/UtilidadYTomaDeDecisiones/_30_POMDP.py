# _30_POMDP.py
# MDP Parcialmente Observable (POMDP)
# El agente NO conoce el estado real del mundo, solo tiene observaciones.
# Mantiene un "estado de creencia" (belief state) = distribucion de probabilidad
# sobre los estados posibles, y lo actualiza con cada observacion.
#
# Ejemplo: el agente esta en una cuadricula y solo sabe si hay "pared" o "libre"

import random

estados       = ['izquierda', 'centro', 'derecha']
observaciones = ['pared', 'libre']

# Probabilidad de observar 'pared' estando en cada estado
prob_observacion = {
    'izquierda': {'pared': 0.9, 'libre': 0.1},
    'centro':    {'pared': 0.2, 'libre': 0.8},
    'derecha':   {'pared': 0.8, 'libre': 0.2},
}

# Transicion con accion 'moverse_derecha'
prob_transicion = {
    'izquierda': {'izquierda': 0.1, 'centro': 0.9, 'derecha': 0.0},
    'centro':    {'izquierda': 0.0, 'centro': 0.1, 'derecha': 0.9},
    'derecha':   {'izquierda': 0.0, 'centro': 0.0, 'derecha': 1.0},
}

def actualizar_creencia(creencia, accion, observacion):
    """Filtro de Bayes: actualiza el belief state"""
    # Prediccion: aplica la transicion
    pred = {s2: 0 for s2 in estados}
    for s in estados:
        for s2 in estados:
            pred[s2] += creencia[s] * prob_transicion[s][s2]

    # Actualizacion: aplica la observacion
    nueva = {s: pred[s] * prob_observacion[s][observacion] for s in estados}

    # Normalizar
    total = sum(nueva.values())
    if total == 0:
        return creencia
    return {s: nueva[s] / total for s in estados}

print("=" * 50)
print("  POMDP - MDP PARCIALMENTE OBSERVABLE")
print("=" * 50)

# Creencia inicial uniforme (no sabe donde esta)
creencia = {s: 1/3 for s in estados}
print("\nCreencia inicial:", {s: f"{v:.2f}" for s, v in creencia.items()})

# Simula 4 pasos: el agente se mueve y observa
pasos = 4
for paso in range(1, pasos + 1):
    obs = random.choices(observaciones, weights=[0.5, 0.5])[0]
    creencia = actualizar_creencia(creencia, 'moverse_derecha', obs)
    print(f"\nPaso {paso} | Observacion: '{obs}'")
    for s, v in creencia.items():
        print(f"  P({s}) = {v:.3f}")
    estado_mas_probable = max(creencia, key=creencia.get)
    print(f"  -> El agente cree estar en: '{estado_mas_probable}'")
