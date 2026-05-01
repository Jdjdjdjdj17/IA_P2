import heapq
from grafo_datos_9 import GRAFO, INICIO, DESTINO

print(f"Grafo cargado: {GRAFO}  Inicio: {INICIO}  |  Destino: {DESTINO}")


HEURISTICA = {
    'A': 20,  # A → C → G → O → M → L  aprox
    'B': 22,  # B → F → I → J → L
    'C': 18,  # C → G → O → M → L
    'D': 24,  # D → F → I → J → L
    'E': 19,  # E → H → O → M → L
    'F': 16,  # F → I → J → L
    'G': 14,  # G → O → M → L
    'H': 13,  # H → O → P → L
    'I': 11,  # I → J → L
    'J': 6,   # J → L directo
    'K': 4,   # K → L directo
    'M': 4,   # M → L directo
    'N': 17,  # N → H → O → P → L
    'O': 7,   # O → M → L
    'P': 2,   # P → L directo
    'L': 0,   # destino
}

print("\n── Heurística ──")
for nodo, valor in sorted(HEURISTICA.items()):
    print(f"  h({nodo}) = {valor}")
print()

def h(nodo):
    return HEURISTICA.get(nodo, 0)
 

def a_estrella(grafo, inicio, destino):
    cola = [(h(inicio), 0, [inicio])]    
    visitado = set()

    while cola:              
        f,  g, camino = heapq.heappop(cola)
        nodo = camino[-1]

        if nodo in visitado:
            continue
        visitado.add(nodo)    

        if nodo == destino:
            print("Costo total A*: ", g)
            return camino     

        for vecino, peso in grafo[nodo]:
            if vecino not in visitado:
                G = g + peso
                F = h(vecino) + G
                heapq.heappush(cola, (F, G, camino + [vecino]))

    return None               
    

def ucs(grafo, inicio, destino):
    cola = [(0, [inicio])]    
    visitado = set()

    while cola:               
        costo, camino = heapq.heappop(cola)
        nodo = camino[-1]

        if nodo in visitado:
            continue
        visitado.add(nodo)    

        if nodo == destino:
            print("Costo total busqueda de anchura: ", costo)
            return camino

        for vecino, peso in grafo[nodo]:
            if vecino not in visitado:
                nuevo_costo = costo + peso
                heapq.heappush(cola, (nuevo_costo, camino + [vecino]))

    return None               


camino_a_estrella = a_estrella(GRAFO, INICIO, DESTINO)
camino_ucs= ucs(GRAFO, INICIO, DESTINO)

if camino_ucs:
    print("En busqueda en anchura el camino mas barato es:", camino_ucs)
else:
    print("No se encontró camino.")

if camino_a_estrella:
    print("En A* el camino mas rapido es:", camino_a_estrella)
else:
    print("No se encontró camino.")