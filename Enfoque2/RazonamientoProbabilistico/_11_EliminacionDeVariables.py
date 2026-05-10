# _11_EliminacionDeVariables.py
# Eliminacion de Variables
# Metodo exacto mas eficiente que enumeracion.
# En lugar de sumar todas las combinaciones juntas, elimina variables
# una por una multiplicando factores y marginalizando.
#
# Evita recalcular los mismos productos repetidamente.

print("=" * 55)
print("  ELIMINACION DE VARIABLES")
print("=" * 55)

# ---- Red: R -> A <- T  (misma que antes) ----
P_R = {"si": 0.001, "no": 0.999}
P_T = {"si": 0.002, "no": 0.998}
P_A_RT = {
    ("si","si"): {"si": 0.95, "no": 0.05},
    ("si","no"): {"si": 0.94, "no": 0.06},
    ("no","si"): {"si": 0.29, "no": 0.71},
    ("no","no"): {"si": 0.001,"no": 0.999},
}

# ---- Consulta: P(R | A=si) ----
# Factores iniciales: f1(R), f2(T), f3(R,T,A=si)
# Eliminar T: multiplicar f2(T) * f3(R,T,A=si) y sumar sobre T -> f4(R)
# Resultado: f1(R) * f4(R), luego normalizar

a_obs = "si"  # evidencia: Alarma = si

print(f"\nEvidencia: Alarma = {a_obs}")
print(f"\nPaso 1: Aplicar evidencia -> reducir f3(R,T,A) a f3(R,T) con A={a_obs}")

# Factor f3 reducido con A=si
f3 = {}
for r in ["si","no"]:
    for t in ["si","no"]:
        f3[(r,t)] = P_A_RT[(r,t)][a_obs]
        print(f"  f3(R={r}, T={t}) = {f3[(r,t)]:.4f}")

print(f"\nPaso 2: Eliminar T -> f4(R) = suma_T [ f2(T) * f3(R,T) ]")
f4 = {}
for r in ["si","no"]:
    f4[r] = sum(P_T[t] * f3[(r,t)] for t in ["si","no"])
    desglose = " + ".join(f"P(T={t})*f3({r},{t})={P_T[t]*f3[(r,t)]:.6f}" for t in ["si","no"])
    print(f"  f4(R={r}) = {desglose}")
    print(f"           = {f4[r]:.8f}")

print(f"\nPaso 3: Multiplicar f1(R) * f4(R)")
f_final = {}
for r in ["si","no"]:
    f_final[r] = P_R[r] * f4[r]
    print(f"  P(R={r})*f4({r}) = {P_R[r]}*{f4[r]:.8f} = {f_final[r]:.10f}")

print(f"\nPaso 4: Normalizar")
total = sum(f_final.values())
for r in ["si","no"]:
    print(f"  P(R={r} | A=si) = {f_final[r]:.10f} / {total:.10f} = {f_final[r]/total:.6f}")

print(f"\nVentaja sobre enumeracion:")
print(f"  Enumeracion: calcula 2^n combinaciones completas.")
print(f"  Eliminacion: factoriza y elimina variables de a una -> mucho mas rapido.")
