# _13_PonderacionDeVerosimilitud.py
# Ponderacion de Verosimilitud (Likelihood Weighting)
# Mejora del muestreo por rechazo: en lugar de rechazar muestras,
# las acepta todas pero les asigna un PESO segun la probabilidad
# de la evidencia observada.
#
# Peso = producto de P(Ei | Padres(Ei)) para cada variable de evidencia Ei.

import random

print("=" * 55)
print("  PONDERACION DE VEROSIMILITUD")
print("=" * 55)

# ---- Misma red: N -> A, N -> L, A+L -> M ----
def p_aspersor(a, n):
    tabla = {"si": {"si":0.10,"no":0.90}, "no": {"si":0.50,"no":0.50}}
    return tabla[n][a]

def p_lluvia(l, n):
    tabla = {"si": {"si":0.80,"no":0.20}, "no": {"si":0.20,"no":0.80}}
    return tabla[n][l]

def p_mojado(m, a, l):
    tabla = {("si","si"):{"si":0.99,"no":0.01}, ("si","no"):{"si":0.90,"no":0.10},
             ("no","si"):{"si":0.90,"no":0.10}, ("no","no"):{"si":0.00,"no":1.00}}
    return tabla[(a,l)][m]

def muestrear(p_si):
    return "si" if random.random() < p_si else "no"

def likelihood_weighting(evidencia, N=10000):
    """
    evidencia: dict con variables fijas, ej. {"M": "si"}
    Retorna estimacion de P(L=si | evidencia)
    """
    peso_l_si  = 0.0
    peso_total = 0.0

    for _ in range(N):
        peso = 1.0

        # Muestrear o fijar segun evidencia (orden topologico)
        n = muestrear(0.5)   # Nublado siempre libre

        if "A" in evidencia:
            a = evidencia["A"]
            peso *= p_aspersor(a, n)
        else:
            a = muestrear(0.10 if n=="si" else 0.50)

        if "L" in evidencia:
            l = evidencia["L"]
            peso *= p_lluvia(l, n)
        else:
            l = muestrear(0.80 if n=="si" else 0.20)

        if "M" in evidencia:
            m = evidencia["M"]
            peso *= p_mojado(m, a, l)
        else:
            m = muestrear(p_mojado("si", a, l))

        peso_total += peso
        if l == "si":
            peso_l_si += peso

    return peso_l_si / peso_total if peso_total > 0 else 0

N_muestras = 10000
evidencia  = {"M": "si"}

print(f"\nConsulta: P(L=si | M=si)")
print(f"Evidencia: {evidencia}")
print(f"Muestras: {N_muestras}\n")

resultado = likelihood_weighting(evidencia, N_muestras)
print(f"P(L=si | M=si) ≈ {resultado:.4f}  (valor real ≈ 0.708)")

print(f"\nVentaja vs Muestreo por Rechazo:")
print(f"  - Nunca descarta muestras")
print(f"  - Mas eficiente cuando la evidencia tiene baja probabilidad")
print(f"  - Sesgo puede aparecer si el peso es muy concentrado en pocas muestras")
