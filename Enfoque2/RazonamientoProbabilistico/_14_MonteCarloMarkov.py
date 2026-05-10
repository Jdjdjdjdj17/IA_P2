# _14_MonteCarloMarkov.py
# Monte Carlo para Cadenas de Markov (MCMC) — Gibbs Sampling
# Metodo de muestreo que genera una cadena de estados donde cada estado
# depende solo del anterior (cadena de Markov).
#
# Gibbs Sampling: en cada paso, muestrea UNA variable a la vez
# condicionada a su Manto de Markov (las demas variables fijas).
# Tras un periodo de calentamiento, las muestras aproximan la distribucion real.

import random
import math

print("=" * 55)
print("  MCMC — GIBBS SAMPLING")
print("=" * 55)

# ---- Red: N -> A, N -> L, A+L -> M ----
def p_nublado_dado_manto(a, l):
    # P(N | A, L) proporcional a P(N)*P(A|N)*P(L|N)
    def calc(n):
        p_n  = 0.5
        p_a  = 0.10 if n=="si" else 0.50 if a=="si" else (0.90 if n=="si" else 0.50)
        p_l  = 0.80 if (n=="si" and l=="si") else \
               0.20 if (n=="si" and l=="no") else \
               0.20 if (n=="no" and l=="si") else 0.80
        # Simplificado
        p_an = {"si":{"si":0.10,"no":0.90},"no":{"si":0.50,"no":0.50}}[n][a]
        p_ln = {"si":{"si":0.80,"no":0.20},"no":{"si":0.20,"no":0.80}}[n][l]
        return p_n * p_an * p_ln
    si = calc("si"); no = calc("no")
    return si / (si + no)

def p_mojado_dado_manto(a, l):
    tabla = {("si","si"):0.99,("si","no"):0.90,("no","si"):0.90,("no","no"):0.00}
    return tabla[(a,l)]

def gibbs_sample(evidencia, query_var, N=5000, warmup=500):
    """Estima P(query_var=si | evidencia) con Gibbs Sampling"""
    # Estado inicial
    estado = {"N":"si", "A":"si", "L":"si", "M":"si"}
    estado.update(evidencia)

    libres = [v for v in estado if v not in evidencia]
    conteo_si = 0
    total = 0

    for t in range(N + warmup):
        for var in libres:
            # Muestrear var condicionada al resto
            if var == "N":
                p = p_nublado_dado_manto(estado["A"], estado["L"])
            elif var == "M":
                p = p_mojado_dado_manto(estado["A"], estado["L"])
            elif var == "A":
                p_an = {"si":{"si":0.10,"no":0.90},"no":{"si":0.50,"no":0.50}}[estado["N"]]["si"]
                p_m  = p_mojado_dado_manto("si", estado["L"])
                p_nm = p_mojado_dado_manto("no", estado["L"])
                p = (p_an * p_m) / (p_an*p_m + (1-p_an)*p_nm)
            elif var == "L":
                p_ln = {"si":{"si":0.80,"no":0.20},"no":{"si":0.20,"no":0.80}}[estado["N"]]["si"]
                p_m  = p_mojado_dado_manto(estado["A"], "si")
                p_nm = p_mojado_dado_manto(estado["A"], "no")
                p = (p_ln * p_m) / (p_ln*p_m + (1-p_ln)*p_nm)
            else:
                p = 0.5
            estado[var] = "si" if random.random() < p else "no"

        if t >= warmup:
            total += 1
            if estado[query_var] == "si":
                conteo_si += 1

    return conteo_si / total if total > 0 else 0

evidencia = {"M": "si"}
print(f"\nConsulta: P(L=si | M=si) con Gibbs Sampling")
print(f"Evidencia: {evidencia}")
print(f"Muestras: 5000 + 500 warmup\n")

resultado = gibbs_sample(evidencia, "L", N=5000, warmup=500)
print(f"P(L=si | M=si) ≈ {resultado:.4f}  (valor real ≈ 0.708)")

print(f"\nVentaja de MCMC/Gibbs:")
print(f"  - Funciona bien incluso con evidencia de baja probabilidad")
print(f"  - Escala mejor que enumeracion o eliminacion en redes grandes")
print(f"  - El warmup descarta las muestras iniciales (sesgo de estado inicial)")
