import random

def conflictos(fila, col, tablero):
    conf = 0
    for f, c in enumerate(tablero):
        if f != fila:
            # Misma columna o diagonal
            if c == col or abs(c - col) == abs(f - fila):
                conf += 1
    return conf

def corte():
    n = 4
    # --- EL CORTE ---
    fila_corte = random.randint(0, n-1)
    columna_fija = random.randint(0, n-1)

    tablero = [random.randint(0, n-1) for _ in range(n)]

    tablero[fila_corte] = columna_fija

    filas_libres = [f for f in range(n) if f != fila_corte]
    
    for paso in range(20):
        # 1. Buscar conflictos solo en las reinas que NO son el corte
        conflictivas = [f for f in filas_libres if conflictos(f, tablero[f], tablero) > 0]
        
        if not conflictivas and conflictos(0, tablero[0], tablero) == 0:
            return tablero, paso

        # 2. Elegir una reina libre y moverla a la mejor columna
        f = random.choice(conflictivas if conflictivas else [0]) 
        # Si la reina del corte (0) tiene conflicto, pero no podemos moverla, 
        # el algoritmo moverá las otras para adaptarse a ella.
        if f in filas_libres:
            tablero[f] = min(range(n), key=lambda c: conflictos(f, c, tablero))
        
    return tablero, 20

sol, pasos = corte()
print(sol)