import math
import random


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


def calcular_heuristica(estado, n_discos):
    discos_fuera_de_lugar = 0
    torre_final = 2
    
    for disco in range(1, n_discos + 1):
        en_torre_final = False
        for torre_idx, torre in enumerate(estado):
            if disco in torre and torre_idx == torre_final:
                en_torre_final = True
                break
        if not en_torre_final:
            discos_fuera_de_lugar += 1
    
    return discos_fuera_de_lugar


def hanoi_recocido_simulado(n_discos, temp_inicial=1000, temp_final=1, enfriamiento=0.95, max_iter_por_temp=100):
    estado_inicial = (
        tuple(range(n_discos, 0, -1)),  
        (), 
        ()
    )
    
    estado_final = (
        (),
        (),
        tuple(range(n_discos, 0, -1))
    )

    print(f"Resolviendo las Torres de Hanoi con {n_discos} discos usando Recocido Simulado...")
    print(f"Temperatura inicial: {temp_inicial}, Temperatura final: {temp_final}, Tasa de enfriamiento: {enfriamiento}")

    estado_actual = estado_inicial
    mejor_estado = estado_actual
    camino_actual = []
    mejor_camino = camino_actual[:]
    
    temperatura = temp_inicial
    
    iteraciones_totales = 0
    movimientos_aceptados = 0
    movimientos_rechazados = 0

    while temperatura > temp_final:
        iteracion_temp_actual = 0
        
        while iteracion_temp_actual < max_iter_por_temp:
            if estado_actual == estado_final:
                print("¡Solución encontrada! 🎉")
                print(f"Número de movimientos: {len(camino_actual)}")
                for i, movimiento in enumerate(camino_actual):
                    print(f"Paso {i+1}: Mover de la torre {movimiento[0]} a la torre {movimiento[1]}")
                return True
            
            # Generar un sucesor aleatorio
            sucesores = generar_sucesores(estado_actual)
            
            if not sucesores:
                print("No hay más movimientos posibles.")
                break
            
            # Elegir un sucesor aleatorio
            estado_siguiente, movimiento = random.choice(sucesores)
            
            # Calcular el cambio en la función objetivo (heurística)
            heuristica_actual = calcular_heuristica(estado_actual, n_discos)
            heuristica_siguiente = calcular_heuristica(estado_siguiente, n_discos)
            delta = heuristica_siguiente - heuristica_actual
            
            # Aceptar o rechazar el nuevo estado
            aceptado = False
            if delta < 0:  # Mejora la solución
                estado_actual = estado_siguiente
                camino_actual.append(movimiento)
                aceptado = True
            else:  # Empeora la solución, aceptar con cierta probabilidad
                probabilidad_aceptacion = math.exp(-delta / temperatura)
                if random.random() < probabilidad_aceptacion:
                    estado_actual = estado_siguiente
                    camino_actual.append(movimiento)
                    aceptado = True
            
            # Actualizar contadores
            if aceptado:
                movimientos_aceptados += 1
            else:
                movimientos_rechazados += 1
            
            # Actualizar el mejor estado si encontramos una mejor solución
            if heuristica_actual < calcular_heuristica(mejor_estado, n_discos):
                mejor_estado = estado_actual
                mejor_camino = camino_actual[:]
            
            iteracion_temp_actual += 1
            iteraciones_totales += 1
        
        # Enfriar la temperatura
        temperatura *= enfriamiento
        
        # Mostrar información periódica
        if iteraciones_totales % (max_iter_por_temp * 10) == 0:
            print(f"Iteración {iteraciones_totales}, Temperatura: {temperatura:.2f}, "
                  f"Heurística actual: {calcular_heuristica(estado_actual, n_discos)}, "
                  f"Mejor heurística: {calcular_heuristica(mejor_estado, n_discos)}")

    print("El algoritmo no encontró una solución dentro de los límites establecidos.")
    print(f"Iteraciones totales: {iteraciones_totales}")
    print(f"Movimientos aceptados: {movimientos_aceptados}, Movimientos rechazados: {movimientos_rechazados}")
    
    # Mostrar información sobre el mejor estado encontrado
    print(f"Mejor estado encontrado: {mejor_estado}")
    print(f"Heurística del mejor estado: {calcular_heuristica(mejor_estado, n_discos)}")
    
    # Mostrar la solución encontrada
    if mejor_estado == estado_final:
        print("¡La mejor solución encontrada alcanzó el estado objetivo!")
        print(f"Número de movimientos: {len(mejor_camino)}")
        for i, movimiento in enumerate(mejor_camino):
            print(f"Paso {i+1}: Mover de la torre {movimiento[0]} a la torre {movimiento[1]}")
        return True
    
    return mejor_estado == estado_final


# --- Uso del programa ---
if __name__ == "__main__":
    try:
        n_discos = int(input("Introduce la cantidad de discos (un número entero): "))
        if n_discos > 0:
            hanoi_recocido_simulado(n_discos)
        else:
            print("Por favor, introduce un número entero positivo.")
    except ValueError:
        print("Entrada no válida. Por favor, introduce un número entero.")