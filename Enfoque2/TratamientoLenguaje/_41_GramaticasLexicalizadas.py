# _41_GramaticasLexicalizadas.py
# Gramaticas Probabilisticas Lexicalizadas
# Extension de las PCFG donde las reglas dependen tambien de la PALABRA
# especifica (lexema) que encabeza cada constituyente.
# Esto permite capturar preferencias de subcategorizacion verbal:
#   "come" prefiere un NP objeto  ->  P(VP->V NP | come) alta
#   "duerme" rara vez tiene objeto -> P(VP->V NP | duerme) baja
#
# Reduce la ambiguedad sintactica que las PCFG no pueden resolver.

import math

print("=" * 55)
print("  GRAMATICAS PROBABILISTICAS LEXICALIZADAS")
print("=" * 55)

# ---- Tabla de probabilidades lexicalizadas ----
# P(expansion | no_terminal, palabra_cabeza)
p_lexi = {
    # VP con distintos verbos
    ("VP", "come"):    {"V_NP": 0.70, "V":    0.10, "V_PP": 0.20},
    ("VP", "duerme"):  {"V_NP": 0.05, "V":    0.85, "V_PP": 0.10},
    ("VP", "ve"):      {"V_NP": 0.60, "V":    0.10, "V_PP": 0.30},
    # NP con distintos determinantes
    ("NP", "el"):      {"Det_N": 0.95, "N": 0.05},
    ("NP", "un"):      {"Det_N": 0.90, "N": 0.10},
}

# ---- PCFG standard (sin lexicalizacion) para comparar ----
p_pcfg = {
    "VP":  {"V_NP": 0.50, "V": 0.30, "V_PP": 0.20},
    "NP":  {"Det_N": 0.60, "N": 0.40},
}

print("\nComparacion de probabilidades de expansion:")
print(f"\n  {'Regla':<20} {'PCFG':>8} {'Lex(come)':>12} {'Lex(duerme)':>13}")
print("  " + "-" * 55)

reglas_vp = ["V_NP", "V", "V_PP"]
for r in reglas_vp:
    p_std  = p_pcfg["VP"][r]
    p_come = p_lexi[("VP","come")][r]
    p_duer = p_lexi[("VP","duerme")][r]
    print(f"  VP -> {r:<14} {p_std:>8.2f} {p_come:>12.2f} {p_duer:>13.2f}")

# ---- Ejemplo de desambiguacion ----
print("\nEjemplo de desambiguacion:")
print("  Oracion: 'El gato come el pescado en el parque'")
print("  Ambiguedad: 'en el parque' modifica 'come' o 'pescado'?")
print()

# Interpretacion 1: VP -> V NP PP (come en el parque)
# Interpretacion 2: VP -> V NP, NP -> N PP (pescado en el parque)
p_interp1_come   = p_lexi[("VP","come")]["V_PP"]    # come con PP
p_interp2_come   = p_lexi[("VP","come")]["V_NP"]    # come con NP (que tiene PP)

p_interp1_duerme = p_lexi[("VP","duerme")]["V_PP"]
p_interp2_duerme = p_lexi[("VP","duerme")]["V_NP"]

print(f"  Con verbo 'come':")
print(f"    P(VP->V NP PP | come)  = {p_interp1_come:.2f}  <- 'come en el parque'")
print(f"    P(VP->V NP    | come)  = {p_interp2_come:.2f}  <- 'pescado en el parque'")
print(f"    Mas probable: {'come en el parque' if p_interp1_come>p_interp2_come else 'pescado en el parque'}")

print(f"\n  Con verbo 'duerme':")
print(f"    P(VP->V NP PP | duerme) = {p_interp1_duerme:.2f}")
print(f"    P(VP->V NP    | duerme) = {p_interp2_duerme:.2f}")
print(f"    Mas probable: {'con PP' if p_interp1_duerme>p_interp2_duerme else 'sin PP'}")

print("\nVentaja de la lexicalizacion:")
print("  Las PCFG no pueden distinguir entre verbos transitivos e intransitivos.")
print("  Las PCFG lexicalizadas resuelven este tipo de ambiguedad automaticamente.")
