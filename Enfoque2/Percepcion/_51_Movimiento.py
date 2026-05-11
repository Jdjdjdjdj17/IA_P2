# _51_Movimiento.py
# Movimiento en Vision por Computador
# Detectar y analizar el movimiento de objetos entre fotogramas de video.
# Tecnicas:
#   - Diferencia de fotogramas: resta entre frames consecutivos
#   - Flujo optico (Optical Flow): estima el vector de desplazamiento de cada pixel
#   - Seguimiento de objetos: mantener la identidad del objeto a lo largo del tiempo
#
# Aqui implementamos diferencia de fotogramas y flujo optico simplificado.

import math

print("=" * 55)
print("  MOVIMIENTO EN VISION POR COMPUTADOR")
print("=" * 55)

# ---- Secuencia de 3 fotogramas 6x8 ----
# Un objeto (valor 200) se mueve de izquierda a derecha
def crear_frame(pos_col, F=6, C=8):
    frame = [[10]*C for _ in range(F)]
    for i in range(1, 5):
        for j in range(pos_col, min(pos_col+2, C)):
            frame[i][j] = 200
    return frame

frame1 = crear_frame(1)
frame2 = crear_frame(3)
frame3 = crear_frame(5)

def imprimir_frame(frame, titulo):
    print(f"\n{titulo}:")
    for fila in frame:
        print("  " + " ".join("█" if v > 100 else "·" for v in fila))

imprimir_frame(frame1, "Frame 1 (t=0)")
imprimir_frame(frame2, "Frame 2 (t=1)")
imprimir_frame(frame3, "Frame 3 (t=2)")

# ---- Diferencia de Fotogramas ----
def diferencia_frames(f1, f2, umbral=50):
    F, C = len(f1), len(f1[0])
    return [[1 if abs(f1[i][j]-f2[i][j]) > umbral else 0
             for j in range(C)] for i in range(F)]

diff12 = diferencia_frames(frame1, frame2)
diff23 = diferencia_frames(frame2, frame3)

print("\n--- DIFERENCIA DE FOTOGRAMAS ---")
print("Diferencia Frame1->Frame2 (pixeles que cambiaron):")
for fila in diff12:
    print("  " + " ".join("█" if v else "·" for v in fila))

# ---- Flujo Optico simplificado (Lucas-Kanade 1D horizontal) ----
print("\n--- FLUJO OPTICO SIMPLIFICADO ---")
print("Estimando desplazamiento horizontal del objeto...")

def centroide(frame, umbral=100):
    """Calcula el centroide de los pixeles activos"""
    puntos = [(i,j) for i,fila in enumerate(frame) for j,v in enumerate(fila) if v>umbral]
    if not puntos:
        return None
    ci = sum(p[0] for p in puntos)/len(puntos)
    cj = sum(p[1] for p in puntos)/len(puntos)
    return (ci, cj)

c1 = centroide(frame1)
c2 = centroide(frame2)
c3 = centroide(frame3)

print(f"\nCentroide del objeto:")
print(f"  t=0: ({c1[0]:.2f}, {c1[1]:.2f})")
print(f"  t=1: ({c2[0]:.2f}, {c2[1]:.2f})")
print(f"  t=2: ({c3[0]:.2f}, {c3[1]:.2f})")

vel12 = (c2[0]-c1[0], c2[1]-c1[1])
vel23 = (c3[0]-c2[0], c3[1]-c2[1])
print(f"\nVector de movimiento t=0->1: dy={vel12[0]:.2f}, dx={vel12[1]:.2f}")
print(f"Vector de movimiento t=1->2: dy={vel23[0]:.2f}, dx={vel23[1]:.2f}")
print(f"\nVelocidad promedio: dx={( vel12[1]+vel23[1])/2:.2f} pixeles/frame")

# ---- Prediccion de posicion futura ----
c4_pred = (c3[0] + vel23[0], c3[1] + vel23[1])
print(f"\nPrediccion para t=3: ({c4_pred[0]:.2f}, {c4_pred[1]:.2f})")

print("\nAplicaciones del analisis de movimiento:")
print("  - Seguridad: deteccion de intrusos")
print("  - Deportes: tracking de jugadores y pelota")
print("  - Autos autonomos: prediccion de trayectorias de peatones")
print("  - Video comprimido (MPEG): codificar solo los cambios entre frames")
