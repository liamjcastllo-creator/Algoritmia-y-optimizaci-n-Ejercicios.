import random
import math
import matplotlib.pyplot as plt

def calculate_total_distance(route, cities):
    """Calcula la distancia total de una ruta cerrada."""
    distance = 0
    n = len(route)
    for i in range(n):
        c1 = cities[route[i]]
        c2 = cities[route[(i + 1) % n]]
        distance += math.hypot(c1[0] - c2[0], c1[1] - c2[1])
    return distance

def nearest_neighbor_tour(cities, start_node):
    """Genera una solución inicial usando la heurística del Vecino Más Cercano."""
    unvisited = list(range(len(cities)))
    current = start_node
    tour = [current]
    unvisited.remove(current)
    
    while unvisited:
        next_node = min(unvisited, key=lambda city: math.hypot(cities[current][0] - cities[city][0], cities[current][1] - cities[city][1]))
        tour.append(next_node)
        current = next_node
        unvisited.remove(current)
        
    return tour

def local_search_2opt(route, cities):
    """Aplica la heurística de búsqueda local 2-opt hasta alcanzar un óptimo local."""
    best_route = list(route)
    best_distance = calculate_total_distance(best_route, cities)
    improvements_count = 0
    improved = True
    
    while improved:
        improved = False
        n = len(best_route)
        for i in range(n - 1):
            for j in range(i + 2, n + 1):
                if j - i == 1 and i == 0 and j == n:
                    continue # Evitar aristas adyacentes redundantes
                
                # Invertir el subsegmento entre i y j (2-opt move)
                new_route = best_route[:i] + list(reversed(best_route[i:j])) + best_route[j:]
                new_distance = calculate_total_distance(new_route, cities)
                
                if new_distance < best_distance:
                    best_route = new_route
                    best_distance = new_distance
                    improvements_count += 1
                    improved = True
                    break
            if improved:
                break
                
    return best_route, best_distance, improvements_count

if __name__ == '__main__':
    # Generar 15 ciudades aleatorias fijas para la prueba
    random.seed(42)
    cities = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(15)]
    
    # Escenario 1: Solución Inicial Aleatoria
    initial_random = list(range(len(cities)))
    random.shuffle(initial_random)
    _, dist_random, mejoras_random = local_search_2opt(initial_random, cities)
    
    # Escenario 2: Solución Inicial con Vecino Más Cercano
    initial_nn = nearest_neighbor_tour(cities, start_node=0)
    _, dist_nn, mejoras_nn = local_search_2opt(initial_nn, cities)
    
    print(f"Escenario Aleatorio -> Mejoras: {mejoras_random}, Costo Final: {dist_random:.2f}")
    print(f"Escenario Vecino Más Cercano -> Mejoras: {mejoras_nn}, Costo Final: {dist_nn:.2f}")
    
    # Visualización comparativa (Gráfica de barras de número de mejoras)
    scenarios = ['Inicio Aleatorio', 'Vecino Más Cercano']
    improvements = [mejoras_random, mejoras_nn]
    
    plt.figure(figsize=(7, 4))
    plt.bar(scenarios, improvements, color=['skyblue', 'salmon'])
    plt.title('Ejercicio 3: Número de Mejoras Requeridas en 2-opt')
    plt.ylabel('Cantidad de Mejoras')
    for i, v in enumerate(improvements):
        plt.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('ejercicio3_tsp.png')
    plt.show()