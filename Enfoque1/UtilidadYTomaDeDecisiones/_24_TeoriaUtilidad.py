# _24_TeoriaUtilidad.py
# Teoría de la Utilidad: Función de Utilidad
# La utilidad mide qué tan "bueno" es un resultado para el agente.
# El agente siempre elige la acción con mayor utilidad esperada.

# ---- Función de Utilidad ----
# Mapea cada resultado a un valor numérico que representa su preferencia
def utilidad(resultado):
    tabla = {
        "ganar_grande": 100,
        "ganar_poco":    40,
        "empate":        10,
        "perder_poco":  -20,
        "perder_grande":-80,
    }
    return tabla.get(resultado, 0)

# ---- Utilidad Esperada ----
# EU(accion) = suma de P(resultado) * U(resultado)
def utilidad_esperada(accion, probabilidades):
    eu = 0
    for resultado, prob in probabilidades[accion].items():
        eu += prob * utilidad(resultado)
    return eu

# ---- Escenario: El agente decide si apostar o guardar dinero ----
# Cada accion tiene posibles resultados con su probabilidad
probabilidades = {
    "apostar": {
        "ganar_grande": 0.20,
        "ganar_poco":   0.30,
        "empate":       0.10,
        "perder_poco":  0.25,
        "perder_grande":0.15,
    },
    "guardar": {
        "empate":       0.60,
        "ganar_poco":   0.40,
    }
}

print("=" * 40)
print("  TEORÍA DE LA UTILIDAD")
print("=" * 40)

mejor_accion = None
mejor_eu = float('-inf')

for accion in probabilidades:
    eu = utilidad_esperada(accion, probabilidades)
    print(f"\nAccion: {accion}")
    for resultado, prob in probabilidades[accion].items():
        u = utilidad(resultado)
        print(f"  P({resultado}) = {prob:.2f}  ->  U = {u}  contribucion = {prob*u:.1f}")
    print(f"  Utilidad Esperada = {eu:.2f}")
    if eu > mejor_eu:
        mejor_eu = eu
        mejor_accion = accion

print(f"\nDECISION: El agente elige '{mejor_accion}' con EU = {mejor_eu:.2f}")
