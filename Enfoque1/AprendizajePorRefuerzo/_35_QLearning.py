# _35_QLearning.py
# Q-Learning
# Aprende el valor de pares (estado, accion) directamente: Q(s, a)
# No necesita modelo del ambiente (model-free).
# La accion optima en cada estado es: argmax_a Q(s, a)
#
# Regla de actualizacion:
#   Q(s,a) <- Q(s,a) + alpha * [R + gamma * max_a' Q(s',a') - Q(s,a)]

import random

estados  = [0, 1, 2, 3]
acciones = [-1, 1]   # -1=izquierda, +1=derecha
gamma    = 0.9
alpha    = 0.1
epsilon  = 0.2
episodios = 2000

def recompensa(estado):
    if estado == 3: return  10
    if estado == 0: return  -5
    return -1

def siguiente(estado, accion):
    return max(0, min(3, estado + accion))

# Tabla Q inicializada en 0
Q = {s: {a: 0.0 for a in acciones} for s in estados}

print("=" * 45)
print("  Q-LEARNING")
print("=" * 45)

for ep in range(episodios):
    s = random.choice([1, 2])
    for _ in range(30):
        if s in [0, 3]:
            break
        # Epsilon-greedy
        if random.random() < epsilon:
            a = random.choice(acciones)
        else:
            a = max(acciones, key=lambda ac: Q[s][ac])

        s2 = siguiente(s, a)
        r  = recompensa(s2)

        # Actualizacion Q-Learning
        mejor_q_siguiente = max(Q[s2].values())
        Q[s][a] = Q[s][a] + alpha * (r + gamma * mejor_q_siguiente - Q[s][a])
        s = s2

print(f"\nEpisodios entrenados: {episodios}\n")
print("Tabla Q aprendida:")
print(f"{'Estado':<8} {'Q(izq)':<12} {'Q(der)':<12} {'Mejor Accion'}")
print("-" * 44)
for s in estados:
    q_izq = Q[s][-1]
    q_der = Q[s][1]
    if s in [0, 3]:
        print(f"  {s:<6}   {q_izq:<10.3f}   {q_der:<10.3f}   TERMINAL")
    else:
        mejor = "derecha" if q_der >= q_izq else "izquierda"
        print(f"  {s:<6}   {q_izq:<10.3f}   {q_der:<10.3f}   {mejor}")
