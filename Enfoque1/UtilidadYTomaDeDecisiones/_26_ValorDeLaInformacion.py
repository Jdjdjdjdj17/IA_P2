# _26_ValorDeLaInformacion.py
# Valor de la Información (VOI)
# ¿Cuánto vale saber algo antes de tomar una decisión?
# VOI = EU(con informacion perfecta) - EU(sin informacion)

def utilidad(resultado):
    tabla = {
        "exito":  80,
        "fracaso": -30,
    }
    return tabla.get(resultado, 0)

# ---- Sin informacion: el agente decide sin saber el resultado ----
# Solo conoce las probabilidades globales
prob_exito   = 0.55
prob_fracaso = 0.45

eu_invertir_sin_info = prob_exito * utilidad("exito") + prob_fracaso * utilidad("fracaso")
eu_no_invertir       = 0  # No hacer nada da 0 de utilidad

eu_sin_info = max(eu_invertir_sin_info, eu_no_invertir)

print("=" * 45)
print("  VALOR DE LA INFORMACIÓN")
print("=" * 45)
print(f"\nSIN informacion:")
print(f"  EU(invertir)    = {eu_invertir_sin_info:.2f}")
print(f"  EU(no invertir) = {eu_no_invertir:.2f}")
print(f"  Mejor decision  = EU = {eu_sin_info:.2f}")

# ---- Con informacion perfecta: el agente sabe el resultado de antemano ----
# Si sabe que hay exito -> invierte (gana 80)
# Si sabe que hay fracaso -> no invierte (gana 0)
eu_con_info = prob_exito * utilidad("exito") + prob_fracaso * eu_no_invertir

print(f"\nCON informacion perfecta:")
print(f"  Si exito   (P={prob_exito}): invierte -> U = {utilidad('exito')}")
print(f"  Si fracaso (P={prob_fracaso}): no invierte -> U = {eu_no_invertir}")
print(f"  EU esperada con info = {eu_con_info:.2f}")

# ---- Valor de la Informacion Perfecta ----
voi = eu_con_info - eu_sin_info
print(f"\nVOI (Valor de la Informacion) = {eu_con_info:.2f} - {eu_sin_info:.2f} = {voi:.2f}")
print(f"\nInterpretacion: El agente pagaria hasta {voi:.2f} puntos de utilidad")
print(f"por conocer el resultado antes de decidir.")
