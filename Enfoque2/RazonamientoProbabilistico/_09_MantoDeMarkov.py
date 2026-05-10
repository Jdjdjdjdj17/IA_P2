# _09_MantoDeMarkov.py
# Manto de Markov (Markov Blanket)
# El manto de Markov de un nodo X en una Red Bayesiana es el conjunto
# de nodos que hacen a X condicionalmente independiente del resto de la red.
#
# Compuesto por: Padres(X) + Hijos(X) + CopadresDeHijos(X)
# Propiedad: P(X | todos los demas) = P(X | Manto(X))

print("=" * 55)
print("  MANTO DE MARKOV")
print("=" * 55)

# ---- Red de ejemplo ----
# Nodos: A, B, C, D, E, F, G
# Aristas (padre -> hijo):
#   A -> C, B -> C, C -> E, D -> E, E -> G, F -> G
#
#   A   B   D   F
#    \ /   \ /
#     C     E --- G
#      \   /
#       (C->E)

# Representacion como diccionario: nodo -> lista de padres
padres = {
    "A": [],
    "B": [],
    "C": ["A", "B"],
    "D": [],
    "E": ["C", "D"],
    "F": [],
    "G": ["E", "F"],
}

# Calcular hijos de cada nodo
hijos = {n: [] for n in padres}
for nodo, ps in padres.items():
    for p in ps:
        hijos[p].append(nodo)

def manto_markov(nodo, padres, hijos):
    """Calcula el Manto de Markov de un nodo"""
    manto = set()
    # 1. Padres del nodo
    for p in padres[nodo]:
        manto.add(p)
    # 2. Hijos del nodo
    for h in hijos[nodo]:
        manto.add(h)
        # 3. Copadres: otros padres de los hijos (excepto el nodo mismo)
        for cp in padres[h]:
            if cp != nodo:
                manto.add(cp)
    return manto

print("\nEstructura de la red:")
for n, ps in padres.items():
    hs = hijos[n]
    print(f"  {n}: padres={ps}  hijos={hs}")

print("\nManto de Markov de cada nodo:")
for nodo in padres:
    manto = manto_markov(nodo, padres, hijos)
    todos = set(padres.keys()) - {nodo}
    independientes = todos - manto
    print(f"  Manto({nodo}) = {sorted(manto)}")
    print(f"    -> {nodo} es independiente de {sorted(independientes)} dado su manto")

print("\nUso en IA:")
print("  El Manto de Markov define la 'vecindad' relevante de un nodo.")
print("  Usado en algoritmos MCMC (Gibbs Sampling) para muestreo eficiente.")
