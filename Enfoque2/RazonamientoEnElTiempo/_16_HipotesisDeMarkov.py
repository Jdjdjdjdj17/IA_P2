# _16_HipotesisDeMarkov.py
# Hipotesis de Markov y Procesos de Markov
# Hipotesis de Markov: el estado futuro depende SOLO del estado presente,
# no del historial completo.
#   P(Xt | X0,...,Xt-1) = P(Xt | Xt-1)
#
# Proceso de Markov de orden 1: la cadena de Markov clasica.
# Simplifica enormemente la representacion de secuencias temporales.

print("=" * 55)
print("  HIPOTESIS DE MARKOV — PROCESOS DE MARKOV")
print("=" * 55)

# ---- Verificacion de la propiedad de Markov ----
print("\nHipotesis de Markov:")
print("  P(Xt | X0, X1, ..., Xt-1) = P(Xt | Xt-1)")
print("  El pasado es irrelevante dado el presente.")

# ---- Cadena de Markov: estados de un robot ----
estados = ["explorando", "cargando", "esperando"]

transicion = {
    "explorando": {"explorando": 0.5, "cargando": 0.3, "esperando": 0.2},
    "cargando":   {"explorando": 0.6, "cargando": 0.1, "esperando": 0.3},
    "esperando":  {"explorando": 0.4, "cargando": 0.1, "esperando": 0.5},
}

print(f"\nCadena de Markov — Robot:")
print(f"Estados: {estados}")

# ---- Prediccion a n pasos ----
def predecir_n_pasos(estado_inicial, n):
    """Distribucion de probabilidad despues de n pasos"""
    dist = {s: 0.0 for s in estados}
    dist[estado_inicial] = 1.0

    for paso in range(n):
        nueva = {s: 0.0 for s in estados}
        for s_ant in estados:
            for s_sig in estados:
                nueva[s_sig] += dist[s_ant] * transicion[s_ant][s_sig]
        dist = nueva
    return dist

print(f"\nPrediccion desde 'explorando':")
for n_pasos in [1, 2, 5, 10, 20]:
    dist = predecir_n_pasos("explorando", n_pasos)
    print(f"  t+{n_pasos:<3}: " + "  ".join(f"{s}={dist[s]:.3f}" for s in estados))

print(f"\nObservacion: con muchos pasos converge a la distribucion estacionaria")
print(f"(sin importar el estado inicial — propiedad ergodica).")

# ---- Proceso de Markov de orden 2 (para comparacion) ----
print(f"\nOrden 1 (Markov): P(Xt | Xt-1)           <- lo que usamos")
print(f"Orden 2:          P(Xt | Xt-1, Xt-2)      <- memoria de 2 pasos")
print(f"Orden k:          P(Xt | Xt-1, ..., Xt-k) <- mas memoria, mas costoso")
print(f"\nEn IA se prefiere orden 1 por su simplicidad computacional.")
