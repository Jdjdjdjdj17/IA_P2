import random
import math

def temple(inicial = 100, baja = .95, iter = 1000):
    actual = random.uniform(-1, 100)
    mejor = actual
    temp = inicial

    def f(x) : return math.sqrt(x + 1)
    
    for i in range(iter):
        if actual < 0 :
            vecino  = actual + random.uniform(0, 2)
        else :
            vecino = actual + random.uniform(-1, 2)
        
        print(actual)
        print(vecino)

        delta = f(actual) - f(vecino)

        if delta > 0 :
            actual = vecino
        else :
            P = math.exp(delta / temp)
            if P > random.random() :
                actual = vecino

        temp *= baja

        if f(actual) < f(vecino) :
            mejor = vecino

    return mejor

mejor = temple()

if mejor :
    print("El mejor numero es: ", mejor)
else :
    print("No hay numeros buenos")