# _15_ProcesosEstacionarios.py
# Procesos Estacionarios
# Un proceso es estacionario si sus probabilidades de transicion NO cambian con el tiempo.
# P(Xt | Xt-1) es la misma para cualquier t.
# Esto simplifica enormemente el modelado de secuencias temporales.

print("=" * 55)
print("  PROCESOS ESTACIONARIOS")
print("=" * 55)

# ---- Ejemplo: clima diario ----
# Estados: sol, nublado, lluvia
# Matriz de transicion (estacionaria = siempre la misma)
estados = ["sol", "nublado", "lluvia"]

# P(estado_t | estado_t-1)
transicion = {
    "sol":     {"sol": 0.7, "nublado": 0.2, "lluvia": 0.1},
    "nublado": {"sol": 0.3, "nublado": 0.4, "lluvia": 0.3},
    "lluvia":  {"sol": 0.2, "nublado": 0.3, "lluvia": 0.5},
}

print("\nMatriz de transicion estacionaria P(Xt | Xt-1):")
print(f"  {'':12}", end="")
for s in estados:
    print(f"{s:>10}", end="")
print()
print("  " + "-"*42)
for s_ant in estados:
    print(f"  {s_ant:<12}", end="")
    for s_sig in estados:
        print(f"{transicion[s_ant][s_sig]:>10.2f}", end="")
    print()

# ---- Verificar que cada fila suma 1 ----
print("\nVerificacion (cada fila debe sumar 1.0):")
for s in estados:
    total = sum(transicion[s].values())
    print(f"  suma({s}) = {total:.1f}")

# ---- Simulacion de 10 pasos ----
import random
estado_actual = "sol"
print(f"\nSimulacion de 10 dias (inicio: {estado_actual}):")
print(f"  t=0: {estado_actual}")
for t in range(1, 11):
    probs = list(transicion[estado_actual].values())
    estado_actual = random.choices(estados, weights=probs)[0]
    print(f"  t={t}: {estado_actual}")

# ---- Distribucion estacionaria (estado estable) ----
# Iterar la distribucion hasta que converja
dist = {"sol": 1/3, "nublado": 1/3, "lluvia": 1/3}
print("\nConvergencia a distribucion estacionaria (estado estable):")
for it in range(50):
    nueva = {s: 0 for s in estados}
    for s_ant in estados:
        for s_sig in estados:
            nueva[s_sig] += dist[s_ant] * transicion[s_ant][s_sig]
    dist = nueva

print("  Distribucion estacionaria pi:")
for s, p in dist.items():
    print(f"    pi({s}) = {p:.4f}")
print("  (El proceso converge a esta distribucion sin importar el inicio)")
