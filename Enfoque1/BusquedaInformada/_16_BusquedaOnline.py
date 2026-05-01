import random

def online(meta=0, inicio=10):
    pos_actual = inicio
    memoria_h = {}
    pasos = 0

    while pos_actual != meta and pasos < 50:
        pasos += 1
        vecinos = [pos_actual - 1, pos_actual + 1]
        
        # AGREGAMOS RANDOM: ¿Exploramos o explotamos?
        if random.random() < 0.15: # 15% de probabilidad de "curiosidad"
            pos_actual = random.choice(vecinos)
            print(f"Paso {pasos}: ¡Curiosidad! Salté a {pos_actual}")
        else:
            # Decisión basada en memoria
            pos_actual = min(vecinos, key=lambda v: memoria_h.get(v, abs(v - meta)))
            
        # Actualizar memoria (LRTA*)
        costo_vecino = memoria_h.get(pos_actual, abs(pos_actual - meta))
        memoria_h[pos_actual] = 1 + costo_vecino
        
    # Al final de la función
    return {
        "llego_a_meta": pos_actual == meta,
        "posicion_final": pos_actual,
        "mapa_aprendido": memoria_h, # El conocimiento oro
        "total_pasos": pasos
    }

top = online(meta=0, inicio=10)

print("\n" + "="*30)
print(f"ESTADO FINAL: {'¡LOGRADO!' if top['llego_a_meta'] else 'FALLIDO'}")
print(f"PASOS DADOS: {top['total_pasos']}")
print("="*30)

print("\nMAPA DE APRENDIZAJE (H-Costs):")
print("Posición | Costo estimado")
print("-------------------------")
# Ordenamos las posiciones para ver el camino
for pos in sorted(top['mapa_aprendido'].keys()):
    costo = top['mapa_aprendido'][pos]
    print(f"   {pos:2d}    |   {costo:.2f}")