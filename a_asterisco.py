import heapq

def calcular_heuristica(estado):
    torre_final = 2
    
    # Buscamos el disco más grande que no esté en su posición final
    for disco in [3, 2, 1]:
        if disco not in estado[torre_final]:
            return pow(2, disco) - 1
        else:
            # Comprobamos si el disco está en la cima (al final de la tupla) de la torre final
            if estado[torre_final][-1] != disco:
                return pow(2, disco) - 1
            # Si el disco está en la torre final y es el más grande en la cima,
            # no se necesitan movimientos para él.
            
    return 0

def generar_sucesores(estado):

    sucesores = []
    
    for i in range(3):
        for j in range(3):
            # Verificamos que no sea la misma torre antes de proceder
            if i != j:
                # Comprobamos que la torre de origen no esté vacía
                if estado[i]:
                    disco_a_mover = estado[i][-1]
                    # Validamos que el movimiento sea legal
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
    

def hanoi_a_star():
    estado_inicial = (
        (3, 2, 1),
        (),
        ()
    )
    estado_final = (
        (),
        (),
        (3, 2, 1)
    )

    # La cola de prioridad almacenará tuplas: (f_score, g_score, estado, camino)
    # f_score = g_score + h_score
    cola_a_star = [(0, 0, estado_inicial, [])]
    
    # El diccionario de visitados almacena el costo más bajo (g_score) para llegar a un estado
    # para evitar ciclos y caminos más largos
    estados_visitados = {estado_inicial: 0}
    
    while cola_a_star:
        # Se extrae el nodo con el f_score más bajo
        f_actual, g_actual, estado_actual, camino_actual = heapq.heappop(cola_a_star)

        if estado_actual == estado_final:
            print("¡Solución encontrada! 🎉")
            print(f"Número de movimientos: {g_actual}")
            for i, movimiento in enumerate(camino_actual):
                print(f"Paso {i+1}: Mover de la torre {movimiento[0]} a la torre {movimiento[1]}")
            return True

        for nuevo_estado, movimiento in generar_sucesores(estado_actual):
            # Calculamos el costo g para el nuevo estado
            g_nuevo = g_actual + 1
            
            # Si el nuevo estado no ha sido visitado, o encontramos un camino más corto
            if nuevo_estado not in estados_visitados or g_nuevo < estados_visitados[nuevo_estado]:
                # Actualizamos el costo en el diccionario de visitados
                estados_visitados[nuevo_estado] = g_nuevo
                # Calculamos el f_score para el nuevo estado
                h_nuevo = calcular_heuristica(nuevo_estado)
                f_nuevo = g_nuevo + h_nuevo
                
                nuevo_camino = camino_actual + [movimiento]
                
                # Agregamos el nuevo estado a la cola de prioridad
                heapq.heappush(cola_a_star, (f_nuevo, g_nuevo, nuevo_estado, nuevo_camino))
    
    print("El algoritmo no encontró una solución.")
    return False

hanoi_a_star()