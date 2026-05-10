# _25_AlgoritmoEM.py
# Algoritmo EM (Expectation-Maximization)
# Aprende parametros de un modelo cuando hay variables LATENTES (ocultas).
# Alterna entre dos pasos:
#   E (Expectation): estima las variables latentes dado los parametros actuales
#   M (Maximization): actualiza los parametros para maximizar la verosimilitud
#
# Ejemplo clasico: Mezcla de Gaussianas (Gaussian Mixture Model)

import random
import math

print("=" * 55)
print("  ALGORITMO EM — MEZCLA DE GAUSSIANAS (1D)")
print("=" * 55)

# ---- Generar datos de dos gaussianas mezcladas ----
random.seed(42)
mu1_real, mu2_real = 2.0, 8.0
sigma = 1.5
datos = [random.gauss(mu1_real, sigma) for _ in range(30)] + \
        [random.gauss(mu2_real, sigma) for _ in range(30)]
random.shuffle(datos)

def gauss(x, mu, sigma):
    return (1/(sigma*math.sqrt(2*math.pi))) * math.exp(-0.5*((x-mu)/sigma)**2)

# ---- Inicializacion aleatoria de parametros ----
mu1, mu2 = 1.0, 9.0   # medias iniciales (intencionalmente incorrectas)
pi1, pi2 = 0.5, 0.5   # pesos de mezcla

print(f"\nDatos: 30 puntos de N({mu1_real},{sigma}) + 30 de N({mu2_real},{sigma})")
print(f"Init:  mu1={mu1}, mu2={mu2}, pi1={pi1:.2f}, pi2={pi2:.2f}\n")
print(f"{'Iter':<6} {'mu1':<10} {'mu2':<10} {'pi1':<8} {'pi2':<8} {'Log-verosim.'}")
print("-" * 54)

for it in range(20):
    # ---- Paso E: calcular responsabilidades ----
    r1 = []; r2 = []
    for x in datos:
        p1 = pi1 * gauss(x, mu1, sigma)
        p2 = pi2 * gauss(x, mu2, sigma)
        total = p1 + p2 + 1e-10
        r1.append(p1/total)
        r2.append(p2/total)

    # ---- Paso M: actualizar parametros ----
    N1 = sum(r1); N2 = sum(r2)
    mu1 = sum(r*x for r,x in zip(r1,datos)) / (N1 + 1e-10)
    mu2 = sum(r*x for r,x in zip(r2,datos)) / (N2 + 1e-10)
    pi1 = N1 / len(datos)
    pi2 = N2 / len(datos)

    # Log-verosimilitud
    log_v = sum(math.log(pi1*gauss(x,mu1,sigma) + pi2*gauss(x,mu2,sigma) + 1e-10) for x in datos)

    if it < 5 or it % 5 == 4:
        print(f"{it+1:<6} {mu1:<10.4f} {mu2:<10.4f} {pi1:<8.4f} {pi2:<8.4f} {log_v:.4f}")

print(f"\nResultado final:")
print(f"  mu1 = {mu1:.4f}  (real: {mu1_real})")
print(f"  mu2 = {mu2:.4f}  (real: {mu2_real})")
print(f"  pi1 = {pi1:.4f}  pi2 = {pi2:.4f}")
