from grafo_datos_3 import GRAFO, INICIO, DESTINO

print(f"Grafo: {GRAFO}  Inicio: {INICIO}  |  Destino: {DESTINO}")

def dfs(grafo, inicio, destino, visitado=None):
    visitado = set()
    pila = [[inicio]]

    while pila:

        camino = pila.pop()
        nodo = camino[-1]

        if nodo in visitado:
            continue

        visitado.add(nodo)

        if nodo == destino:
            return camino
        
        for vecino in grafo[nodo]:
            if vecino not in visitado:
                pila.append(camino + [vecino])

    return None

camino = dfs(GRAFO, INICIO, DESTINO)

if camino:
    print(f"Camino: {' → '.join(camino)}")
else:
    print("No se encontró camino.")
