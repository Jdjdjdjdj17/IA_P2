# _18_AlgoritmoHaciaDelanteAtras.py
# Algoritmo Hacia Delante-Atras (Forward-Backward)
# Calcula el suavizado P(Xk | e1:t) para todos los pasos de tiempo.
# Combina dos pasadas:
#   - Hacia Delante: f1:k = P(Xk, e1:k)  acumula evidencia pasada
#   - Hacia Atras:   bk+1:t = P(ek+1:t | Xk)  acumula evidencia futura
#   - Suavizado: P(Xk | e1:t) proporcional a f1:k * bk+1:t

print("=" * 55)
print("  ALGORITMO HACIA DELANTE-ATRAS (FORWARD-BACKWARD)")
print("=" * 55)

estados  = ["si", "no"]   # lluvia
prior    = {"si": 0.5, "no": 0.5}
trans    = {"si":{"si":0.7,"no":0.3}, "no":{"si":0.3,"no":0.7}}
sensor   = {"si":{"paraguas":0.9,"no_paraguas":0.1},
            "no":{"paraguas":0.2,"no_paraguas":0.8}}
obs_seq  = ["paraguas", "paraguas", "no_paraguas"]

def normalizar(d):
    t = sum(d.values())
    return {k: v/t for k,v in d.items()}

# ---- Pasada Hacia Delante ----
print("\nPasada HACIA DELANTE f[t] = P(Xt, e1:t):")
forward = [prior.copy()]
for t, obs in enumerate(obs_seq):
    f_prev = forward[-1]
    pred   = {s2: sum(f_prev[s1]*trans[s1][s2] for s1 in estados) for s2 in estados}
    f_new  = {s: pred[s]*sensor[s][obs] for s in estados}
    forward.append(f_new)
    fn     = normalizar(f_new)
    print(f"  t={t+1} obs={obs}: f(si)={f_new['si']:.6f}  f(no)={f_new['no']:.6f}")
    print(f"          normalizado: P(si|e1:{t+1})={fn['si']:.4f}")

# ---- Pasada Hacia Atras ----
print("\nPasada HACIA ATRAS b[t] = P(et+1:T | Xt):")
T = len(obs_seq)
backward = [None] * (T + 1)
backward[T] = {"si": 1.0, "no": 1.0}   # condicion inicial
print(f"  t={T}: b(si)=1.0000  b(no)=1.0000")

for t in range(T-1, -1, -1):
    obs  = obs_seq[t]
    b    = backward[t+1]
    b_new = {}
    for s1 in estados:
        b_new[s1] = sum(trans[s1][s2]*sensor[s2][obs]*b[s2] for s2 in estados)
    backward[t] = b_new
    print(f"  t={t}: b(si)={b_new['si']:.6f}  b(no)={b_new['no']:.6f}")

# ---- Suavizado: combinar forward y backward ----
print("\nSUAVIZADO P(Xt | e1:T) = normalizar(f[t] * b[t]):")
for t in range(1, T+1):
    producto = {s: forward[t][s] * backward[t][s] for s in estados}
    suav     = normalizar(producto)
    print(f"  t={t}: P(lluvia=si | toda evidencia) = {suav['si']:.4f}")

print(f"\nNota: el suavizado es mas preciso que el filtrado")
print(f"porque usa tanto evidencia pasada como futura.")
