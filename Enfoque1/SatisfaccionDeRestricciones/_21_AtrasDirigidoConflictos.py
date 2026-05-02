def cbj_solver(indices, dominios, restricciones, asignacion, sets_conflicto):
    # Si todas las variables están asignadas, terminamos
    if not indices:
        return True, None

    v_actual = indices[0]
    otros_indices = indices[1:]

    for valor in dominios[v_actual]:
        # 1. Verificar conflictos con lo ya asignado
        culpables = [v for v in restricciones.get(v_actual, []) if v in asignacion and asignacion[v] == valor]
        
        if not culpables:
            # Intentar asignar
            asignacion[v_actual] = valor
            exito, salto_a = cbj_solver(otros_indices, dominios, restricciones, asignacion, sets_conflicto)
            
            if exito: return True, None
            
            # Si hay un salto y no es para mí, sigo propagando el salto hacia atrás
            if salto_a is not None and salto_a != v_actual:
                del asignacion[v_actual]
                return False, salto_a
            
            # Si el fallo fue en el nivel inmediatamente superior, absorbo sus conflictos
            # (Quitando a la variable actual de la culpa)
            idx_siguiente = otros_indices[0] if otros_indices else None
            if idx_siguiente:
                sets_conflicto[v_actual].update(sets_conflicto[idx_siguiente] - {v_actual})
            
            del asignacion[v_actual]
        else:
            # Si hay conflicto directo, guardamos quién nos bloqueó
            sets_conflicto[v_actual].update(culpables)

    # Si agotamos el dominio, saltamos al culpable más reciente (el 'max' de los conflictos)
    if not sets_conflicto[v_actual]:
        return False, None
    
    objetivo_salto = max(sets_conflicto[v_actual], key=lambda x: "ABC".find(x)) # Orden lógico
    return False, objetivo_salto

# --- CONFIGURACIÓN DEL PROBLEMA ---
vars_lista = ["A", "B", "C"]
doms = {"A": [1], "B": [1, 2], "C": [1]} # Forzamos conflicto: A=1, B=2, C=? (A y B bloquean a C)
restrs = {"B": ["A"], "C": ["A", "B"]}   # Todos conectados entre sí
conf_sets = {v: set() for v in vars_lista}

exito, _ = cbj_solver(vars_lista, doms, restrs, {}, conf_sets)
print(f"¿Solucionado?: {exito}")