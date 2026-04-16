from collections import deque

# ---- Construcción del grafo ----
grafo = {}
destino = input("Cual sera el destino? (De la A la F): " )

def agregar_arista(g, origen, destino):
    if origen not in g:
        g[origen] = []
    if destino not in g:
        g[destino] = []
    g[origen].append(destino)
    g[destino].append(origen)  # No dirigido

agregar_arista(grafo, 'A', 'B')
agregar_arista(grafo, 'A', 'C')
agregar_arista(grafo, 'B', 'D')
agregar_arista(grafo, 'B', 'E')
agregar_arista(grafo, 'C', 'F')

# ---- BFS con camino ----
def bfs_camino(grafo, inicio, destino):
    visitados = set()
    cola = deque([[inicio]])       # La cola guarda caminos, no nodos solos
    visitados.add(inicio)

    while cola:
        camino = cola.popleft()    # Saca el camino más antiguo
        nodo = camino[-1]          # El nodo actual es el último del camino

        if nodo == destino:
            return camino          # ¡Encontrado! Regresa el camino completo

        for vecino in grafo[nodo]:
            if vecino not in visitados:
                visitados.add(vecino)
                nuevo_camino = camino + [vecino]  # Extiende el camino
                cola.append(nuevo_camino)

    return None  # No hay camino 

resultado = bfs_camino(grafo, 'A', destino)
print("Camino encontrado:", resultado)
