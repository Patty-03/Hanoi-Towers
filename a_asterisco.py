import heapq

def calcular_heuristica(estado, n_discos):
    """
    Calcula la heurística (2^N - 1) para el estado actual,
    donde N es el disco más grande que no está en la torre final.
    """
    torre_final = 2
    
    # Recorremos los discos del más grande (n_discos) al más pequeño (1)
    for disco in range(n_discos, 0, -1):
        if disco not in estado[torre_final]:
            # El disco no está en la torre final
            return pow(2, disco) - 1
        else:
            # Si el disco está en la torre final pero no es el disco superior,
            # significa que hay discos más pequeños encima que deben ser movidos
            if estado[torre_final][-1] != disco:
                return pow(2, disco) - 1
            
    # Si todos los discos están en la torre final, la heurística es 0
    return 0

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

def hanoi_a_star(n_discos):
    """
    Implementa el algoritmo de búsqueda A* para resolver
    las Torres de Hanoi de forma óptima para 'n_discos',
    mostrando el trazado de los valores (f, g, h).
    """
    print(f"\nIniciando Búsqueda A* con {n_discos} discos...")
    
    # Generación dinámica del estado inicial y final
    discos = tuple(range(n_discos, 0, -1))
    
    estado_inicial = (discos, (), ())
    estado_final = ((), (), discos)
    
    # Inicialización
    h_inicial = calcular_heuristica(estado_inicial, n_discos)
    f_inicial = 0 + h_inicial # g_score inicial es 0
    
    # Cola: (f_score, g_score, estado, camino)
    cola_a_star = [(f_inicial, 0, estado_inicial, [])]
    estados_visitados = {estado_inicial: 0}
    
    contador_pasos_busqueda = 0

    print(f"| {'Paso Exp':<8} | {'F (g+h)':<8} | {'G (Costo)':<8} | {'H (Heur)':<8} | Estado Extraído |")
    print("-" * 75)
    
    while cola_a_star:
        # 1. Extraer el nodo con el f_score más bajo (La decisión de A*)
        f_actual, g_actual, estado_actual, camino_actual = heapq.heappop(cola_a_star)
        contador_pasos_busqueda += 1

        # 2. Imprimir el trazado del nodo que se va a expandir
        h_actual = f_actual - g_actual
        movimiento_anterior = camino_actual[-1] if camino_actual else "INICIO"
        
        print(f"| {contador_pasos_busqueda:<8} | {f_actual:<8} | {g_actual:<8} | {h_actual:<8} | Moviendo: {movimiento_anterior} | {estado_actual} |")

        # 3. Comprobación de meta
        if estado_actual == estado_final:
            print("-" * 75)
            print("¡SOLUCIÓN ENCONTRADA! 🎉")
            print(f"Movimientos del camino óptimo: {g_actual}")
            print(f"Movimientos teóricos óptimos (2^N - 1): {pow(2, n_discos) - 1}")
            
            # Devolvemos el camino para una futura visualización
            return camino_actual

        # 4. Generación de sucesores
        for nuevo_estado, movimiento in generar_sucesores(estado_actual):
            g_nuevo = g_actual + 1
            
            # Relajación: solo expandimos si encontramos un camino mejor
            if nuevo_estado not in estados_visitados or g_nuevo < estados_visitados[nuevo_estado]:
                estados_visitados[nuevo_estado] = g_nuevo
                
                h_nuevo = calcular_heuristica(nuevo_estado, n_discos)
                f_nuevo = g_nuevo + h_nuevo
                
                nuevo_camino = camino_actual + [movimiento]
                
                heapq.heappush(cola_a_star, (f_nuevo, g_nuevo, nuevo_estado, nuevo_camino))
    
    print("El algoritmo no encontró una solución.")
    return None

if __name__ == "__main__":
    try:
        n_discos_input = input("Introduce la cantidad de discos (un entero positivo, ej. 4): ")
        n_discos = int(n_discos_input)
        
        if n_discos < 1:
            print("Por favor, introduce un número entero positivo (al menos 1).")
        else:
            # Puedes llamar a hanoi_a_star y guardar la secuencia de movimientos si quieres
            # manipularlos después.
            solucion = hanoi_a_star(n_discos)
            
            if solucion:
                print("\nSecuencia de movimientos del camino óptimo:")
                for i, mov in enumerate(solucion):
                    print(f"  Paso {i+1}: Torre {mov[0]} -> Torre {mov[1]}")
            
    except ValueError:
        print("Entrada no válida. Por favor, introduce un número entero.")