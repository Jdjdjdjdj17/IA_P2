# _07_RedBayesiana.py
# Red Bayesiana (Bayesian Network)
# Grafo dirigido aciclico (DAG) donde:
#   - Nodos = variables aleatorias
#   - Aristas = dependencias causales
#   - Cada nodo tiene una tabla de probabilidad condicional (CPT)
#
# Permite representar distribuciones conjuntas de forma compacta.
# P(X1,...,Xn) = producto de P(Xi | Padres(Xi))

print("=" * 55)
print("  RED BAYESIANA")
print("=" * 55)

# ---- Red: Nublado -> Aspersor, Nublado -> Lluvia
#           Aspersor -> Mojado, Lluvia -> Mojado        ----
#
#   Nublado (N)
#    /       \
# Aspersor(A) Lluvia(L)
#    \       /
#    Mojado(M)

# Tablas de probabilidad condicional (CPT)
P_N = {"si": 0.5, "no": 0.5}

P_A_dado_N = {
    "si": {"si": 0.10, "no": 0.90},   # si nublado, aspersor poco probable
    "no": {"si": 0.50, "no": 0.50},
}

P_L_dado_N = {
    "si": {"si": 0.80, "no": 0.20},
    "no": {"si": 0.20, "no": 0.80},
}

P_M_dado_A_L = {
    ("si","si"): {"si": 0.99, "no": 0.01},
    ("si","no"): {"si": 0.90, "no": 0.10},
    ("no","si"): {"si": 0.90, "no": 0.10},
    ("no","no"): {"si": 0.00, "no": 1.00},
}

print("\nEstructura: Nublado -> Aspersor, Lluvia -> Mojado")

def joint(n, a, l, m):
    """Calcula P(N=n, A=a, L=l, M=m) usando la regla de la cadena de la red"""
    p = P_N[n]
    p *= P_A_dado_N[n][a]
    p *= P_L_dado_N[n][l]
    p *= P_M_dado_A_L[(a,l)][m]
    return p

# Verificar que la distribucion suma 1
total = 0
print("\nAlgunas probabilidades conjuntas:")
print(f"  {'N':<5} {'A':<5} {'L':<5} {'M':<5} {'P(N,A,L,M)'}")
print("  " + "-" * 38)
for n in ["si","no"]:
    for a in ["si","no"]:
        for l in ["si","no"]:
            for m in ["si","no"]:
                p = joint(n,a,l,m)
                total += p
                if p > 0.01:
                    print(f"  {n:<5} {a:<5} {l:<5} {m:<5} {p:.4f}")

print(f"\nSuma total de la distribucion conjunta: {total:.4f}  (debe ser 1.0)")

# Consulta: P(M=si) marginalizando todo
p_m_si = sum(joint(n,a,l,"si") for n in ["si","no"]
             for a in ["si","no"] for l in ["si","no"])
print(f"\nConsulta P(Mojado=si) = {p_m_si:.4f}")
