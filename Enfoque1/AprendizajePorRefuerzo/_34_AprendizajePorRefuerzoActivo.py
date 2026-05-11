# _34_AprendizajePorRefuerzoActivo.py
# Aprendizaje por Refuerzo Activo
# A diferencia del pasivo, el agente SÍ elige sus acciones mientras aprende.
# Debe resolver el dilema exploracion vs explotacion.
#
# Metodo: TD-Learning (Temporal Difference) con politica epsilon-greedy
# El agente actualiza V(s) en cada paso sin esperar al final del episodio:
#   V(s) <- V(s) + alpha * [R + gamma * V(s') - V(s)]

import random

estados  = [0, 1, 2, 3]
acciones = [-1, 1]
gamma    = 0.9
alpha    = 0.1   # tasa de aprendizaje
epsilon  = 0.2   # probabilidad de explorar (accion aleatoria)
episodios = 1000

def recompensa(estado):
    if estado == 3: return  10
    if estado == 0: return  -5
    return -1

def siguiente(estado, accion):
    return max(0, min(3, estado + accion))

# Valores iniciales
V = {s: 0.0 for s in estados}

print("=" * 45)
print("  APRENDIZAJE POR REFUERZO ACTIVO")
print("  (TD-Learning con epsilon-greedy)")
print("=" * 45)

for ep in range(episodios):
    s = random.choice([1, 2])  # inicio en estado no terminal
    for _ in range(30):
        if s in [0, 3]:
            break
        # Politica epsilon-greedy: explorar o explotar
        if random.random() < epsilon:
            a = random.choice(acciones)  # explorar
        else:
            # Explotar: mejor accion segun V actual
            a = max(acciones, key=lambda ac: recompensa(siguiente(s, ac)) + gamma * V[siguiente(s, ac)])

        s2 = siguiente(s, a)
        r  = recompensa(s2)

        # Actualizacion TD
        V[s] = V[s] + alpha * (r + gamma * V[s2] - V[s])
        s = s2

print(f"\nEpisodios entrenados: {episodios}")
print(f"Alpha={alpha}  Gamma={gamma}  Epsilon={epsilon}\n")
print(f"{'Estado':<8} {'V(s) aprendido':<16} {'Mejor accion'}")
print("-" * 38)
for s in estados:
    if s in [0, 3]:
        print(f"  {s:<6}   {V[s]:<14.4f}   TERMINAL")
        continue
    mejor_a = max(acciones, key=lambda a: recompensa(siguiente(s,a)) + gamma * V[siguiente(s,a)])
    dir_str = "derecha" if mejor_a == 1 else "izquierda"
    print(f"  {s:<6}   {V[s]:<14.4f}   {dir_str}")
