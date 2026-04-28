"""
grafo_datos.py — Generado por grafo_ia.py
Importa esto en tu algoritmo con:
  from grafo_datos import GRAFO, INICIO, DESTINO
"""

import networkx as nx

MODO    = "pesos"
INICIO  = "A"
DESTINO = "L"

# Grafo como diccionario — úsalo en tus algoritmos
# Sin pesos:  GRAFO[nodo] = [vecino1, vecino2, ...]
# Con pesos:  GRAFO[nodo] = [(vecino1, costo), ...]
GRAFO = {
    "A": [("B", 4.0), ("C", 2.0), ("E", 1.0)],
    "B": [("A", 4.0), ("D", 3.0), ("F", 6.0)],
    "C": [("A", 2.0), ("G", 9.0), ("H", 4.0)],
    "E": [("A", 1.0), ("H", 2.0), ("N", 4.0)],
    "D": [("B", 3.0), ("I", 1.0), ("N", 3.0)],
    "F": [("B", 6.0), ("O", 9.0)],
    "G": [("C", 9.0)],
    "H": [("C", 4.0), ("E", 2.0)],
    "I": [("D", 1.0), ("J", 5.0)],
    "J": [("I", 5.0), ("K", 4.0), ("L", 2.0)],
    "K": [("J", 4.0), ("P", 4.0)],
    "L": [("J", 2.0)],
    "N": [("D", 3.0), ("E", 4.0)],
    "O": [("F", 9.0), ("M", 5.0), ("P", 2.0)],
    "M": [("O", 5.0)],
    "P": [("O", 2.0), ("K", 4.0)],
}

# Grafo como objeto NetworkX (opcional)
G = nx.Graph()
G.add_edge("A", "B", weight=4.0)
G.add_edge("A", "C", weight=2.0)
G.add_edge("A", "E", weight=1.0)
G.add_edge("B", "D", weight=3.0)
G.add_edge("B", "F", weight=6.0)
G.add_edge("C", "G", weight=9.0)
G.add_edge("C", "H", weight=4.0)
G.add_edge("E", "H", weight=2.0)
G.add_edge("D", "I", weight=1.0)
G.add_edge("I", "J", weight=5.0)
G.add_edge("J", "K", weight=4.0)
G.add_edge("J", "L", weight=2.0)
G.add_edge("D", "N", weight=3.0)
G.add_edge("N", "E", weight=4.0)
G.add_edge("F", "O", weight=9.0)
G.add_edge("O", "M", weight=5.0)
G.add_edge("O", "P", weight=2.0)
G.add_edge("P", "K", weight=4.0)
