from collections import deque

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

def hanoi_busqueda_a_lo_ancho(n_discos):
    """
    Resuelve el problema de las Torres de Hanoi con búsqueda a lo ancho (BFS)
    para una cantidad 'n' de discos.
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

    cola = deque([(estado_inicial, [])])
    estados_visitados = {estado_inicial}
    
    print(f"Resolviendo las Torres de Hanoi con {n_discos} discos...")

    while cola:
        estado_actual, camino_actual = cola.popleft()

        if estado_actual == estado_final:
            print("¡Solución encontrada! 🎉")
            print(f"Número de movimientos: {len(camino_actual)}")
            for i, movimiento in enumerate(camino_actual):
                print(f"Paso {i+1}: Mover de la torre {movimiento[0]} a la torre {movimiento[1]}")
            return True

        for nuevo_estado, movimiento in generar_sucesores(estado_actual):
            if nuevo_estado not in estados_visitados:
                estados_visitados.add(nuevo_estado)
                nuevo_camino = camino_actual + [movimiento]
                cola.append((nuevo_estado, nuevo_camino))
    
    print("El algoritmo no encontró una solución.")
    return False

# --- Uso del programa ---
if __name__ == "__main__":
    try:
        n_discos = int(input("Introduce la cantidad de discos (un número entero): "))
        if n_discos > 0:
            hanoi_busqueda_a_lo_ancho(n_discos)
        else:
            print("Por favor, introduce un número entero positivo.")
    except ValueError:
        print("Entrada no válida. Por favor, introduce un número entero.")