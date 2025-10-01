import random
import time


def generar_estado_inicial(n_discos):
    discos = tuple(range(n_discos, 0, -1))
    return (discos, (), ())


def generar_estado_final(n_discos):
    discos = tuple(range(n_discos, 0, -1))
    return ((), (), discos)


def validar_estado(estado, n_discos):
    discos_en_estado = []
    for torre in estado:
        discos_en_estado.extend(torre)
    
    # Verificar que haya exactamente n_discos discos
    if len(discos_en_estado) != n_discos:
        return False
    
    # Verificar que cada disco tenga un valor válido
    discos_en_estado.sort()
    if discos_en_estado != list(range(1, n_discos + 1)):
        return False
    
    # Verificar que en cada torre los discos estén en orden válido (más grandes abajo)
    for torre in estado:
        for i in range(len(torre) - 1):
            if torre[i] < torre[i + 1]:  # Disco grande debajo de disco pequeño
                return False
    
    return True


def aplicar_movimiento(estado, movimiento):
    origen, destino = movimiento
    if origen < 0 or origen > 2 or destino < 0 or destino > 2:
        return estado
    
    if origen == destino:
        return estado 
    
    if not estado[origen]: 
        return estado
    
    disco_superior = estado[origen][-1]
    if estado[destino] and disco_superior > estado[destino][-1]:
        return estado
    
    nuevo_estado = []
    for i, torre in enumerate(estado):
        if i == origen:
            nueva_torre = torre[:-1] 
        elif i == destino:
            nueva_torre = torre + (disco_superior,)  
        else:
            nueva_torre = torre
        nuevo_estado.append(nueva_torre)
    
    return tuple(nuevo_estado)


def generar_movimientos_validos(estado):
    movimientos = []
    for origen in range(3):
        for destino in range(3):
            if origen != destino:
                if estado[origen]:
                    disco_superior = estado[origen][-1]
                    if not estado[destino] or disco_superior < estado[destino][-1]:
                        movimientos.append((origen, destino))
    return movimientos


def calcular_distancia_estado(estado, estado_final):
    #Calcula una medida de cuán lejos está un estado del estado final.

    distancia = 0
    for disco in range(1, len(estado[0]) + len(estado[1]) + len(estado[2]) + 1):
        # Encontrar en qué torre está el disco en el estado actual
        torre_actual = None
        pos_actual = None
        for i, torre in enumerate(estado):
            if disco in torre:
                torre_actual = i
                pos_actual = torre.index(disco)
                break
        
        # Encontrar en qué torre debería estar el disco en el estado final
        torre_final = None
        pos_final = None
        for i, torre in enumerate(estado_final):
            if disco in torre:
                torre_final = i
                pos_final = torre.index(disco)
                break
        
        if torre_actual is not None and torre_final is not None:
            if torre_actual != torre_final:
                # Si el disco no está en la torre correcta, penalizar
                distancia += disco * 2  # Los discos más grandes tienen más peso
            elif pos_actual != pos_final:
                # Si el disco está en la torre correcta pero en la posición incorrecta
                distancia += 1
    
    return distancia


def evaluar_solucion(movimientos, n_discos):
    #Devuelve un valor de fitness

    estado_inicial = generar_estado_inicial(n_discos)
    estado_final = generar_estado_final(n_discos)
    
    estado_actual = estado_inicial
    
    # Aplicar movimientos
    for movimiento in movimientos:
        estado_actual = aplicar_movimiento(estado_actual, movimiento)
        if estado_actual == estado_final:
            # Solución encontrada, devolver fitness alto
            return 10000 - len(movimientos)  # Penalizar por longitud de la solución
    
    # Calcular distancia al estado final
    distancia_final = calcular_distancia_estado(estado_actual, estado_final)
    
    # El fitness es menor cuanto más larga es la secuencia y más lejos está del objetivo
    # Se penalizan secuencias largas y se premian soluciones mas cerca del objetivo
    if distancia_final == 0:
        return 10000 - len(movimientos)
    else:
        # Penalizar proporcionalmente a la distancia y longitud de la secuencia
        max_movimientos_posibles = 2 ** n_discos - 1  # Máximo teórico de movimientos
        fitness = max(0, 10000 - distancia_final * 10 - len(movimientos) * 5)
        return fitness


def generar_secuencia_aleatoria(n_discos, longitud_maxima):
    estado_actual = generar_estado_inicial(n_discos)
    secuencia = []
    
    for _ in range(longitud_maxima):
        movimientos_posibles = generar_movimientos_validos(estado_actual)
        if not movimientos_posibles:
            break  # No se pueden hacer más movimientos
        
        movimiento = random.choice(movimientos_posibles)
        secuencia.append(movimiento)
        estado_actual = aplicar_movimiento(estado_actual, movimiento)
        
        # Terminar si se alcanza el estado final
        if estado_actual == generar_estado_final(n_discos):
            break
    
    return secuencia


def mutar_secuencia_evolutiva(secuencia, n_discos, sigma=0.3):
    """
    Muta una secuencia de movimientos usando estrategia evolutiva.
    """
    if not secuencia:
        return secuencia
    
    secuencia_mutada = secuencia.copy()
    
    # Aplicar mutaciones a cada posición de la secuencia con una probabilidad
    for i in range(len(secuencia_mutada)):
        if random.random() < sigma:
            # Generar un movimiento aleatorio válido en la posición i
            estado_actual = generar_estado_inicial(n_discos)
            
            # Llegar al estado justo antes de este movimiento
            for j in range(i):
                estado_actual = aplicar_movimiento(estado_actual, secuencia_mutada[j])
            
            movimientos_validos = generar_movimientos_validos(estado_actual)
            if movimientos_validos:
                secuencia_mutada[i] = random.choice(movimientos_validos)
    
    # Añadir o eliminar movimientos con menor probabilidad
    if random.random() < sigma/2:
        # Añadir un movimiento aleatorio al final
        if len(secuencia_mutada) < 2 * n_discos:  # Limitar longitud
            estado_actual = generar_estado_inicial(n_discos)
            for mov in secuencia_mutada:
                estado_actual = aplicar_movimiento(estado_actual, mov)
            
            movimientos_validos = generar_movimientos_validos(estado_actual)
            if movimientos_validos:
                secuencia_mutada.append(random.choice(movimientos_validos))
    
    if random.random() < sigma/2 and len(secuencia_mutada) > 1:
        # Eliminar un movimiento aleatorio
        idx = random.randint(0, len(secuencia_mutada) - 1)
        secuencia_mutada.pop(idx)
    
    return secuencia_mutada


def hanoi_estrategia_evolutiva(n_discos, tam_poblacion=20, tam_offspring=40, generaciones=500):
    print(f"\nResolviendo Torres de Hanoi con {n_discos} discos usando Estrategia Evolutiva...")
    print(f"Tamaño de la población (mu): {tam_poblacion}, Tamaño de lambda (cantidad de hijos generados): {tam_offspring}, Generaciones: {generaciones}")
    
    # Parámetros
    longitud_maxima_secuencia = min(2 ** n_discos - 1, n_discos * 4)
    tam_elite = tam_poblacion  # Seleccionamos los mu mejores de la población actual + lambda
    
    # Inicializar población (mu)
    poblacion = []
    for _ in range(tam_poblacion):
        secuencia = generar_secuencia_aleatoria(n_discos, longitud_maxima_secuencia)
        poblacion.append(secuencia)
    
    mejor_global = None
    mejor_fitness_global = float('-inf')
    mejor_generacion = 0
    
    for generacion in range(generaciones):
        # Evaluar fitness de cada individuo en la población actual
        fitnesses_poblacion = [evaluar_solucion(secuencia, n_discos) for secuencia in poblacion]
        
        # Generar offspring (lambda nuevos individuos)
        offspring = []
        fitnesses_offspring = []
        for _ in range(tam_offspring):
            # Seleccionar un padre al azar de la población actual
            padre_idx = random.randint(0, len(poblacion) - 1)
            padre = poblacion[padre_idx]
            
            # Muta el padre para generar un hijo
            hijo = mutar_secuencia_evolutiva(padre, n_discos)
            
            # Evaluar el hijo
            fitness_hijo = evaluar_solucion(hijo, n_discos)
            
            offspring.append(hijo)
            fitnesses_offspring.append(fitness_hijo)
        
        # Combinar población y offspring
        toda_la_poblacion = poblacion + offspring
        todos_los_fitnesses = fitnesses_poblacion + fitnesses_offspring
        
        # Seleccionar los mu mejores (estrategia (mu + lambda))
        indices_ordenados = sorted(range(len(todos_los_fitnesses)), 
                                  key=lambda i: todos_los_fitnesses[i], reverse=True)
        
        # Los mu mejores pasan a la siguiente generación
        nueva_poblacion = []
        for i in range(tam_poblacion):
            idx = indices_ordenados[i]
            nueva_poblacion.append(toda_la_poblacion[idx])
        
        # Actualizar el mejor global
        mejor_idx = indices_ordenados[0]
        mejor_actual = toda_la_poblacion[mejor_idx]
        fitness_mejor_actual = todos_los_fitnesses[mejor_idx]
        
        if fitness_mejor_actual > mejor_fitness_global:
            mejor_global = mejor_actual
            mejor_fitness_global = fitness_mejor_actual
            mejor_generacion = generacion
            
            # Verificar si encontramos la solución óptima
            estado_resultado = generar_estado_inicial(n_discos)
            for mov in mejor_global:
                estado_resultado = aplicar_movimiento(estado_resultado, mov)
            
            if estado_resultado == generar_estado_final(n_discos):
                print(f"¡Solución óptima encontrada en la generación {generacion}! 🎉")
                print(f"Número de movimientos: {len(mejor_global)}")
                print(f"Cantidad óptima teórica: {2**n_discos - 1}")
                return mejor_global
        
        # Mostrar progreso
        if generacion % 50 == 0 or generacion == generaciones - 1:
            print(f"Generación {generacion}: Mejor fitness actual = {fitness_mejor_actual}, "
                  f"Mejor global = {mejor_fitness_global} (gen {mejor_generacion})")
        
        # Actualizar la población
        poblacion = nueva_poblacion
    

    print(f"\nEjecución finalizada Mejor solución encontrada en la generación {mejor_generacion}")
    print(f"Fitness de la mejor solución: {mejor_fitness_global}")
    
    # Aplicar la mejor solución encontrada para ver el estado final
    estado_resultado = generar_estado_inicial(n_discos)
    for mov in mejor_global:
        estado_resultado = aplicar_movimiento(estado_resultado, mov)
    
    print(f"Estado final alcanzado: {estado_resultado}")
    print(f"Estado objetivo: {generar_estado_final(n_discos)}")
    print(f"Número de movimientos de la mejor solución: {len(mejor_global)}")
    
    if estado_resultado == generar_estado_final(n_discos):
        print("¡La solución alcanzó el estado objetivo!")
        return mejor_global
    else:
        print("La solución no alcanzó el estado objetivo.")
        return mejor_global


if __name__ == "__main__":
    try:
        n_discos_input = input("Introduce la cantidad de discos (un entero positivo, ej. 4): ")
        n_discos = int(n_discos_input)
        
        if n_discos < 1:
            print("Por favor, introduce un número entero positivo (al menos 1).")
        else:
            solucion = hanoi_estrategia_evolutiva(n_discos)
            
            if solucion:
                print(f"\nSecuencia de movimientos encontrada ({len(solucion)} movimientos):")
                for i, mov in enumerate(solucion):
                    print(f"  Paso {i+1}: Torre {mov[0]} -> Torre {mov[1]}")
            
    except ValueError:
        print("Entrada no válida. Por favor, introduce un número entero.")