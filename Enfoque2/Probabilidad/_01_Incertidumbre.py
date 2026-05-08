# _01_Incertidumbre.py
# Incertidumbre en IA
# El mundo real es incierto: el agente no siempre sabe el estado exacto.
# La probabilidad es la herramienta matematica para manejar esa incertidumbre.
#
# Tipos de incertidumbre:
#   - Ignorancia: falta de informacion
#   - Aleatoriedad: el mundo es intrinsecamente impredecible
#
# Ejemplo: el agente no sabe si va a llover, pero puede asignarle una probabilidad.

import random

print("=" * 45)
print("  INCERTIDUMBRE EN IA")
print("=" * 45)

# ---- Escenario: diagnostico medico incierto ----
# El agente no sabe con certeza si el paciente tiene gripe
# pero tiene evidencia (sintomas) y probabilidades asociadas

sintomas_observados = ["fiebre", "tos"]

# Base de conocimiento con incertidumbre
enfermedades = {
    "gripe":     {"fiebre": 0.9, "tos": 0.8, "erupciones": 0.1},
    "resfriado": {"fiebre": 0.4, "tos": 0.9, "erupciones": 0.05},
    "alergia":   {"fiebre": 0.1, "tos": 0.6, "erupciones": 0.7},
}

print(f"\nSintomas observados: {sintomas_observados}")
print("\nProbabilidad de cada sintoma por enfermedad:")
print(f"{'Enfermedad':<14}", end="")
for s in sintomas_observados:
    print(f"{s:<12}", end="")
print()
print("-" * 38)

scores = {}
for enfermedad, probs in enfermedades.items():
    score = 1.0
    print(f"{enfermedad:<14}", end="")
    for s in sintomas_observados:
        p = probs.get(s, 0)
        print(f"{p:<12}", end="")
        score *= p
    scores[enfermedad] = score
    print()

# Normalizar para obtener probabilidades aproximadas
total = sum(scores.values())
print("\nProbabilidad aproximada (producto normalizado):")
for enf, s in scores.items():
    print(f"  P({enf} | sintomas) ~ {s/total:.3f}")

mas_probable = max(scores, key=scores.get)
print(f"\nDiagnostico mas probable: {mas_probable}")
print("\nNota: esto es incertidumbre manejada con probabilidad,")
print("no certeza absoluta. El agente razona bajo informacion incompleta.")
