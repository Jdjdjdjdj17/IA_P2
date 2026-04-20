"""
grafo_datos.py — Generado por grafo_ia.py
Importa esto en tu algoritmo con:
  from grafo_datos import GRAFO, INICIO, DESTINO
"""

import networkx as nx

MODO    = "no_dirigido"
INICIO  = "A"
DESTINO = "M"

# Grafo como diccionario — úsalo en tus algoritmos
# Sin pesos:  GRAFO[nodo] = [vecino1, vecino2, ...]
# Con pesos:  GRAFO[nodo] = [(vecino1, costo), ...]
GRAFO = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "I", "J"],
    "D": ["B", "E"],
    "E": ["D", "F", "G"],
    "F": ["E"],
    "G": ["E", "H"],
    "H": ["G"],
    "I": ["C", "K", "L"],
    "J": ["C"],
    "K": ["I"],
    "L": ["I", "M"],
    "M": ["L"],
}

# Grafo como objeto NetworkX (opcional)
G = nx.Graph()
G.add_edge("A", "B")
G.add_edge("A", "C")
G.add_edge("B", "D")
G.add_edge("D", "E")
G.add_edge("E", "F")
G.add_edge("E", "G")
G.add_edge("G", "H")
G.add_edge("C", "I")
G.add_edge("C", "J")
G.add_edge("I", "K")
G.add_edge("I", "L")
G.add_edge("L", "M")
