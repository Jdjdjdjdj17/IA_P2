import random
import math

def haz_local(inicio, k = 5, iter = 1000) :

    haz = [inicio for i in range(k)]

    def f(x) :
        if x >= -1 : return math.sqrt(x + 1)
        return random.uniform(-1, 100)
        
    

    for i in range(iter) : 
        
        candidatos = []

        for i in haz :

            vecino =  [i + random.uniform(-1, 1) for j in range(10)]

            candidatos.extend(vecino)

        candidatos = [c for c in candidatos if c >= -.99]

        candidatos.sort(key = lambda x : f(x))
        haz = candidatos[:k]

    return haz[0]


        
    
top = haz_local(inicio = random.randint(-1, 100))

if top :
    print("Este es el mejor numero: ",top)
else :
    print("No se encontro mejor numero")