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

def get_2opt_neighbor(route):
    """Genera un vecino aplicando un movimiento 2-opt aleatorio."""
    n = len(route)
    i = random.randint(0, n - 2)
    j = random.randint(i + 2, n)
    new_route = route[:i] + list(reversed(route[i:j])) + route[j:]
    return new_route

def simulated_annealing(cities, cooling_schedule='exponential', initial_temp=1000.0, cooling_rate=0.995, iterations=2000):
    """Ejecuta Recocido Simulado para el TSP con diferentes esquemas de enfriamiento."""
    n = len(cities)
    current_route = list(range(n))
    random.shuffle(current_route)
    current_cost = calculate_total_distance(current_route, cities)
    
    best_route = list(current_route)
    best_cost = current_cost
    
    temp = initial_temp
    cost_history = [current_cost]
    
    for step in range(1, iterations + 1):
        # Generar vecino
        neighbor_route = get_2opt_neighbor(current_route)
        neighbor_cost = calculate_total_distance(neighbor_route, cities)
        
        # Calcular delta de costo
        delta = neighbor_cost - current_cost
        
        # Criterio de aceptación de Metropolis
        if delta < 0 or random.random() < math.exp(-delta / max(temp, 1e-8)):
            current_route = neighbor_route
            current_cost = neighbor_cost
            if current_cost < best_cost:
                best_route = list(current_route)
                best_cost = current_cost
                
        cost_history.append(current_cost)
        
        # Esquema de enfriamiento
        if cooling_schedule == 'exponential':
            temp *= cooling_rate
        elif cooling_schedule == 'linear':
            temp -= (initial_temp / iterations)
            if temp < 0: temp = 0
            
    return best_route, best_cost, cost_history

if __name__ == '__main__':
    random.seed(42)
    cities = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(15)]
    
    # Ejecutar con enfriamiento Exponencial
    _, best_exp, history_exp = simulated_annealing(cities, cooling_schedule='exponential', iterations=1500)
    # Ejecutar con enfriamiento Lineal
    _, best_lin, history_lin = simulated_annealing(cities, cooling_schedule='linear', iterations=1500)
    
    print(f"Enfriamiento Exponencial -> Costo Final: {best_exp:.2f}")
    print(f"Enfriamiento Lineal -> Costo Final: {best_lin:.2f}")
    
    # Visualización 1: Curvas de convergencia
    plt.figure(figsize=(9, 4.5))
    plt.plot(history_exp, label='Enfriamiento Exponencial', color='purple')
    plt.plot(history_lin, label='Enfriamiento Lineal', color='orange', alpha=0.8)
    plt.title('Ejercicio 4: Curvas de Convergencia (Costo vs Iteraciones)')
    plt.xlabel('Iteraciones')
    plt.ylabel('Costo de la Ruta')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Guardar explícitamente la imagen en disco
    plt.savefig('ejercicio4_convergencia.png', dpi=300, bbox_inches='tight')
    print("Gráfica guardada exitosamente como 'ejercicio4_convergencia.png'")
    
    # Comenta plt.show() si estás en una terminal sin interfaz gráfica
    # plt.show()