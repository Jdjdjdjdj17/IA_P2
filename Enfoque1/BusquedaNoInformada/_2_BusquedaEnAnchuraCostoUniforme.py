import heapq
from grafo_datos_2 import GRAFO, INICIO, DESTINO

print(f"Grafo cargado: {GRAFO}  Inicio: {INICIO}  |  Destino: {DESTINO}")

def ucs(grafo, inicio, destino):
    cola = [(0, [inicio])]    # ← inicio adentro
    visitado = set()

    while cola:               # ← adentro de la función
        costo, camino = heapq.heappop(cola)
        nodo = camino[-1]

        if nodo in visitado:
            continue
        visitado.add(nodo)    # ← add no append

        if nodo == destino:
            print("Costo total: ", costo)
            return camino     # ← camino no cola

        for vecino, peso in grafo[nodo]:
            if vecino not in visitado:
                nuevo_costo = costo + peso
                heapq.heappush(cola, (nuevo_costo, camino + [vecino]))

    return None               # ← N mayúscula

camino = ucs(GRAFO, INICIO, DESTINO)

if camino:
    print("El camino mas barato es:", camino)
else:
    print("No se encontró camino.")

print("Este espacio es para el algoritmo de Busqueda en anchura de costo uniforme")
