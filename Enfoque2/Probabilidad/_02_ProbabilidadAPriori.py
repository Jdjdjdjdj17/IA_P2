# _02_ProbabilidadAPriori.py
# Probabilidad a Priori (Prior)
# Es la probabilidad de un evento ANTES de observar evidencia.
# Representa el conocimiento inicial del agente sobre el mundo.
#
# P(A) = numero de casos favorables / total de casos posibles
# Tambien puede venir de frecuencias historicas o conocimiento experto.

print("=" * 45)
print("  PROBABILIDAD A PRIORI")
print("=" * 45)

# ---- Ejemplo 1: dado de 6 caras ----
caras = [1, 2, 3, 4, 5, 6]
evento_par = [c for c in caras if c % 2 == 0]

p_par = len(evento_par) / len(caras)
print(f"\nDado de 6 caras: {caras}")
print(f"Evento 'par': {evento_par}")
print(f"P(par) = {len(evento_par)}/{len(caras)} = {p_par:.3f}")

# ---- Ejemplo 2: datos historicos de clima ----
historial = ["sol", "sol", "nublado", "lluvia", "sol", "lluvia",
             "nublado", "sol", "sol", "lluvia"]

conteos = {}
for dia in historial:
    conteos[dia] = conteos.get(dia, 0) + 1

total = len(historial)
print(f"\nHistorial climatico ({total} dias): {historial}")
print("\nProbabilidades a priori del clima:")
for estado, cnt in conteos.items():
    print(f"  P({estado}) = {cnt}/{total} = {cnt/total:.3f}")

# ---- Distribuciones a priori comunes ----
print("\nDistribuciones a priori tipicas en IA:")
print("  - Uniforme: todos los eventos igualmente probables")
print("  - Basada en datos: frecuencia relativa observada")
print("  - Bayesiana: conocimiento experto codificado como distribucion")

# ---- Tabla conjunta de probabilidades a priori ----
# Variables: Lluvia (L) y Trafico (T)
print("\nTabla conjunta P(Lluvia, Trafico):")
tabla = {
    ("si", "si"):  0.30,
    ("si", "no"):  0.05,
    ("no", "si"):  0.25,
    ("no", "no"):  0.40,
}
print(f"  {'Lluvia':<8} {'Trafico':<10} {'P(L,T)'}")
print("  " + "-" * 28)
for (l, t), p in tabla.items():
    print(f"  {l:<8} {t:<10} {p:.2f}")

p_lluvia = sum(v for (l,t), v in tabla.items() if l == "si")
print(f"\n  P(Lluvia=si) = {p_lluvia:.2f}  <- marginalizacion")
