import random
import math

def ascenso_colinas(inicio, iter = 1000) :

    def f(x) :
        if x < -1 : return random.randint(100, 200)
        return math.sqrt(x + 1)
    
    

    for i in range(iter) : 
        
        vecino = inicio - random.uniform(-1 ,1)  
        
        print(inicio)
        print(vecino)
        
        if f(inicio) > f(vecino) :
            inicio = vecino

    return inicio             
        
    
top = ascenso_colinas(inicio = random.randint(-1, 100))

if top :
    print("Este es el mejor numero: ",top)
else :
    print("No se encontro mejor numero")