def generar_sucesores(estado):
    """
    Genera todos los estados válidos a los que se puede transicionar.
    """
    sucesores = []
    
    for i in range(3):
        for j in range(3):
            if i != j:
                if estado[i]:
                    disco_a_mover = estado[i][-1]
                    if not estado[j] or disco_a_mover < estado[j][-1]:
                        nueva_torre_origen = list(estado[i])
                        nueva_torre_destino = list(estado[j])

                        nueva_torre_origen.pop()
                        nueva_torre_destino.append(disco_a_mover)
                        
                        nuevo_estado_list = list(estado)
                        nuevo_estado_list[i] = tuple(nueva_torre_origen)
                        nuevo_estado_list[j] = tuple(nueva_torre_destino)
                        nuevo_estado = tuple(nuevo_estado_list)
                        
                        movimiento = (i, j)
                        sucesores.append((nuevo_estado, movimiento))
    return sucesores


def calcular_heuristica(estado, n_discos):
    """
    Calcula una heurística para el estado actual.
    Devuelve el número de discos que no están en la torre objetivo (torre 2).
    """
    discos_fuera_de_lugar = 0
    torre_final = 2
    
    # Contamos los discos que no están en la torre final
    for disco in range(1, n_discos + 1):
        en_torre_final = False
        for torre_idx, torre in enumerate(estado):
            if disco in torre and torre_idx == torre_final:
                en_torre_final = True
                break
        if not en_torre_final:
            discos_fuera_de_lugar += 1
    
    return discos_fuera_de_lugar


def hanoi_busqueda_tabu(n_discos, tamano_lista_tabu=10, max_iter=10000):
    """
    Resuelve el problema de las Torres de Hanoi con búsqueda tabú.
    
    La búsqueda tabú evita ciclos mediante el uso de una lista tabú,
    que almacena movimientos recientes que están prohibidos temporalmente.
    """
    # Se genera el estado inicial a partir de n_discos
    estado_inicial = (
        tuple(range(n_discos, 0, -1)),  # Torre 0: discos del más grande al más pequeño
        (),  # Torre 1: vacía
        ()   # Torre 2: vacía
    )
    
    # Se genera el estado final
    estado_final = (
        (),
        (),
        tuple(range(n_discos, 0, -1)) # Torre 2: discos apilados correctamente
    )

    print(f"Resolviendo las Torres de Hanoi con {n_discos} discos usando Búsqueda Tabú...")

    estado_actual = estado_inicial
    camino_actual = []
    
    # Lista tabú que almacena movimientos recientes para evitar ciclos
    lista_tabu = []
    
    # Almacenar el mejor estado encontrado
    mejor_estado = estado_actual
    mejor_heuristica = calcular_heuristica(mejor_estado, n_discos)

    for iteracion in range(max_iter):
        if estado_actual == estado_final:
            print("¡Solución encontrada! 🎉")
            print(f"Número de movimientos: {len(camino_actual)}")
            for i, movimiento in enumerate(camino_actual):
                print(f"Paso {i+1}: Mover de la torre {movimiento[0]} a la torre {movimiento[1]}")
            return True

        # Generar todos los sucesores válidos
        sucesores = generar_sucesores(estado_actual)
        
        if not sucesores:
            print("No hay más movimientos posibles.")
            break

        # Buscar el mejor movimiento que no esté en la lista tabú
        mejor_sucesor = None
        mejor_heuristica_sucesor = float('inf')
        mejor_movimiento = None
        
        for sucesor_estado, movimiento in sucesores:
            # Solo considerar movimientos que no estén en la lista tabú
            if movimiento not in lista_tabu:
                heuristica = calcular_heuristica(sucesor_estado, n_discos)
                # Buscar el mejor sucesor no tabú
                if heuristica < mejor_heuristica_sucesor:
                    mejor_heuristica_sucesor = heuristica
                    mejor_sucesor = sucesor_estado
                    mejor_movimiento = movimiento
            else:
                # Verificar si es un movimiento de aspiración (mejora el mejor resultado global)
                heuristica = calcular_heuristica(sucesor_estado, n_discos)
                if heuristica < mejor_heuristica:
                    # Movimiento de aspiración - usarlo a pesar de estar en la lista tabú
                    mejor_heuristica_sucesor = heuristica
                    mejor_sucesor = sucesor_estado
                    mejor_movimiento = movimiento

        if mejor_sucesor is not None:
            # Actualizar estado
            estado_actual = mejor_sucesor
            camino_actual.append(mejor_movimiento)
            
            # Agregar movimiento a la lista tabú
            lista_tabu.append(mejor_movimiento)
            
            # Mantener tamaño máximo de la lista tabú
            if len(lista_tabu) > tamano_lista_tabu:
                lista_tabu.pop(0)  # Remover el movimiento más antiguo
            
            # Actualizar el mejor estado si encontramos uno mejor
            if mejor_heuristica_sucesor < mejor_heuristica:
                mejor_heuristica = mejor_heuristica_sucesor
                mejor_estado = mejor_sucesor
        else:
            # No se encontró un sucesor no tabú, intentar con sucesor no tabú de mejor calidad
            # En este caso, simplemente elegiremos el mejor movimiento posible
            mejor_heuristica_sucesor = float('inf')
            for sucesor_estado, movimiento in sucesores:
                heuristica = calcular_heuristica(sucesor_estado, n_discos)
                if heuristica < mejor_heuristica_sucesor:
                    mejor_heuristica_sucesor = heuristica
                    mejor_sucesor = sucesor_estado
                    mejor_movimiento = movimiento
            
            if mejor_sucesor is not None:
                estado_actual = mejor_sucesor
                camino_actual.append(mejor_movimiento)
                
                # Agregar movimiento a la lista tabú
                lista_tabu.append(mejor_movimiento)
                if len(lista_tabu) > tamano_lista_tabu:
                    lista_tabu.pop(0)

    print("El algoritmo no encontró una solución dentro del límite de iteraciones.")
    print(f"Iteraciones realizadas: {max_iter}")
    
    # Mostrar información sobre el mejor estado encontrado
    print(f"Mejor estado encontrado: {mejor_estado}")
    print(f"Heurística del mejor estado: {mejor_heuristica}")
    
    return estado_actual == estado_final


# --- Uso del programa ---
if __name__ == "__main__":
    try:
        n_discos = int(input("Introduce la cantidad de discos (un número entero): "))
        if n_discos > 0:
            hanoi_busqueda_tabu(n_discos)
        else:
            print("Por favor, introduce un número entero positivo.")
    except ValueError:
        print("Entrada no válida. Por favor, introduce un número entero.")