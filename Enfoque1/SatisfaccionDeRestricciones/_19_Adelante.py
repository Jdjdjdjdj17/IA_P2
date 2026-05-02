import copy

def adelante(fila_actual, dominios):
    n = len(dominios)
    
    # CASO BASE: Si llegamos a la última fila, éxito
    if fila_actual == n:
        return {}

    # Probamos cada columna que todavía sea posible para ESTA fila
    for col in dominios[fila_actual]:
        # 1. Hacemos copia de los dominios para "simular" el futuro
        dominios_futuro = copy.deepcopy(dominios)
        
        # 2. "Tachamos" el futuro: eliminamos esta columna y diagonales de las filas de abajo
        posible_continuar = True
        for fila_siguiente in range(fila_actual + 1, n):
            
            # Quitar misma columna
            if col in dominios_futuro[fila_siguiente]:
                dominios_futuro[fila_siguiente].remove(col)
            
            # Quitar diagonal hacia abajo-izquierda
            distancia = fila_siguiente - fila_actual
            diag_izq = col - distancia

            if diag_izq in dominios_futuro[fila_siguiente]:
                dominios_futuro[fila_siguiente].remove(diag_izq)
                
            # Quitar diagonal hacia abajo-derecha
            diag_der = col + distancia
            
            if diag_der in dominios_futuro[fila_siguiente]:
                dominios_futuro[fila_siguiente].remove(diag_der)
            
            # Poda: Si una fila del futuro se quedó sin opciones, esta rama no sirve
            if not dominios_futuro[fila_siguiente]:
                posible_continuar = False
                break
        
        # 3. Si el futuro aún es viable, seguimos
        if posible_continuar:
            resultado = adelante(fila_actual + 1, dominios_futuro)
            if resultado is not None:
                # Guardamos nuestra elección y las de las filas siguientes
                resultado[fila_actual] = col
                return resultado
                
    return None


N = 5
# Inicializamos dominios: cada fila puede elegir cualquier columna [0, 1, 2, 3, 4]
dominios_iniciales = {i: list(range(N)) for i in range(N)}

#[0, 1, 2, 3, 4]
#[0, 1, 2, 3, 4]
#[0, 1, 2, 3, 4]
#[0, 1, 2, 3, 4]
#[0, 1, 2, 3, 4]

solucion = adelante(0, dominios_iniciales)

if solucion:
    # Ordenar por fila para imprimir bonito
    resultado = [solucion[i] for i in range(N)]
    print(f"Solución con Forward Checking: {resultado}")
else:
    print("No se encontró acomodo")