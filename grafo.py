"""
grafo_ia.py — Crea y exporta un grafo para tus algoritmos
==========================================================
Uso:
  1. Corre: python3 grafo_ia.py
  2. Responde las preguntas
  3. Se guarda el grafo en grafo_datos.py
  4. En tu algoritmo haz: from grafo_datos import GRAFO, INICIO, DESTINO
"""

import os
import subprocess
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import deque


# ══════════════════════════════════════════════════════════
#  PREGUNTAS POR TERMINAL
# ══════════════════════════════════════════════════════════

def preguntar_opcion(pregunta, opciones):
    print(f"\n{pregunta}")
    for i, op in enumerate(opciones, 1):
        print(f"  {i}. {op}")
    while True:
        try:
            sel = int(input("→ ")) - 1
            if 0 <= sel < len(opciones):
                return sel
            print(f"  Elige entre 1 y {len(opciones)}")
        except ValueError:
            print("  Escribe solo el número.")


def pedir_aristas(modo):
    print("\n── Ingresa las aristas ──")
    if modo == 'pesos':
        print("Formato: origen destino costo   (ej: A B 3)")
    else:
        print("Formato: origen destino          (ej: A B)")
    print("Escribe 'fin' cuando termines.\n")

    aristas = []
    while True:
        entrada = input("Arista: ").strip()
        if entrada.lower() == 'fin':
            break
        partes = entrada.split()
        try:
            if modo == 'pesos' and len(partes) == 3:
                aristas.append((partes[0], partes[1], float(partes[2])))
            elif modo != 'pesos' and len(partes) == 2:
                aristas.append((partes[0], partes[1]))
            else:
                print("  Formato incorrecto, intenta de nuevo.")
        except ValueError:
            print("  El costo debe ser un número.")
    return aristas


# ══════════════════════════════════════════════════════════
#  CONSTRUCCIÓN DEL GRAFO
# ══════════════════════════════════════════════════════════

def construir_grafo(modo, aristas):
    G = nx.DiGraph() if modo == 'dirigido' else nx.Graph()
    for arista in aristas:
        if len(arista) == 3:
            G.add_edge(arista[0], arista[1], weight=arista[2])
        else:
            G.add_edge(arista[0], arista[1])
    return G


# ══════════════════════════════════════════════════════════
#  LAYOUT EN ÁRBOL
# ══════════════════════════════════════════════════════════

def layout_arbol(G, raiz):
    niveles = {}
    visitados = set()
    cola = deque([(raiz, 0)])
    visitados.add(raiz)
    while cola:
        nodo, nivel = cola.popleft()
        niveles.setdefault(nivel, []).append(nodo)
        for vecino in G.neighbors(nodo):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, nivel + 1))
    for nodo in G.nodes():
        if nodo not in visitados:
            niveles.setdefault(99, []).append(nodo)
    pos = {}
    for nivel, nodos in niveles.items():
        ancho = len(nodos)
        for i, nodo in enumerate(nodos):
            pos[nodo] = ((i - ancho / 2) + 0.5, -nivel)
    return pos


# ══════════════════════════════════════════════════════════
#  VISUALIZACIÓN
# ══════════════════════════════════════════════════════════

def visualizar(G, modo, inicio, destino, camino=None, archivo='grafo_temp.png'):
    pos = layout_arbol(G, inicio)

    aristas_camino = set()
    if camino:
        for i in range(len(camino) - 1):
            aristas_camino.add((camino[i], camino[i+1]))
            aristas_camino.add((camino[i+1], camino[i]))

    color_nodos = []
    for nodo in G.nodes():
        if nodo == inicio:
            color_nodos.append('#2ecc71')
        elif nodo == destino:
            color_nodos.append('#e74c3c')
        elif camino and nodo in camino:
            color_nodos.append('#f39c12')
        else:
            color_nodos.append('#7f8c8d')

    color_aristas, grosor_aristas = [], []
    for u, v in G.edges():
        if (u, v) in aristas_camino:
            color_aristas.append('#f39c12')
            grosor_aristas.append(4.0)
        else:
            color_aristas.append('#4a5568')
            grosor_aristas.append(1.5)

    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')

    nx.draw_networkx_edges(G, pos,
                           edge_color=color_aristas,
                           width=grosor_aristas,
                           arrows=True if modo == 'dirigido' else False,
                           arrowsize=20 if modo == 'dirigido' else 10,
                           ax=ax)

    nx.draw_networkx_nodes(G, pos,
                           node_color=color_nodos,
                           node_size=1800, ax=ax)

    nx.draw_networkx_labels(G, pos,
                            font_size=14, font_weight='bold',
                            font_color='white', ax=ax)

    if modo == 'pesos':
        pesos = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos,
                                     font_color='black',
                                     font_size=11, ax=ax)

    parches = [
        mpatches.Patch(color='#2ecc71', label=f'Inicio ({inicio})'),
        mpatches.Patch(color='#e74c3c', label=f'Destino ({destino})'),
        mpatches.Patch(color='#7f8c8d', label='Otros nodos'),
    ]
    if camino:
        parches.insert(2, mpatches.Patch(color='#f39c12', label='Camino resaltado'))

    ax.legend(handles=parches, loc='lower left',
              facecolor='#16213e', labelcolor='white', fontsize=11)

    camino_str = ' → '.join(camino) if camino else 'sin resaltar'
    ax.set_title(f'Grafo {modo}  |  {camino_str}',
                 color='white', fontsize=13, pad=15)

    ax.axis('off')
    plt.tight_layout()
    plt.savefig(archivo, dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close()


def mostrar_y_borrar(archivo):
    print("\nAbriendo imagen... (ciérrala para continuar)")
    try:
        subprocess.run(['eog', archivo], check=True)
    except FileNotFoundError:
        subprocess.run(['xdg-open', archivo])
        input("Presiona Enter cuando hayas terminado...")
    if os.path.exists(archivo):
        os.remove(archivo)


# ══════════════════════════════════════════════════════════
#  EXPORTAR GRAFO A ARCHIVO
# ══════════════════════════════════════════════════════════

def exportar_grafo(G, modo, inicio, destino, aristas):
    """Guarda el grafo en grafo_datos.py para que lo importen tus algoritmos."""
    import os
    print("\n── ¿Dónde quieres guardar grafo_datos.py? ──")
    print("  Deja vacío para guardarlo en la carpeta actual")
    print("  O escribe la ruta completa (ej: /home/lolita/Documentos/IA/IA_P2)")
    ruta = input("→ ").strip()

    if ruta == '':
        archivo_salida = 'grafo_datos.py'
    else:
        ruta = os.path.expanduser(ruta)
        os.makedirs(ruta, exist_ok=True)
        archivo_salida = os.path.join(ruta, 'grafo_datos.py')

    with open(archivo_salida, 'w') as f:
        f.write('"""\n')
        f.write('grafo_datos.py — Generado por grafo_ia.py\n')
        f.write('Importa esto en tu algoritmo con:\n')
        f.write('  from grafo_datos import GRAFO, INICIO, DESTINO\n')
        f.write('"""\n\n')
        f.write('import networkx as nx\n\n')

        f.write(f'MODO    = "{modo}"\n')
        f.write(f'INICIO  = "{inicio}"\n')
        f.write(f'DESTINO = "{destino}"\n\n')

        # Diccionario de adyacencia (fácil para algoritmos manuales)
        f.write('# Grafo como diccionario — úsalo en tus algoritmos\n')
        f.write('# Sin pesos:  GRAFO[nodo] = [vecino1, vecino2, ...]\n')
        f.write('# Con pesos:  GRAFO[nodo] = [(vecino1, costo), ...]\n')
        f.write('GRAFO = {\n')
        for nodo in G.nodes():
            vecinos = []
            for vecino in G.neighbors(nodo):
                peso = G[nodo][vecino].get('weight', None)
                if peso is not None:
                    vecinos.append(f'("{vecino}", {peso})')
                else:
                    vecinos.append(f'"{vecino}"')
            f.write(f'    "{nodo}": [{", ".join(vecinos)}],\n')
        f.write('}\n\n')

        # Objeto NetworkX (opcional)
        f.write('# Grafo como objeto NetworkX (opcional)\n')
        f.write('G = nx.DiGraph()\n' if modo == 'dirigido' else 'G = nx.Graph()\n')
        for arista in aristas:
            if len(arista) == 3:
                f.write(f'G.add_edge("{arista[0]}", "{arista[1]}", weight={arista[2]})\n')
            else:
                f.write(f'G.add_edge("{arista[0]}", "{arista[1]}")\n')

    print(f"\nGrafo exportado a {archivo_salida}")
    print("En tu algoritmo escribe:")
    print("  from grafo_datos import GRAFO, INICIO, DESTINO")


# ══════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("\n" + "═"*50)
    print("  GRAFO IA — Configuración")
    print("═"*50)

    # 1. Modo
    modos = ['No dirigido  (BFS, DFS, Bidireccional)',
             'Dirigido     (búsqueda en grafos)',
             'Con pesos    (Costo Uniforme, A*, Voraz)']
    idx_modo = preguntar_opcion("¿Qué tipo de grafo quieres?", modos)
    modo = ['no_dirigido', 'dirigido', 'pesos'][idx_modo]

    # 2. Aristas
    aristas = pedir_aristas(modo)
    if not aristas:
        print("No ingresaste aristas, saliendo.")
        exit()

    # 3. Inicio y destino
    nodos = sorted(set(n for a in aristas for n in a[:2]))
    print(f"\nNodos detectados: {', '.join(nodos)}")
    inicio  = input("\nNodo de inicio:  ").strip()
    destino = input("Nodo de destino: ").strip()

    # 4. Construir y mostrar
    G = construir_grafo(modo, aristas)
    archivo = 'grafo_temp.png'
    visualizar(G, modo, inicio, destino, archivo=archivo)
    mostrar_y_borrar(archivo)

    # 5. Exportar para tus algoritmos
    exportar_grafo(G, modo, inicio, destino, aristas)
