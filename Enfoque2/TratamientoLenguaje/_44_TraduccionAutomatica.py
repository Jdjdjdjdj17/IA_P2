# _44_TraduccionAutomatica.py
# Traduccion Automatica Estadistica (SMT — Statistical Machine Translation)
# Modelo clasico antes de los transformers.
# P(traduccion | original) = P(original | traduccion) * P(traduccion) / P(original)
#   = Modelo de traduccion * Modelo de lenguaje
#
# Aqui implementamos un traductor simple basado en:
#   - Tabla de probabilidades de traduccion de palabras (IBM Model 1 simplificado)
#   - Modelo de bigrama del idioma destino

import math
import random
from collections import defaultdict

print("=" * 55)
print("  TRADUCCION AUTOMATICA ESTADISTICA")
print("=" * 55)

# ---- Tabla de traduccion: P(palabra_es | palabra_en) ----
tabla_traduccion = {
    "the":   {"el": 0.5, "la": 0.3, "los": 0.1, "las": 0.1},
    "cat":   {"gato": 0.8, "felino": 0.2},
    "dog":   {"perro": 0.9, "can": 0.1},
    "eats":  {"come": 0.7, "ingiere": 0.2, "devora": 0.1},
    "runs":  {"corre": 0.8, "huye": 0.2},
    "fish":  {"pescado": 0.6, "pez": 0.4},
    "park":  {"parque": 1.0},
    "in":    {"en": 0.7, "dentro": 0.2, "hacia": 0.1},
    "quickly":{"rapido": 0.6, "velozmente": 0.4},
    "a":     {"un": 0.5, "una": 0.5},
    "big":   {"grande": 0.7, "enorme": 0.3},
}

# ---- Modelo de lenguaje (bigrama) del espanol simplificado ----
modelo_lenguaje = {
    ("<s>", "el"):      0.15,  ("<s>", "la"):     0.10,  ("<s>", "un"):    0.08,
    ("el",  "gato"):    0.20,  ("el",  "perro"):  0.20,  ("el",  "parque"):0.10,
    ("la",  "gata"):    0.15,  ("un",  "gato"):   0.10,
    ("gato","come"):    0.30,  ("perro","corre"):  0.25,  ("perro","come"): 0.20,
    ("come","pescado"): 0.40,  ("corre","rapido"): 0.30,  ("come","rapido"):0.10,
    ("pescado","</s>"): 0.50,  ("rapido","</s>"):  0.60,  ("parque","</s>"):0.40,
    ("en",  "el"):      0.50,  ("el", "parque"):   0.30,
}

def p_traduccion(palabra_es, palabra_en):
    return tabla_traduccion.get(palabra_en, {}).get(palabra_es, 0.001)

def p_bigrama_es(w2, w1):
    return modelo_lenguaje.get((w1, w2), 0.01)

def traducir_greedy(oracion_en):
    """Traduce palabra a palabra eligiendo la traduccion mas probable"""
    palabras = oracion_en.lower().split()
    traduccion = []
    for pal_en in palabras:
        opciones = tabla_traduccion.get(pal_en, {pal_en: 1.0})
        mejor = max(opciones, key=opciones.get)
        traduccion.append(mejor)
    return " ".join(traduccion)

def score_traduccion(oracion_es, oracion_en):
    """Calcula log P(en|es) * P(es)"""
    tokens_en = oracion_en.lower().split()
    tokens_es = oracion_es.lower().split()
    log_score  = 0

    # Modelo de traduccion (alineamiento simple 1-a-1)
    for en, es in zip(tokens_en, tokens_es):
        log_score += math.log(p_traduccion(es, en) + 1e-10)

    # Modelo de lenguaje en espanol
    tokens_full = ["<s>"] + tokens_es + ["</s>"]
    for i in range(len(tokens_full)-1):
        log_score += math.log(p_bigrama_es(tokens_full[i+1], tokens_full[i]) + 1e-10)

    return log_score

# ---- Ejemplos de traduccion ----
oraciones_en = [
    "the cat eats fish",
    "the dog runs quickly",
    "a big dog runs in the park",
]

print("\nTraduccion Greedy (palabra a palabra):")
for oracion in oraciones_en:
    trad = traducir_greedy(oracion)
    print(f"  EN: '{oracion}'")
    print(f"  ES: '{trad}'\n")

# ---- Evaluar candidatos ----
print("Evaluacion de candidatos (score = log P(en|es) + log P(es)):")
candidatos = [
    ("the cat eats fish", "el gato come pescado"),
    ("the cat eats fish", "la gato pescado come"),
    ("the dog runs quickly", "el perro corre rapido"),
]
for en, es in candidatos:
    s = score_traduccion(es, en)
    print(f"  '{en}' -> '{es}'  score={s:.3f}")
