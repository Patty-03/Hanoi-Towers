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


def hanoi_hill_climbing(n_discos, max_iter=10000):
    """
    Resuelve el problema de las Torres de Hanoi con el algoritmo Hill Climbing.
    
    Este algoritmo busca mejorar el estado actual seleccionando en cada paso
    al sucesor con la mejor heurística (más cercano al estado objetivo),
    sin permitir movimientos que empeoren la solución.
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

    print(f"Resolviendo las Torres de Hanoi con {n_discos} discos usando Hill Climbing...")

    estado_actual = estado_inicial
    camino_actual = []

    for iteracion in range(max_iter):
        if estado_actual == estado_final:
            print("¡Solución encontrada! 🎉")
            print(f"Número de movimientos: {len(camino_actual)}")
            for i, movimiento in enumerate(camino_actual):
                print(f"Paso {i+1}: Mover de la torre {movimiento[0]} a la torre {movimiento[1]}")
            return True

        sucesores = generar_sucesores(estado_actual)
        
        if not sucesores:
            print("No hay más movimientos posibles.")
            break
        
        # Hill Climbing: seleccionamos el mejor sucesor (menor heurística)
        mejor_sucesor = None
        mejor_heuristica = float('inf')
        
        for sucesor_estado, movimiento in sucesores:
            heuristica = calcular_heuristica(sucesor_estado, n_discos)
            if heuristica < mejor_heuristica:
                mejor_heuristica = heuristica
                mejor_sucesor = (sucesor_estado, movimiento)
        
        # En Hill Climbing, solo avanzamos si encontramos un mejor estado
        # Si el mejor sucesor no mejora (mínimo local), terminamos
        if mejor_sucesor is not None and mejor_heuristica < calcular_heuristica(estado_actual, n_discos):
            estado_actual = mejor_sucesor[0]
            camino_actual.append(mejor_sucesor[1])
        else:
            print("Algoritmo Hill Climbing atascado en un mínimo local.")
            break

    print("El algoritmo no encontró una solución (posiblemente atascado en un mínimo local).")
    print(f"Iteraciones realizadas: {iteracion + 1}")
    return False


# --- Uso del programa ---
if __name__ == "__main__":
    try:
        n_discos = int(input("Introduce la cantidad de discos (un número entero): "))
        if n_discos > 0:
            hanoi_hill_climbing(n_discos)
        else:
            print("Por favor, introduce un número entero positivo.")
    except ValueError:
        print("Entrada no válida. Por favor, introduce un número entero.")