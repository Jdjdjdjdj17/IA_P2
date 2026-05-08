# _05_IndependenciaCondicional.py
# Independencia Condicional
# A y B son condicionalmente independientes dado C si:
#   P(A, B | C) = P(A | C) * P(B | C)
# Es decir, una vez que conocemos C, saber B no cambia nuestra creencia sobre A.
#
# Esto es la base de las Redes Bayesianas: simplifica enormemente el calculo.

print("=" * 55)
print("  INDEPENDENCIA CONDICIONAL")
print("=" * 55)

# ---- Ejemplo: lluvia, aspersor y cesped mojado ----
# Variables: Lluvia (L), Aspersor (A), Cesped_Mojado (M)
# El cesped se moja si llueve O si el aspersor esta activo.
# Dado que sabemos que el cesped esta mojado (M=si),
# Lluvia y Aspersor YA NO son independientes (explicacion-por-via).

# Tabla conjunta completa P(L, A, M)
tabla = {
    # (L, A, M)       prob
    ("si","si","si"): 0.288,
    ("si","si","no"): 0.012,
    ("si","no","si"): 0.180,
    ("si","no","no"): 0.020,
    ("no","si","si"): 0.216,
    ("no","si","no"): 0.144,
    ("no","no","si"): 0.000,
    ("no","no","no"): 0.140,
}

print("\nTabla conjunta P(Lluvia, Aspersor, Cesped_Mojado):")
print(f"  {'L':<5} {'A':<5} {'M':<5} {'P'}")
print("  " + "-" * 24)
for (l,a,m), p in tabla.items():
    print(f"  {l:<5} {a:<5} {m:<5} {p:.3f}")

# ---- Verificar independencia marginal de L y A ----
p_l_si = sum(v for (l,a,m),v in tabla.items() if l=="si")
p_a_si = sum(v for (l,a,m),v in tabla.items() if a=="si")
p_l_a_si = sum(v for (l,a,m),v in tabla.items() if l=="si" and a=="si")

print(f"\nIndependencia marginal P(L,A) = P(L)*P(A)?")
print(f"  P(L=si)          = {p_l_si:.3f}")
print(f"  P(A=si)          = {p_a_si:.3f}")
print(f"  P(L=si)*P(A=si)  = {p_l_si*p_a_si:.3f}")
print(f"  P(L=si, A=si)    = {p_l_a_si:.3f}")
ind = abs(p_l_si*p_a_si - p_l_a_si) < 0.01
print(f"  Son independientes marginalmente: {ind}")

# ---- Verificar independencia condicional dado M=si ----
p_m_si = sum(v for (l,a,m),v in tabla.items() if m=="si")
p_l_m  = sum(v for (l,a,m),v in tabla.items() if l=="si" and m=="si") / p_m_si
p_a_m  = sum(v for (l,a,m),v in tabla.items() if a=="si" and m=="si") / p_m_si
p_la_m = sum(v for (l,a,m),v in tabla.items() if l=="si" and a=="si" and m=="si") / p_m_si

print(f"\nIndependencia condicional dado M=si:")
print(f"  P(L=si|M=si)             = {p_l_m:.3f}")
print(f"  P(A=si|M=si)             = {p_a_m:.3f}")
print(f"  P(L=si|M=si)*P(A=si|M=si)= {p_l_m*p_a_m:.3f}")
print(f"  P(L=si,A=si|M=si)        = {p_la_m:.3f}")
cond_ind = abs(p_l_m*p_a_m - p_la_m) < 0.01
print(f"  Son condicionalmente independientes dado M: {cond_ind}")
print(f"\nConclucion: al saber que el cesped esta mojado, L y A se vuelven DEPENDIENTES.")
