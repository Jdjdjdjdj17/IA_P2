def sat(numeros, objetivo):
    
    # 1. Ordenar es obligatorio para que los punteros funcionen
    numeros.sort() 
    
    izq = 0                      # Puntero al inicio (el más chico)
    der = len(numeros) - 1       # Puntero al final (el más grande)

    while izq < der:
        suma = numeros[izq] + numeros[der]

        if suma == objetivo:
            return (numeros[izq], numeros[der]) # ¡Lo encontramos!
        
        if suma < objetivo:
            izq += 1  # La suma es muy chica, necesitamos alguien más grande
        else:
            der -= 1  # La suma es muy grande, necesitamos alguien más chico

    return None # No hubo pareja que sumara eso

resultado = sat([3,7,9,3,1,2,5], 11)

if resultado: # Si resultado no es None
    p1, p2 = resultado
    print(f"Esta es la pareja de números:\nP1: {p1}\nP2: {p2}")
else:
    print("NO se encontró pareja")