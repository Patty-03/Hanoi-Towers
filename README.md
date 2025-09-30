# Proyecto Torres de Hanoi

Este proyecto contiene implementaciones de diferentes algoritmos de inteligencia artificial para resolver el clásico problema de las Torres de Hanoi. El problema consiste en mover una pila de discos de una torre a otra, siguiendo ciertas reglas: solo se puede mover un disco a la vez, y un disco más grande nunca puede estar encima de uno más pequeño.

## Descripción de los Archivos

### 1. `a_asterisco.py` - Algoritmo A*
Contiene una implementación del algoritmo de búsqueda A* para resolver las Torres de Hanoi:
- **Función `calcular_heuristica`**: Implementa una heurística basada en la potencia de 2 para estimar el número de movimientos necesarios para alcanzar el estado objetivo
- **Función `generar_sucesores`**: Genera todos los estados válidos accesibles desde un estado dado, siguiendo las reglas del juego
- **Función `hanoi_a_star`**: Implementa el algoritmo A* que utiliza la heurística para encontrar la solución óptima, mostrando un trazado detallado de los valores f, g y h

### 2. `busqueda_a_lo_ancho.py` - Búsqueda en Anchura (BFS)
Contiene la implementación del algoritmo de búsqueda en anchura:
- Utiliza una cola (deque) para explorar todos los estados a la misma profundidad antes de avanzar a la siguiente
- Garantiza encontrar la solución óptima (con el menor número de movimientos)
- Explora sistemáticamente todos los posibles estados siguiendo un enfoque FIFO

### 3. `busqueda_profundidad.py` - Búsqueda en Profundidad (DFS)
Contiene la implementación del algoritmo de búsqueda en profundidad:
- Utiliza una pila (deque) para explorar tan profundo como sea posible antes de retroceder
- No garantiza encontrar la solución óptima
- Puede quedar atrapado en ramas infinitas (en este problema, se evita con el control de estados visitados)

### 4. `busqueda_voraz.py` - Búsqueda Voraz
Contiene una implementación de búsqueda voraz (greedy search):
- Utiliza una cola de prioridad (heapq) y se basa en la heurística para elegir el siguiente estado
- En cada paso, selecciona el estado que parece más prometedor según la heurística
- No garantiza la solución óptima, pero puede ser más eficiente que BFS

### 5. `profundidad_limitada.py` - Búsqueda en Profundidad Limitada
Contiene una implementación del algoritmo de búsqueda en profundidad limitada (DFS-Limited):
- Extiende el algoritmo de búsqueda en profundidad estándar con un límite de profundidad
- Explora hasta una profundidad específica antes de retroceder
- Evita explorar caminos infinitos o muy largos al imponer un límite máximo de profundidad
- No garantiza encontrar la solución óptima si el límite es demasiado bajo

## Archivos Vacíos

Los siguientes archivos están presentes en la estructura de directorios pero actualmente están vacíos:
- `busqueda_local.py` - Búsqueda Local
- `alg_genetico.py` - Algoritmo Genético
- `hill_climbing.py` - Hill Climbing
- `busqueda_tabu.py` - Búsqueda Tabú
- `estrategia_evolutiva.py` - Estrategia Evolutiva
- `recocido_simulado.py` - Recocido Simulado

## Estructura de los Estados

En todos los algoritmos implementados, los estados se representan como tuplas de 3 elementos, donde cada elemento representa una torre:
- Cada torre es una tupla que contiene los discos presentes en ella, ordenados del más pequeño (arriba) al más grande (abajo)
- Por ejemplo, con 3 discos: `((3, 2, 1), (), ())` representa el estado inicial donde todos los discos están en la primera torre
- El estado objetivo sería `(() , (), (3, 2, 1))` donde todos los discos están en la tercera torre

## Funciones Comunes

Muchos archivos comparten una función común `generar_sucesores` que implementa la lógica de movimiento:
- Recorre todas las combinaciones posibles de torres de origen y destino
- Verifica que el movimiento sea válido (una torre no está vacía y el disco superior puede moverse a la torre destino sin violar las reglas)
- Genera todos los estados alcanzables desde el estado actual

## Características Generales del Proyecto

- Los algoritmos se pueden ejecutar directamente desde la línea de comandos
- Permiten al usuario especificar el número de discos
- Incluyen validación de entrada
- Proporcionan información detallada sobre la solución encontrada
- Muestran el número de movimientos realizados
- Comparan con la solución teórica óptima (2^N - 1 movimientos)

Este proyecto proporciona un excelente ejemplo de cómo diferentes algoritmos de IA pueden aplicarse al mismo problema, permitiendo comparar su eficiencia, optimalidad y comportamiento.