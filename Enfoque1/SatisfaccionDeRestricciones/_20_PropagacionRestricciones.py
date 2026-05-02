"Checa si el numero puede ir en una posicion"

def seguro(tablero, fila, col, num) :
    #Revisa cuadro de 9x9

    cuadro_f = (fila // 3) * 3
    cuadro_c = (col // 3) * 3

    for f in range(cuadro_f, cuadro_f + 3) :
        for c in range(cuadro_c, cuadro_c + 3) :
            if tablero[f][c] == num :
                return False

    #Revisa filas
    if num in tablero[fila] :
        return False
    
    #Revisa colmnas
    if num in [tablero[f][col] for f in range(9)] :
        return False

    return True

    

def propagacion(sudoku) :
    n = len(sudoku)

    
    for fila in range(n) :
        for col in range(n) :
            if sudoku[fila][col] == 0 :

                for i in range(1,10) :
                    if seguro(sudoku, fila, col, i) :
                        sudoku[fila][col] = i

                        if propagacion(sudoku) :
                            return True
                        
                        sudoku[fila][col] = 0


                return False
    return True

# Sudoku como matriz 9x9
# 0 = celda vacía
SUDOKU = [
    [5, 3, 0,   0, 7, 0,   0, 0, 0],
    [6, 0, 0,   1, 9, 5,   0, 0, 0],
    [0, 9, 8,   0, 0, 0,   0, 6, 0],

    [8, 0, 0,   0, 6, 0,   0, 0, 3],
    [4, 0, 0,   8, 0, 3,   0, 0, 1],
    [7, 0, 0,   0, 2, 0,   0, 0, 6],

    [0, 6, 0,   0, 0, 0,   2, 8, 0],
    [0, 0, 0,   4, 1, 9,   0, 0, 5],
    [0, 0, 0,   0, 8, 0,   0, 7, 9],
]

tablero = propagacion(SUDOKU)

if tablero :
    for fila in SUDOKU :
        print(fila)