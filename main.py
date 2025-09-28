def ejecutar_algoritmo(nombre_algoritmo, n_discos):
    """
    Ejecuta el algoritmo especificado con el número de discos indicado.
    """
    if nombre_algoritmo == "1":
        from busqueda_a_lo_ancho import hanoi_busqueda_a_lo_ancho
        return hanoi_busqueda_a_lo_ancho(n_discos)
    elif nombre_algoritmo == "2":
        from busqueda_profundidad import hanoi_busqueda_profundidad
        return hanoi_busqueda_profundidad(n_discos)
    elif nombre_algoritmo == "3":
        from busqueda_voraz import hanoi_voraz
        return hanoi_voraz(n_discos)
    elif nombre_algoritmo == "4":
        from busqueda_local import hanoi_busqueda_local
        return hanoi_busqueda_local(n_discos)
    elif nombre_algoritmo == "5":
        from hill_climbing import hanoi_hill_climbing
        return hanoi_hill_climbing(n_discos)
    elif nombre_algoritmo == "6":
        from busqueda_tabu import hanoi_busqueda_tabu
        return hanoi_busqueda_tabu(n_discos)
    elif nombre_algoritmo == "7":
        from recocido_simulado import hanoi_recocido_simulado
        return hanoi_recocido_simulado(n_discos)
    elif nombre_algoritmo == "8":
        from estrategia_evolutiva import hanoi_estrategia_evolutiva
        return hanoi_estrategia_evolutiva(n_discos)
    elif nombre_algoritmo == "9":
        from alg_genetico import hanoi_algoritmo_genetico
        return hanoi_algoritmo_genetico(n_discos)
    elif nombre_algoritmo == "10":
        from a_asterisco import hanoi_a_star  # Asumiendo que este archivo está implementado
        return hanoi_a_star(n_discos)
    elif nombre_algoritmo == "11":
        from profundidad_limitada import hanoi_profundidad_limitada  # Asumiendo que este archivo está implementado
        return hanoi_profundidad_limitada(n_discos)
    else:
        print("Opción no válida.")
        return False


def mostrar_menu():
    """
    Muestra el menú de algoritmos disponibles.
    """
    print("\n" + "="*60)
    print("            MENÚ DE ALGORITMOS PARA TORRES DE HANOI")
    print("="*60)
    print("1.  Búsqueda a lo ancho (BFS)")
    print("2.  Búsqueda en profundidad (DFS)")
    print("3.  Búsqueda voraz (Greedy)")
    print("4.  Búsqueda local")
    print("5.  Hill Climbing")
    print("6.  Búsqueda tabú")
    print("7.  Recocido simulado")
    print("8.  Estrategia evolutiva")
    print("9.  Algoritmo genético")
    print("10. A* (A estrella)")
    print("11. Búsqueda en profundidad limitada")
    print("0.  Salir")
    print("="*60)


def main():
    """
    Función principal que maneja la interacción con el usuario.
    """
    print("¡Bienvenido al sistema de resolución de Torres de Hanoi!")
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\nSelecciona un algoritmo (0-11): ").strip()
            
            if opcion == "0":
                print("¡Gracias por usar el sistema! Hasta luego. 😊")
                break
            
            if opcion in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]:
                n_discos_input = input("Introduce la cantidad de discos (un número entero): ")
                n_discos = int(n_discos_input)
                
                if n_discos <= 0:
                    print("Por favor, introduce un número entero positivo.")
                    continue
                
                print(f"\nEjecutando algoritmo...")
                resultado = ejecutar_algoritmo(opcion, n_discos)
                
                if not resultado:
                    print("El algoritmo no encontró una solución o encontró un error.")
                
                # Preguntar si desea ejecutar otro algoritmo
                continuar = input("\n¿Deseas ejecutar otro algoritmo? (s/n): ").strip().lower()
                if continuar != 's' and continuar != 'si':
                    print("¡Gracias por usar el sistema! Hasta luego. 😊")
                    break
            else:
                print("Opción no válida. Por favor, selecciona un número entre 0 y 11.")
        
        except ValueError:
            print("Entrada no válida. Por favor, introduce un número entero.")
        except ImportError as e:
            print(f"Error al importar el módulo: {e}")
            print("Asegúrate de que el archivo del algoritmo existe y está correctamente implementado.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")


if __name__ == "__main__":
    main()