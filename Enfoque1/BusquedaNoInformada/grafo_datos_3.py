"""
grafo_datos.py — Generado por grafo_ia.py
Importa esto en tu algoritmo con:
  from grafo_datos import GRAFO, INICIO, DESTINO
"""

import networkx as nx

MODO    = "no_dirigido"
INICIO  = "A"
DESTINO = "G"

# Grafo como diccionario — úsalo en tus algoritmos
# Sin pesos:  GRAFO[nodo] = [vecino1, vecino2, ...]
# Con pesos:  GRAFO[nodo] = [(vecino1, costo), ...]
GRAFO = {
    "A": ["B", "C", "D"],
    "B": ["A", "E", "F"],
    "C": ["A", "G", "H"],
    "D": ["A", "I"],
    "E": ["B"],
    "F": ["B"],
    "G": ["C"],
    "H": ["C"],
    "I": ["D"],
}

# Grafo como objeto NetworkX (opcional)
G = nx.Graph()
G.add_edge("A", "B")
G.add_edge("A", "C")
G.add_edge("A", "D")
G.add_edge("B", "E")
G.add_edge("B", "F")
G.add_edge("C", "G")
G.add_edge("C", "H")
G.add_edge("D", "I")
