import heapq

def calcular_heuristica(estado, n_discos):
    torre_final = 2
    
    for disco in range(n_discos, 0, -1):
        if disco not in estado[torre_final]:
            return pow(2, disco) - 1
        else:
            if estado[torre_final][-1] != disco:
                return pow(2, disco) - 1
            
    return 0

def generar_sucesores(estado):
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

def hanoi_voraz(n_discos):

    print(f"\nResolviendo Torres de Hanoi con {n_discos} discos usando Búsqueda Voraz...")
    
    discos = tuple(range(n_discos, 0, -1))
    
    estado_inicial = (discos, (), ())
    estado_final = ((), (), discos)

    # La cola de prioridad almacena (heuristica, estado, camino)
    h_inicial = calcular_heuristica(estado_inicial, n_discos)
    pila_voraz = [(h_inicial, estado_inicial, [])]
    
    estados_visitados = {estado_inicial}
    
    while pila_voraz:
        # Se extrae el nodo con la heurística más baja
        h_actual, estado_actual, camino_actual = heapq.heappop(pila_voraz)

        if estado_actual == estado_final:
            print("¡Solución encontrada! 🎉")
            print(f"Número de movimientos: {len(camino_actual)}")
            print(f"La solución óptima es: {pow(2, n_discos) - 1} movimientos.")
            return True

        for nuevo_estado, movimiento in generar_sucesores(estado_actual):
            if nuevo_estado not in estados_visitados:
                estados_visitados.add(nuevo_estado)
                h_nuevo = calcular_heuristica(nuevo_estado, n_discos)
                nuevo_camino = camino_actual + [movimiento]
                heapq.heappush(pila_voraz, (h_nuevo, nuevo_estado, nuevo_camino))
    
    print("El algoritmo no encontró una solución.")
    return False

if __name__ == "__main__":
    try:
        n_discos_input = input("Introduce la cantidad de discos (un entero positivo, ej. 4): ")
        n_discos = int(n_discos_input)
        
        if n_discos < 1:
            print("Por favor, introduce un número entero positivo (al menos 1).")
        else:
            hanoi_voraz(n_discos)
            
    except ValueError:
        print("Entrada no válida. Por favor, introduce un número entero.")