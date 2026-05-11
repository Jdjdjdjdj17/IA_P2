# _43_ExtraccionDeInformacion.py
# Extraccion de Informacion (Information Extraction)
# Identifica y estructura informacion especifica de texto no estructurado.
# Tareas principales:
#   - NER (Named Entity Recognition): identificar entidades (personas, lugares, orgs)
#   - Extraccion de relaciones: ej. "X trabaja en Y"
#   - Extraccion de eventos: ej. "X compro Y por Z dolares"
# Aqui implementamos un NER basado en reglas y un extractor de relaciones simple.

import re

print("=" * 55)
print("  EXTRACCION DE INFORMACION")
print("=" * 55)

# ---- NER basado en diccionarios y reglas ----
entidades = {
    "PERSONA":    {"Ana", "Carlos", "Maria", "Juan", "Pedro", "Luis"},
    "LUGAR":      {"Mexico", "Guadalajara", "Madrid", "Paris", "CETI", "UdeG"},
    "ORGANIZACION":{"Google", "Anthropic", "Microsoft", "OpenAI", "Apple"},
    "FECHA":      set(),  # detectada por regex
}

patron_fecha = re.compile(r'\b(\d{1,2}/\d{1,2}/\d{4}|\d{4}|enero|febrero|marzo|abril|mayo|'
                           r'junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\b')

def ner(texto):
    tokens  = texto.split()
    etiquetas = ["O"] * len(tokens)

    for i, token in enumerate(tokens):
        tok_limpio = token.strip(".,;:!?\"'")
        # Buscar en diccionarios
        for tipo, conjunto in entidades.items():
            if tok_limpio in conjunto:
                etiquetas[i] = f"B-{tipo}"
                break
        # Fechas por regex
        if patron_fecha.match(tok_limpio):
            etiquetas[i] = "B-FECHA"

    return list(zip(tokens, etiquetas))

# ---- Extraccion de relaciones simples ----
patrones_relacion = [
    (re.compile(r'(\w+) trabaja en (\w+)'),       "TRABAJA_EN"),
    (re.compile(r'(\w+) estudio en (\w+)'),       "ESTUDIO_EN"),
    (re.compile(r'(\w+) fundó (\w+)'),             "FUNDO"),
    (re.compile(r'(\w+) nació en (\w+)'),          "NACIO_EN"),
]

def extraer_relaciones(texto):
    relaciones = []
    for patron, tipo in patrones_relacion:
        for match in patron.finditer(texto):
            relaciones.append((match.group(1), tipo, match.group(2)))
    return relaciones

# ---- Textos de ejemplo ----
textos = [
    "Ana trabaja en Google desde 2020.",
    "Carlos estudio en UdeG y luego en Madrid.",
    "Maria nació en Guadalajara en 1990.",
    "Juan fundó Anthropic junto con otros investigadores.",
    "Pedro trabaja en Microsoft en su oficina de Mexico.",
]

print("\nNER (Reconocimiento de Entidades Nombradas):")
for texto in textos:
    print(f"\n  Texto: '{texto}'")
    resultado = ner(texto)
    entidades_encontradas = [(t,e) for t,e in resultado if e != "O"]
    if entidades_encontradas:
        for tok, etiq in entidades_encontradas:
            print(f"    [{etiq}] {tok}")

print("\nExtraccion de Relaciones:")
for texto in textos:
    rels = extraer_relaciones(texto)
    if rels:
        for suj, rel, obj in rels:
            print(f"  ({suj}) --[{rel}]--> ({obj})")
