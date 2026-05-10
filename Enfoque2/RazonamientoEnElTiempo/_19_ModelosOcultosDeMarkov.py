# _19_ModelosOcultosDeMarkov.py
# Modelos Ocultos de Markov (HMM — Hidden Markov Model)
# El estado real es OCULTO; solo observamos senales ruidosas.
# Componentes:
#   - Estados ocultos X (ej. clima real)
#   - Observaciones O (ej. si el agente lleva paraguas)
#   - Matriz de transicion A: P(Xt | Xt-1)
#   - Matriz de emision B: P(Ot | Xt)
#   - Distribucion inicial pi
#
# Tres problemas clasicos:
#   1. Evaluacion: P(O | modelo) — Algoritmo Forward
#   2. Decodificacion: secuencia oculta mas probable — Viterbi
#   3. Aprendizaje: estimar A, B, pi — Baum-Welch (ver _23)

print("=" * 55)
print("  MODELOS OCULTOS DE MARKOV (HMM)")
print("=" * 55)

estados     = ["sol", "lluvia"]
obs_posibles= ["seco", "humedo", "mojado"]
pi   = {"sol": 0.6, "lluvia": 0.4}
A    = {"sol":{"sol":0.7,"lluvia":0.3}, "lluvia":{"sol":0.4,"lluvia":0.6}}
B    = {"sol":{"seco":0.6,"humedo":0.3,"mojado":0.1},
        "lluvia":{"seco":0.1,"humedo":0.4,"mojado":0.5}}

obs_seq = ["seco", "humedo", "mojado"]

print(f"\nEstados ocultos: {estados}")
print(f"Observaciones  : {obs_seq}")

# ---- Problema 1: Evaluacion con Algoritmo Forward ----
print("\n--- Problema 1: Evaluacion P(O | HMM) ---")
alpha = [{s: pi[s]*B[s][obs_seq[0]] for s in estados}]
print(f"t=1 obs={obs_seq[0]}: " + "  ".join(f"alpha({s})={alpha[0][s]:.6f}" for s in estados))

for t in range(1, len(obs_seq)):
    obs   = obs_seq[t]
    a_prev= alpha[-1]
    a_new = {s2: B[s2][obs]*sum(a_prev[s1]*A[s1][s2] for s1 in estados) for s2 in estados}
    alpha.append(a_new)
    print(f"t={t+1} obs={obs}: " + "  ".join(f"alpha({s})={a_new[s]:.6f}" for s in estados))

p_obs = sum(alpha[-1].values())
print(f"P(O | HMM) = {p_obs:.8f}")

# ---- Problema 2: Decodificacion con Viterbi ----
print("\n--- Problema 2: Decodificacion (Viterbi) ---")
viterbi = [{s: pi[s]*B[s][obs_seq[0]] for s in estados}]
camino  = [{s: [s] for s in estados}]

for t in range(1, len(obs_seq)):
    obs   = obs_seq[t]
    v_prev= viterbi[-1]
    v_new = {}
    c_new = {}
    for s2 in estados:
        mejor_s1 = max(estados, key=lambda s1: v_prev[s1]*A[s1][s2])
        v_new[s2] = v_prev[mejor_s1]*A[mejor_s1][s2]*B[s2][obs]
        c_new[s2] = camino[-1][mejor_s1] + [s2]
    viterbi.append(v_new)
    camino.append(c_new)

mejor_final = max(estados, key=lambda s: viterbi[-1][s])
print(f"Secuencia oculta mas probable: {camino[-1][mejor_final]}")
print(f"Probabilidad: {viterbi[-1][mejor_final]:.8f}")
