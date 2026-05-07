# _28_IteracionDePoliticas.py
# Iteracion de Politicas (Policy Iteration)
# Alternativa a Iteracion de Valores para resolver MDPs.
# En lugar de iterar sobre valores, itera sobre politicas:
#   1. Evaluacion de Politica: calcula V dado una politica fija
#   2. Mejora de Politica:     actualiza la politica con la mejor accion segun V
# Repite hasta que la politica no cambie.

estados  = [0, 1, 2, 3]
gamma    = 0.9
acciones = [-1, 1]

def recompensa(estado):
    if estado == 3: return  10
    if estado == 0: return  -5
    return -1

def siguiente(estado, accion):
    return max(0, min(3, estado + accion))

# ---- Paso 1: Politica inicial aleatoria ----
import random
politica = {s: random.choice(acciones) for s in estados if s not in [0, 3]}
politica[0] = 0   # terminales no tienen accion relevante
politica[3] = 0

print("=" * 40)
print("  ITERACION DE POLITICAS")
print("=" * 40)
print("\nPolitica inicial:", {s: ("der" if a==1 else "izq") for s,a in politica.items() if s not in [0,3]})

iteracion = 0
while True:
    # ---- Evaluacion de Politica ----
    # Resuelve el sistema de ecuaciones lineales iterativamente
    V = {s: 0 for s in estados}
    for _ in range(1000):  # iteraciones internas hasta convergencia
        for s in estados:
            if s in [0, 3]:
                V[s] = recompensa(s)
                continue
            a  = politica[s]
            s2 = siguiente(s, a)
            V[s] = recompensa(s2) + gamma * V[s2]

    # ---- Mejora de Politica ----
    politica_estable = True
    for s in estados:
        if s in [0, 3]:
            continue
        accion_antigua = politica[s]
        # Elige la mejor accion segun los valores actuales
        politica[s] = max(acciones, key=lambda a: recompensa(siguiente(s,a)) + gamma * V[siguiente(s,a)])
        if politica[s] != accion_antigua:
            politica_estable = False

    iteracion += 1
    if politica_estable:
        break

print(f"Convergio en {iteracion} iteracion(es)\n")
print(f"{'Estado':<8} {'V(s)':<10} {'Accion'}")
print("-" * 28)
for s in estados:
    accion_str = "TERMINAL" if s in [0,3] else ("derecha" if politica[s]==1 else "izquierda")
    print(f"  {s:<6}   {V[s]:<8.3f}   {accion_str}")
