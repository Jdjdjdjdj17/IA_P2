def seguro(tablero, fila, col) :
    for i in range(fila) :
        if tablero[i] == col :
            return False
    
    for i, j in zip(range(fila - 1, -1, -1), range(col - 1, -1, -1)) :
        if tablero[i] == j :
            return False
        
    for i, j in zip(range(fila - 1, -1, -1), range(col + 1, len(tablero))) :
        if tablero[i] == j :
            return False
        
    return True

def vuelta(tablero, fila) :
    n = len(tablero)

    if fila == n :
        return True
    
    for col in range(n) :
        if seguro(tablero, fila, col) :
            tablero[fila] = col

            if vuelta(tablero, fila + 1) : 
                return True

            tablero[fila] = -1

    return False

tab = [-1] * 5

tablero = vuelta(tab, 0)

if tablero :
    print(tab)
else :
    print("No se encontro acomodo")