# _10_InferenciaPorEnumeracion.py
# Inferencia por Enumeracion en Redes Bayesianas
# Metodo exacto: suma sobre todas las combinaciones de variables ocultas.
#
# P(X | e) = alpha * suma_y P(X, e, y)
# Donde e = evidencia, y = variables ocultas, alpha = normalizacion

print("=" * 55)
print("  INFERENCIA POR ENUMERACION")
print("=" * 55)

# ---- Red: Robo(R) -> Alarma(A) <- Terremoto(T) ----
P_R = {"si": 0.001, "no": 0.999}
P_T = {"si": 0.002, "no": 0.998}
P_A_dado_RT = {
    ("si","si"): {"si": 0.95, "no": 0.05},
    ("si","no"): {"si": 0.94, "no": 0.06},
    ("no","si"): {"si": 0.29, "no": 0.71},
    ("no","no"): {"si": 0.001,"no": 0.999},
}

def prob_conjunta(r, t, a):
    return P_R[r] * P_T[t] * P_A_dado_RT[(r,t)][a]

# ---- Consulta: P(Robo | Alarma=si) ----
# Variables ocultas: Terremoto
# P(R=si, A=si) = suma_T P(R=si, T, A=si)
evidencia_a = "si"

print(f"\nConsulta: P(Robo | Alarma={evidencia_a})")
print(f"Variable oculta: Terremoto\n")

resultados = {}
for r_val in ["si","no"]:
    # Sumar sobre la variable oculta T
    p_r_a = sum(prob_conjunta(r_val, t, evidencia_a) for t in ["si","no"])
    resultados[r_val] = p_r_a
    print(f"  P(R={r_val}, A=si) = sum_T P(R={r_val},T,A=si)")
    for t in ["si","no"]:
        p = prob_conjunta(r_val, t, evidencia_a)
        print(f"    T={t}: {p:.8f}")
    print(f"    Subtotal = {p_r_a:.8f}\n")

# Normalizar
total = sum(resultados.values())
print(f"P(A=si) = {total:.8f}  (factor de normalizacion alpha = 1/{total:.6f})")
print(f"\nResultado normalizado P(Robo | Alarma=si):")
for r_val, p in resultados.items():
    print(f"  P(R={r_val} | A=si) = {p:.8f} / {total:.8f} = {p/total:.6f}")

print(f"\nInterpretacion:")
print(f"  Si suena la alarma, la prob de robo sube de {P_R['si']:.3f} a {resultados['si']/total:.4f}")
