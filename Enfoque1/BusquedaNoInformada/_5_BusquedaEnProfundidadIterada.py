from grafo_datos_5 import GRAFO, INICIO, DESTINO

print(f"Grafo: {GRAFO}  Inicio: {INICIO}  |  Destino: {DESTINO}")

def iddfs(grafo, inicio, destino, visitado=None):
    limitemax = int(input("Dame un nivel limite: "))
    limite = 0
    for limite in range(limitemax):
        print("Limite #", limite)

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

            if  len(camino) - 1 == limite:
                 continue

            
            for vecino in grafo[nodo]:
                if vecino not in visitado:
                    pila.append(camino + [vecino])
    return None

camino = iddfs(GRAFO, INICIO, DESTINO)

if camino:
    print(f"Camino: {' → '.join(camino)}")
else:
    print("No se encontro en los limites dados")
