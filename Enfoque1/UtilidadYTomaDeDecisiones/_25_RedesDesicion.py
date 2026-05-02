# 25_RedesDecision.py

import random

# Esto es como una función común en C++ que devuelve un puntaje
def obtener_puntos(conflictos):
    if conflictos == 0:
        return 100 # Máxima felicidad/utilidad
    elif conflictos == 1:
        return 50  # Regular
    else:
        return 10  # Muy mal
    
def ejecutar_red_decision():
    # Variables de probabilidad (Incertidumbre)
    # Ejemplo: Hay un 70% de probabilidad de que el tablero sea estable
    prob_estable = 0.7
    prob_caos = 0.3
    
    n = 4 # Tamaño del tablero (4 reinas)
    mejor_utilidad_esperada = -1.0
    mejor_columna = -1
    
    # Nodo de Decisión: Vamos a probar cada columna posible (0, 1, 2, 3)
    for col in [0, 1, 2, 3]:
        
        # Simulamos dos escenarios posibles (Azar)
        # Escenario 1: Pocos conflictos
        utilidad_estable = obtener_puntos(random.randint(0, 1))
        
        # Escenario 2: Muchos conflictos (caos)
        utilidad_caos = obtener_puntos(random.randint(2, 3))
        
        # Ecuación de la Utilidad Esperada: EU = (P1 * U1) + (P2 * U2)
        utilidad_esperada = (prob_estable * utilidad_estable) + (prob_caos * utilidad_caos)
        
        print("Columna " + str(col) + " tiene utilidad de: " + str(utilidad_esperada))
        

        if utilidad_esperada > mejor_utilidad_esperada:
            mejor_utilidad_esperada = utilidad_esperada
            mejor_columna = col
            
    print("\nCONCLUSION:")
    print("La mejor decision es poner la reina en la columna: " + str(mejor_columna))

# En lugar de usar cosas raras, simplemente llamamos a la función
# Esto es lo primero que se ejecutará
ejecutar_red_decision()