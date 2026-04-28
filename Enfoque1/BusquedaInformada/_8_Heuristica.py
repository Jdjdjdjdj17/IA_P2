from grafo_datos_8 import GRAFO, INICIO, DESTINO
import heapq
 
print(f"Grafo: {GRAFO}  Inicio: {INICIO}  |  Destino: {DESTINO}")
 
# ---- Heurística ----
# Ingresa el valor h para cada nodo (estimación al destino)
HEURISTICA = {}
print("\nIngresa h(n) para cada nodo (el destino siempre es 0):")
for nodo in GRAFO:
    while True:
        try:
            HEURISTICA[nodo] = float(input(f"  h({nodo}) = "))
            break
        except ValueError:
            print("  Escribe un número.")
 
def h(nodo):
    return HEURISTICA.get(nodo, 0)
 
# ---- Verificación de admisibilidad ----
def costo_real(grafo, inicio, destino):
    cola = [(0, inicio)]
    visitados = set()
    while cola:
        costo, nodo = heapq.heappop(cola)
        if nodo in visitados:
            continue
        visitados.add(nodo)
        if nodo == destino:
            return costo
        for entrada in grafo[nodo]:
            vecino, peso = entrada if isinstance(entrada, tuple) else (entrada, 1)
            if vecino not in visitados:
                heapq.heappush(cola, (costo + peso, vecino))
    return float('inf')
 
print(f"\n{'Nodo':<6} {'h(n)':<8} {'Costo real':<12} {'Admisible'}")
print("─" * 35)
for nodo in GRAFO:
    hn   = h(nodo)
    real = costo_real(GRAFO, nodo, DESTINO)
    ok   = "✓" if hn <= real else "✗"
    print(f"{nodo:<6} {hn:<8} {real:<12} {ok}")


print("Espacio para un algoritmo de heurostica, que al parecer es una filosofia")
