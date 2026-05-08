# _04_DistribucionDeProbabilidad.py
# Distribucion de Probabilidad
# Asigna una probabilidad a cada posible valor de una variable aleatoria.
# - Discreta: valores contables (dados, monedas, diagnosticos)
# - Continua: valores reales (temperatura, altura) — aqui usamos histogramas

import random
import math

print("=" * 50)
print("  DISTRIBUCIONES DE PROBABILIDAD")
print("=" * 50)

# ---- 1. Distribucion Uniforme Discreta ----
print("\n1. Uniforme discreta — dado de 6 caras:")
caras = list(range(1, 7))
p = 1 / len(caras)
for c in caras:
    barra = "█" * 10
    print(f"   P(X={c}) = {p:.3f}  {barra}")

# ---- 2. Distribucion de Bernoulli ----
p_exito = 0.7
print(f"\n2. Bernoulli — exito con P={p_exito}:")
print(f"   P(X=1) = {p_exito:.2f}  {'█'*int(p_exito*20)}")
print(f"   P(X=0) = {1-p_exito:.2f}  {'█'*int((1-p_exito)*20)}")

# ---- 3. Distribucion Binomial (n lanzamientos) ----
def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)

def combinatoria(n, k):
    return factorial(n) // (factorial(k) * factorial(n-k))

def binomial(n, k, p):
    return combinatoria(n, k) * (p**k) * ((1-p)**(n-k))

n, p_bin = 5, 0.5
print(f"\n3. Binomial — {n} lanzamientos de moneda justa:")
for k in range(n+1):
    pb = binomial(n, k, p_bin)
    barra = "█" * int(pb * 60)
    print(f"   P(X={k}) = {pb:.4f}  {barra}")

# ---- 4. Distribucion Normal (aproximacion discreta) ----
def normal_pdf(x, mu, sigma):
    return (1/(sigma * math.sqrt(2*math.pi))) * math.exp(-0.5*((x-mu)/sigma)**2)

mu, sigma = 0, 1
print(f"\n4. Normal aproximada — mu={mu}, sigma={sigma}:")
for x_val in [-2, -1, 0, 1, 2]:
    p_n = normal_pdf(x_val, mu, sigma)
    barra = "█" * int(p_n * 80)
    print(f"   f({x_val:+}) = {p_n:.4f}  {barra}")

print("\nPropiedad clave: la suma (o integral) de toda distribucion = 1")
