# _12_MuestreoDirectoYRechazo.py
# Muestreo Directo y Por Rechazo
# Metodos aproximados de inferencia en Redes Bayesianas.
#
# Muestreo Directo: genera muestras siguiendo el orden topologico de la red.
# Muestreo Por Rechazo: igual, pero descarta muestras que no coinciden con la evidencia.
# La fraccion de muestras aceptadas aproxima la probabilidad consultada.

import random

print("=" * 55)
print("  MUESTREO DIRECTO Y POR RECHAZO")
print("=" * 55)

# ---- Red: Nublado(N) -> Aspersor(A), Lluvia(L) -> Mojado(M) <- Aspersor ----
def muestrear_nublado():
    return "si" if random.random() < 0.5 else "no"

def muestrear_aspersor(n):
    p = 0.10 if n == "si" else 0.50
    return "si" if random.random() < p else "no"

def muestrear_lluvia(n):
    p = 0.80 if n == "si" else 0.20
    return "si" if random.random() < p else "no"

def muestrear_mojado(a, l):
    tabla = {("si","si"):0.99, ("si","no"):0.90, ("no","si"):0.90, ("no","no"):0.00}
    return "si" if random.random() < tabla[(a,l)] else "no"

def muestra_completa():
    n = muestrear_nublado()
    a = muestrear_aspersor(n)
    l = muestrear_lluvia(n)
    m = muestrear_mojado(a, l)
    return {"N":n, "A":a, "L":l, "M":m}

N_muestras = 10000

# ---- Muestreo Directo: P(L=si) ----
print(f"\nMuestreo Directo ({N_muestras} muestras)")
print("Estimando P(Lluvia=si)...")
conteo_l_si = sum(1 for _ in range(N_muestras) if muestra_completa()["L"] == "si")
p_l_aprox = conteo_l_si / N_muestras
print(f"  Muestras con L=si: {conteo_l_si}/{N_muestras}")
print(f"  P(L=si) ≈ {p_l_aprox:.4f}  (valor real ≈ 0.50)")

# ---- Muestreo Por Rechazo: P(L=si | M=si) ----
print(f"\nMuestreo Por Rechazo ({N_muestras} muestras)")
print("Estimando P(Lluvia=si | Mojado=si)...")
aceptadas  = 0
l_si_dado_m_si = 0
for _ in range(N_muestras):
    s = muestra_completa()
    if s["M"] == "si":          # solo acepta si coincide con evidencia
        aceptadas += 1
        if s["L"] == "si":
            l_si_dado_m_si += 1

if aceptadas > 0:
    p_cond = l_si_dado_m_si / aceptadas
else:
    p_cond = 0

print(f"  Muestras aceptadas (M=si): {aceptadas}/{N_muestras}")
print(f"  De esas, L=si: {l_si_dado_m_si}")
print(f"  P(L=si | M=si) ≈ {p_cond:.4f}  (valor real ≈ 0.708)")

print(f"\nDesventaja del rechazo: si la evidencia es rara,")
print(f"se descartan demasiadas muestras (ineficiente).")
print(f"Solucion: Ponderacion de Verosimilitud o MCMC.")
