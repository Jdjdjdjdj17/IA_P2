import random

def contar_conflictos(fila, col, tablero):
    # Cuenta cuántas otras reinas atacan la posición (fila, col)
    conf = 0
    for f, c in enumerate(tablero):
        if f != fila:
            # Misma columna o misma diagonal
            if c == col or abs(c - col) == abs(f - fila):
                conf += 1
    return conf

def min_conflicts(n=4):
    # Estado inicial: reina en columna aleatoria para cada fila
    # El índice es la fila, el valor es la columna: [col, col, col, col]
    tablero = [random.randint(0, n-1) for _ in range(n)]
    
    for paso in range(20):
        # 1. Buscar filas que tienen conflictos
        conflictivas = [f for f in range(n) if contar_conflictos(f, tablero[f], tablero) > 0]
        
        if not conflictivas: return tablero, paso # ¡Logrado!

        # 2. Elegir una fila con conflicto y mover su reina a la mejor columna
        f = random.choice(conflictivas)
        tablero[f] = min(range(n), key=lambda c: contar_conflictos(f, c, tablero))
        
    return tablero, 20

# --- Ejecución simple ---
sol, pasos = min_conflicts(4)
print(f"Columnas finales (por fila): {sol} en {pasos} pasos")