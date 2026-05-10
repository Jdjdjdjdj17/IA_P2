# _20_FiltrosDeKalman.py
# Filtros de Kalman
# Extension del HMM para variables CONTINUAS con ruido gaussiano.
# Asume que las transiciones y observaciones son lineales con ruido gaussiano.
#
# Estado: x_t = A*x_{t-1} + ruido_proceso   (ruido ~ N(0, Q))
# Obs:    z_t = H*x_t    + ruido_sensor     (ruido ~ N(0, R))
#
# El filtro mantiene una distribucion gaussiana: (media, varianza)
# y la actualiza en dos pasos: Prediccion y Actualizacion.

print("=" * 55)
print("  FILTRO DE KALMAN (1D)")
print("=" * 55)

# ---- Modelo 1D: seguimiento de posicion de un objeto ----
# El objeto se mueve a velocidad constante con pequeno ruido
# El sensor mide posicion con ruido

A = 1.0   # modelo de transicion (posicion = posicion anterior)
H = 1.0   # modelo de observacion (observamos directamente la posicion)
Q = 0.1   # varianza del ruido del proceso
R = 1.0   # varianza del ruido del sensor

# Estado inicial: posicion estimada = 0, incertidumbre alta
mu  = 0.0    # media estimada
P   = 1.0    # varianza estimada

# Posicion real y observaciones ruidosas simuladas
import random
random.seed(42)
pos_real = 0.0
observaciones = []
for _ in range(10):
    pos_real += 1.0 + random.gauss(0, Q**0.5)          # movimiento con ruido
    obs = pos_real + random.gauss(0, R**0.5)           # sensor ruidoso
    observaciones.append((round(pos_real, 3), round(obs, 3)))

print(f"\nModelo: posicion avanza ~1 por paso")
print(f"Ruido proceso Q={Q}, Ruido sensor R={R}\n")
print(f"{'t':<4} {'Pos_real':<12} {'Obs':<10} {'Est_previa':<13} {'Ganancia_K':<13} {'Est_final':<12} {'Varianza_P'}")
print("-" * 78)

for t, (pos_real_t, z) in enumerate(observaciones, 1):
    # ---- Prediccion ----
    mu_pred = A * mu        # prediccion de la media
    P_pred  = A*P*A + Q     # prediccion de la varianza

    # ---- Actualizacion ----
    K   = P_pred * H / (H*P_pred*H + R)   # ganancia de Kalman
    mu  = mu_pred + K*(z - H*mu_pred)     # media actualizada
    P   = (1 - K*H) * P_pred              # varianza actualizada

    print(f"{t:<4} {pos_real_t:<12} {z:<10.3f} {mu_pred:<13.3f} {K:<13.4f} {mu:<12.3f} {P:.4f}")

print(f"\nInterpretacion de la Ganancia K:")
print(f"  K cercano a 1 -> confiar mas en la observacion")
print(f"  K cercano a 0 -> confiar mas en el modelo de prediccion")
print(f"  K converge a un valor estable (estado estacionario del filtro)")
