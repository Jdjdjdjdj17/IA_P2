# _40_GramaticasIndependientesContexto.py
# Gramaticas Probabilisticas Independientes del Contexto (PCFG)
# Una gramatica libre de contexto define reglas de produccion:
#   S -> NP VP
#   NP -> Det N
#   VP -> V NP
# En la version probabilistica, cada regla tiene una probabilidad.
# P(arbol) = producto de probabilidades de todas las reglas usadas.
# Usado en analisis sintactico (parsing) de lenguaje natural.

import math
import random

print("=" * 55)
print("  GRAMATICAS PROBABILISTICAS INDEPENDIENTES DEL CONTEXTO (PCFG)")
print("=" * 55)

# ---- Gramatica ----
# Formato: no_terminal -> [(prob, produccion), ...]
gramatica = {
    "S":   [(1.0,  ["NP", "VP"])],
    "NP":  [(0.6,  ["Det", "N"]),
            (0.4,  ["N"])],
    "VP":  [(0.5,  ["V", "NP"]),
            (0.3,  ["V"]),
            (0.2,  ["V", "PP"])],
    "PP":  [(1.0,  ["P", "NP"])],
    "Det": [(0.5,  ["el"]),
            (0.3,  ["la"]),
            (0.2,  ["un"])],
    "N":   [(0.4,  ["gato"]),
            (0.3,  ["perro"]),
            (0.2,  ["parque"]),
            (0.1,  ["pescado"])],
    "V":   [(0.5,  ["come"]),
            (0.3,  ["ve"]),
            (0.2,  ["corre"])],
    "P":   [(0.6,  ["en"]),
            (0.4,  ["con"])],
}

terminales = {"el","la","un","gato","perro","parque","pescado","come","ve","corre","en","con"}

def es_terminal(simbolo):
    return simbolo in terminales

def generar(simbolo, profundidad=0):
    """Genera una oracion y su probabilidad"""
    if profundidad > 10:
        return [], 1.0
    if es_terminal(simbolo):
        return [simbolo], 1.0

    opciones = gramatica.get(simbolo, [])
    if not opciones:
        return [simbolo], 1.0

    probs  = [p for p,_ in opciones]
    idx    = random.choices(range(len(opciones)), weights=probs)[0]
    prob_r, produccion = opciones[idx]

    oracion = []; prob_total = prob_r
    for s in produccion:
        sub, p = generar(s, profundidad+1)
        oracion += sub
        prob_total *= p
    return oracion, prob_total

def log_prob_oracion(oracion_tokens, simbolo="S"):
    """CYK simplificado: calcula log-prob de la oracion dada la gramatica"""
    # Evaluacion aproximada usando la regla mas probable
    return None  # CYK completo es muy extenso; mostrar concepto

print("\nGramatica PCFG definida:")
for nt, reglas in gramatica.items():
    for prob, prod in reglas:
        print(f"  {nt} -> {' '.join(prod)}  [P={prob:.1f}]")

print("\nOraciones generadas con sus probabilidades:")
random.seed(1)
for _ in range(6):
    tokens, prob = generar("S")
    oracion = " ".join(tokens)
    print(f"  '{oracion}'  P={prob:.6f}  log_P={math.log(prob+1e-10):.3f}")

print("\nUso en PLN:")
print("  - Analisis sintactico probabilistico (CYK con probabilidades)")
print("  - Desambiguacion: elegir el arbol sintatico mas probable")
print("  - Entrenamiento: algoritmo Inside-Outside (analogo a Baum-Welch para HMM)")
