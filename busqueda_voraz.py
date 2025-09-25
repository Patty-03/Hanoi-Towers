import heapq

def calcular_heuristica(estado):
    torre_final = 2
    h = 0
    
    # Buscamos el disco más grande que no esté en su posición final
    for disco in [3, 2, 1]:
        if disco not in estado[torre_final]:
            h = pow(2, disco) - 1
        else:
            # Comprobamos si el disco está en la cima (al final de la tupla) de la torre final
            if estado[torre_final][-1] != disco:
                h =  pow(2, disco) - 1
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

def hanoi_voraz():

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

    pila_voraz = [(calcular_heuristica(estado_inicial), estado_inicial, [])]
    estados_visitados = {estado_inicial}
    
    while pila_voraz:
        h_actual, estado_actual, camino_actual = heapq.heappop(pila_voraz)

        if estado_actual == estado_final:
            print("¡Solución encontrada! 🎉")
            print(f"Número de movimientos: {len(camino_actual)}")
            for i, movimiento in enumerate(camino_actual):
                print(f"Paso {i+1}: Mover de la torre {movimiento[0]} a la torre {movimiento[1]}")
            return True

        for nuevo_estado, movimiento in generar_sucesores(estado_actual):
            if nuevo_estado not in estados_visitados:
                estados_visitados.add(nuevo_estado)
                h_nuevo = calcular_heuristica(nuevo_estado)
                nuevo_camino = camino_actual + [movimiento]
                heapq.heappush(pila_voraz, (h_nuevo, nuevo_estado, nuevo_camino))
    
    print("El algoritmo no encontró una solución.")
    return False

if __name__ == "__main__":
    hanoi_voraz()