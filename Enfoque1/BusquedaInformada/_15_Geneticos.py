import random
import math

def alg_gen(pob_num, generaciones) :
    poblacion = [random.uniform(-1, 500) for i in range(pob_num)]
    def f(x):
        if x < -1 : return random.random()
        return math.sqrt(x + 1)
    
    for _ in range(generaciones):
        poblacion.sort(key = lambda x : f(x))
        new_gen = poblacion [:2]

        while len(new_gen) < pob_num :
            p1, p2 = random.sample(poblacion[:10], 2)

            hijo = (p1 + p2)/2

            if random.random() < 0.2:
                    hijo += random.uniform(-0.5, 0.5)

            if hijo >= -1 :
                new_gen.append(hijo)

        poblacion = new_gen

    return poblacion[0]

top = alg_gen(30, 1000)
if top :
    print("El mejor numero: ",top)
else :
    print("No hay mejor numero")