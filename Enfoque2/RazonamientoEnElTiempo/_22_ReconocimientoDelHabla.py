# _22_ReconocimientoDelHabla.py
# Reconocimiento del Habla
# Aplicacion clasica de HMMs: cada palabra o fonema se modela como un HMM.
# El sistema encuentra la secuencia de palabras mas probable dado el audio.
#
# P(palabras | audio) proporcional a P(audio | palabras) * P(palabras)
#                                     (modelo acustico)   (modelo de lenguaje)
#
# Aqui simulamos una version simplificada con vectores de caracteristicas.

import random
import math

print("=" * 55)
print("  RECONOCIMIENTO DEL HABLA (SIMPLIFICADO)")
print("=" * 55)

# ---- Modelo simplificado ----
# Vocabulario de 3 palabras, cada una representada por un HMM de 2 estados
# Caracteristicas: un valor numerico (frecuencia dominante simplificada)

palabras = ["hola", "adios", "gracias"]

# Para cada palabra: distribucion de probabilidad sobre "frecuencias" observadas
# (en un sistema real serian vectores MFCC)
modelos_acusticos = {
    "hola":    [0.5, 0.3, 0.1, 0.1],   # prob de frecuencia baja, media-baja, media-alta, alta
    "adios":   [0.1, 0.2, 0.4, 0.3],
    "gracias": [0.1, 0.1, 0.3, 0.5],
}

modelo_lenguaje = {
    "hola": 0.50, "adios": 0.30, "gracias": 0.20
}

def generar_audio(palabra, n_frames=5):
    """Simula frames de audio para una palabra"""
    probs = modelos_acusticos[palabra]
    return [random.choices([0,1,2,3], weights=probs)[0] for _ in range(n_frames)]

def log_verosimilitud(frames, palabra):
    """Log P(audio | palabra) = suma log P(frame_i | palabra)"""
    probs = modelos_acusticos[palabra]
    return sum(math.log(probs[f] + 1e-10) for f in frames)

def reconocer(frames):
    """Encuentra la palabra con mayor P(audio|pal)*P(pal)"""
    scores = {}
    for pal in palabras:
        log_acustico  = log_verosimilitud(frames, pal)
        log_lenguaje  = math.log(modelo_lenguaje[pal])
        scores[pal]   = log_acustico + log_lenguaje
    return scores

print("\nSimulacion de reconocimiento de 5 utterances:")
print(f"{'Palabra_real':<14} {'Audio(frames)':<20} {'Reconocida':<12} {'Correcto'}")
print("-" * 58)

correctos = 0
for _ in range(5):
    pal_real = random.choice(palabras)
    frames   = generar_audio(pal_real)
    scores   = reconocer(frames)
    reconocida = max(scores, key=scores.get)
    ok = "✓" if reconocida == pal_real else "✗"
    if reconocida == pal_real: correctos += 1
    print(f"{pal_real:<14} {str(frames):<20} {reconocida:<12} {ok}")

print(f"\nPrecision: {correctos}/5")
print(f"\nEn sistemas reales:")
print(f"  - Audio -> MFCC (vectores de 13-39 coeficientes por frame de 25ms)")
print(f"  - Modelo acustico: HMM por fonema entrenado con miles de horas de audio")
print(f"  - Modelo de lenguaje: n-gramas o redes neuronales sobre millones de textos")
