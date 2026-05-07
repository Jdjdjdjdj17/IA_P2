# _32_TeoriaDeJuegosEquilibrios.py
# Teoria de Juegos: Equilibrios y Mecanismos
# Estudia como agentes racionales toman decisiones estrategicas.
# Equilibrio de Nash: ningún jugador puede mejorar cambiando solo su estrategia.
#
# Ejemplo clasico: El Dilema del Prisionero

# ---- Matriz de pagos ----
# Dos jugadores: A y B
# Estrategias: Cooperar (C) o Traicionar (T)
# pagos[estrategia_A][estrategia_B] = (pago_A, pago_B)

pagos = {
    'C': {
        'C': (3, 3),   # Ambos cooperan: los dos ganan bien
        'T': (0, 5),   # A coopera, B traiciona: A pierde, B gana mucho
    },
    'T': {
        'C': (5, 0),   # A traiciona, B coopera: A gana mucho, B pierde
        'T': (1, 1),   # Ambos traicionan: los dos ganan poco
    }
}

estrategias = ['C', 'T']

print("=" * 50)
print("  TEORIA DE JUEGOS — DILEMA DEL PRISIONERO")
print("=" * 50)

print("\nMatriz de pagos (Jugador A, Jugador B):")
print(f"{'':>10} {'B=Cooperar':>12} {'B=Traicionar':>14}")
print("-" * 40)
for ea in estrategias:
    nombre_a = "A=Cooperar" if ea == 'C' else "A=Traiciona"
    fila = f"{nombre_a:>10}"
    for eb in estrategias:
        pa, pb = pagos[ea][eb]
        fila += f"    ({pa}, {pb})   "
    print(fila)

# ---- Encontrar Equilibrio de Nash ----
# Para cada par de estrategias, verificar si alguno tiene incentivo de cambiar
print("\nAnalizando Equilibrios de Nash:")
equilibrios = []
for ea in estrategias:
    for eb in estrategias:
        pa, pb = pagos[ea][eb]
        # A puede mejorar cambiando su estrategia?
        mejor_a = all(pagos[ea2][eb][0] <= pa for ea2 in estrategias)
        # B puede mejorar cambiando su estrategia?
        mejor_b = all(pagos[ea][eb2][1] <= pb for eb2 in estrategias)
        if mejor_a and mejor_b:
            equilibrios.append((ea, eb))
            nombre_ea = "Cooperar" if ea == 'C' else "Traicionar"
            nombre_eb = "Cooperar" if eb == 'C' else "Traicionar"
            print(f"  EQUILIBRIO DE NASH encontrado: A={nombre_ea}, B={nombre_eb}  -> pagos=({pa},{pb})")

if not equilibrios:
    print("  No se encontro equilibrio de Nash puro.")

print("\nConclusion:")
print("  Aunque (Cooperar, Cooperar) da el mejor resultado COLECTIVO (3,3),")
print("  el equilibrio de Nash es (Traicionar, Traicionar) (1,1).")
print("  Cada jugador tiene incentivo individual de traicionar.")
