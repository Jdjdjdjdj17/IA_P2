from grafo_datos_6 import GRAFO, INICIO, DESTINO

print("Grafo: ",GRAFO, "Inicio: ", INICIO, "| Destino: ", DESTINO)

def bidireccional(grafo, inicio, destino):
    if inicio == destino:
        return [inicio]

    frente = {inicio : [inicio]}
    atras = {destino : [destino]}
    while frente and atras:
        nuevoFrente = {}
        for nodo, camino in frente.items():
            for vecino in grafo[nodo]:
                if vecino not in frente:
                    nuevoFrente[vecino] = camino + [vecino]
                if vecino in atras:
                    return camino + list(reversed(atras[vecino]))

        frente.update(nuevoFrente)

        nuevoAtras = {}
        for nodo, camino in atras.items():
            for vecino in grafo[nodo]:
                if vecino not in atras:
                    nuevoAtras[vecino] = camino + [vecino]
                if vecino in frente:
                    return frente[vecino] + list(reversed(camino))

        atras.update(nuevoAtras)

    return None

camino = bidireccional(GRAFO, INICIO, DESTINO)

if camino:
    print("Camino: ", camino)
else:
    print("No se encontro camino")
