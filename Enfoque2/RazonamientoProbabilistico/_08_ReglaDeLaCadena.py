# _08_ReglaDeLaCadena.py
# Regla de la Cadena (Chain Rule)
# Permite factorizar la distribucion conjunta de n variables:
#
#   P(X1, X2, ..., Xn) = P(X1) * P(X2|X1) * P(X3|X1,X2) * ... * P(Xn|X1,...,Xn-1)
#
# En una Red Bayesiana se simplifica usando las independencias condicionales:
#   P(X1,...,Xn) = producto de P(Xi | Padres(Xi))

print("=" * 55)
print("  REGLA DE LA CADENA")
print("=" * 55)

# ---- Ejemplo con 3 variables: Alarma, Robo, Terremoto ----
# Red: Robo -> Alarma <- Terremoto

P_R  = {"si": 0.001, "no": 0.999}   # Robo
P_T  = {"si": 0.002, "no": 0.998}   # Terremoto

# P(Alarma | Robo, Terremoto)
P_A_dado_RT = {
    ("si","si"): {"si": 0.95, "no": 0.05},
    ("si","no"): {"si": 0.94, "no": 0.06},
    ("no","si"): {"si": 0.29, "no": 0.71},
    ("no","no"): {"si": 0.001,"no": 0.999},
}

print("\nRed: Robo -> Alarma <- Terremoto")
print("\nRegla de la Cadena aplicada a esta red:")
print("  P(R, T, A) = P(R) * P(T) * P(A | R, T)")
print("  (R y T son independientes = sin arista entre ellos)")

# Calcular probabilidad conjunta para varios escenarios
escenarios = [
    ("si","si","si"),
    ("si","no","si"),
    ("no","no","si"),
    ("no","no","no"),
]

print(f"\n{'R':<5} {'T':<5} {'A':<5} {'P(R)*P(T)*P(A|R,T)'}")
print("-" * 42)
for r, t, a in escenarios:
    p = P_R[r] * P_T[t] * P_A_dado_RT[(r,t)][a]
    print(f"{r:<5} {t:<5} {a:<5} {p:.8f}")

# Calcular P(A=si) marginalizando R y T
p_a_si = sum(
    P_R[r] * P_T[t] * P_A_dado_RT[(r,t)]["si"]
    for r in ["si","no"] for t in ["si","no"]
)
print(f"\nP(Alarma=si) marginalizando R y T = {p_a_si:.6f}")

# Mostrar la cadena paso a paso
print("\nDescomposicion paso a paso (regla de la cadena general):")
print("  P(X1) = P(X1)")
print("  P(X1,X2) = P(X1) * P(X2|X1)")
print("  P(X1,X2,X3) = P(X1) * P(X2|X1) * P(X3|X1,X2)")
print("  Con independencias: cada factor solo depende de sus padres en la red.")
