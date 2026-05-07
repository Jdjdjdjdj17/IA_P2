# _29_MDP.py
# Proceso de Decision de Markov (MDP)
# Un MDP modela la toma de decisiones bajo incertidumbre.
# El agente elige acciones, el ambiente responde con probabilidad.
#
# Componentes:
#   S  = conjunto de estados
#   A  = conjunto de acciones
#   P  = probabilidad de transicion P(s'|s,a)
#   R  = recompensa R(s,a,s')
#   gamma = factor de descuento

# ---- MDP: cuadricula 1x4 con transiciones probabilistas ----
# El agente quiere llegar al estado 3 (meta)
# Accion "derecha" lleva al estado correcto con P=0.8, y al lugar con P=0.2

estados  = [0, 1, 2, 3]
acciones = ['derecha', 'izquierda']
gamma    = 0.9
epsilon  = 0.001

# Recompensas
def recompensa(estado):
    if estado == 3: return 10
    if estado == 0: return -5
    return -1

# Transicion probabilista
def transicion(estado, accion):
    """Devuelve lista de (prob, estado_siguiente)"""
    if estado in [0, 3]:
        return [(1.0, estado)]  # terminales no se mueven
    if accion == 'derecha':
        s_intento = min(3, estado + 1)
        s_resval  = max(0, estado - 1)
        return [(0.8, s_intento), (0.2, s_resval)]
    else:
        s_intento = max(0, estado - 1)
        s_resval  = min(3, estado + 1)
        return [(0.8, s_intento), (0.2, s_resval)]

print("=" * 45)
print("  PROCESO DE DECISION DE MARKOV (MDP)")
print("=" * 45)

# ---- Resolucion por Iteracion de Valores ----
V = {s: 0 for s in estados}

iteracion = 0
while True:
    delta = 0
    V_nuevo = {}
    for s in estados:
        if s in [0, 3]:
            V_nuevo[s] = recompensa(s)
            continue
        mejor = float('-inf')
        for a in acciones:
            valor_accion = sum(
                prob * (recompensa(s2) + gamma * V[s2])
                for prob, s2 in transicion(s, a)
            )
            if valor_accion > mejor:
                mejor = valor_accion
        V_nuevo[s] = mejor
        delta = max(delta, abs(V_nuevo[s] - V[s]))
    V = V_nuevo
    iteracion += 1
    if delta < epsilon:
        break

print(f"\nResuelto en {iteracion} iteraciones\n")
print(f"{'Estado':<8} {'V*(s)':<10} {'Mejor Accion'}")
print("-" * 32)
for s in estados:
    if s in [0, 3]:
        print(f"  {s:<6}   {V[s]:<8.3f}   TERMINAL")
        continue
    mejor_a = max(acciones, key=lambda a: sum(
        prob * (recompensa(s2) + gamma * V[s2])
        for prob, s2 in transicion(s, a)
    ))
    print(f"  {s:<6}   {V[s]:<8.3f}   {mejor_a}")
