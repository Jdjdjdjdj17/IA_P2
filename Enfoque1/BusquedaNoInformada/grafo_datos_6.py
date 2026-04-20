"""
grafo_datos.py — Generado por grafo_ia.py
Importa esto en tu algoritmo con:
  from grafo_datos import GRAFO, INICIO, DESTINO
"""

import networkx as nx

MODO    = "no_dirigido"
INICIO  = "A"
DESTINO = "I"

# Grafo como diccionario — úsalo en tus algoritmos
# Sin pesos:  GRAFO[nodo] = [vecino1, vecino2, ...]
# Con pesos:  GRAFO[nodo] = [(vecino1, costo), ...]
GRAFO = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F", "G"],
    "D": ["B", "H"],
    "E": ["B", "H"],
    "F": ["C", "I"],
    "G": ["C", "I"],
    "H": ["D", "E"],
    "I": ["F", "G"],
}

# Grafo como objeto NetworkX (opcional)
G = nx.Graph()
G.add_edge("A", "B")
G.add_edge("A", "C")
G.add_edge("B", "D")
G.add_edge("B", "E")
G.add_edge("C", "F")
G.add_edge("C", "G")
G.add_edge("D", "H")
G.add_edge("E", "H")
G.add_edge("F", "I")
G.add_edge("G", "I")
