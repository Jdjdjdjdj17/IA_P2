# _17_FiltradoPrediccionSuavizado.py
# Filtrado, Prediccion, Suavizado y Explicacion
# Cuatro tareas fundamentales de inferencia en modelos temporales:
#
# - FILTRADO:    P(Xt | e1:t)         estado actual dado evidencia hasta ahora
# - PREDICCION:  P(Xt+k | e1:t)       estado futuro dado evidencia hasta ahora
# - SUAVIZADO:   P(Xk | e1:t)  k<t   estado pasado dado toda la evidencia
# - EXPLICACION: argmax P(x1:t | e1:t) secuencia mas probable (Viterbi)

print("=" * 55)
print("  FILTRADO, PREDICCION, SUAVIZADO Y EXPLICACION")
print("=" * 55)

# ---- Modelo oculto simple: estado binario (lluvia/no) ----
# P(Xt | Xt-1)
trans = {
    "si": {"si": 0.7, "no": 0.3},
    "no": {"si": 0.3, "no": 0.7},
}
# P(Ot | Xt) — el sensor detecta paraguas
sensor = {
    "si": {"paraguas": 0.9, "no_paraguas": 0.1},
    "no": {"paraguas": 0.2, "no_paraguas": 0.8},
}
estados  = ["si", "no"]
prior    = {"si": 0.5, "no": 0.5}
obs_seq  = ["paraguas", "paraguas", "no_paraguas"]  # observaciones t=1,2,3

def normalizar(d):
    total = sum(d.values())
    return {k: v/total for k,v in d.items()}

# ---- FILTRADO: actualizar creencia en cada paso ----
print("\n1. FILTRADO P(Xt | e1:t):")
bel = prior.copy()
historico = [bel.copy()]
for t, obs in enumerate(obs_seq, 1):
    # Prediccion
    pred = {s2: sum(bel[s1]*trans[s1][s2] for s1 in estados) for s2 in estados}
    # Actualizacion
    upd  = {s: pred[s]*sensor[s][obs] for s in estados}
    bel  = normalizar(upd)
    historico.append(bel.copy())
    print(f"  t={t} obs={obs}: P(lluvia=si)={bel['si']:.4f}, P(lluvia=no)={bel['no']:.4f}")

# ---- PREDICCION: k pasos al futuro desde el ultimo estado ----
print("\n2. PREDICCION P(Xt+k | e1:3) desde t=3:")
dist = bel.copy()
for k in range(1, 4):
    nueva = {s2: sum(dist[s1]*trans[s1][s2] for s1 in estados) for s2 in estados}
    dist = nueva
    print(f"  k={k}: P(lluvia=si|e1:3)={dist['si']:.4f}")

# ---- SUAVIZADO: reestimar estados pasados con toda la evidencia ----
print("\n3. SUAVIZADO P(Xk | e1:3) para k=1 (hacia atras):")
# Mensaje hacia atras b[k] = P(ek+1:t | Xk)
b = {"si": 1.0, "no": 1.0}  # b[t] = 1
suavizados = []
for t in range(len(obs_seq)-1, -1, -1):
    obs = obs_seq[t]
    # Suavizado = forward * backward normalizado
    suav = normalizar({s: historico[t][s]*b[s] for s in estados})
    suavizados.insert(0, suav)
    # Propagar b hacia atras
    b_nuevo = {}
    for s1 in estados:
        b_nuevo[s1] = sum(trans[s1][s2]*sensor[s2][obs]*b[s2] for s2 in estados)
    b = b_nuevo

for t, s in enumerate(suavizados, 1):
    print(f"  t={t}: P(lluvia=si|toda_evidencia)={s['si']:.4f}")

print("\n4. EXPLICACION: secuencia mas probable -> ver algoritmo Viterbi (_18_)")
