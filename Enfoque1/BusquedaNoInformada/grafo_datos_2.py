"""
grafo_datos.py — Generado por grafo_ia.py
Importa esto en tu algoritmo con:
  from grafo_datos import GRAFO, INICIO, DESTINO
"""

import networkx as nx

MODO    = "pesos"
INICIO  = "A"
DESTINO = "F"

# Grafo como diccionario — úsalo en tus algoritmos
# Sin pesos:  GRAFO[nodo] = [vecino1, vecino2, ...]
# Con pesos:  GRAFO[nodo] = [(vecino1, costo), ...]
GRAFO = {
    "A": [("B", 2.0), ("C", 3.0)],
    "B": [("A", 2.0), ("D", 4.0), ("E", 1.0)],
    "C": [("A", 3.0), ("F", 2.0)],
    "D": [("B", 4.0), ("F", 5.0)],
    "E": [("B", 1.0)],
    "F": [("C", 2.0), ("D", 5.0)],
}

# Grafo como objeto NetworkX (opcional)
G = nx.Graph()
G.add_edge("A", "B", weight=2.0)
G.add_edge("A", "C", weight=3.0)
G.add_edge("B", "D", weight=4.0)
G.add_edge("B", "E", weight=1.0)
G.add_edge("C", "F", weight=2.0)
G.add_edge("D", "F", weight=5.0)
