import heapq
from grafo_datos_9 import GRAFO, INICIO, DESTINO

print(f"Grafo cargado: {GRAFO}  Inicio: {INICIO}  |  Destino: {DESTINO}")
 

def bTabu(grafo, inicio, destino, tam_lista = 5):
    cola = [(0, [inicio])]    
    tabu = []

    while cola:              
        g, camino = heapq.heappop(cola)
        nodo = camino[-1]

        if nodo in tabu:
            continue   

        tabu.append(nodo)

        if len(tabu) > tam_lista :
            tabu.pop(0)


        if nodo == destino:
            print("Costo total: ", g)
            return camino   

        for vecino, peso in grafo[nodo]:
            if vecino not in tabu:
                heapq.heappush(cola, (g +peso, camino + [vecino]))

    return None

camino = bTabu(GRAFO, INICIO, DESTINO)

if camino:
    print("Mejor camino: ", camino)
else:
    print("No se encontro camino")