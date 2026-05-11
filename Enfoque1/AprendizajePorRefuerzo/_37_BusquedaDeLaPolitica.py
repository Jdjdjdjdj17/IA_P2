# _37_BusquedaDeLaPolitica.py
# Busqueda de la Politica (Policy Search / REINFORCE)
# En lugar de aprender V(s) o Q(s,a), optimiza directamente los parametros
# de la politica pi(a|s; theta) usando gradiente de la recompensa esperada.
#
# Metodo: REINFORCE (Williams, 1992) — simplificado con politica tabular
# Actualiza: theta(s,a) += alpha * G_t * log pi(a|s)
# donde G_t es el retorno acumulado desde el paso t.

import random
import math

estados  = [0, 1, 2, 3]
acciones = [-1, 1]
gamma    = 0.9
alpha    = 0.05
episodios = 3000

def recompensa(estado):
    if estado == 3: return  10
    if estado == 0: return  -5
    return -1

def siguiente(estado, accion):
    return max(0, min(3, estado + accion))

# Parametros de la politica (preferencias): theta[s][a]
theta = {s: {a: 0.0 for a in acciones} for s in estados}

def softmax(s):
    """Convierte preferencias en probabilidades usando softmax"""
    vals  = [theta[s][a] for a in acciones]
    mx    = max(vals)
    exps  = [math.exp(v - mx) for v in vals]
    total = sum(exps)
    return {a: e/total for a, e in zip(acciones, exps)}

def elegir_accion(s):
    probs = softmax(s)
    r = random.random()
    acumulado = 0
    for a, p in probs.items():
        acumulado += p
        if r <= acumulado:
            return a
    return acciones[-1]

print("=" * 45)
print("  BUSQUEDA DE LA POLITICA (REINFORCE)")
print("=" * 45)

for ep in range(episodios):
    # Generar episodio
    s = random.choice([1, 2])
    trayectoria = []
    for _ in range(30):
        if s in [0, 3]:
            break
        a  = elegir_accion(s)
        s2 = siguiente(s, a)
        r  = recompensa(s2)
        trayectoria.append((s, a, r))
        s  = s2

    # Calcular retornos G_t para cada paso
    G = 0
    retornos = []
    for _, _, r in reversed(trayectoria):
        G = r + gamma * G
        retornos.insert(0, G)

    # Actualizar parametros theta
    for t, (s, a, _) in enumerate(trayectoria):
        if s in [0, 3]:
            continue
        probs = softmax(s)
        G_t   = retornos[t]
        for a2 in acciones:
            indicador = 1 if a2 == a else 0
            grad = indicador - probs[a2]  # gradiente log pi
            theta[s][a2] += alpha * G_t * grad

print(f"\nEpisodios entrenados: {episodios}\n")
print("Politica aprendida (probabilidades softmax):")
print(f"{'Estado':<8} {'P(izquierda)':<16} {'P(derecha)':<14} {'Accion preferida'}")
print("-" * 54)
for s in estados:
    if s in [0, 3]:
        print(f"  {s:<6}   {'---':<14}   {'---':<12}   TERMINAL")
        continue
    probs = softmax(s)
    p_izq = probs[-1]
    p_der = probs[1]
    preferida = "derecha" if p_der > p_izq else "izquierda"
    print(f"  {s:<6}   {p_izq:<14.3f}   {p_der:<12.3f}   {preferida}")
