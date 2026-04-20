from grafo_datos_4 import GRAFO, INICIO, DESTINO

print(f"Grafo: {GRAFO}  Inicio: {INICIO}  |  Destino: {DESTINO}")

def dfsl(grafo, inicio, destino, visitado=None):
    visitado = set()
    pila = [[inicio]]
    limite = int(input("Dame un nivel limite: "))

    while pila:
        camino = pila.pop()
        nodo = camino[-1]

        if nodo in visitado:
            continue

        visitado.add(nodo)

        if nodo == destino:
            return camino

        if  len(camino) - 1 == limite:
            continue
        
        for vecino in grafo[nodo]:
            if vecino not in visitado:
                pila.append(camino + [vecino])

    return None

camino = dfsl(GRAFO, INICIO, DESTINO)

if camino:
    print(f"Camino: {' → '.join(camino)}")
else:
    print("No se encontró camino.")
