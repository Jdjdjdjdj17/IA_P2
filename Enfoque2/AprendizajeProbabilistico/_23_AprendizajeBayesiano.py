# _23_AprendizajeBayesiano.py
# Aprendizaje Bayesiano
# En lugar de aprender UN solo modelo, el agente mantiene una distribucion
# sobre todos los modelos posibles y la actualiza con los datos.
#
# P(hipotesis | datos) = P(datos | hipotesis) * P(hipotesis) / P(datos)
# La prediccion promedia sobre todas las hipotesis: P(y | datos) = suma_h P(y|h)*P(h|datos)

import random
import math

print("=" * 55)
print("  APRENDIZAJE BAYESIANO")
print("=" * 55)

# ---- Ejemplo: inferir la probabilidad p de cara en una moneda ----
# Hipotesis: p puede ser 0.1, 0.2, ..., 0.9
# Prior uniforme sobre las hipotesis

hipotesis = [round(i*0.1, 1) for i in range(1, 10)]  # 0.1 a 0.9
prior     = {h: 1/len(hipotesis) for h in hipotesis}  # uniforme

def verosimilitud(datos, p):
    """P(datos | p) = producto de P(cada lanzamiento | p)"""
    resultado = 1.0
    for d in datos:
        resultado *= p if d == "cara" else (1 - p)
    return resultado

def actualizar(prior, datos):
    """Regla de Bayes: calcula posterior dado los datos"""
    posterior = {}
    for h in hipotesis:
        posterior[h] = prior[h] * verosimilitud(datos, h)
    total = sum(posterior.values())
    return {h: posterior[h]/total for h in hipotesis}

def predecir_cara(posterior):
    """P(siguiente=cara | datos) = suma_h P(cara|h)*P(h|datos) = suma_h h*P(h|datos)"""
    return sum(h * posterior[h] for h in hipotesis)

print(f"\nMoneda: inferir prob de cara con aprendizaje bayesiano")
print(f"Hipotesis: {hipotesis}")
print(f"\nPrior: uniforme = {1/len(hipotesis):.3f} para cada hipotesis\n")

# Simular lanzamientos de una moneda con p_real = 0.6
p_real = 0.6
posterior = prior.copy()
datos_acumulados = []

print(f"{'Lanzam.':<10} {'Resultado':<12} {'Prediccion_cara':<18} {'H_mas_probable'}")
print("-" * 54)
for i in range(1, 16):
    resultado = "cara" if random.random() < p_real else "cruz"
    datos_acumulados.append(resultado)
    posterior = actualizar(prior, datos_acumulados)
    pred      = predecir_cara(posterior)
    mejor_h   = max(hipotesis, key=lambda h: posterior[h])
    print(f"{i:<10} {resultado:<12} {pred:<18.4f} {mejor_h}")

print(f"\nPosterior final sobre hipotesis:")
for h, p in sorted(posterior.items(), key=lambda x: -x[1])[:5]:
    barra = "█" * int(p * 40)
    print(f"  P(p={h} | datos) = {p:.4f}  {barra}")
print(f"\nP(cara real) = {p_real}  |  Prediccion final = {predecir_cara(posterior):.4f}")
