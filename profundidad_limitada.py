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


def hanoi_busqueda_profundidad_limitada(n_discos, limite_profundidad):
    """
    Resuelve el problema de las Torres de Hanoi con búsqueda en profundidad limitada (DFS-Limited)
    para una cantidad 'n' de discos con un límite de profundidad.
    """
    print(f"Torres de Hanoi usando busqueda en profundidad limitada con {n_discos} discos y límite de profundidad {limite_profundidad}")
    
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

    # La pila ahora contendrá (estado, camino, profundidad)
    pila = deque([(estado_inicial, [], 0)])
    estados_visitados = {estado_inicial}

    while pila:
        estado_actual, camino_actual, profundidad_actual = pila.pop()

        if estado_actual == estado_final:
            print("¡Solución encontrada! 🎉")
            print(f"Número de movimientos: {len(camino_actual)}")
            for i, movimiento in enumerate(camino_actual):
                print(f"Paso {i+1}: Mover de la torre {movimiento[0]} a la torre {movimiento[1]}")
            return True

        # Solo expandir si no hemos alcanzado el límite de profundidad
        if profundidad_actual < limite_profundidad:
            sucesores = generar_sucesores(estado_actual)
            for nuevo_estado, movimiento in reversed(sucesores):
                if nuevo_estado not in estados_visitados:
                    estados_visitados.add(nuevo_estado)
                    nuevo_camino = camino_actual + [movimiento]
                    # Añadir el nuevo estado con profundidad incrementada
                    pila.append((nuevo_estado, nuevo_camino, profundidad_actual + 1))
    
    print("El algoritmo no encontró una solución dentro del límite de profundidad...")
    return False


if __name__ == "__main__":
    try:
        n_discos = int(input("Introduce la cantidad de discos (un número entero): "))
        limite = int(input("Introduce el límite de profundidad (un número entero): "))
        if n_discos > 0 and limite > 0:
            hanoi_busqueda_profundidad_limitada(n_discos, limite)
        else:
            print("Por favor, introduce números enteros positivos.")
    except ValueError:
        print("Entrada no válida. Por favor, introduce números enteros.")