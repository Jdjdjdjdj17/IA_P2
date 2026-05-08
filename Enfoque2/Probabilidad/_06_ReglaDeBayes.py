# _06_ReglaDeBayes.py
# Regla de Bayes
# Permite actualizar la probabilidad de una hipotesis dado nueva evidencia.
#
# Formula:
#   P(H | E) = P(E | H) * P(H) / P(E)
#
# Donde:
#   P(H)     = probabilidad a priori de la hipotesis
#   P(E | H) = verosimilitud: prob de ver la evidencia si H es cierta
#   P(E)     = probabilidad total de la evidencia (normalizacion)
#   P(H | E) = probabilidad a posteriori (lo que queremos calcular)

print("=" * 50)
print("  REGLA DE BAYES")
print("=" * 50)

# ---- Ejemplo: prueba medica ----
# Enfermedad rara: P(enfermo) = 0.01
# Prueba positiva si enfermo: P(+|enfermo) = 0.95
# Falso positivo: P(+|sano)  = 0.05

p_enfermo    = 0.01
p_sano       = 1 - p_enfermo
p_pos_enfermo = 0.95   # sensibilidad
p_pos_sano    = 0.05   # tasa de falso positivo

print(f"\nPrueba medica para enfermedad rara")
print(f"  P(enfermo)           = {p_enfermo}")
print(f"  P(+ | enfermo)       = {p_pos_enfermo}  (sensibilidad)")
print(f"  P(+ | sano)          = {p_pos_sano}  (tasa falso positivo)")

# Probabilidad total de test positivo: P(+) = P(+|E)*P(E) + P(+|S)*P(S)
p_positivo = p_pos_enfermo * p_enfermo + p_pos_sano * p_sano
print(f"\n  P(+) = P(+|E)*P(E) + P(+|S)*P(S)")
print(f"       = {p_pos_enfermo}*{p_enfermo} + {p_pos_sano}*{p_sano}")
print(f"       = {p_positivo:.4f}")

# Aplicar Bayes
p_enfermo_dado_pos = (p_pos_enfermo * p_enfermo) / p_positivo
p_sano_dado_pos    = (p_pos_sano    * p_sano)    / p_positivo

print(f"\n  P(enfermo | +) = P(+|E)*P(E) / P(+)")
print(f"                 = {p_pos_enfermo}*{p_enfermo} / {p_positivo:.4f}")
print(f"                 = {p_enfermo_dado_pos:.4f}")
print(f"\n  P(sano | +)    = {p_sano_dado_pos:.4f}")
print(f"\nSuma de posteriori: {p_enfermo_dado_pos + p_sano_dado_pos:.1f}")

print(f"\nInterpretacion:")
print(f"  Aunque la prueba es 95% precisa, si el test da positivo")
print(f"  solo hay un {p_enfermo_dado_pos*100:.1f}% de probabilidad de estar enfermo.")
print(f"  Esto se debe a lo rara que es la enfermedad (prior bajo).")

# ---- Actualizacion iterativa de Bayes ----
print(f"\n--- Actualizacion iterativa con mas evidencia ---")
p_h = p_enfermo
evidencias = [("segunda prueba +", 0.90, 0.03),
              ("sintomas presentes", 0.80, 0.10)]

for nombre, p_e_h, p_e_no_h in evidencias:
    p_no_h = 1 - p_h
    p_e = p_e_h * p_h + p_e_no_h * p_no_h
    p_h = (p_e_h * p_h) / p_e
    print(f"  Tras '{nombre}': P(enfermo) = {p_h:.4f}")
