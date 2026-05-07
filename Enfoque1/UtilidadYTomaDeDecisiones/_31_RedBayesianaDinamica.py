# _31_RedBayesianaDinamica.py
# Red Bayesiana Dinamica (DBN - Dynamic Bayesian Network)
# Modela como cambia el estado del mundo a lo largo del tiempo.
# Usa el modelo de Markov: el estado en t solo depende del estado en t-1.
#
# Aplicacion clasica: seguimiento de posicion de un objeto
# (simplificado sin matrices, solo con probabilidades manuales)

# ---- Modelo ----
# Estados posibles de posicion: 'A', 'B', 'C'
# El objeto se mueve con ciertas probabilidades de transicion

estados = ['A', 'B', 'C']

# P(estado_t | estado_t-1)  — modelo de transicion
transicion = {
    'A': {'A': 0.6, 'B': 0.3, 'C': 0.1},
    'B': {'A': 0.2, 'B': 0.5, 'C': 0.3},
    'C': {'A': 0.1, 'B': 0.3, 'C': 0.6},
}

# P(observacion | estado) — modelo de observacion (sensor ruidoso)
observacion_modelo = {
    'A': {'obs_A': 0.8, 'obs_B': 0.15, 'obs_C': 0.05},
    'B': {'obs_A': 0.1, 'obs_B': 0.75, 'obs_C': 0.15},
    'C': {'obs_A': 0.05,'obs_B': 0.2,  'obs_C': 0.75},
}

def predecir(creencia):
    """Paso de prediccion: aplica el modelo de transicion"""
    nueva = {s: 0 for s in estados}
    for s_ant in estados:
        for s_nuevo in estados:
            nueva[s_nuevo] += creencia[s_ant] * transicion[s_ant][s_nuevo]
    return nueva

def actualizar(creencia, obs):
    """Paso de actualizacion: incorpora la observacion"""
    nueva = {s: creencia[s] * observacion_modelo[s][obs] for s in estados}
    total = sum(nueva.values())
    return {s: nueva[s] / total for s in estados} if total > 0 else creencia

def normalizar(d):
    total = sum(d.values())
    return {k: v/total for k, v in d.items()}

print("=" * 50)
print("  RED BAYESIANA DINAMICA")
print("=" * 50)

# Creencia inicial
creencia = {'A': 0.6, 'B': 0.3, 'C': 0.1}
print("\nCreencia inicial:", {s: f"{v:.2f}" for s, v in creencia.items()})

# Secuencia de observaciones del sensor a lo largo del tiempo
secuencia_obs = ['obs_A', 'obs_B', 'obs_B', 'obs_C', 'obs_C']

for t, obs in enumerate(secuencia_obs, start=1):
    creencia = predecir(creencia)
    creencia = actualizar(creencia, obs)
    print(f"\nt={t} | Observacion: {obs}")
    for s, v in creencia.items():
        barra = "█" * int(v * 20)
        print(f"  P(X={s}) = {v:.3f}  {barra}")
    print(f"  -> Estado mas probable: {max(creencia, key=creencia.get)}")
