# _03_ProbabilidadCondicionada.py
# Probabilidad Condicionada y Normalizacion
# P(A|B) = P(A ^ B) / P(B)
# Es la probabilidad de A dado que ya sabemos que B ocurrio.
# Normalizacion: ajustar probabilidades para que sumen 1 tras observar evidencia.

print("=" * 50)
print("  PROBABILIDAD CONDICIONADA Y NORMALIZACION")
print("=" * 50)

# ---- Tabla conjunta: Enfermedad (E) y Fiebre (F) ----
# P(E=si, F=si), P(E=si, F=no), etc.
tabla = {
    ("si", "si"): 0.42,   # enfermo y con fiebre
    ("si", "no"): 0.08,   # enfermo sin fiebre
    ("no", "si"): 0.10,   # sano con fiebre (otra causa)
    ("no", "no"): 0.40,   # sano sin fiebre
}

print("\nTabla conjunta P(Enfermedad, Fiebre):")
print(f"  {'E':<6} {'F':<6} {'P(E,F)'}")
print("  " + "-" * 22)
for (e, f), p in tabla.items():
    print(f"  {e:<6} {f:<6} {p:.2f}")

# ---- P(E) y P(F) marginales ----
p_e_si = sum(v for (e,f),v in tabla.items() if e=="si")
p_f_si = sum(v for (e,f),v in tabla.items() if f=="si")
print(f"\nMarginales:")
print(f"  P(E=si) = {p_e_si:.2f}")
print(f"  P(F=si) = {p_f_si:.2f}")

# ---- Probabilidad Condicionada ----
# P(E=si | F=si) = P(E=si, F=si) / P(F=si)
p_e_dado_f = tabla[("si","si")] / p_f_si
print(f"\nProbabilidad Condicionada:")
print(f"  P(E=si | F=si) = P(E=si,F=si) / P(F=si)")
print(f"                 = {tabla[('si','si')]:.2f} / {p_f_si:.2f} = {p_e_dado_f:.3f}")

# ---- Normalizacion ----
# Dado que F=si, renormalizamos la distribucion sobre E
print(f"\nNormalizacion dado F=si:")
sin_norm = {e: tabla[(e,"si")] for e in ["si","no"]}
total    = sum(sin_norm.values())
norm     = {e: v/total for e,v in sin_norm.items()}
print(f"  Sin normalizar: {sin_norm}")
print(f"  Total         : {total:.2f}")
print(f"  Normalizado   : {{E=si: {norm['si']:.3f}, E=no: {norm['no']:.3f}}}")
print(f"  Suma          : {sum(norm.values()):.1f}  <- siempre debe ser 1")
