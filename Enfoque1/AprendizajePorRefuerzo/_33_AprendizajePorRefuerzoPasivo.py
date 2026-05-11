# _33_AprendizajePorRefuerzoPasivo.py
# Aprendizaje por Refuerzo Pasivo
# El agente sigue una politica FIJA y aprende el valor de cada estado
# observando las recompensas que recibe (no elige acciones, solo observa).
#
# Metodo: Estimacion Directa de Utilidad (Monte Carlo)
# V(s) = promedio de recompensas acumuladas obtenidas desde s

import random

# ---- Entorno: cuadricula 1x4 ----
estados  = [0, 1, 2, 3]
gamma    = 0.9

def recompensa(estado):
    if estado == 3: return  10
    if estado == 0: return  -5
    return -1

# Politica fija que el agente sigue (siempre va a la derecha)
def politica_fija(estado):
    return 1  # siempre derecha

def siguiente(estado, accion):
    return max(0, min(3, estado + accion))

# ---- Generar episodios siguiendo la politica fija ----
def generar_episodio(inicio):
    episodio = []
    s = inicio
    for _ in range(20):  # maximo 20 pasos
        a = politica_fija(s)
        s2 = siguiente(s, a)
        r = recompensa(s2)
        episodio.append((s, r))
        s = s2
        if s in [0, 3]:  # terminal
            episodio.append((s, recompensa(s)))
            break
    return episodio

# ---- Aprendizaje: estimar V(s) por promedio de retornos ----
retornos = {s: [] for s in estados}
num_episodios = 500

for _ in range(num_episodios):
    inicio = random.choice([1, 2])  # empieza en estados no terminales
    ep = generar_episodio(inicio)
    # Calcula retorno acumulado desde cada estado del episodio
    G = 0
    for t in reversed(range(len(ep))):
        s, r = ep[t]
        G = r + gamma * G
        retornos[s].append(G)

V = {s: (sum(retornos[s]) / len(retornos[s])) if retornos[s] else 0 for s in estados}

print("=" * 45)
print("  APRENDIZAJE POR REFUERZO PASIVO")
print("  (Estimacion Directa de Utilidad)")
print("=" * 45)
print(f"\nEpisodios simulados: {num_episodios}")
print(f"Politica seguida: siempre ir a la derecha\n")
print(f"{'Estado':<8} {'V(s) aprendido'}")
print("-" * 25)
for s in estados:
    print(f"  {s:<6}   {V[s]:.4f}")
