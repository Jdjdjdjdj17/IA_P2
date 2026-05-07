# _27_IteracionDeValores.py
# Iteración de Valores (Value Iteration)
# Algoritmo para resolver MDPs (Procesos de Decision de Markov).
# Calcula el valor optimo V*(s) para cada estado iterando hasta converger.
#
# Formula de Bellman:
#   V(s) = max_a [ R(s,a) + gamma * suma_s'[ P(s'|s,a) * V(s') ] ]

# ---- MDP simple: cuadricula 1D con 4 estados ----
# Estados: 0, 1, 2, 3
# Estado 3 = meta (recompensa +10)
# Estado 0 = pozo (recompensa -5)
# Acciones: izquierda (-1) o derecha (+1)

estados   = [0, 1, 2, 3]
gamma     = 0.9   # Factor de descuento
epsilon   = 0.001 # Umbral de convergencia

# Recompensa al llegar a cada estado
def recompensa(estado):
    if estado == 3: return  10
    if estado == 0: return  -5
    return -1  # Paso normal

# Transicion determinista: moverse izq/der sin salir del rango
def siguiente(estado, accion):
    nuevo = estado + accion
    return max(0, min(3, nuevo))

acciones = [-1, 1]  # izquierda, derecha

# ---- Algoritmo de Iteracion de Valores ----
V = {s: 0 for s in estados}  # Valores iniciales en 0

print("=" * 40)
print("  ITERACION DE VALORES")
print("=" * 40)

iteracion = 0
while True:
    delta = 0
    V_nuevo = {}
    for s in estados:
        if s in [0, 3]:  # Estados terminales no cambian
            V_nuevo[s] = recompensa(s)
            continue
        # Calcula el valor maximo sobre todas las acciones
        mejor = max(
            recompensa(siguiente(s, a)) + gamma * V[siguiente(s, a)]
            for a in acciones
        )
        V_nuevo[s] = mejor
        delta = max(delta, abs(V_nuevo[s] - V[s]))
    V = V_nuevo
    iteracion += 1
    if delta < epsilon:
        break

print(f"\nConvergio en {iteracion} iteraciones\n")
print(f"{'Estado':<8} {'Valor V*(s)'}")
print("-" * 22)
for s in estados:
    print(f"  {s:<6}   {V[s]:.4f}")

# ---- Politica optima derivada ----
print("\nPolitica optima:")
for s in estados:
    if s in [0, 3]:
        print(f"  Estado {s} -> TERMINAL")
        continue
    mejor_a = max(acciones, key=lambda a: recompensa(siguiente(s,a)) + gamma * V[siguiente(s,a)])
    direccion = "derecha" if mejor_a == 1 else "izquierda"
    print(f"  Estado {s} -> ir a la {direccion}")
