"""
grafo_datos.py — Generado por grafo_ia.py
Importa esto en tu algoritmo con:
  from grafo_datos import GRAFO, INICIO, DESTINO
"""

import networkx as nx

MODO    = "no_dirigido"
INICIO  = "A"
DESTINO = "J"

# Grafo como diccionario — úsalo en tus algoritmos
# Sin pesos:  GRAFO[nodo] = [vecino1, vecino2, ...]
# Con pesos:  GRAFO[nodo] = [(vecino1, costo), ...]
GRAFO = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "E", "F"],
    "D": ["B"],
    "E": ["B", "C", "G", "I"],
    "F": ["C", "H"],
    "G": ["E"],
    "H": ["F", "J"],
    "I": ["E"],
    "J": ["H"],
}

# Grafo como objeto NetworkX (opcional)
G = nx.Graph()
G.add_edge("A", "B")
G.add_edge("A", "C")
G.add_edge("B", "D")
G.add_edge("B", "E")
G.add_edge("C", "E")
G.add_edge("C", "F")
G.add_edge("E", "G")
G.add_edge("F", "H")
G.add_edge("E", "I")
G.add_edge("H", "J")
